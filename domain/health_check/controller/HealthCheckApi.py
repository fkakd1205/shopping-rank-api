from flask_restx import Namespace, Resource
from http import HTTPStatus
from domain.message.dto.MessageDto import MessageDto
from domain.health_check.dto.HealthCheckKeyDto import HealthCheckKeyDto

HealthCheckApi = Namespace('HealthCheckApi')

@HealthCheckApi.route('', methods=['GET'])
class HealthCheck(Resource):
    def get(self):
        message = MessageDto()

        message.set_status(HTTPStatus.OK)
        message.set_message("nrank api server is healthy")

        return message.__dict__, message.status_code
    
@HealthCheckApi.route('/keys', methods=['GET'])
class HealthCheck(Resource):
    def get(self):
        message = MessageDto()

        message.set_status(HTTPStatus.OK)
        message.set_message(f"Compile Time Key : {HealthCheckKeyDto.COMPILE_TIME_KEY}")

        return message.__dict__, message.status_code
