from json import loads, JSONEncoder

from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response


class FileDefEncoder(JSONEncoder):
    def default(self, o):
        return o.__dict__


class FileDefinition:
    encoder = FileDefEncoder()

    def __init__(self, data):
        file_data = loads(data)
        self.file_id = file_data['fileId']
        self.file_name = file_data['fileName']

    def encode(self):
        return FileDefinition.encoder.encode(self)


@api_view(['POST'])
def index(request):
    file_def = FileDefinition(request.body)
    return Response(file_def.encode())


def about(request):
    return HttpResponse("My name is Aaron Smith!")
