import json


class BytesToUtf8JsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (bytes, bytearray)):
            return obj.decode("UTF-8")
        return json.JSONEncoder.default(self, obj)
