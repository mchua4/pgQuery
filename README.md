# pgQuery
Phenotype-Genotype Query tool

* ABOUT *

Web front-end for phenotype-genotype analysis in cancer models. Created for the final project of class AS.410.712.82.SP21 Advanced Practical Computer Concepts for Bioinformatics at Johns Hopkins University.

Source code can be obtained here:
/var/www/html/mchua4/final/pgQuery.tar

Demo with pre-uploaded files:
http://bfx3.aap.jhu.edu/mchua4/final/pgQuery.cgi?search_term=TP53


Included ea-utils binaries are Linux ELF x86.

Storage is minimal.   Data transfer should be at least 2 mbit for reasonable
processing times of FASTQs.

Recommended memory/cpu is 1gb, 1.8ghz per simultaneous user.

* DETAILED USAGE *

1. Enter the protein ID or name.  

2. Click "Submit"

3. Each table should appear with id, protein name, database found, url, accession, version, trait, snp-rs, context, gene, gene_id, second gene (related to the first gene), id of the 2nd gene, p-value, source, pubmed, analysis-id, study-id, and study name. 


* DEMO DATA *

Truncated demo data can be found here:

http:// bfx3.aap.jhu.edu/mchua4/final/ pgQuery.tar
Demo files are based on data from GenPept:

https://www.ncbi.nlm.nih.gov/protein/
