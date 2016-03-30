from tfidf_pm import *
import csv
import os

#### should use MatrixSimilarity
pubmed_sim = similarities.Similarity.load('./pmc_models_serialized/pubmed_sim')
pubmed_tfidf = models.tfidfmodel.TfidfModel.load('./pmc_models_serialized/pubmed_tfidf')
pubmed_lsi = models.LsiModel.load('./pmc_models_serialized/pubmed_lsi')
pubmed_corpus_lsi = models.LsiModel.load('./pmc_models_serialized/pubmed_corpus_lsi')
DOCUMENT_FILE_NAMES = pubmed_corpus_lsi.corpus.corpus.document_file_names
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

def get_pmc_number(sim_num):
    
    

def main():







