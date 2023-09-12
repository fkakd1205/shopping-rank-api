from flask_restx import Namespace, Resource
from flask import make_response
from http import HTTPStatus

from domain.message.dto.MessageDto import MessageDto
from domain.csrf_token.service.CsrfTokenService import CsrfTokenService

from decorators import *

CsrfTokenApi = Namespace('CsrfTokenApi')

@CsrfTokenApi.route('', methods=['GET'])
class CsrfToken(Resource):
    
    @required_login
    def get(self):
        message = MessageDto()
        response = make_response()

        csrfTokenService = CsrfTokenService()
        csrfTokenService.get_csrf_token(response)
        message.set_status(HTTPStatus.OK)
        message.set_message("success")
        
        return message.__dict__, message.status_code, response.headers
