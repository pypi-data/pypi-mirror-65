import pandas as pd
from conf.configuration import *
import csv
from topic_modeling import *

def load_arguments():
    dataset_preprocessed_path =get_sample_path('args-me')
    arguments= pd.read_csv(dataset_preprocessed_path,quotechar='"',sep="|",quoting=csv.QUOTE_ALL,encoding="utf-8")
    ids = list(arguments['argument-id'])
    texts= list(arguments['text'])
    return texts,ids

def model_arguments(arguments,topic_ontology):
    argument_vectors = esa_model(topic_ontology,arguments)
    return argument_vectors

def save_argument_vectors(argument_ids,argument_vectors,path):
    columns = {}
    columns['argument-id']=argument_ids
    columns['argument-vector']=argument_vectors

    argument_vectors = pd.DataFrame(columns)
    argument_vectors.to_pickle(path)

a=get_path_preprocessed_documents('args-me')
print(a)
texts,ids = load_arguments()
print(ids[0])
argument_vectors = model_arguments(texts,'strategic-intelligence-sub-topics')
path = get_path_argument_vectors('args-me','strategic-intelligence-sub-topics','esa')
save_argument_vectors(ids,argument_vectors,path)