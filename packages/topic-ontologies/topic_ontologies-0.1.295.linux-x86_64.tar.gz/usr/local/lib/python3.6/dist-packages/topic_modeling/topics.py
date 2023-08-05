from argument_esa_model.esa import ESA
from conf.configuration import *
import csv
esa_model_debatepedia = None
esa_model_strategic_intelligence = None
import pandas as pd
from topic_modeling import *
import argument_esa_model.esa_all_terms


def load_topics(topic_ontology):
        path_topics = get_path_topics(topic_ontology)
        topics_df=pd.read_csv(path_topics,sep=",",quoting=csv.QUOTE_ALL,quotechar='"',encoding='utf-8').sort_values('name')
        return list(topics_df['name'])

def load_topics_with_ids(topic_ontology):
    path_topics = get_path_topics(topic_ontology)
    topics_df=pd.read_csv(path_topics,sep=",",quoting=csv.QUOTE_ALL,quotechar='"',encoding='utf-8',dtype={'id': object}).sort_values('name')
    return list(topics_df['name']),list(topics_df['id'])


#save_topics_for('ontology-strategic-intelligence-sub-topics')

#topics=load_topics('ontology-wikipedia')
#print(topics)
#esa_model_debatepedia,esa_model_strategic_intelligence=initialize_models()
#save_topics_for('ontology-strategic-intelligence')
#save_topics_for('ontology-debatepedia')