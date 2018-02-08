import os
import _pickle as cPickle
import json
import logging
import numpy as np
import pandas as pd
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.pipeline import Pipeline
logger = logging.getLogger('score.%s' % __name__)
logger.info('in run_score')


def get_score(app_path, file_name):
    cwd = os.getcwd()
    result = {'scores':[], 'success':True}
    try:
        os.chdir(os.path.join(app_path, 'score_model'))
        result['upto1'] = 'working'
        from score_model.score_auto_gbm.FeatureTransformer import FeatureTransformer
        result['upto2'] = 'working'
        with open("gbmFit.pkl", "rb") as pickle_file:
            gbmFit = cPickle.load(pickle_file)
            input_file = os.path.join(app_path, "data", file_name)
            if not os.path.exists(input_file):
                result = {'success':False, 'error':'%s file not exists'%(input_file)}
                os.chdir(cwd)
                return result

            with open(input_file, "r") as f:
                for line in f:
                    datum = json.loads(line)
                    score = list(gbmFit.predict(pd.DataFrame([datum])))[0]
                    result['scores'].append(json.dumps(score))
    except Exception as e:
         result['success'] = False
         result['error'] = e
         result['path'] = os.path.join(app_path, 'score_model')
         result['cwd'] = os.getcwd()
         result['list'] = os.listdir(os.getcwd())
    os.chdir(cwd)
    return(result)
