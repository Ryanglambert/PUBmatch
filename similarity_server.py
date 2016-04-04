from gensim import corpora, models, similarities, matutils, interfaces, utils
import multiprocessing
import csv
import os
import pdb
import fileinput
from pprint import pprint 
import logging
import sys
from lxml import html

from tfidf_pm import PubmedCorpus

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

TITLE_DICT = {}
pubmed_link_cache = {}

#### should use MatrixSimilarity

with open('./pmc_data/file_list.txt', 'rb') as csv_f:
    reader = csv.reader(csv_f, delimiter='\t', )
    next(reader, None)
    for row in reader:
        file_name = os.path.basename(os.path.splitext(os.path.splitext(row[0])[0])[0])
        pmc_num = row[3].replace('PMID:', '')
        pmid = row[2]
        pm_title = row[1]
        TITLE_DICT[file_name] = pmc_num, pmid, pm_title

def try_pubmed_cache(pm_link):
    try:
        title = pubmed_link_cache[pm_link]
    except KeyError:
        return None

def get_similarity_list(new_doc):
    new_doc = utils.tokenize(new_doc)
    new_doc_bow = pubmed_corpus_lsi.corpus.corpus.dictionary.doc2bow(new_doc)
    new_doc_tfidf = pubmed_tfidf[new_doc_bow]
    new_doc_lsi = pubmed_lsi[new_doc_tfidf]
    new_doc_sims = pubmed_sim[new_doc_lsi]
    return new_doc_sims

def get_pmc_number(doc_tuple):
    if isinstance(doc_tuple, tuple):
        sim_num = doc_tuple[0]
        doc_file_name = DOCUMENT_FILE_NAMES[sim_num]
        pmc_num = ''
        pmc_page_title = ''
        try:
            pmc_num = TITLE_DICT[doc_file_name][0]
            pmc_link = 'http://www.ncbi.nlm.nih.gov/pubmed/{}'.format(pmc_num)
            try:
                pmc_page_title = pubmed_link_cache[pmc_link]
            except KeyError:
                print "didn't get from cache"
                t = html.parse(pmc_link)
                pmc_page_title = t.find(".//title").text
                pubmed_link_cache[pmc_link] = pmc_page_title

        except KeyError:
            return None
        if pmc_num == '':
            pmid = TITLE_DICT[doc_file_name][1]
            pmid_link = 'http://www.ncbi.nlm.nih.gov/pubmed/?term={}'.format(pmid)
            try:
                pmc_page_title = pubmed_link_cache[pmid_link]
            except KeyError:
                print "didn't get frmo cache"
                t = html.parse(pmid_link)
                pmc_page_title = t.find(".//title").text
                pubmed_link_cache[pmid_link] = pmc_page_title
            return pmid_link, pmc_page_title
        return pmc_link, pmc_page_title

def get_pmc_title(doc_tuple):
    if isinstance(doc_tuple, tuple):
        sim_num = doc_tuple[0]
        doc_file_name = DOCUMENT_FILE_NAMES[sim_num]
        try:
            pm_title = TITLE_DICT[doc_file_name][2]
            return pm_title
        except KeyError:
            return None

def document_file_names_stripper(file_name):
    stripped_name = os.path.basename(os.path.slitext(file_name)[0])
    return stripped_name

MODEL_FOLDER = './pmc_models_from_remote/pmc_models_serialized_300f_pruneat200000'
# MODEL_FOLDER = './pmc_models_serialized_small/'

pubmed_sim = similarities.MatrixSimilarity.load(os.path.join(MODEL_FOLDER, 'pubmed_sim'))
pubmed_sim.num_best = 20
pubmed_tfidf = models.tfidfmodel.TfidfModel.load(os.path.join(MODEL_FOLDER, 'pubmed_tfidf'))
pubmed_lsi = models.LsiModel.load(os.path.join(MODEL_FOLDER, 'pubmed_lsi'))
pubmed_corpus_lsi = models.LsiModel.load(os.path.join(MODEL_FOLDER, 'pubmed_corpus_lsi'))
DOCUMENT_FILE_NAMES = pubmed_corpus_lsi.corpus.corpus.document_file_names
DOCUMENT_FILE_NAMES = map(lambda x: os.path.basename(os.path.splitext(x)[0]), DOCUMENT_FILE_NAMES)

###### Flask Starts Here ######

from flask import Flask, url_for, request, render_template
app = Flask(__name__)

@app.route('/')
def my_form():
    return render_template('article_input.html')

@app.route('/', methods=['POST'])
def my_form_post():
    new_doc = request.form['article_input_2']
    new_doc_sims = get_similarity_list(new_doc)
    new_doc_sims = map(lambda x: (x[0], round(x[1], 2)), new_doc_sims)
    sim_pm_titles = map(get_pmc_title, new_doc_sims)
    pmc_sim_nums = map(get_pmc_number, new_doc_sims)
    pmc_doc_sims = zip(pmc_sim_nums, new_doc_sims, sim_pm_titles)
    
    return render_template('pubmed_list.html', pmids=pmc_doc_sims)

if __name__ == '__main__':
    app.run(debug=True)








