from http.client import responses

__all__ = (
    "ImperialError"
)


class ImperialError(Exception):

    def __init__(self, message: str, status: int = None):
        self.message = message
        self.status = status

    def __str__(self):
        # pretty hacky solution to get the add the status keyword param tbh
        msg = self.message
        if self.status:
            msg += " status={} {}".format(self.status, responses[self.status])
        return msg
