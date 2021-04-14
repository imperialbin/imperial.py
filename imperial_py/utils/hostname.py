class Host:

    @staticmethod
    def remove_leading_slash(text):
        return text[1:] if text.startswith("/") else text

    @staticmethod
    def remove_tailing_slash(text):
        return text[:-1] if text.endswith("/") else text

    def __init__(self, name=None):
        self.path = "https://imperialb.in"
        if name:
            self.path = self.remove_tailing_slash(name)

    def __truediv__(self, endpoint):
        # handle / operator
        endpoint = self.remove_leading_slash(endpoint)
        endpoint = self.remove_tailing_slash(endpoint)
        self.path = f"{self.path}/{endpoint}"
        return Host(self.path)

    def __repr__(self):
        return self.path + "/"
