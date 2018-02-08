from flask import Flask
from flask import jsonify, request
import logging
import json, os
from score_model.run_score import get_score
from settings import app_name, app_path
app = Flask(__name__)

logger = logging.getLogger('score.%s' % __name__)
logger.info('working')


@app.route('/')
def welcone():
    return "Hello iam done"


@app.route('/first', methods=['GET'])
def first():
    return jsonify({'work':'done'})




@app.route('/run_score', methods=['POST', 'GET'])
def run_score():
    resp = {'success':True}
    if request.method == 'GET':
        resp = {'success':False, 'error':'/run_score is a post call'}
        resp = get_score(app_path, 'gbm_input_data_multiline.json')
        logger.info(resp)
        return jsonify(resp)
    try:
        data = json.loads(request.data)
        logger.info('Running score model')
        resp = get_score(data.get('input_file', 'gbm_input_data_multiline.json'))
    except Exception as e:
        logger.error(e)
        resp['success'] = False
        resp['error'] = e
    logger.info(resp)
    return resp


if __name__ == "__main__":
        app.run()

