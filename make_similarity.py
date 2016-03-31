from tfidf_pm import *

print "################# MAKE SIMILARITY OBJECT #############"


# pubmed_tfidf = models.tfidfmodel.TfidfModel.load('./pmc_models_serialized/pubmed_tfidf')

pubmed_lsi = models.LsiModel.load('./pmc_models_serialized/pubmed_lsi')
pubmed_corpus_lsi = models.LsiModel.load('./pmc_models_serialized/pubmed_corpus_lsi')

pubmed_sim = similarities.MatrixSimilarity(pubmed_corpus_lsi, pubmed_lsi.num_topics)

pubmed_sim.save('./pmc_models_serialized/pubmed_sim')


