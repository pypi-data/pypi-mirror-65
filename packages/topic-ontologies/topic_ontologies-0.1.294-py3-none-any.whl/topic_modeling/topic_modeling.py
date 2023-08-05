import argument_esa_model.esa_all_terms
import argument_esa_model.esa_top_n_terms
import tqdm
import numpy as np
from conf.configuration import *
from topics import *
import pandas as pd

import logging
import os

import codecs
import pickle



def dict_to_np_array(dictionary):
    vector  = []
    for key in sorted(dictionary):
        vector.append(dictionary[key])
    np_arr= np.array(vector)

    return np_arr

def esa_model(topic_ontology,texts):
    path_topic_model = get_path_topic_model('ontology-'+topic_ontology,'esa')
    path_word2vec_model = get_path_topic_model('word2vec','word2vec')
    path_word2vec_vocab = get_path_vocab('word2vec')
    document_vectors = []
    for text in tqdm.tqdm(texts):
        vector = argument_esa_model.esa_all_terms.model_topic(path_topic_model,path_word2vec_model,path_word2vec_vocab,'cos',text)
        document_vectors.append(dict_to_np_array(vector))
    return document_vectors

def word2vec_esa_model(topic_ontology,texts):
    None

def model(topic_ontology,topic_model,texts):
    document_vectors = []
    if topic_model =='esa':
        if topic_ontology=='strategic-intlligence':
            for text in tqdm.tqdm(texts):
                vector = esa_model_strategic_intelligence.process(text, False)
                document_vectors.append(dict_to_np_array(vector))
        if topic_ontology == 'debatepedia':
            for text in tqdm.tqdm(texts):
                vector = esa_model_debatepedia.process(text, False)

                document_vectors.append(dict_to_np_array(vector))
    return document_vectors


def parse_file(path):

    vectors=[]
    ids=[]
    with open(path,'r',encoding='utf-8') as file:
        for i,line in enumerate(file):
            line_without_brackts = line[1:-2]
            tokens = line_without_brackts.split("', '")
            if len(tokens)!=2:
                tokens = line_without_brackts.split("\", '")
                if len(tokens)!=2:
                    raise ValueError("format mismatch")
            id = tokens[1][:-1]
            ids.append(id)

            np_array = pickle.loads(codecs.decode(tokens[0][1:].replace('\\n','').encode(), "base64"))

            vectors.append(np_array)
    return vectors,ids


def load_topics(topic_ontology):
    path_topics = get_path_topics(topic_ontology)
    topics_df=pd.read_csv(path_topics).sort_values('name')
    return list(topics_df['name'])

def read_cluster_topic_vectors(dataset,topic_ontology,topic_model):
    granularity = get_granularity(dataset)
    logging.warning("Preprocessing %s with %s and %s"%(dataset,topic_ontology,topic_model))
    if granularity == 'argument':
        path_argument_vectors = get_path_argument_vectors(dataset,topic_ontology,topic_model)
        path_argument_vectors_cluster = get_path_argument_vectors(dataset,topic_ontology,topic_model).replace(".csv","")
        vectors_with_ids= {}
        vectors_with_ids['argument-id']=[]
        vectors_with_ids['argument-vector']=[]
        for root,dirs,files in os.walk(path_argument_vectors_cluster):
            for file in tqdm.tqdm(files):
                path = os.path.join(root,file)
                vectors,ids=parse_file(path)
                vectors_with_ids['argument-id'].extend(ids)
                vectors_with_ids['argument-vector'].extend(vectors)
        df_argument_vectors=pd.DataFrame(vectors_with_ids)
        df_argument_vectors.to_pickle(path_argument_vectors)
    elif granularity == 'document':
        path_document_vectors = get_path_document_vectors(dataset,topic_ontology,topic_model)
        path_document_vectors_cluster = get_path_document_vectors(dataset,topic_ontology,topic_model).replace(".csv","")
        logging.warning("Converting vectors form %s to %s"%(path_document_vectors_cluster,path_document_vectors))
        vectors_with_ids= {}
        vectors_with_ids['document-id']=[]
        vectors_with_ids['document-vector']=[]

        for root,dirs,files in os.walk(path_document_vectors_cluster):
            for file in tqdm.tqdm(files):
                path = os.path.join(root,file)
                logging.warning("Preprocessing %s"%file)
                vectors,ids=parse_file(path)
                logging.warning(("Found %d vectors"%(len(vectors))))
                vectors_with_ids['document-id'].extend(ids)
                vectors_with_ids['document-vector'].extend(vectors)
            logging.warning(("Example id is %s ")%str(vectors_with_ids['document-id'][0]))
            logging.warning(("Example vector is %s ")%str(vectors_with_ids['document-vector'][0]))
        df_document_vectors=pd.DataFrame(vectors_with_ids)
        df_document_vectors.to_pickle(path_document_vectors)



def convert_topic_vectors_from_cluster(ontology,model):
    corpora = load_corpora_list()
    logging.warning("preprocessing vectors of %d corpus modeled with %s and %s"%(len(corpora),ontology,model))
    for corpus in corpora:
        logging.warning("preprocessing %s "%corpus)
        read_cluster_topic_vectors(corpus,ontology,model)


#convert_topic_vectors_from_cluster('debatepedia','word2vec-esa-10')
def convert_topic_vectors_sample():
    #read_cluster_topic_vectors('sample','debatepedia','word2vec-esa-100')
    #read_cluster_topic_vectors('sample','wikipedia','word2vec-esa-100')
    #read_cluster_topic_vectors('sample','strategic-intelligence','word2vec-esa-100')
    #read_cluster_topic_vectors('sample','wikipedia-categories','word2vec-esa-100')
    #read_cluster_topic_vectors('sample','strategic-intelligence-sub-topics-part1','word2vec-esa-100')
    #read_cluster_topic_vectors('sample','strategic-intelligence-sub-topics-part2','word2vec-esa-100')

    #read_cluster_topic_vectors('sample','debatepedia','word2vec-esa-10')
    read_cluster_topic_vectors('sample','wikipedia','word2vec-esa-10')
    #read_cluster_topic_vectors('sample','strategic-intelligence','word2vec-esa-10')
    #read_cluster_topic_vectors('sample','wikipedia-categories','word2vec-esa-10')
    #read_cluster_topic_vectors('sample','strategic-intelligence-sub-topics-part1','word2vec-esa-10')
    #read_cluster_topic_vectors('sample','strategic-intelligence-sub-topics-part2','word2vec-esa-10')
convert_topic_vectors_sample()