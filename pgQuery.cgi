#!/usr/local/bin/python3

import mysql.connector
import cgi
import jinja2
from database_creator import AddTables


# Use the AddTables class from database_creator
tables = AddTables


# Query the tables in database_creator
def main():

    form = cgi.FieldStorage()
    search_term = form.getvalue('search_term')

    # Create environment and load a specific template
    templateLoader = jinja2.FileSystemLoader(searchpath='./templates')
    env = jinja2.Environment(loader=templateLoader)
    template = env.get_template('template.html')

    # Connect to MySQL database
    conn = mysql.connector.connect(user='mchua4', password='Mecwy90*', host='localhost', database='mchua4')
    cursor = conn.cursor()

    # Results dictionary
    results = {'match_count': 0, 'matches': list()}

    # Query protein info
    if search_term is not None:
        qry = """
            SELECT f.unique_name, f.description, db.name AS database, db.url, db_xref.accession, db_xref.version
            FROM feature f
                JOIN db_xref dx on f.dbxref_id = dx.dbxref_id
                JOIN db ON db_xref.db_id = db_xref.db_id = db.db_id
                WHERE unique_name LIKE %s;

            """
        cursor.execute(qry, ('%' + search_term + '%',))

        # Add protein and database information
        for (unique_name, description, database, url, accession, version) in cursor:
            results['matches'].append({'unique_name': unique_name, 'description': description, 'database': database, 'url': url, 'accession': accession, 'version': version})

    # Query Phenotype-Genotype info
    if search_term is not None:
        qry = """
            SELECT pg.trait, pg.snp_rs, pg.context, pg.gene, pg.gene_id, pg.gene_2, pg.gene_id_2, pg.p_value, pg.source, pg.pubmed, pg.analysis_id, pg.study_id, pg.study_name
            FROM phe_gen_i pg
                JOIN feature f ON f.feature_id = pg.feature_id
                WHERE gene LIKE %s;
            """
        cursor.execute(qry, ('%' + search_term + '%', ))

        # Add Phenotype-Genotype information
        for (trait, snp_rs, context, gene, gene_id, gene_2, gene_id_2, p_value, source, pubmed, analysis_id, study_id, study_name) in cursor:
            results['matches'].append({'trait': trait, 'snp_rs': snp_rs, 'context': context, 'gene': gene, 'gene_id': gene_id, 'gene_2': gene_2, 'gene_id_2': gene_id_2, 'p_value': p_value, 'source': source, 'pubmed': pubmed, 'analysis_id': analysis_id, 'study_id': study_id, 'study_name': study_name})

    cursor.close()
    conn.close()

    print('Content-Type: text/html\n\n')
    print(template.render(results=results,))


if __name__ == '__main__':
    main()
