class ErrorCode:
    def __init__(self, http_code: int, exception_code: str, message: str = None):
        self.http_code = http_code
        self.exception_code = exception_code
        self.message = message


USER_NOT_FOUND = ErrorCode(404, "USER_NOT_FOUND")
USER_ALREADY_EXISTS = ErrorCode(400, "USER_ALREADY_EXISTS")
EMAIL_ALREADY_VERIFIED = ErrorCode(409, "EMAIL_ALREADY_VERIFIED")
UNABLE_SEND_EMAIL = ErrorCode(500, "UNABLE_SEND_EMAIL")
INCORRECT_VERIFICATION_CODE = ErrorCode(400, "INCORRECT_VERIFICATION_CODE")
USER_DELETE_ERROR = ErrorCode(500, "USER_DELETE_ERROR")