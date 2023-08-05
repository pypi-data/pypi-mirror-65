import logging
import os
import operator
from pyteomics import parser, mzid
import re
import sqlite3
import sys

from fastg2protlib.mzid_sax_parsing import parse_mzid

logger = logging.getLogger(__name__)
logger.setLevel(level=os.environ.get("LOGLEVEL", "INFO"))
handler = logging.StreamHandler()
formatter = logging.Formatter("%(asctime)s %(name)-12s %(levelname)-8s %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)

session_db_name = None


class ProteinScore:
    def __init__(self):
        self.protein_id = None
        self.pct_pep_coverage = None
        self.pct_sequence_coverage = None
        self.verified_peptides = None

    def __format__(self, formatstr):
        return f"ID: {self.protein_id} Peptide Coverage by Count: {self.pct_pep_coverage} Protein Sequence Covered: {self.pct_sequence_coverage}"


def _query_db(sql):
    global session_db_name
    conn = sqlite3.connect(session_db_name)
    cursor = conn.cursor()
    rs = cursor.execute(sql)
    return rs


def _proteins_for_peptide(pep_id):
    """
    peptide_to_protein
                    (peptide_id INTEGER, protein_id INTEGER);
    """
    rs = _query_db(
        "SELECT protein_id FROM peptide_to_protein WHERE peptide_id = " + str(pep_id)
    )
    proteins = []
    for r in rs.fetchall():
        proteins.append(r[0])
    return (pep_id, proteins)


def _pepseq_mapping(peptides):
    """
        Uses a set of peptide sequences to return
        a list of tuples:
        (peptide id, list of protein ids the peptide sequence is part of)
    """
    sql_in = ",".join(map('"{0}"'.format, peptides))

    rs = _query_db("SELECT * FROM peptide WHERE peptide.sequence IN (" + sql_in + ")")
    ret_val = []
    for r in rs.fetchall():
        ret_val.append(_proteins_for_peptide(r[0]))
    return ret_val


def _protein_sequence_coverage(p_dict):
    """
    Return a list of ProteinScore objects. Coverage is filled out.
    """
    ret_val = []
    for k, v in p_dict.items():
        in_clause = "(" + ",".join(map(lambda x: str(x), v)) + ")"
        pep_rs = _query_db("select sequence from peptide where id in " + in_clause)
        pep_sequences = list(map(lambda x: x[0], pep_rs.fetchall()))
        prot_rs = _query_db("select sequence from protein where id = " + str(k))
        prot_seq = prot_rs.fetchone()[0]
        ps = ProteinScore()
        ps.verified_peptides = v
        ps.protein_id = k
        ps.pct_sequence_coverage = round(parser.coverage(prot_seq, pep_sequences), 3)
        ret_val.append(ps)
    return ret_val


def _protein_dict(pep_lst):
    # region
    """
    Create a dictionary:
        key = protein id
        value = list of peptides associated with protein    )

    Dictionary gives us the raw count of unique peptide count for each protein.

    Parameters
    ----------
    pep_lst

    Returns
    -------
    dictionary

    """
    # endregion
    protein_dict = dict()
    for peptide_id, proteins in pep_lst:
        for protein_id in proteins:
            p_id = int(protein_id)
            if p_id not in protein_dict:
                protein_dict[p_id] = []
            protein_dict[p_id].append(int(peptide_id))
    return protein_dict


def _peptide_pct_coverage(lst):
    # sqlite> select protein_id, GROUP_CONCAT(peptide_id)  from peptide_to_protein where protein_id =323;
    # 323|283,327,334,338,354,2305,2821,2822,2824,3070,3590,3591,3592,3593,3594,3693,3702,4023,6636
    for ps in lst:
        sql = f"SELECT protein_id, GROUP_CONCAT(peptide_id) FROM peptide_to_protein WHERE protein_id = {ps.protein_id}"
        rs = _query_db(sql)
        ps.pct_pep_coverage = round(
            len(ps.verified_peptides) / len(rs.fetchall()[0][1]), 3
        )


def _read_mzid(mzid_file, score_config):
    logger.info(f"Starting to read MZIdentML file {mzid_file}")

    verified_peptides = parse_mzid(mzid_file, score_config)

    logger.info(f"Finished with the MZIdentML file {mzid_file}")
    return verified_peptides


def _write_protein_scores(p_scores):
    with open("protein_scores.csv", "w") as f:
        f.write("protein_id,pct_sequence_coverage,pct_peptide_coverage")
        f.write(os.linesep)
        for ps in p_scores:
            f.write(f"{ps.protein_id},{ps.pct_sequence_coverage},{ps.pct_pep_coverage}")
            f.write(os.linesep)


def _write_fasta(p_scores):
    with open("protein.fasta", "w") as f:
        for ps in p_scores:
            s = f"SELECT sequence FROM protein WHERE id = {ps.protein_id}"
            rs = _query_db(s)
            sequence = rs.fetchone()[0]
            rs = _query_db(
                f"SELECT walk FROM walk WHERE id IN (SELECT walk_id FROM protein_to_walk WHERE protein_id = {ps.protein_id})"
            )
            f.write(f">Protein_{ps.protein_id}|{rs.fetchone()[0]}")
            f.write(os.linesep)
            f.write(f"{sequence}")
            f.write(os.linesep)


def score_tabular(tabular_file, fdr_level, decoy_header, db_name):
    # region
    """
    Use tabular MSGF+ output to score the proteins via FDR.
    """
    # endregion
    global session_db_name
    session_db_name = db_name

    fwd_id = 0
    rev_id = 0

    peptide_sequences = set()
    regex = re.compile(r"[^A-Za-z]")

    with open(tabular_file) as f:
        header = f.readline().strip().split("\t")
        for line in f:
            values = line.strip().split("\t")
            psm = dict(zip(header, values))
            if psm["Protein"].startswith(decoy_header):
                rev_id += 1.0
            else:
                fwd_id += 1.0
            if (float(rev_id) / fwd_id) > fdr_level:
                break
            else:
                # Add peptide sequence, remove modification value
                peptide_sequences.add(regex.sub("", psm["Peptide"]))
    logger.info(
        f"Generated {len(peptide_sequences)} unique peptide sequences at FDR <= {fdr_level}"
    )
    proteins_to_peptides = _pepseq_mapping(peptide_sequences)

    protein_dict = _protein_dict(proteins_to_peptides)
    protein_scores = _protein_sequence_coverage(protein_dict)
    _peptide_pct_coverage(protein_scores)
    _write_protein_scores(protein_scores)
    _write_fasta(protein_scores)
    logger.info("Completed scoring using MSGF+ tabular output")


"""
{
    '#SpecFile': 'T4A.mzML', 'SpecID': 'index=262484', 'ScanNum': '-1', 
    'FragMethod': 'CID', 'Precursor': '1111.6', 'IsotopeError': '1', 
    'PrecursorError(ppm)': '5.181823', 'Charge': '3', 'Peptide': 'FDIPIIQLQPPFVVDLLDSNIAVFGAAM+15.995SGK', 
    'Protein': 'Pep_1590|Protein_133(pre=-,post=-)', 'DeNovoScore': '160', 'MSGFScore': '-61', 
    'SpecEValue': '0.025976893', 'EValue': '6830.0264', 'QValue': '0.4996623', 'PepQValue': '0.80702245'}
"""


def score_proteins(mzid_file, score_object, db_name="tst.db"):
    # region
    """
        Purpose
        -------
        User has searched peptides against MSMS data. Now, we will produce
        a FASTA library of proteins based on the verified peptides from the search

        Inputs
        ------
        MzIdentML file.

        Return
        ------
        Protein FASTA file.
        
    """
    # endregion
    global session_db_name
    session_db_name = db_name

    verified_peptides = _read_mzid(mzid_file, score_object)
    proteins_to_peptides = _pepseq_mapping(verified_peptides)

    protein_dict = _protein_dict(proteins_to_peptides)
    protein_scores = _protein_sequence_coverage(protein_dict)
    _peptide_pct_coverage(protein_scores)
    _write_protein_scores(protein_scores)
    _write_fasta(protein_scores)
    logger.info("Completed scoring")
