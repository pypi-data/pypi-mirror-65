import pandas as pd
from conf.configuration import *
import csv
from topic_modeling import *

def model_documents(documents,topic_ontology,topic_model):
    if topic_model == 'esa':
        document_vectors = esa_model(topic_ontology,documents)
    return document_vectors

def save_argument_vectors(argument_ids,argument_vectors,path):
    columns = {}
    columns['argument-id']=argument_ids
    columns['argument-vector']=argument_vectors

    document_vectors = pd.DataFrame(columns)
    document_vectors.to_pickle(path)

def save_document_vectors(document_ids,document_vectors,path):
    columns = {}
    columns['document-id']=document_ids
    columns['document-vector']=document_vectors

    document_vectors = pd.DataFrame(columns)
    print(path)
    document_vectors.to_pickle(path)



def load_dataset(dataset):
    granularity = get_granularity(dataset)
    if granularity =='argument':
        path = get_path_preprocessed_arguments(dataset)
        df_arguments = pd.read_csv(path,quotechar='"',sep="|",quoting=csv.QUOTE_ALL,encoding='utf-8')
        return df_arguments
    else:
        path = get_path_preprocessed_documents(dataset)
        df_documents = pd.read_csv(path,quotechar='"',sep="|",quoting=csv.QUOTE_ALL,encoding='utf-8')
        return df_documents


def model_corpora(topic_ontology,topic_model):
    cluster_corpora = ['args-me','ibm-debater-claim-sentence-search']
    corpora = load_corpora_list()
    for corpus in corpora:
        if corpus not in cluster_corpora:
            granularity= get_granularity(corpus)
            if granularity =='document':
                path = get_path_document_vectors(corpus,topic_ontology,topic_model)
                dataset= load_dataset(corpus)
                document_ids = list(dataset['document-id'])
                documents = list(dataset['document'])
                document_vectors = model_documents(documents,topic_ontology,topic_model)
                save_document_vectors(document_ids,document_vectors,path)
            else:
                path = get_path_argument_vectors(corpus,topic_ontology,topic_model)
                dataset=load_dataset(corpus)
                argument_ids= list(dataset['argument-id'])
                arguments = list(dataset['argument'])
                argument_vectors = model_documents(arguments,topic_ontology,topic_model)
                save_argument_vectors(argument_ids,argument_vectors,path)


#model_corpora('strategic-intelligence','esa')
model_corpora('strategic-intelligence-sub-topics','esa')
#model_corpora('debatepedia','esa')
model_corpora('wikipedia','esa')
