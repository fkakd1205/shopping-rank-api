from flask_restx import Api
from flask import Flask
from flask_cors import CORS

from utils.db.v2.DBUtils import init_app
from exception.CustomExceptionHandler import CustomExceptionHandler
from domain.nrank_record.controller.NRankRecordApi import NRankRecordApi
from domain.nrank_record_detail.controller.NRankRecordDetailApi import NRankRecordDetailApi
from domain.test.TestApi import TestApi

from config.filter.JwtAuthorizationFilter import JwtAuthorizationFitler

app = Flask(__name__)

api = Api(app)
CORS(
    app,
    supports_credentials=True
)

init_app(app)

@app.before_request
def before_request():
    # access token 검사
    JwtAuthorizationFitler.filter()

api.add_namespace(NRankRecordApi, "/api/v1/nrank-records")
api.add_namespace(NRankRecordDetailApi, "/api/v1/nrank-record-details")
api.add_namespace(TestApi, "/api/v1/test")

CustomExceptionHandler(api)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=5000)