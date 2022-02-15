import random


class TimeStampURLManager:
    urls = [
        "http://timestamp.comodoca.com/rfc3161",
        "http://timestamp.digicert.com",
        "http://timestamp.globalsign.com/scripts/timestamp.dll",
        "http://timestamp.sectigo.com",
        "http://tsa.starfieldtech.com",
    ]

    urls = [
        "http://timestamp.digicert.com",
    ]

    @property
    def url(self):
        cls = type(self)
        return random.choice(cls.urls)
