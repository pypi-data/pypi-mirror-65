import enum


class ResponseCode(enum.Enum):
    SUCCESS = "SUCCESS"
    RESOURCE_NOT_FOUND = "RESOURCE_NOT_FOUND"
    UNKNOWN_ERROR = "UNKNOWN_ERROR"
    BAD_REQUEST = "BAD_REQUEST"
    INVALID_REQUEST_DATA = "INVALID_REQUEST_DATA"
    AUTHENTICATION_FAILED = "AUTHENTICATION_FAILED"
    AUTHORISATION_FAILED = "AUTHORISATION_FAILED"
    TOO_MANY_REQUESTS = "TOO_MANY_REQUESTS"


class BaseResponse:

    def __init__(self, status, status_code, message, data):
        self.status = status
        self.status_code = status_code
        self.message = message
        self.data = data

    def to_json(self):
        return {
            "status": self.status,
            "status_code": str(self.status_code.value),
            "message": self.message,
            "data": self.data,
        }

    @staticmethod
    def get_response(status=0, status_code=ResponseCode.UNKNOWN_ERROR, message=None, data=None):
        return BaseResponse(status, status_code, message, data).toJSON()


class EntityAction(enum.Enum):
    CREATE = "CREATE"
    UPDATE = "UPDATE"
    READ = "READ"
    DELETE = "DELETE"
    SEARCH = "SEARCH"
    SUMMARY = "SUMMARY"


class UserStatus(enum.Enum):
    ACTIVE = "ACTIVE"
    PENDING_VERIFICATION = "PENDING_VERIFICATION"
    DISABLED = "DISABLED"
    SUSPENDED = "SUSPENDED"
    HIDDEN = "HIDDEN"


class UserVerificationStatus(enum.Enum):
    UNVERIFIED = "UNVERIFIED"
    VERIFIED = "VERIFIED"


class UserSource(enum.Enum):
    WEBSITE = "WEBSITE"
    APP_ANDROID = "APP_ANDROID"
    APP_IOS = "APP_IOS"
    APP_DESKTOP = "APP_DESKTOP"
    APP_MAC = "APP_MAC"
    ADMIN = "ADMIN"
    PARTNER = "PARTNER"


class UserSubscriptionType(enum.Enum):
    FREE = "FREE"
    PREMIUM = "PREMIUM"
    STAR = "STAR"
    ENTERPRISE = "ENTERPRISE"


class RackWalletType(enum.Enum):
    REAL = "REAL"
    VIRTUAL = "VIRTUAL"
