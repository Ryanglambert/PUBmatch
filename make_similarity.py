from tfidf_pm import *
import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)


print "################# MAKE SIMILARITY OBJECT #############"


# pubmed_tfidf = models.tfidfmodel.TfidfModel.load('./pmc_models_serialized/pubmed_tfidf')

print "################ LOADING LSI MODEL ###############"
pubmed_lsi = models.LsiModel.load('./pmc_models_serialized/pubmed_lsi')

print "################ LOADING LSI CORPUS ###############"

pubmed_corpus_lsi = models.LsiModel.load('./pmc_models_serialized/pubmed_corpus_lsi')

print "################ MAKING SIMILARITY MATRIX ################"

pubmed_sim = similarities.MatrixSimilarity(pubmed_corpus_lsi, num_features=pubmed_lsi.num_topics)

pubmed_sim.save('./pmc_models_serialized/pubmed_sim')


