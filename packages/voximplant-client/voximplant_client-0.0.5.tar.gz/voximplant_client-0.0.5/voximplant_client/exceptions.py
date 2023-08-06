class VoximplantClientException(BaseException):
    pass


class VoximplantBadApplicationNameException(VoximplantClientException):
    pass


class VoximplantQueueDoesNotExistsException(VoximplantClientException):
    pass


class VoximplantQueueBindException(VoximplantClientException):
    pass


class VoximplantUserDoesNotExistsException(VoximplantClientException):
    pass


class VoximplantUserCreationException(VoximplantClientException):
    pass


class VoximplantUserAlreadyExistsException(VoximplantClientException):
    pass


class VoximplantUserUpdateException(VoximplantClientException):
    pass


class VoximplantRuleCreationError(VoximplantClientException):
    pass


class VoximplantBadRuleNameException(VoximplantClientException):
    pass


class VoximplantBadRuleId(VoximplantClientException):
    pass
