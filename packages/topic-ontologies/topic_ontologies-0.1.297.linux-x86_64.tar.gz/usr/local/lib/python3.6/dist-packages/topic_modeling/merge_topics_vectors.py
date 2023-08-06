import numpy as np
from conf.configuration import *
import pandas as pd
import csv
import logging
logging

def merge_topics(topic_model):
    path_topic_vectors_part1 = get_path_document_vectors('sample','strategic-intelligence-sub-topics-part1',topic_model)
    path_topic_vectors_part2 = get_path_document_vectors('sample','strategic-intelligence-sub-topics-part2',topic_model)
    path_final_merged_document_vectors=get_path_document_vectors('sample','strategic-intelligence-sub-topics',topic_model)
    logging.warning("part 1 path %s"%path_topic_vectors_part1)
    logging.warning("part 2 path %s"%path_topic_vectors_part2)

    vectors_df_part1 = pd.read_pickle(path_topic_vectors_part1)
    vectors_df_part2 = pd.read_pickle(path_topic_vectors_part2)

    logging.warning("part 1 shape %s"%str(vectors_df_part1.shape))
    logging.warning("part 1 dimension %s"%str(len(vectors_df_part1['document-vector'][0])))
    logging.warning("part 2 shape %s"%str(vectors_df_part2.shape))
    logging.warning("part 2 dimension %s"%str(len(vectors_df_part2['document-vector'][0])))

    vectors_df_part2.rename(columns={'document-vector':'document-vector-2'},inplace=True)


    logging.warning("part 2 before merge df %s"%str(vectors_df_part2.info()))
    logging.warning("part 1 before merge %s"%str(vectors_df_part1.info()))

    merged_df = pd.merge(vectors_df_part1,vectors_df_part2,on='document-id')
    logging.warning("columns final dataset df %s before concatenation"%str(merged_df.info()))
    merged_df['merged-document-vector']=merged_df.apply(lambda row:np.concatenate([row['document-vector'],row['document-vector-2']]),axis=1)
    del merged_df['document-vector-2']
    del merged_df['document-vector']
    merged_df.rename(columns={'merged-document-vector':'document-vector'},inplace=True)
    logging.warning("part 1 columns after merge %s"%vectors_df_part1.info())


    logging.warning("final dataset after merge df %s"%merged_df.info())
    logging.warning("final shape final dataset df %s"%str(merged_df.shape))
    logging.warning("final path %s"%str(path_final_merged_document_vectors))
    logging.warning("final dataset type %s"%str(len(merged_df['document-vector'][0])))
    merged_df.to_pickle(path_final_merged_document_vectors)
    #return document_ids,document_vectors

merge_topics('word2vec-esa-10')