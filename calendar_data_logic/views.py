from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.decorators import api_view
import requests
from requests import exceptions

from .serializers import EventSerializer


class EventCreateView(generics.GenericAPIView):
    serializer_class = EventSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        # posting data to zuri core after validation
        # the organization_id would be dynamic; based on the request data
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

        try:
            response = requests.post(url=url, json=payload)

            if response.status_code == 201:
                return Response(status=status.HTTP_201_CREATED)
            else:
                return Response({"error": response.json()['message']}, status=response.status_code)

        except exceptions.ConnectionError as e:
            return Response(str(e), status=status.HTTP_502_BAD_GATEWAY)
        


@api_view(['GET'])
def event_list_view(request):
    if request.method == "GET":
        # getting data from zuri core
        # /data/read/{plugin_id}/{collection_name}/{organization_id}
        url = 'https://zccore.herokuapp.com//data/read/613348c2bfba0a42d7f38e92/events/Global Link'

        try:
            response = requests.get(url=url)

            if response.status_code == 200:
                events_data = response.json()['data']
                return Response(events_data, status=status.HTTP_200_OK)
            else:
                return Response({"error": response.json()['message']}, status=response.status_code)

        except exceptions.ConnectionError as e:
            return Response(str(e), status=status.HTTP_502_BAD_GATEWAY)
