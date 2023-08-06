class ApiError(BaseException):
    def __str__(self):
        return repr(self.data)


class ApiAuthenticationError(ApiError):

    def __init__(self, data):
        self.data = 'Authentication failed with key: "{data}"'.format(
            data=data)


class ApiCodeTranslationError(ApiError):

    def __init__(self, data):
        self.data = 'Can\'t translate: {data}'.format(
            data=data)


class ApiUnknownReportNameError(ApiError):

    def __init__(self, data):
        self.data = 'Invailid report name: {data}'.format(
            data=data)


class ApiInvalidBIRVersionProvided(ApiError):  # TODO: test case

    def __init__(self, data, choices):
        self.data = 'Invailid BIR version: {data} not in {choices}'.format(
            data=data, choices=choices
        )
