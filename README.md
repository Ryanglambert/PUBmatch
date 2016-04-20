# kojak

Kojak is my final project at thisismetis.com it is now hosted live at PUBmatch.co

This project uses Latent Semantic Indexing to index the entire PubMed Corpus (48GB) in a matter of seconds finding the most conceptually similar research articles for a given email or news article, or anything really.  No keywords necessary.

For a brief overview of the motivation for such a tool please see: http://www.ryanglambert.com/blog/pubmatchco-a-recommendation-engine-for-pubmed

There are two parts of this project: Model Creation and The Similarity Server hosted at PUBmatch.co

### Model Creation

Corresponding code in https://github.com/Ryanglambert/kojak/blob/master/tfidf_pm.py

1. This is done using gensim distributed on a relatively beefy AWS instance with the latest ATLAS BLAS libraries for numpy
1. Memory friendly using a generator (see tfidf_pm.py line 17 - 50)
1. Used multiprocessing library to speed up the generation of the Term Document Matrix from the Pubmed corpus.  Reduced time at this step from 6 hours to 1.5 hours. 
1. TFIDF weighting and Singular Value Decomposition to 300 components takes roughly 4 hours.  
1. Creation of Matrix Similarity gensim object takes roughly 2 hours
1. Total LSI model build time takes ~7-9 hours on a 32 Core 244GB Ram instance on AWS

### Website and Model in Production for querying at PUBmatch.co

Corresponding code in (https://github.com/Ryanglambert/kojak/blob/master/similarity_server.py)

1. Boot Strap + Flask
1. Querying the index for 50 results is done in less than a second.  (However, getting titles for links needs to be ironed out and is slow right now)
1. The LSI model is ~<2GB thanks to SVD bringing it down from 48GB


### Future Improvements

1. Use a database instead of have it sit in memory.  It needs to run on an 8GB instance since the model sits in memory, this makes it fast, but hard to scale if it were to be used by a lot of people at once. It's also a bit expensive to run on AWS for me so there's some financial inspiration as well.  :)

##### Dependencies

Text Processing

`gensim[distributed]`   also see (https://github.com/Ryanglambert/kojak/blob/master/provisioning_gensim_and_blas)
  - `libatlas-base-dev`
  - `gfortran`
  - `numpy`
  - `scipy`

`nltk`

Front End Stuff

`lxml`

`flask`


