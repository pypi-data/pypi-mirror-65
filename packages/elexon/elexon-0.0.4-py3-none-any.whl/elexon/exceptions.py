class ElexonException(Exception):
    """The base Elexon Exception that all other exception classes extend."""
    pass

class ElexonError(ElexonException):
    """Exception class for errors received from Elexon."""

    def __init__(self, code, type, desc):
        self.code = code
        self.type = type
        self.desc = desc
        Exception.__init__(self, code, type, desc)

    def __str__(self):
        return 'Error %s: %s' % (self.code, self.type)

#
# class Unavailable(ElexonException):
#     pass
#
# class PaymentGatewayError(ElexonException):
#     def __init__(self, code, message):
#         self.code = code
#         self.message = message
#
# class Refused(PaymentGatewayError):
#     pass
#
# class Stolen(PaymentGatewayError):
#     pass
