import pkg_resources

['Train']
FILE_NAME = pkg_resources.resource_filename('resume_classification', 'model/')

['Prediction']
PATH_CLF = FILE_NAME + 'latest_model.pkl'
PATH_COUNT_VECT = FILE_NAME + 'count_vect.pkl'
PATH_ENCODER = FILE_NAME + 'classes.npy'