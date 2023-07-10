from flask_restx import Api
from flask import Flask
from flask_cors import CORS

from utils.db.DBUtils import init_app
from domain.nrank_record.controller.NRankRecordApi import NRankRecordApi
from domain.nrank_record_detail.controller.NRankRecordDetailApi import NRankRecordDetailApi

app = Flask(__name__)

api = Api(app)
CORS(
    app,
    supports_credentials=True
)

init_app(app)
# register_interceptor(app)   # TODO :: register_interceptor에서 @app.request_before

api.add_namespace(NRankRecordApi, "/api/v1/nrank-records")
api.add_namespace(NRankRecordDetailApi, "/api/v1/nrank-record-details")

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=5000)