#!/usr/bin/env python3

import os
import glob
import json
import pandas as pd
from Bio import SeqIO, GenBank
from annotation import GenPeptEntry, Feature, PhenotypeGenotype


# Record database name
def get_db_name(self):
    return str(self)


# Parse from GenBank using biopython
class GenBankParser:

    def __init__(self, id=None, get_url=None):
        self.id = id
        self.get_url = get_url

    def parse(self):
        with open("GenBank/*.gb") as handle:
            for record in GenBank.parse(handle):
                self.id += 1
                return get_db_name(self), self.id, record.accession, self.get_url, record.id, record.name, record.dbxrefs


# Parse from GenPept
class GenPeptParser:
    genpept_entry = GenPeptEntry()
    feature = Feature()

    gi = genpept_entry.get_gi()
    protein = genpept_entry.get_proteins()

    feature_id = feature.feature_id()
    db_id = feature.db_id()

    def __init__(self, id=None, info=None, annotate=None, seq_record=None, unique_name=None, accession=None, seq_feature=None, feature_id=None, url=None):

        self.id = id
        self.info = info
        self.annotate = annotate
        self.seq_record = seq_record
        self.unique_name = unique_name
        self.accession = accession
        self.seq_feature = seq_feature
        self.url = url

        self.Feature_ID = feature_id

        feature = pd.DataFrame({'self.Feature_ID': None, 'record.accession': None, 'self.feature': None, 'self.info': None}, index=[0])

        def iter_rows(df):
            for row in df.itertuples(index=True, name='Pandas'):
                yield row.self.Feature_ID, row.record.accession, row.self.feature, row.self.info

        self.feature = iter_rows(feature)


    # Parse the GenPept data files
    path = 'data/protein/*'

    def parse(self, path):
        for self.seq_record in glob.glob(os.path.join(path)):
            print(self.seq_record)
            for index, record, get_db_name, gi, url, accession, version in enumerate(SeqIO.parse('self.seq_record', 'genpept')):
                for info in self.info:
                    ordered_dict = info.annotations['structured_comment']
                    self.annotate = json.loads(json.dumps(ordered_dict))
                    self.id += 1
                    return self.id, get_db_name(self), self.gi, record.accession, self.get_url, record.id, record.name, record.dbxrefs

    # Action support
    def get_url(self):
        if 'URL' in self.annotate['Genome-Annotation-Data']['Annotation Provider']:
            return self.url

    # Feature information
    def add_feature(self):
        for feature in self.seq_record.seq_feature:
            self.Feature_ID += 1
            if 'locus_tag' in feature.qualifiers:
                self.unique_name = feature.qualifiers['locus_tag'][0]
                return self.unique_name, self.feature_id


# Parse from PheGenI
class PheGenIParser:
    phe_gen = PhenotypeGenotype()

    number = 0
    gene_id = phe_gen.gene_id()
    gene_id_2 = phe_gen.gene_id_2

    def __init__(self=None, file=None, phe_gen_i=None, id=None, gene=None, gene_id=None, gene_2=None, gene_id_2=None, trait=None, snp_rs=None, context=None, chromosome=None, location=None, p_value=None, source=None, pubmed=None, analysis_id=None, study_id=None, study_name=None):

        self.unique_name = None
        self.file = file
        self.phe_gen_i = phe_gen_i
        self.id = id
        self.gene = gene
        self.gene_id = gene_id
        self.gene_2 = gene_2
        self.gene_id_2 = gene_id_2
        self.trait = trait
        self.snp_rs = snp_rs
        self.context = context
        self.chromosome = chromosome
        self.location = location
        self.p_value = p_value
        self.source = source
        self.pubmed = pubmed
        self.analysis_id = analysis_id
        self.study_id = study_id
        self.study_name = study_name

        if self.study_id is None:
            self.study_id = list()

        if self.study_name is None:
            self.study_name = list()

    def parse(self, annotate=None):

        # Parse the Phe_Gen data file
        with pd.readcsv('PheGenI.tab', sep='\t', engine='python') as self.file:
            for info in self.file:
                return self.id, get_db_name(self), annotate.PhenotypeGenotype(self.add_phegeni)

    def get_number(self):
        self.number = self.file.phegen['#'][0]
        return self.number

    # Add Phenotype-Genotype information
    def add_phegeni(self, genbank=None):
        for self.phegeni in self.file.number:
            if self.file.phegen[4] == genbank.add_feature(self.unique_name):
                self.number += 1
                self.trait = self.file.phegen[1]
                self.snp_rs = self.file.phegen[2]
                self.context = self.file.phegen[3]
                self.gene = self.file.phegen[4]
                self.gene_id = self.file.phegen[5]
                self.gene_2 = self.file.phegen[6]
                self.gene_id_2 = self.file.phegen[7]
                self.chromosome = self.file.phegen[8]
                self.location = self.file.phegen[9]
                self.p_value = self.file.phegen[10]
                self.source = self.file.phegen[11]
                self.pubmed = self.file.phegen[12]
                self.analysis_id = self.file.phegen[13]
                self.study_id = self.file.phegen[14]
                self.study_name = self.file.phegen[15]

                return self.number, self.trait, self.snp_rs, self.context, self.gene, self.gene_id, self.gene_2, self.gene_id_2, self.chromosome, self.location, self.p_value, self.source, self.pubmed, self.analysis_id, self.study_id, self.study_name
