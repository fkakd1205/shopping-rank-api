from flask_restx import Api
from flask import Flask
from flask_cors import CORS

from exception.CustomExceptionHandler import CustomExceptionHandler
from domain.nrank_record.controller.NRankRecordApi import NRankRecordApi
from domain.nrank_record_detail.controller.NRankRecordDetailApi import NRankRecordDetailApi
from domain.test.TestApi import TestApi
from domain.workspace.controller.WorkspaceApi import WorkspaceApi

from utils.db.v2.DBUtils import init_db

app = Flask(__name__)

api = Api(app)
CORS(
    app,
    supports_credentials=True,
    resources={
        r'*': {'origins': 'http://localhost:3000'}
    }
)

# === register controller ===
api.add_namespace(NRankRecordApi, "/api/v1/nrank-records")
api.add_namespace(NRankRecordDetailApi, "/api/v1/nrank-record-details")
api.add_namespace(WorkspaceApi, "/api/v1/workspaces")
# api.add_namespace(TestApi, "/api/v1/test")

init_db(app)

CustomExceptionHandler(api)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=5000)