import logging
import pandas as pd
from conf.configuration import *
import csv
import argument_esa_model.esa_all_terms
from topic_modeling import *
def load_documents(corpus):
    granularity = get_granularity(corpus)
    if granularity =='document':
        dataset_preprocessed_path =get_path_preprocessed_documents(corpus)
        df_documents= pd.read_csv(dataset_preprocessed_path,quotechar='"',sep="|",quoting=csv.QUOTE_ALL,encoding="utf-8")
        ids = list(df_documents['document-id'])
        texts= list(df_documents['document'])
    else:
        dataset_preprocessed_path =get_path_preprocessed_arguments(corpus)
        df_arguments= pd.read_csv(dataset_preprocessed_path,quotechar='"',sep="|",quoting=csv.QUOTE_ALL,encoding="utf-8")
        ids = list(df_arguments['argument-id'])
        texts= list(df_arguments['argument'])

    return texts,ids

def model_text(topic_ontology,text):
    path_topic_model = get_path_topic_model('ontology-'+topic_ontology,'esa')
    path_word2vec_model = get_path_topic_model('word2vec','word2vec')
    path_word2vec_vocab = get_path_vocab('word2vec')

    topic_dict = argument_esa_model.esa_all_terms.model_topic(path_topic_model,path_word2vec_model,path_word2vec_vocab,'cos',text)
    sorted_topic_dict = sorted(topic_dict )
    return  sorted_topic_dict.keys()


def save_argument_vectors(argument_ids,argument_vectors,path):
    columns = {}
    columns['argument-id']=argument_ids
    columns['document-vector']:argument_vectors
    df_argument_vectors = pd.DataFrame(columns)
    df_argument_vectors.to_pickle(path)
def save_document_vectors(document_ids,document_vectors,path):
    columns = {}
    columns['document-id']=document_ids
    columns['document-vector']=document_vectors

    df_document_vectors = pd.DataFrame(columns)
    df_document_vectors.to_pickle(path)


def configure_logging(corpus):
    file_name="../logs/model-%s.log"%corpus
    logging.basicConfig(filename=file_name,level=logging.DEBUG)
def mode_corpus(corpus):
    configure_logging(corpus)

    texts,ids = load_documents(corpus)

    granularity = get_granularity(corpus)
    logging.warning("Read %d %s"%(len(texts),granularity))
    topic_ontologies = get_topic_ontologies()

    for topic_ontology in topic_ontologies:
        logging.warning("Modeling corpus %s with ontology %s "%(corpus,topic_ontology))
        argument_esa_model.esa_all_terms.initialize_model()
        vectors=esa_model(topic_ontology,texts)

        if granularity=='document':
            path = get_path_document_vectors(corpus,topic_ontology,'esa')
            save_document_vectors(ids,vectors,path)
        else:
            path = get_path_argument_vectors(corpus,topic_ontology,'esa')
            save_argument_vectors(ids,vectors,path)
mode_corpus('cornell-change-my-view')