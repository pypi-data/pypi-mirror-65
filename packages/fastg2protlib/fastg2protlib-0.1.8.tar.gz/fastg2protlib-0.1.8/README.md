# FASTG to Protein Library


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