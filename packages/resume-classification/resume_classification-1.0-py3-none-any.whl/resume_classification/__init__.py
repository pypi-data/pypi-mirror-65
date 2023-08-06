import sys




def train(path):
    
    from resume_classification.training.train import Train
    train_obj = Train(path)
    try:
        train_obj.extract_resume_content()
    except:
        print('ERROR, Path incorrect or folder structure not correct')
        sys.exit()
    train_obj.train_model()
    train_obj.test_model()


def predict(path):

    from resume_classification.prediction.predict import ModelPrediction
    try:
        predict_obj = ModelPrediction(path)
        predict_obj.predict()
    except:
        print('ERROR, Path incorrect.')
        sys.exit()