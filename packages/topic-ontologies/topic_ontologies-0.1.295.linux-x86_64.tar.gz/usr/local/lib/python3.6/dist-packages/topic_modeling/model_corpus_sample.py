import pandas as pd
from conf.configuration import *
import csv
from topic_modeling import *
import argument_esa_model.esa_all_terms
def load_documents():
    dataset_preprocessed_path =get_path_preprocessed_documents('sample')
    documents= pd.read_csv(dataset_preprocessed_path,quotechar='"',sep="|",quoting=csv.QUOTE_ALL,encoding="utf-8")
    ids = list(documents['document-id'])
    documents= list(documents['document'])
    return documents,ids

def model_documents(documents,topic_ontology):
    document_vectors = esa_model(topic_ontology,documents)
    return document_vectors

def save_document_vectors(document_ids,document_vectors,path):
    columns = {}
    columns['document-id']=document_ids
    columns['document-vector']=document_vectors

    document_vectors = pd.DataFrame(columns)
    document_vectors.to_pickle(path)


texts,ids = load_documents()
# document_vectors = model_documents(texts,'wikipedia')
# path_document_vectors_wiki_esa = get_path_document_vectors('sample', 'wikipedia', 'esa')
# save_document_vectors(ids, document_vectors, path_document_vectors_wiki_esa)
# argument_esa_model.esa_all _terms.initliaze_model()
#
# document_vectors_debatepedia = model_documents(texts,'debatepedia')
# path_document_vectors_debatepedia_esa = get_path_document_vectors('sample', 'debatepedia', 'esa')
# save_document_vectors(ids, document_vectors_debatepedia,path_document_vectors_debatepedia_esa)
#
# argument_esa_model.esa_all_terms.initliaze_model()
#
# document_vectors_strategic_sub = model_documents(texts, 'strategic-intelligence')
# path_document_vectors_strategic_intelligence_esa = get_path_document_vectors('sample', 'strategic-intelligence', 'esa')
# save_document_vectors(ids, document_vectors_strategic_sub, path_document_vectors_strategic_intelligence_esa)

#argument_esa_model.esa_all_terms.initliaze_model()
#document_vectors_strategic_sub = model_documents(texts, 'strategic-intelligence-sub-topics')
#path_document_vectors_strategic_intelligence_subtopics_esa = get_path_document_vectors('sample', 'strategic-intelligence-sub-topics', 'esa')
#save_document_vectors(ids, document_vectors_strategic_sub, path_document_vectors_strategic_intelligence_subtopics_esa)

argument_esa_model.esa_all_terms.initliaze_model()
document_vectors_wikipedia_categories = model_documents(texts, 'wikipedia-categories')
path_document_vectors_wikipedia_categories_esa = get_path_document_vectors('sample', 'wikipedia-categories', 'esa')
save_document_vectors(ids, document_vectors_wikipedia_categories, path_document_vectors_wikipedia_categories_esa )
