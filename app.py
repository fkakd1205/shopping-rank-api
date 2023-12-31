from flask_restx import Api
from flask import Flask
from flask_cors import CORS

from exception.CustomExceptionHandler import CustomExceptionHandler
from domain.nrank_record.controller.NRankRecordApi import NRankRecordApi
from domain.nrank_record_detail.controller.NRankRecordDetailApi import NRankRecordDetailApi
from domain.health_check.controller.HealthCheckApi import HealthCheckApi
from domain.csrf_token.controller.CsrfTokenApi import CsrfTokenApi
from domain.nrank_record_category.controller.NRankRecordCategoryApi import NRankRecordCategoryApi
from domain.nrank_record_info.controller.NRankRecordInfoApi import NRankRecordInfoApi

from utils import init_db, OriginUtils
from config.filter.CustomAuthenticationFilter import CustomAuthenticationFilter
from exception.CustomExceptionHandler import CustomExceptionHandler

app = Flask(__name__)

api = Api(app)
CORS(
    app,
    supports_credentials=True,
    resources={
        r'*': {'origins': OriginUtils.get_allowed_origins()}
    }
)

# === init database setting ===
init_db(app)

# === authentication filter ===
CustomAuthenticationFilter(app)

# === register controller ===
api.add_namespace(NRankRecordApi, "/api/v1/nrank-records")
api.add_namespace(NRankRecordInfoApi, "/api/v1/nrank-record-infos")
api.add_namespace(NRankRecordDetailApi, "/api/v1/nrank-record-details")
api.add_namespace(NRankRecordCategoryApi, "/api/v1/nrank-record-categories")
api.add_namespace(HealthCheckApi, "/healthCheck")
api.add_namespace(CsrfTokenApi, "/api/v1/csrf")

# === global exception handler ===
CustomExceptionHandler(api)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=23081, load_dotenv=True)


