from flask import make_response
from http import HTTPStatus

from domain.message.dto.MessageDto import MessageDto

from config.csrf.CsrfAuthenticationFilter import CsrfAuthenticationFilter
from exception.types.CustomException import *

def CustomAuthenticationFilter(app):
    
    @app.before_request
    def csrf_authentication_filter():
        csrfAuthenticationFilter = CsrfAuthenticationFilter()

        try:
            csrfAuthenticationFilter.filter()
        except (CustomCsrfJwtExpiredException, CustomCsrfJwtAccessDeniedException, CustomCsrfJwtDecodeException) as e:
            message = MessageDto()
            response = make_response()

            csrfAuthenticationFilter.clear_all_csrf_tokens(response)
            message.set_data(None)
            message.set_status(HTTPStatus.FORBIDDEN)
            message.set_message("invalid_csrf")
            message.set_memo(str(e))
            
            return message.__dict__, message.status_code, response.headers

        
