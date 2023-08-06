class APIError(Exception):
    message = None
    error_code = None

    def __init__(self, message=None, error_code=None):
        if message is not None:
            self.message = message

        if error_code is not None:
            self.error_code = error_code
