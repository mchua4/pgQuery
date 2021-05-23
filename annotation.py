#!/usr/bin/env python3

class GenPeptEntry:

    # Use a constructor to initialize fundamental methods for annotating GenPept entries
    def __init__(self, features=None, gi=None, accession=None, version=None, url=None, annotation_provider=None):

        self.features = features
        self.gi = gi
        self.accession = accession
        self.version = version
        self.url = url
        self.annotation_provider = annotation_provider

    # Represent the class object get_gi as a string
    def __str__(self):
        return 'GenPeptEntry-' + str(self.get_gi())

    def __repr__(self):
        return '<GenPeptEntry {0} {1}>'.format(self.get_gi(), self.feature())

    # Use a comparison predicate to define the behavior of the less-than operator
    def __lt__(self, other):
        if type(self) != type(other):
            raise Exception('Incompatible argument to __lt__: ' + str(other))
        return self.get_gi() < other.get_gi()

    # Access methods to return values based on the fields of an instance
    def get_gi(self):
        return self.gi

    def get_proteins(self):
        if self.features is not None:
            return [feature.get_qualifier('protein') for feature in self.features if feature.is_protein()]

    def feature(self):
        return self.feature


class Feature:
    # Class fields
    Feature_ID = 0
    DB_ID = 0

    @classmethod
    def feature_id(cls):
        cls.Feature_ID += 1

    @classmethod
    def db_id(cls):
        cls.DB_ID += 1

    # Use a constructor to initialize fundamental methods for the features
    def __init__(self, db=None, feature=None):
        self.db = db
        self.feature = feature

        if self.feature is None:
            self.feature = list()

    # Represent the class object db as a string
    def __str__(self):
        self.representation = 'Database: {0}\nIdentifier : {self.db}\n'

        if len(self.feature) > 0:
            self.representation += 'feature:\n'

            for sequence in self.feature:
                self.representation += '\t{0}:{4}\n'.format(sequence.id, sequence.unique_name, sequence.residues, sequence.qualifier)

        else:
            self.representation += 'feature:\n'

            return self.representation


class PhenotypeGenotype:
      # Class fields
    number = 0

    # Use a constructor to initialize fundamental methods for phenotype and genotype
    def __init__(self, gene=None, gene_2=None):
        self.gene_id_2 = None
        self.gene = gene
        self.gene_2 = gene_2

    # Represent the class objects as a string
    def __str__(self):

        self.representation = '{0}\n ({1}\n) associated with {2}\n ({3}\n)'.format(self.gene)

        if len(self.gene) > 0:
            self.representation = 'Gene:\n'
            for number in self.gene:
                self.representation += '\tGene:{0}\n'.format(number.gene_id)

        else:
            self.representation += 'Gene: None\n'

        if len(self.gene_2) > 0:
            self.representation = 'Gene_2:\n'
            for gene_2 in self.gene_2:
                self.representation += '\tGene_2:{0}'.format(gene_2.gene_id_2)

        else:
            self.representation = 'Gene_2: None\n'

        return self.representation

    def gene_id(self):
        return self.gene_id
