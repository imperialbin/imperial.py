__all__ = (
    "https",
)

from imperial_py.utils.parser import remove_tailing_slash, remove_leading_slash


class https:
    # just so pycharm doesn't yell at me :/
    imperialbin = None

    def __init__(self, name: str):
        self.path = remove_tailing_slash(name)

    def __truediv__(self, endpoint: str):
        # handle / operator
        endpoint = str(endpoint)
        endpoint = remove_leading_slash(endpoint)
        endpoint = remove_tailing_slash(endpoint)
        return https(self.path + "/" + endpoint)

    def __repr__(self):
        return self.path


# because python doesn't have static getters,
# and I don't want the ()
# used as https.imperialbin / "whatever"
https.imperialbin = https("https://imperialb.in")
