from rest_framework import generics, status
from rest_framework.response import Response
import requests

from .serializers import EventSerializer


class EventCreateView(generics.GenericAPIView):
    serializer_class = EventSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        # posting data to zuri core after validation
        event = serializer.data
        payload = {
            "plugin_id": "613348c2bfba0a42d7f38e92",
            "organization_id": "Global Link",
            "collection_name": "events",
            "bulk_write": False,
            "object_id": "",
            "filter": {},
            "payload": event
        }
        url = 'https://zccore.herokuapp.com/data/write'
        response = requests.post(url=url, json=payload)

        if response.status_code == 201:
            return Response(status=status.HTTP_201_CREATED)
        else:
            return Response(status=status.HTTP_501_NOT_IMPLEMENTED)


