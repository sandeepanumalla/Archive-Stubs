import json
from flask import Response
def rest_api():
    return Response("{'a':'b'}", status=200, mimetype='application/json')