class BaseInternalException(Exception):
    """
    Why Python3 loose the message?!
    """

    def __init__(self, *args, **kwargs):
        self.errors = kwargs.pop("errors", None)

        super(BaseInternalException, self).__init__(*args, **kwargs)

    @property
    def message(self):
        """
        This no longer exist in Python3.X

        :return: 
        """

        msg = ""

        if len(self.args) > 0:
            msg = self.args[0]

        return msg


class DocumentNotFound(BaseInternalException):
    """
    Raise when a document is not found.
    """

    def __str__(self):
        return "DocumentNotFound"


class InvalidFormat(BaseInternalException):
    """
    Raise when a specific value is in wrong format.
    """

    def __str__(self):
        return "InvalidFormat"


class InvalidValue(BaseInternalException):
    """
    Raise when a specific value have a wrong value.
    """

    def __str__(self):
        return "InvalidValue"


class MissingArguments(BaseInternalException):
    """
    Raise when a specific value is missing.
    """

    def __str__(self):
        return "MissingArguments"


class CPPAlreadySent(BaseInternalException):
    """
    Raise when the cpp was already sent.
    """

    def __str__(self):
        return "CPPAlreadySent"


class PresenceCertificateAlreadySent(BaseInternalException):
    """
    Raise when the cpp was already sent.
    """

    def __str__(self):
        return "PresenceCertificateAlreadySent"


class ConnectionError(BaseInternalException):
    """
    Raise when there is a connection problem.
    """

    def __str__(self):
        return "ConnectionError"


class InvalidScope(BaseInternalException):
    """
    Raise when a specific scope is missing.
    """

    def __str__(self):
        return "InvalidScope"


class Unauthorized(BaseInternalException):
    """
    Raise when a request is not authorized due to authentication.
    """

    def __str__(self):
        return "Unauthorized"


class ContentNotFound(BaseInternalException):
    """
    Raise when a content is not found.
    """

    def __str__(self):
        return "ContentNotFound"


class ContentNotAvailable(BaseInternalException):
    """
    Raise when a content is not available.
    """

    def __str__(self):
        return "ContentNotAvailable"


class ValueAlreadyExists(BaseInternalException):
    """
    Raise when a value already exists.
    """

    def __str__(self):
        return "ValueAlreadyExists"


class MemcacheLockException(BaseInternalException):
    """
    Raise when a there some sort of problem with Memcache.
    """

    def __init__(self, *args, **kwargs):
        Exception.__init__(self, *args, **kwargs)

    def __str__(self):
        return "MemcacheLockException"


class ExpiredTokenException(BaseInternalException):
    """
    Raise when a there some sort of problem with token expiration time.
    """

    def __init__(self, *args, **kwargs):
        Exception.__init__(self, *args, **kwargs)

    def __str__(self):
        return "ExpiredTokenException"


class InactiveUserException(BaseInternalException):
    """
    Raise when a user (from Django Auth User) is not active.
    """

    def __init__(self, *args, **kwargs):
        Exception.__init__(self, *args, **kwargs)

    def __str__(self):
        return "InactiveUserException"


class DocumentAlreadyExist(BaseInternalException):
    """
    Raise when a try to create a new document that already exists
    (within a set of params).
    """

    def __str__(self):
        return "DocumentAlreadyExist"


class CannotDeleteDocument(BaseInternalException):
    """
    Raise when a try to delete a document that cannot be deleted for some reason
    """

    def __str__(self):
        return "CannotDeleteObject"


class HashDigestMismatchError(BaseInternalException):
    """
    Raise when a hash digest from a loaded file is nor equal to que hash kept
    on database for reference, meaning that the file on disk was changed
    """

    def __str__(self):
        return "HashDigestMismatchError"


class CreatingDocumentError(BaseInternalException):
    """
    Raise when creating a ES document using a DAO preferably.
    """

    def __str__(self):
        return "CreatingDocumentError"


class ScrollingDocumentsError(BaseInternalException):
    """
    Raise when fails to scroll an ES query.
    """

    def __str__(self):
        return "ScrollingDocumentsError"


class UpdateDocumentError(BaseInternalException):
    """
    Raise when fails to update an ES document.
    """

    def __str__(self):
        return "DeleteDocumentError"


class DeleteDocumentError(BaseInternalException):
    """
    Raise when fails to delete an ES document.
    """

    def __str__(self):
        return "DeleteDocumentError"


class ReadOnlyModeError(BaseInternalException):
    """
    Raise when try to update an ES document which is in read only mode.
    """

    def __str__(self):
        return "ReadOnlyModeError"
