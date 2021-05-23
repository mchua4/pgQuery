#!/usr/bin/env python3

from __future__ import print_function
import mysql.connector
from mysql.connector import errorcode
from parse import GenBankParser, GenPeptParser, PheGenIParser

# Use GenBankParser and PheGenIParser classes from the parser.py file
genbank = GenBankParser()
genpept = GenPeptParser()
phegeni = PheGenIParser()


# Update database with new table(s)
class AddTables:

    def __init__(self=None, tables=None, qry=None):

        self.tables = tables
        self.qry = qry
        self.item = ['id', 'name', 'url', 'db_xref_id', 'db_id', 'accession', 'version', 'feature_id', 'unique_name', 'number', 'trait', 'snp_rs', 'context', 'gene', 'gene_id', 'gene_2', 'gene_id_2', 'chromosome', 'location', 'p_value', 'source', 'pubmed', 'analysis_id', 'study_id', 'study_name']

        self.conn = mysql.connector.connect(user='mchua4', password='mecwy90', host='localhost', database='mchua4')
        self.cursor = self.conn.cursor

        # Table values
        self.db_val = [self.item[0], self.item[1], self.item[2], self.item[3], self.item[4], self.item[5], self.item[6]]
        self.feature_val = [self.item[7], self.item[4], self.item[10]]
        self.phe_gen_i_val = [self.item[11], self.item[12], self.item[13], self.item[7], self.item[15], self.item[16], self.item[17], self.item[18], self.item[19], self.item[20], self.item[21], self.item[22], self.item[23], self.item[24], self.item[25], self.item[26]]

        # Do not create the table if it already exists
        self.cursor.execute("""DROP TABLE IF EXISTS db""")
        self.cursor.execute("""DROP TABLE IF EXISTS feature""")
        self.cursor.execute("""DROP TABLE IF EXISTS phe_gen_i""")

    def create_table(self=None):
        # Create tables in mchua4 database
        self.tables['db'] = (
            "CREATE TABLE IF NOT EXISTS `mchua4`.`db` ("
            " `id` BIGINT NOT NULL,"
            " `name` VARCHAR(255) NOT NULL,"
            " `url` VARCHAR(255) NULL,"
            " `accession` VARCHAR(255) NOT NULL,"
            " `version` VARCHAR(255) NOT NULL,"
            " PRIMARY KEY (`id`),"
            " UNIQUE INDEX `name_UNIQUE` (`name` ASC) VISIBLE,"
            " UNIQUE INDEX `accession_UNIQUE` (`accession` ASC) VISIBLE,"
            " UNIQUE INDEX `version_UNIQUE` (`version` ASC) VISIBLE,"
            " CONSTRAINT `db`"
            "   FOREIGN KEY (`id`)"
            "   REFERENCES `mchua4`.`db` (`id`)"
            "   ON DELETE NO ACTION"
            "   ON UPDATE NO ACTION"
            ") ENGINE = InnoDB;")

        self.tables['feature'] = (
            "CREATE TABLE IF NOT EXISTS `mchua4`.`feature` ("
            " `feature_id` BIGINT NOT NULL,"
            " `unique_name` TEXT NOT NULL,"
            " PRIMARY KEY (`feature_id`),"
            " UNIQUE INDEX `unique_name_UNIQUE` (`unique_name` ASC) VISIBLE,"
            " INDEX `idx` (`id` ASC) VISIBLE,"
            " CONSTRAINT `db`"
            "   FOREIGN KEY (`id`)"
            "   REFERENCES `mchua4`.`db` (`id`)"
            "   ON DELETE NO ACTION"
            "   ON UPDATE NO ACTION"
            ") ENGINE = InnoDB;")

         self.tables['phe_gen_i'] = (
            "CREATE TABLE IF NOT EXISTS `mchua4`.`phe_gen_i` ("
            " `number` BIGINT NOT NULL,"
            " `id` BIGINT NOT NULL,"
            " `trait` TEXT NOT NULL,"
            " `snp_rs` INT NOT NULL,"
            " `context` VARCHAR(255) NOT NULL,"
            " `gene` VARCHAR(255) NOT NULL,"
            " `gene_id` INT NOT NULL,"
            " `gene_2` VARCHAR(255) NOT NULL,"
            " `gene_id_2` INT NOT NULL,"
            " `chromosome` TINYINT NOT NULL,"
            " `location` INT NOT NULL,"
            " `p_value` INT NULL,"
            " `source` VARCHAR(255) NULL,"
            " `pubmed` INT NULL,"
            " `analysis_id` INT NULL,"
            " `study_id` INT NULL,"
            " `study_name` VARCHAR(255) NULL,"
            " PRIMARY KEY (`number`),"
            " INDEX `id` (`feature_id` ASC) VISIBLE,"
            " CONSTRAINT `feature`,"
            "   FOREIGN KEY (`id`),"
            "   REFERENCES `mchua4`.`db` (`id`),"
            "   ON DELETE NO ACTION,"
            "   ON UPDATE NO ACTION,"
            ") ENGINE = InnoDB;")

         # Create tables by iterating over the items of the TABLES dictionary
        for table_name in self.tables:
            table_description = self.tables[table_name]
            try:
                print("Creating table {}: ".format(table_name), end='')
                self.cursor.execute(table_description)
            except mysql.connector.Error as err:
                if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                    print('already exists')
                else:
                    print(err.msg)
            else:
                print("OK")

            return self.tables

    def insert_data(self):
        # Insert and query data
        db_qry = "INSERT INTO `mchua4`.`db`(id, self.description, self.url, self.accession, self.version) VALUES (%s, %s, %s, %s, %s)"
        for self.item in genbank.parse():
            self.cursor.execute(db_qry, self.db_val)
        for self.item in genpept.parse():
            self.cursor.execute(db_qry, self.db_val)

        feature_qry = "INSERT INTO `mchua4`.`feature`(feature_id, db_xref_id, unique_name) VALUES (%s, %s, %)"
        for self.item in genbank.parse():
            self.cursor.execute(feature_qry, self.feature_val)
        for self.item in genpept.parse():
            self.cursor.execute(feature_qry, self.feature_val)

        phe_gen_i_qry = "INSERT INTO `mchua4`.`phe_gen_i`(number, feature_id, trait, snp_rs, context, gene, gene_id, gene_2, gene_id_2, chromosome, location, p_value, source, pubmed, analysis_id, study_id, study_name) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        for self.item in phegeni.parse():
            self.cursor.execute(phe_gen_i_qry, self.phe_gen_i_val)

        self.conn.commit()

        self.cursor.close()
        self.conn.close()

        return self.cursor.execute(db_qry, self.db_val), self.cursor.execute(feature_qry, self.feature_val), self.cursor.execute(phe_gen_i_qry, self.phe_gen_i_val)
