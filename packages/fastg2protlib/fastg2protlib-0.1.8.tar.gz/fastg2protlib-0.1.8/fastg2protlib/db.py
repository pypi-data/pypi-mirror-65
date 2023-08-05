import logging
import os
import sqlite3


class DBManager:
    def __init__(self, name="app.db"):
        self.database_name = name
        self.conn = sqlite3.connect(self.database_name)
        self.cursor = self.conn.cursor()
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(level=os.environ.get("LOGLEVEL", "INFO"))
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            "%(asctime)s %(name)-12s %(levelname)-8s %(message)s"
        )
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
        # Build the tables
        self.cursor.execute(
            """CREATE TABLE IF NOT EXISTS walk
                    (id INTEGER PRIMARY KEY, walk TEXT, dna_sequence TEXT)
                """
        )

        self.cursor.execute(
            """CREATE TABLE IF NOT EXISTS protein 
                    (id INTEGER PRIMARY KEY, sequence TEXT)"""
        )

        self.cursor.execute(
            """CREATE TABLE IF NOT EXISTS peptide
                    (id INTEGER PRIMARY KEY, sequence TEXT)"""
        )

        self.cursor.execute(
            """CREATE TABLE IF NOT EXISTS protein_to_walk
                    (walk_id INTEGER, protein_id INTEGER)"""
        )

        self.cursor.execute(
            """CREATE TABLE IF NOT EXISTS peptide_to_protein
                    (peptide_id INTEGER, protein_id INTEGER)"""
        )

        self.conn.commit()

    def exec_query(self, query):
        return self.cursor.execute(query).fetchall()

    def d_quote(self, str):
        return '"' + str + '"'

    def link_proteins_peptides(self, prot_peps):
        """
        Populate many-to-many table linking peptides to proteins
        prot_pep object:
        {
            "prot_id": int,
            "peptides": set()
        }
        """
        self.logger.info("Begin link_proteins_peptides")
        sql = sqlite3.connect(self.database_name)
        sql.isolation_level = None
        c = sql.cursor()
        c.execute("begin")
        try:
            for obj in prot_peps:
                protein_id = obj["prot_id"]
                pep_seqs = []
                for pep_seq in obj["peptides"]:
                    pep_seqs.append(pep_seq)
                in_clause = "(" + ",".join(list(map(self.d_quote, pep_seqs))) + ")"
                sql_q = f"SELECT id FROM peptide WHERE sequence IN {in_clause}"
                pep_ids = c.execute(sql_q).fetchall()
                ins_data = []
                for pep_id in pep_ids:
                    ins_data.append((pep_id[0], protein_id))
                sql_ins = f"INSERT INTO peptide_to_protein(peptide_id, protein_id) VALUES (?, ?)"
                c.executemany(sql_ins, ins_data)
            c.execute("commit")
        except sql.Error:
            self.logger.error(
                "Transaction failed, rolling back in link_proteins_peptides"
            )
            c.execute("rollback")
        self.logger.info("End link_proteins_peptides")

    def insert_peptides(self, prot_peps):
        """{
            "prot_id": int,
            "peptides": set()
        }
        """
        self.logger.info(f"Begin Insert peptides")
        sql = sqlite3.connect(self.database_name)
        sql.isolation_level = None
        c = sql.cursor()
        c.execute("begin")

        def data_iter(data):
            """Filter out duplicate sequences
            """
            seen = set()
            for item in data:
                if item in seen:
                    pass
                else:
                    seen.add(item)
                    yield item

        try:
            pep_seqs = []
            for pp in prot_peps:
                for p in pp["peptides"]:
                    pep_seqs.append((p,))
            c.executemany(
                "INSERT INTO peptide(sequence) VALUES (?)", data_iter(pep_seqs)
            )
            c.execute("commit")
        except sql.Error:
            self.logger.error("Transaction failed, rolling back in insert_peptides")
            c.execute("rollback")
        self.link_proteins_peptides(prot_peps)
        self.logger.info(f"End Insert peptides")

    def build_links(self, objects):
        """
            Populate many-to-many for proteins to walk traversals
        """
        self.logger.info(f"Begin build_links")
        sql = sqlite3.connect(self.database_name)
        sql.isolation_level = None
        c = sql.cursor()
        c.execute("begin")
        try:
            for object in objects:
                walk = ",".join(object["walk"])
                w_s = f'select id from walk where walk = "{walk}"'
                w_id = c.execute(w_s).fetchone()
                prot_seqs = []
                for p in object["proteins"]:
                    prot_seqs.append(p)
                in_clause = "(" + ",".join(list(map(self.d_quote, prot_seqs))) + ")"
                sql_q = f"SELECT id FROM protein WHERE sequence IN {in_clause}"
                prot_ids = c.execute(sql_q).fetchall()
                ins_data = []
                for prot_id in prot_ids:
                    ins_data.append((w_id[0], prot_id[0]))
                sql_ins = (
                    "INSERT INTO protein_to_walk(walk_id, protein_id) VALUES (?,?)"
                )
                c.executemany(sql_ins, ins_data)
            c.execute("commit")
        except sql.Error:
            self.logger.error("Transaction failed, rolling back in build_links")
            c.execute("rollback")
        self.logger.info(f"End build_links")

    def insert_protein_walk_objects(self, objects):
        self.logger.info(f"Begin insert_protein_walk_objects")
        sql = sqlite3.connect(self.database_name)
        sql.isolation_level = None
        c = sql.cursor()
        c.execute("begin")

        def protein_sequence_iter(objects):
            for object in objects:
                for p in object["proteins"]:
                    yield (p,)

        def walk_sequence_iter(objects):
            for object in objects:
                walk = ",".join(object["walk"])
                seq = object["dna_sequence"]
                yield (walk, seq)

        try:
            c.executemany(
                "INSERT INTO protein(sequence) VALUES (?)",
                protein_sequence_iter(objects),
            )
            c.executemany(
                "INSERT INTO walk (walk, dna_sequence) VALUES (?,?)",
                walk_sequence_iter(objects),
            )
            c.execute("commit")
        except sql.Error:
            self.logger.error(
                "Transaction failed, rolling back in insert_protein_walk_objects"
            )
            c.execute("rollback")
        self.build_links(objects)
        self.logger.info(f"End insert_protein_walk_objects")

    def get_protein_sequences(self):
        self.logger.info(f"Begin get_protein_sequences")
        c = self.conn.execute("select id, sequence from protein")
        r_val = [x for x in c]
        self.logger.info(f"End get_protein_sequences")
        return r_val
