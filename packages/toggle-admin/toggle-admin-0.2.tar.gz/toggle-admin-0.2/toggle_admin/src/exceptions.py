class ToggleAdminError(Exception):
    pass


class InvalidAuthData(ToggleAdminError):
    pass


class InvalidSession(ToggleAdminError):
    pass