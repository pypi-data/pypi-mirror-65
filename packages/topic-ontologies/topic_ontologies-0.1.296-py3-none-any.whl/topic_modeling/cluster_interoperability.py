from conf.configuration import *
from topic_modeling.topic_modeling import *
import logging




def convert_topic_vectors_from_cluster(ontology,model):
    corpora = load_corpora_list()
    logging.warning("preprocessing vectors of %d corpus modeled with %s and %s"%(len(corpora)),ontology,model)
    for corpus in corpora:
        logging.warning("preprocessing %s "%corpus)
        read_cluster_topic_vectors(corpus,ontology,model)


convert_topic_vectors_from_cluster('debatepedia','word2vec-esa-10')