class EMAKIPError(Exception):
    pass

class NotFoundError(EMAKIPError):
    pass

class AuthenticationError(EMAKIPError):
    pass

class VectorStoreError(EMAKIPError):
    pass
