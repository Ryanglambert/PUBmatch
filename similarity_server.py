from gensim import corpora, models, similarities, matutils, interfaces, utils
import multiprocessing
import csv
import os
import pdb
import fileinput
from pprint import pprint 
import sys

from tfidf_pm import PubmedCorpus

#### should use MatrixSimilarity
pubmed_sim = similarities.MatrixSimilarity.load('./pmc_models_serialized/pubmed_sim')
pubmed_tfidf = models.tfidfmodel.TfidfModel.load('./pmc_models_serialized/pubmed_tfidf')
pubmed_lsi = models.LsiModel.load('./pmc_models_serialized/pubmed_lsi')
pubmed_corpus_lsi = models.LsiModel.load('./pmc_models_serialized/pubmed_corpus_lsi')
DOCUMENT_FILE_NAMES = pubmed_corpus_lsi.corpus.corpus.document_file_names
DOCUMENT_FILE_NAMES = map(lambda x: os.path.basename(os.path.splitext(x)[0]), DOCUMENT_FILE_NAMES)
TITLE_DICT = {}

with open('./pmc_data/file_list.txt', 'rb') as csv_f:
    reader = csv.reader(csv_f, delimiter='\t', )
    next(reader, None)
    for row in reader:
        file_name = os.path.basename(os.path.splitext(os.path.splitext(row[0])[0])[0])
        pmc_num = row[3].replace('PMID:', '')
        TITLE_DICT[file_name] = pmc_num

def get_similarity_list(new_doc):
    new_doc = utils.tokenize(new_doc)
    new_doc_bow = pubmed_corpus_lsi.corpus.corpus.dictionary.doc2bow(new_doc)
    new_doc_tfidf = pubmed_tfidf[new_doc_bow]
    new_doc_lsi = pubmed_lsi[new_doc_tfidf]
    new_doc_sims = pubmed_sim[new_doc_lsi]
    return new_doc_sims

def get_pmc_number(doc_tuple):
    sim_num = doc_tuple[0]
    doc_file_name = DOCUMENT_FILE_NAMES[sim_num]
    pmc_num = TITLE_DICT[doc_file_name]
    pmc_link = 'http://www.ncbi.nlm.nih.gov/pubmed/{}'.format(pmc_num)
    return pmc_link

def document_file_names_stripper(file_name):
    stripped_name = os.path.basename(os.path.slitext(file_name)[0])
    return stripped_name

def main():

    while True:
        pmc_sim_nums = []
        new_doc = raw_input('input string: ')
        new_doc_sims = get_similarity_list(new_doc)
        # new_doc_sims_threshold = filter(lambda x: x[1] > .5, new_doc_sims)
        new_doc_sims_threshold = new_doc_sims
        pmc_sim_nums = map(get_pmc_number, new_doc_sims_threshold)
        pmc_doc_sims = zip(pmc_sim_nums, new_doc_sims_threshold)
        pprint(pmc_doc_sims)

if __name__ == '__main__':
    main()








