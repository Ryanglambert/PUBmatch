#!/bin/bash
export PYRO_THREADPOOL_SIZE=30
python -m Pyro4.naming -n 0.0.0.0 &     #Start the Pyro namenode
# Start gensim workers, run this once for each core that you want to distribute over
# Probably at least leave one core out
python -m gensim.models.lsi_worker &
python -m gensim.models.lsi_worker &
python -m gensim.models.lsi_worker &
python -m gensim.models.lsi_worker &
python -m gensim.models.lsi_worker &
python -m gensim.models.lsi_worker &
python -m gensim.models.lsi_worker &
python -m gensim.models.lsi_worker &
python -m gensim.models.lsi_worker &
python -m gensim.models.lsi_worker &
python -m gensim.models.lsi_worker &
python -m gensim.models.lsi_worker &
python -m gensim.models.lsi_worker &
python -m gensim.models.lsi_worker &
python -m gensim.models.lsi_worker &
python -m gensim.models.lsi_worker &
python -m gensim.models.lsi_worker &
python -m gensim.models.lsi_worker &
python -m gensim.models.lsi_worker &
python -m gensim.models.lsi_worker &
python -m gensim.models.lsi_worker &
python -m gensim.models.lsi_worker &
python -m gensim.models.lsi_worker &
python -m gensim.models.lsi_worker &
python -m gensim.models.lsi_worker &
python -m gensim.models.lsi_worker &
# Start gensim dispatcher (organizes jobs to send work to workers)
# You only need to run one of these
python -m gensim.models.lsi_dispatcher &
