from resume_classification import utils as st
from resume_classification import config as cf

import re
import pickle
import warnings
import numpy as np
import pandas as pd
from glob import glob
from tika import parser
from collections import Counter
import matplotlib.pyplot as plt
import logging
import pkg_resources
import sys


from nltk.stem.snowball import SnowballStemmer
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics import confusion_matrix, f1_score, accuracy_score

warnings.filterwarnings('ignore')
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s:%(levelname)s:%(funcName)s:%(message)s')

stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)

logger.addHandler(stream_handler)

class Train :
    '''
    This class is used to train the resumes.
    '''
    def __init__(self,path) :
        self.path = path 
        self.count_vect = CountVectorizer()
        self.le = LabelEncoder()
        self.df = pd.DataFrame()
        self.scaler = StandardScaler()
        logger.info('Module Train: Initialization complete')
        
    def preprocess_resume(self,path) :

        logger.info('Inside preprocess_resume method')
        '''
        This method performs the pre-processing of the resumes,
        getting the text out of resume, getting the common words and its count,
        getting the stop word count.

        @param path :: string: Contains the path to resumes file.

        @return:
            txt :: string: Extracted text from resume.
            common_word :: string: List of common word present in text.
            common_count :: int: Count of common words
            stop_count :: int: Count of stopwords
        '''


        try:
            txt = parser.from_file(path)['content'].lower().strip()
            txt = re.sub(st.PREPROCESS_STRING, " ", txt)
            txt_list = re.sub(st.SPACE_STRING, " ", txt).split(' ')    
            stop_count = len(set(txt_list) & st.STOP )
            txt_list = [ word for word in txt_list if word not in st.STOP ]
            common_words = ' '.join(list(zip(*Counter(txt_list).most_common(10)))[0])
            common_count = Counter(txt_list).most_common(1)[0][1]
            txt = ' '.join(txt_list)
            logger.info('Features successful extracted for {}'.format(path.split('/')[-1]))
        except:
            txt = ''
            common_words = ''
            common_count = 0
            stop_count = 0
            logger.error('Data for file {} could not be extracted'.format(path.split('/')[-1]))
        
        logger.info('Execution Complete')
        
        return txt, common_words, common_count, stop_count
        
    def extract_resume_content(self) :
        logger.info('Inside extract_resume_content method')

        '''
        This method adds the following features:
            :path :: string: path to resumes - Path to resumes is passed by the user in config file.
            :resume_name :: string: File name
            :resume_type :: string: Domain

        '''

        
        self.df['path'] = glob(self.path + '*/**/*')
        self.df['resume_name'] = self.df['path'].astype(str).str.split('/').str[-1]
        self.df['resume_type'] = self.df['path'].astype(str).str.split('/').str[-2]
        self.df['resume'], self.df['common_words'], self.df['common_count'], self.df['stop_count'] = zip(*self.df['path'].apply(self.preprocess_resume))

                   
        
        logger.info('Execution complete')
    def add_features(self) :

        logger.info('Inside add_features method')
        '''
        This method adds some more feature for model training:
            :word_count :: int: Count of each word
            :character_count :: int: Count of each character
            :avg_word_size :: int: Average word count
        '''

        self.df['word_count'] = self.df['resume'].astype(str).str.split().str.len()
        self.df['character_count'] = self.df['resume'].astype(str).str.len()
        self.df['avg_word_size'] = self.df['character_count']/self.df['word_count']
        
        logger.info('Execution Complete! Successfully added features: word_count, character_count, avg_word_size')
        
    def train_model(self) :

        logger.info('Inside train_model method')
        '''
        This method will train the model using Logistic regression.
        
        '''

        self.df.drop_duplicates(subset='resume',inplace=True)
        self.add_features()
        self.save_data('resume_dataframe',self.df)
        self.df['resume_type'] = self.le.fit_transform(self.df['resume_type'])                  # data leakage.

        X = self.df.drop('resume_type', axis = 1)
        y = self.df['resume_type']

        self.save_encoder('classes')

        x_train, x_test, y_train, y_test = train_test_split(X, y, test_size = 0.25, random_state = 123)
        
        self.x_test = x_test
        self.y_test = y_test
        
        x_train_count = self.count_vect.fit_transform(x_train['resume'], y = y_train)
        
        self.save_data('count_vect',self.count_vect)

        clf = LogisticRegression(random_state = 123, class_weight = 'balanced')       
         
        clf.fit(x_train_count, y_train)
        
        self.clf = clf
        self.save_data('latest_model', clf)    

        logger.info('Model Training Completed successfully.')
    def test_model(self) :

        logger.info('Inside test_model')
        
        '''
        This method test the model accuracy on unseen test data and gives the following metrics
            :Accuracy
            :F1 Score
            :Confusion matix
        '''

        x_test_count = self.count_vect.transform(self.x_test['resume'])
        
        y_pred = self.clf.predict(x_test_count)

        print('The accuracy score of model is '+ str(round((accuracy_score(self.y_test, y_pred)) * 100, 2)))
        print('The f1 score of model is '+ str(round((f1_score(self.y_test, y_pred, average = 'macro')) * 100, 2)))
        print('Confusion matix '+ str(confusion_matrix(self.y_test, y_pred)))
        
    def save_data(self, filename, data) :

        logger.info('Inside save_data method')
        '''
        This method is used to save the object passed using pickle.

        @param filename :: string: Name of object to be saved.
        @param data :: object: Object to be saved.
        '''
        file_name = cf.FILE_NAME + filename + '.pkl'
        #file_name = './model/' + filename +'.pkl'
        pickle.dump(data, open(file_name, 'wb'))
        logger.info('{} saved successfully at location : {}'.format(filename, str(file_name)))

    def save_encoder(self, filename):
        
        logger.info('Inside save_encoder method')
        '''
        This method saves the encoder using numpy.

        '''
        file_name = cf.FILE_NAME + filename + '.npy'
        np.save(file_name, self.le.classes_)
        logger.info('{} saved successfully at location : {}'.format(filename, file_name))