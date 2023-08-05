from Bio.Seq import Seq
from Bio.Alphabet import IUPAC
from collections import defaultdict
import datetime
import logging
import networkx as nx
import os
from pyteomics import parser
import re
import sys


from fastg2protlib.db import DBManager
from fastg2protlib.protein_score import score_proteins, score_tabular

logger = logging.getLogger(__name__)
logger.setLevel(level=os.environ.get("LOGLEVEL", "INFO"))
handler = logging.StreamHandler()
formatter = logging.Formatter("%(asctime)s %(name)-12s %(levelname)-8s %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)


def _parse_edges(edge_name, edge_str):
    """
    EDGE_71_length_1904_cov_38.3193,EDGE_72_length_57_cov_29.75

    becomes [(node_name, '71+'), ('71+', '72+')]
    :param edge_name:
    :param edge_str:
    :return: list of tuples
    """
    r_val = []

    all_edges = edge_str.split(",")
    leading_edge = edge_name
    for e in all_edges:
        rc = False
        if e.endswith("'"):
            rc = True
        regex = re.compile(r"(?:EDGE|NODE)_(?P<node_name>[a-zA-Z\d]+?)_length_")
        m = regex.search(e)
        node_name = m.group("node_name")
        if rc:
            node_name += "-"
        else:
            node_name += "+"
        r_val.append((leading_edge, node_name))
        leading_edge = node_name
    return r_val


def _parse_fastg_header(header):
    # region
    """
    Parse FASTG header and return
        * node_name: '1+'
        * length: 449
        * coverage: 82.5991
        * edges: [('1+', '71+'), ('71+', '72+')]
        * sequence: None
        * warnings: [list of warning message, if any]

    >EDGE_1_length_449_cov_82.5991:EDGE_71_length_1904_cov_38.3193,EDGE_72_length_57_cov_29.75;

    :param header:
    :return:
    """
    # endregion
    keys = ["node_name", "length", "coverage", "edges", "sequence", "warnings"]
    obj = dict.fromkeys(keys)

    header = header.lstrip(">").rstrip(";")
    num_colons = sum([1 for x in header if x == ":"])
    if num_colons > 1:
        obj["warnings"] = ["Too many colons in header, not in FASTG file format"]

    rev_compl = False
    chunks = header.split(":")

    if chunks[0].endswith("'"):
        rev_compl = True
    regex = re.compile(
        r"(?:EDGE|NODE)_(?P<node>[a-zA-Z\d]+?)_length_(?P<length>\d+?)_cov_(?P<cov>[\d|\.]+)"
    )
    m = regex.search(chunks[0])
    if m is None:
        obj["warnings"].append("Regex parsing failed")
    node_name = m.group("node")
    if rev_compl:
        node_name += "-"
    else:
        node_name += "+"
    obj["node_name"] = node_name
    obj["length"] = m.group("length")
    obj["coverage"] = m.group("cov")
    if len(chunks) > 1:
        obj["edges"] = _parse_edges(node_name, chunks[1])
    else:
        obj["edges"] = None
    obj["sequence"] = ""

    return obj


def _expand_walk(walks):
    # region
    """

    We expand existing depth-first traversals here.
    A node with multiple predecessors has multiple full length traversals.
    This function splices together existing walks where a node is traversed more than once.

    Parameters
    ----------
    walks: list of DFS edge traversals

    Returns
    -------
    expanded_walks: list of DFS edge traversals expanded with longer paths.
    """
    # endregion
    expanded_walks = []
    walk_starts = {}
    for i, walk in enumerate(walks):
        walk_starts[walk[0]] = i

    for walk in walks:
        path = []
        for i, node in enumerate(walk):
            if node in walk_starts and i > 0:
                if node != walk[0]:
                    p = path
                    p.extend(walks[walk_starts[node]])
                    expanded_walks.append(p)
                    path = []
            path.append(node)
    return expanded_walks


def _generate_sequence(G, graph_path):
    """
    G.nodes['1+']
    :param graph_path:
    :return:
    """
    dna_seq = ""
    for node_name in graph_path:
        dna_seq += G.nodes[node_name]["sequence"]
    return dna_seq


def _translate_dna(seq, min_length=150):

    frame_sequences = {}
    # translate for each frame
    for frame_start in range(3):
        frame_seq = seq[frame_start:]
        rem = len(frame_seq) % 3
        if rem == 1:
            frame_seq += "NN"
        if rem == 2:
            frame_seq += "N"

        mrna = Seq(frame_seq, IUPAC.ambiguous_dna)
        t_seq = mrna.translate()
        frame_sequences[frame_start] = f"{t_seq}"

    def filter_protein(p):
        redundancy_pct = 0.80
        if len(p) < min_length:
            return False
        d = defaultdict(int)
        for aa in p:
            d[aa] += 1
        if max(d.values()) / len(p) > redundancy_pct:
            return False
        return True

    return_list = []
    for item in frame_sequences.items():
        return_list.extend(list(filter(filter_protein, item[1].split("*"))))
    return return_list


def _extract_continuous_traversals(graph):
    # region
    """
        Traversal Extraction
        --------------------
        Given a list of depth-first-search edges, find and extract all
        continuous traversals.

    :param dfs_edge_list: a list of depth-first-search edges
    :return: list of traversals
    """
    # endregion
    logger.info("Begin extracting traversals")
    ret_val = []
    dfs_edge_list = nx.edge_dfs(graph)
    walk = []
    for edge in dfs_edge_list:
        if len(walk) == 0:
            walk.extend([x for x in edge])
        elif edge[0] == walk[-1]:
            walk.append(edge[1])
        else:
            ret_val.append(walk)
            walk = []
            walk.extend([x for x in edge])
    if len(walk) > 0:
        ret_val.append(walk)
    _expand_walk(ret_val)
    logger.info("Finished extracting traversals")
    return ret_val


def _add_node(graph, node):
    graph.add_node(
        node["node_name"],
        length=node["length"],
        coverage=node["coverage"],
        sequence=node["sequence"],
    )
    if node["edges"] is not None:
        graph.add_edges_from(node["edges"])


def _generate_graph(fastg_fname):
    # region
    """
        Generates a digraph from the FASTG file provided.
        The FASTG file must be in SPADES format.
        
        :param fastg_fname: FASTG filename as a full path
        :return: DiGraph based on FASTG edge/node data 
    """
    # endregion
    g = nx.DiGraph()
    with open(fastg_fname, "r") as f:
        node = {}
        for line in f:
            line = line.strip()
            if line.startswith(">"):
                if len(node) > 0:
                    _add_node(g, node)
                    node = {}
                node = _parse_fastg_header(line)
            else:
                node["sequence"] += line.strip()
    _add_node(g, node)
    return g


def _proteins_for_walk(graph, walk, min_length=150):
    obj = {
        "walk": walk,
        "dna_sequence": _generate_sequence(graph, walk),
        "proteins": [],
    }
    obj["proteins"] = _translate_dna(obj["dna_sequence"], min_length=min_length)
    return obj


def _protein_digest(proteins, enz_cleavage="trypsin", min_length=10):
    # (1, 'LTQQNKTIFRLLIAALIIL...EFQLMEAVE') <- p
    prot_pep = []
    for p in proteins:
        o = {
            "prot_id": p[0],
            "peptides": parser.cleave(
                p[1], parser.expasy_rules[enz_cleavage], min_length=min_length
            ),
        }
        prot_pep.append(o)
    return prot_pep


def format_pep_head(item):
    header = ">Pep_"
    header += str(item[0]) + "|Protein_"
    prots = item[1].split(",")
    header += "_".join(prots)
    return header


def write_peptide_fasta(db, fasta_name="peptide.fasta"):
    # (1, '1,1,600')
    pep_prot = db.exec_query(
        "SELECT peptide_id, GROUP_CONCAT(protein_id) FROM peptide_to_protein GROUP BY peptide_id"
    )
    with open(fasta_name, "w") as f:
        for item in pep_prot:
            s = db.exec_query("SELECT sequence FROM peptide WHERE id = " + str(item[0]))
            f.write(format_pep_head(item))
            f.write(os.linesep)
            f.write(s[0][0])
            f.write(os.linesep)


def peptides_for_fastg(
    fastg_filename,
    cleavage="trypsin",
    min_protein_length=166,
    min_peptide_length=10,
    db_name="tst.db",
):
    # region
    """
        FASTG to Protein Library
        ------------------------

        This package generates a candidate protein library in two phases:

            1) Parsing a FASTG file to create graph traversals of longer stretches of DNA
                - FASTG is parsed into a directed graph. A depth-first search is made on all connecting
                    edges. The DFS traversal is then used to concatenate all DNA sequences in the path.
                - DNA sequences are translated to mRNA and split into candidate proteins at the stop 
                    codon. Each DFS traversal can, and will, produce a set of candidate protein sequences.
                - Protein sequences are filtered on length and amino acid redundancy. 
                - Protein sequences are cleaved into peptide sequences.
                - DFS traversals, proteins and peptides are stored in a SQLite database. The linking 
                    relationship between all three is maintained in the DB.
                - A FASTA file of peptides is produced for the user. This FASTA file is to be used
                    in a search against MSMS data.
            2) Using verified peptides as a filter to produce a final candidate peptide library
                - The user will invoke the code with 
                    - DB
                    - list of peptide sequences or peptide FASTA
                - It is expected that the submitted peptides have been verified against MSMS and
                    they represent found and identified peptide sequences
                - The verified peptides are used to filter proteins from the database, these
                    proteins become the final library.
                - The verified peptides are used to score the proteins for 
                    - coverage
                    - percent of verified v. total peptide association
                - Final user output
                    - SQLite database
                    - Protein score text file, comma delimited
                    - Filtered protein FASTA file

    """
    # endregion

    logger.info(f"FASTG file: {fastg_filename}")
    logger.info(f"Protein len: {min_protein_length}")
    logger.info(f"Peptide len: {min_peptide_length}")
    logger.info(f"Cleavage: {cleavage}")
    logger.info(f"Database Name: {db_name}")
    logger.info(f"============================================")

    logger.info("Begin _generate_graph")
    g = _generate_graph(fastg_filename)
    logger.info("End _generate_graph")

    walks = _extract_continuous_traversals(g)
    protein_walk_objs = []

    logger.info("Begin walks")
    for walk in walks:
        obj = _proteins_for_walk(g, walk, min_length=min_protein_length)
        protein_walk_objs.append(obj)
    logger.info("End walks")

    logger.info("Clearing graph object from memory")
    g.clear()

    db = DBManager(db_name)
    db.insert_protein_walk_objects(protein_walk_objs)

    proteins = db.get_protein_sequences()
    db.insert_peptides(
        _protein_digest(proteins, enz_cleavage=cleavage, min_length=min_peptide_length)
    )

    # Write peptide fasta
    write_peptide_fasta(db)


def verified_proteins(
    tabular_file, fdr_level=0.10, decoy_header="XXX_", db_name="tst.db"
):
    # region
    """
        Purpose
        -------
        User has searched peptides against MSMS data. Now, we will produce
        a FASTA library of proteins based on the verified peptides from the search

        Input
        ----------
        MSGF+ tabular output file.

        db_name: DB name used in production of peptide_file

        Output
        -------
        A protein fasta file is written to disk

        A protein score text file is written to disk

    """
    # endregion
    score_tabular(tabular_file, fdr_level, decoy_header, db_name)

