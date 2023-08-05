"""Helper utilities for the client library"""
import json

class Util():
    """All utilities are found here"""
    @classmethod
    def pretty_print(cls, data):
        """Pretty print JSON"""
        print(json.dumps(data, indent=4))
