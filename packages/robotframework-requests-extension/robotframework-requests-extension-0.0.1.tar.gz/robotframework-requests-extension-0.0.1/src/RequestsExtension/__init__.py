from .ApiLibKeywords import ApiLibKeywords
from .version import VERSION

_version_ = VERSION


class RequestsExtension(ApiLibKeywords):
    """
    ``RequestsExtension`` is an extension of ``RequestsLibrary`` [https://github.com/kennethreitz/requests|Requests]
    """
    ROBOT_LIBRARY_SCOPE = 'GLOBAL'
