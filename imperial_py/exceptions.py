from http.client import responses


class ImperialError(Exception):

    def __init__(self, message, *, status=None):
        """
        :type message: str
        :type status: int
        """
        self.message = message
        self.status = status

    def __str__(self):
        # pretty hacky solution to get the add the status keyword param tbh
        msg = self.message
        if self.status:
            msg += f" status={self.status} {responses[self.status]}"
        return msg
