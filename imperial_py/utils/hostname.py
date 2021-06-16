__all__ = (
    "https",
)


class https:
    # just so pycharm doesn't yell at me :/
    imperialbin = None
    impbin = None

    def __init__(self, name: str):
        self.path = str(name).removesuffix("/")

    def __truediv__(self, endpoint: str):
        # handle / operator
        endpoint = str(endpoint)
        endpoint = endpoint.removeprefix("/")
        endpoint = endpoint.removesuffix("/")
        return https(self.path + "/" + endpoint)

    def __repr__(self):
        return self.path


# because python doesn't have static getters,
# and I don't want the ()
# used as https.imperialbin / "whatever"
https.imperialbin = https("https://imperialb.in")
https.impbin = https("https://impb.in")
