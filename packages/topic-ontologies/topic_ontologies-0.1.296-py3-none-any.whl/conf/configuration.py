import os
source_label ="source"
sample_label ="sample"
source_label_template="source-%s"
preprocessed_documents_label = "preprocessed-documents"
preprocessed_arguments_label = "preprocessed-arguments"
preprocessed_arguments_version_label_template="preprocessed-arguments-%s"
preprocessed_documents_version_label_template= "preprocessed-documents-%s"
document_vectors_label_template="document-vectors-%s-%s"
argument_vectors_label_template="argument-vectors-%s-%s"
histogram_label_template= "%s_histogram_%s"
two_parameter_histogram_template= "histogram-%s-over-%s"
two_parameter_histogram_template_figure = "figure-histogram-%s-over-%s"
histogram_label_fig_template= "%s-histogram-%s-fig"
model_label_template="%s-model"
vocab_label_template="%s-vocab"
topics_label="topics"
granularity_label="granularity"
top_k_topics_per_document_label= "top-k-topics-per-document"
dirname = os.path.dirname(__file__)
cluster_mode=False
cluster_conf_path="/mnt/ceph/storage/data-in-progress/topic-ontologies/conf/"
windows_mode=False

def get_dataset_conf_path(dataset_name):
    if cluster_mode:
        dataset_conf = cluster_conf_path+("/%s.conf"%dataset_name)
    else:
        dataset_conf = dirname+("/%s.conf"%dataset_name)
    return dataset_conf

def get_path_source(dataset_name):
    dataset_conf_path = get_dataset_conf_path(dataset_name)
    dataset_source_path = get_property_value(dataset_conf_path,source_label)
    return dataset_source_path

def get_source_subset_path(dataset_name,subdataset):
    dataset_conf_path = get_dataset_conf_path(dataset_name)
    source_label = source_label_template % subdataset
    dataset_source_subset_path = get_property_value(dataset_conf_path,source_label)
    return dataset_source_subset_path

def get_sample_path(dataset_name):
    dataset_conf_path = get_dataset_conf_path(dataset_name)
    dataset_sample_path = get_property_value(dataset_conf_path,sample_label)
    return dataset_sample_path

def get_path_document_vectors(dataset_name,topic_ontology,topic_model):
    dataset_conf_path = get_dataset_conf_path(dataset_name)
    document_vectors_label = document_vectors_label_template % (topic_ontology, topic_model)
    return get_property_value(dataset_conf_path,document_vectors_label)

def get_path_argument_vectors(dataset_name,topic_ontology,topic_model):
    dataset_conf_path = get_dataset_conf_path(dataset_name)
    argument_vectors_label = argument_vectors_label_template % (topic_ontology, topic_model)
    return get_property_value(dataset_conf_path,argument_vectors_label )

def get_path_vocab(dataset_name):
    dataset_conf_path = get_dataset_conf_path(dataset_name)
    vocab_label = vocab_label_template% dataset_name
    path_vocab = get_property_value(dataset_conf_path,vocab_label)
    return path_vocab

def get_path_preprocessed_documents(dataset_name):
    dataset_conf_path = get_dataset_conf_path(dataset_name)
    path_preprocessed_documents = get_property_value(dataset_conf_path,preprocessed_documents_label)
    return path_preprocessed_documents

def get_path_preprocessed_arguments(dataset_name):
    dataset_conf_path = get_dataset_conf_path(dataset_name)
    path_preprocessed_arguments = get_property_value(dataset_conf_path,preprocessed_arguments_label)
    return path_preprocessed_arguments

def get_path_preprocessed_arguments_version(dataset_name,version):
    dataset_conf_path = get_dataset_conf_path(dataset_name)
    preprocessed_arguments_version_label = preprocessed_arguments_version_label_template% version
    path_preprocessed_arguments_template = get_property_value(dataset_conf_path,preprocessed_arguments_version_label)
    return path_preprocessed_arguments_template

def get_path_preprocessed_documents_version(dataset_name,version):
    dataset_conf_path = get_dataset_conf_path(dataset_name)
    path_preprocessed_documents_template = get_property_value(dataset_conf_path, preprocessed_documents_version_label_template)
    return path_preprocessed_documents_template%version

def get_histogram_path_figure(dataset_name,attribute):
    dataset_conf_path = get_dataset_conf_path(dataset_name)
    dataset_histogram_attribute_label = histogram_label_fig_template % (dataset_name, attribute)
    dataset_histogram_figure_attribute_path = get_property_value(dataset_conf_path,dataset_histogram_attribute_label)
    return dataset_histogram_figure_attribute_path

def get_path_histogram_two_parameters(dataset_name, x, y):
    dataset_conf_path = get_dataset_conf_path(dataset_name)
    dataset_histogram_label = two_parameter_histogram_template % ( x, y)
    dataset_histogram_path = get_property_value(dataset_conf_path,dataset_histogram_label)
    return dataset_histogram_path

def get_figure_path_histogram_two_parameters(dataset_name,x,y):
    dataset_conf_path = get_dataset_conf_path(dataset_name)
    dataset_histogram_label = two_parameter_histogram_template_figure % (x, y)
    dataset_histogram_figure_path = get_property_value(dataset_conf_path,dataset_histogram_label)
    return dataset_histogram_figure_path

def get_path_topics(ontology_name):
    dataset_conf_path = get_dataset_conf_path(ontology_name)
    path_topics = get_property_value(dataset_conf_path,'topics')
    return path_topics

def get_path_topic_model(ontology_name,model):
    dataset_conf_path = get_dataset_conf_path(ontology_name)
    model_label = model_label_template % model
    path_topic_model = get_property_value(dataset_conf_path,model_label)
    return path_topic_model

def get_histogram_path(dataset_name,attribute):
    dataset_conf_path = get_dataset_conf_path(dataset_name)
    dataset_histogram_attribute_label = histogram_label_template % (dataset_name, attribute)
    dataset_histogram_attribute_path = get_property_value(dataset_conf_path,dataset_histogram_attribute_label)
    return dataset_histogram_attribute_path

def get_path_top_k_topics_per_document(dataset,topic_ontology,topic_model,k):
    dataset_conf_path = get_dataset_conf_path(dataset)
    top_k_topics_per_document_path_template = get_property_value(dataset_conf_path,top_k_topics_per_document_label)
    top_k_topics_per_document_path=  top_k_topics_per_document_path_template % (k,topic_ontology, topic_model)
    return top_k_topics_per_document_path

def get_property_value(dataset_conf_path,property_label):
    conf_file = open(dataset_conf_path,'r')
    for line in conf_file:
        label = line.split("=")[0].strip()
        value = line.split("=")[1].strip()
        if label == property_label:
            if cluster_mode:
                value=value.replace("/mnt/disk1/","/user/befi8957/")
            if windows_mode:
                value=value.replace("/mnt/disk1/","C:\\Users\\user\\disk1\\")
            return value

def get_granularity(dataset):
    dataset_conf_path = get_dataset_conf_path(dataset)
    granularity = get_property_value(dataset_conf_path,granularity_label)
    return granularity

def load_corpora_list():
    corpora_path = get_dataset_conf_path('corpora')
    with open(corpora_path,'r') as corpora_file:
        return [l.strip() for l in corpora_file.readlines()]

def set_cluster_mode():
    global cluster_mode
    cluster_mode=True

def set_windows_mode():
    global windows_mode
    windows_mode=True