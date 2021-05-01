__all__ = (
    "https"
)


class https:
    # just so pycharm doesn't yell at me :/
    imperialbin = None

    @staticmethod
    def remove_leading_slash(text: str):
        return text[1:] if text.startswith("/") else text

    @staticmethod
    def remove_tailing_slash(text: str):
        return text[:-1] if text.endswith("/") else text

    def __init__(self, name: str):
        self.path = self.remove_tailing_slash(name)

    def __truediv__(self, endpoint: str):
        # handle / operator
        endpoint = self.remove_leading_slash(endpoint)
        endpoint = self.remove_tailing_slash(endpoint)
        return https(self.path + "/" + endpoint)

    def __repr__(self):
        return self.path


# because python doesn't have static getters,
# and I don't want the ()
# used as https.imperialbin / "whatever"
https.imperialbin = https("https://imperialb.in")
