import pandas as pd

path_df_cluster_argument_vectors='/mnt/disk1/topic-ontologies/args-me/argument-vectors-debatepedia-esa-corpus-args-me-cluster.csv'
path_df_local_argument_vectors='/mnt/disk1/topic-ontologies/args-me/argument-vectors-debatepedia-esa-corpus-args-me-local.csv'

df_cluster = pd.read_pickle(path_df_cluster_argument_vectors)
df_local = pd.read_pickle(path_df_local_argument_vectors)

print(df_cluster)
print(df_local)
