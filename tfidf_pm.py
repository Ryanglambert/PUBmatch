import pdb 
import os
import pickle
from gensim import corpora, models, similarities, matutils, interfaces, utils
from nltk.corpus import stopwords
import numpy as np
import sys
import multiprocessing
import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

pool_size = max(1, multiprocessing.cpu_count() - 3)
STOP_WORDS = stopwords.words('english')
DATA_PATH = (u'./pmc_data/pmc_text_files/')
SAVE_LOCATION = './pmc_models_serialized/'

class PubmedCorpus(corpora.textcorpus.TextCorpus):
    def __init__(self, data_folder=DATA_PATH):
        self.data_folder = data_folder
        self.dictionary = corpora.Dictionary()
        self.document_file_names = []
        
    def __iter__(self):
        pool = multiprocessing.Pool(pool_size)        
        for file_chunk in utils.chunkize(self.file_path_iter(), chunksize=200, maxsize=20):
            docs = pool.imap(tokenized_from_file, file_chunk)
            for doc_tokenized in docs:
                yield self.dictionary.doc2bow(doc_tokenized)
        pool.terminate()     

    def __len__(self):
        if not hasattr(self, 'length'):
            self.length = sum(1 for _ in self.__iter__())
        return self.length

### TODO clean up redundancy    

    def load_corpus(self):
        pool = multiprocessing.Pool(pool_size)
        for file_chunk in utils.chunkize(self.file_path_iter(), chunksize=200 , maxsize=20):
            results = pool.imap(tokenized_from_file, file_chunk)
            self.dictionary.add_documents(results, prune_at=200000)
            self.document_file_names += [file_path for file_path in file_chunk]
        pool.terminate()            

    def file_path_iter(self):
        for root, dirs, files in os.walk(self.data_folder):
            for file_name in files:
                file_path = os.path.join(root, file_name)
                yield file_path

def tokenized_from_file(file_path):
    with open(file_path, 'rb') as f:
        doc = f.read()
        doc_token_gen = utils.tokenize(doc, lowercase=True)
        doc_tokenized = [i for i in doc_token_gen if i not in STOP_WORDS]
        return doc_tokenized

def is_dist_or_not():
    dist_input = ''
    try:
        dist_input = sys.argv[1]
    except IndexError:
        pass
    if dist_input == 'distributed':
        dist_or_not = True
    else:
        dist_or_not = False
    return dist_or_not


def to_unicode_or_bust(
        obj, encoding='utf-8'):
    if isinstance(obj, basestring):
        if not isinstance(obj, unicode):
            obj = unicode(obj, encoding)
    return obj
              
def main():
    pubmed_corpus = PubmedCorpus()
    
    print "################ BUILDING CORPUS ###############"

    pubmed_corpus.load_corpus()
    pubmed_corpus.dictionary.save(os.path.join(SAVE_LOCATION, 'pubmed_corpus.dict'))
    with open(os.path.join(SAVE_LOCATION, 'document_file_names'), 'w') as f:
        pickle.dump(pubmed_corpus.document_file_names, f)
    corpora.MmCorpus.serialize('./pmc_models_serialized/pubmed_corpus.mm', pubmed_corpus)
    
    print "################ BUILDING TFIDF ###############"
    pubmed_tfidf = models.TfidfModel(pubmed_corpus, normalize=True)
    pubmed_tfidf.save(os.path.join(SAVE_LOCATION, 'pubmed_tfidf'))
    
    pubmed_corpus_tfidf = pubmed_tfidf[pubmed_corpus]
    pubmed_corpus_tfidf.save(os.path.join(SAVE_LOCATION, 'pubmed_corpus_tfidf'))

    print "################# STARTING LSI MODEL ###############"

    pubmed_lsi = models.LsiModel(pubmed_corpus_tfidf, 
                                 id2word=pubmed_corpus.dictionary, 
                                 num_topics=1000,
                                 chunksize=20000,
                                 distributed=is_dist_or_not())

    print "################# STARTING LSI TRANSFORMATION #############"

    pubmed_corpus_lsi = pubmed_lsi[pubmed_corpus_tfidf]

    print "################# SAVING LSI AND LSI_CORPUS  #############"

    pubmed_lsi.save(os.path.join(SAVE_LOCATION, 'pubmed_lsi'))
    pubmed_corpus_lsi.save(os.path.join(SAVE_LOCATION, 'pubmed_corpus_lsi'))

    print("######### DONE!!!! ##########")

if __name__ == '__main__':
    main()
