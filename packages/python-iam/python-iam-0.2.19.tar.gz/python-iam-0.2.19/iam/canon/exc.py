

class LoginAborted(Exception):
    """Raised when the login process is aborted."""

    def __init__(self, redirect_to, reason):
        self.redirect_to = redirect_to
        self.reason = reason
