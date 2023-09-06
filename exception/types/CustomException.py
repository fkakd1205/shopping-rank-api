# 1. Duplication Exception
class CustomDuplicationException(Exception):
    pass

# 2. Invalid Value Exception
class CustomInvalidValueException(Exception):
    pass

# 3. Not Found Exception
class CustomNotFoundException(Exception):
    pass

# 4. Method Not Allowed Exception
class CustomMethodNotAllowedException(Exception):
    pass

# 5. Invalid User Exception
class CustomInvalidUserException(Exception):
    pass

# 6. Invalid Workspace Exception
class CustomInvalidWorkspaceException(Exception):
    pass

# 7. Access Denied Permission Exception
class CustomAccessDeniedPermissionException(Exception):
    pass

# 8. Timeout Exception
class CustomTimeoutException(Exception):
    pass

# 9. Not Matched Format Exception
class CustomNotMatchedFormatException(Exception):
    pass

# 10. Csrf Jwt Expired Exception
class CustomCsrfJwtExpiredException(Exception):
    pass

# 11. Csrf Jwt Access Denied Exception
class CustomCsrfJwtAccessDeniedException(Exception):
    pass

# 12. Csrf Jwt Decode Exception
class CustomCsrfJwtDecodeException(Exception):
    pass
