import pandas as pd
from conf.configuration import *
import csv
import argument_esa_model.esa_all_terms

def load_documents():
    dataset_preprocessed_path =get_path_preprocessed_documents('utdallas-icle-essay-scoring')
    documents= pd.read_csv(dataset_preprocessed_path,quotechar='"',sep="|",quoting=csv.QUOTE_ALL,encoding="utf-8")

    ids = list(documents['document-id'])
    texts= list(documents['document'])

    return texts,ids

def model_text(topic_ontology,text):
    path_topic_model = get_path_topic_model('ontology-'+topic_ontology,'esa')
    path_word2vec_model = get_path_topic_model('word2vec','word2vec')
    path_word2vec_vocab = get_path_vocab('word2vec')

    topic_dict = argument_esa_model.esa_all_terms.model_topic(path_topic_model,path_word2vec_model,path_word2vec_vocab,'cos',text)
    sorted_topic_dict = sorted(topic_dict )
    return  sorted_topic_dict.keys()


def save_document_vectors(document_ids,document_vectors,path):
    columns = {}
    columns['document-id']=document_ids
    columns['document-vector']=document_vectors

    document_vectors = pd.DataFrame(columns)
    document_vectors.to_pickle(path)


texts,ids = load_documents()
document_vectors = model_text('strategic-intlligence','esa')
path = get_path_document_vectors('utdallas-icle-essay-scoring','strategic-intelligence','esa')
save_document_vectors(ids,document_vectors,path)