
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.decorators import api_view
import requests
from urllib import parse
from requests import exceptions

from .serializers import EventSerializer
from environs import Env

env = Env()
env.read_env()

plugin_id = env.str("plugin_id")


class EventCreateView(generics.GenericAPIView):
    serializer_class = EventSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        # posting data to zuri core after validation
        # the organization_id would be dynamic; based on the request data
        event = serializer.data
        payload = {
            "plugin_id": plugin_id,
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
        url = "https://zccore.herokuapp.com/data/read/" + parse.quote(f"{plugin_id}/events/Global Link")

        try:
            response = requests.get(url=url)

            if response.status_code == 200:
                events_data = response.json()['data']
                return Response(events_data, status=status.HTTP_200_OK)
            else:
                return Response({"error": response.json()['message']}, status=response.status_code)

        except exceptions.ConnectionError as e:
            return Response(str(e), status=status.HTTP_502_BAD_GATEWAY)


class EventUpdateView(generics.UpdateAPIView):
    serializer_class = EventSerializer

    def example_of_update(self, request, *args, **kwargs):
        object_id = self.kwargs['data_id']

        get_url = "https://zccore.herokuapp.com/data/read/" + parse.quote(f"{plugin_id}/events/Global Link")
        response = requests.get(url=get_url)

        instance = None
        if response.status_code == 200:
            response_data = response.json()['data']
            for data in response_data:
                if data['_id'] == object_id:
                    instance = data
                    break
            if not instance:
                return

        else:
            return Response({"error": response.json()['message']}, status=response.status_code)

        object_id = instance.pop('_id')
        partial = kwargs.pop('partial', False)

        serializer = self.get_serializer(data=request.data, instance=instance, partial=partial)

        if serializer.is_valid():
            serializer.save()

        event_update = serializer.data
        payload = {
            "plugin_id": plugin_id,
            "organization_id": "Global Link",
            "collection_name": "events",
            "object_id": object_id,
            "filter": {},
            "payload": event_update
        }
        response = requests.put('https://zccore.herokuapp.com/data/write', json=payload)
        return Response(data=response.json())

    def update(self, request, *args, **kwargs):
        return self.example_of_update(request, *args, **kwargs)
        # object_id = self.kwargs['data_id']
        # partial = kwargs.pop('partial', True)
        #
        # serializer = self.get_serializer(data=request.data, partial=partial)
        #
        # serializer.is_valid(raise_exception=True)
        #
        # event_update = serializer.data
        # return Response(data=event_update)
