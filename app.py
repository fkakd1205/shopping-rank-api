from flask_restx import Api
from flask import Flask
from flask_cors import CORS

from utils.db.DBUtils import db, init_app
from domain.nrank_record.controller.NRankRecordApi import NRankRecordApi

app = Flask(__name__)
api = Api(app)
CORS(
    app,
    supports_credentials=True
)

init_app(app)

api.add_namespace(NRankRecordApi, "/api/v1/nrank-records")

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=5000)