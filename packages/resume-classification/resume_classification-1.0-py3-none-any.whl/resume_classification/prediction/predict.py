from resume_classification import utils as st
from resume_classification import config as cf

import warnings
warnings.filterwarnings('ignore')
import re
import pickle
import numpy as np
import pandas as pd
from glob import glob
from tika import parser
import logging

from sklearn.preprocessing import LabelEncoder
from sklearn.feature_extraction.text import CountVectorizer

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s:%(levelname)s:%(funcName)s:%(message)s')

stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)

logger.addHandler(stream_handler)


class ModelPrediction:
    
    
    def __init__(self, path):

        
        self.path = path

        self.le = LabelEncoder()
        self.clf = pickle.load(open(cf.PATH_CLF, 'rb'))
        self.le.classes_ = np.load(cf.PATH_ENCODER, allow_pickle=True)
        self.count_vect = pickle.load(open(cf.PATH_COUNT_VECT, 'rb'))
        self.df = pd.DataFrame()
        logger.info('Module Predict: Initialization complete')
    
    def predict_extract_preprocessed_text(self, path):

        logger.info('Inside predict_extract_preprocessed_text ')

        '''
        This method predicts the 'Resume Type' using text from resume.

        @param path :: string: Path to resume file

        @return:
            :filename :: string: Name of the file
            :resume_type_pred :: string: Predicted value
        '''


        filename = path.split('/')[-1]
        try:
            txt = parser.from_file(path)['content'].lower().strip()
            txt = re.sub(st.PREPROCESS_STRING, " ", txt)
            txt_list = re.sub(st.SPACE_STRING, " ", txt).split(' ')    
            txt_list = [ word for word in txt_list if word not in st.STOP ]
            text = [' '.join(txt_list)]

            test_count = self.count_vect.transform(text)
            resume_type_pred = self.le.inverse_transform(self.clf.predict(test_count))[0]

        except:
            resume_type_pred = 'Data not present'
            logger.error('Data for file {} could not be extracted'.format(filename))
        
        logger.info('Execution Complete')
        return filename, resume_type_pred
        




    def predict(self):

        logger.info('Inside Predict Method')

        self.df['FileName'], self.df['Predicted Type'] = zip(*pd.Series(glob(self.path + '*/*')).apply(self.predict_extract_preprocessed_text))
        logger.info('Execution Complete')
        print(self.df.head(20))

        return self.df