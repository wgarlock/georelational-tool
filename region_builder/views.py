from django.views.generic import DetailView
from rest_framework.response import Response
from rest_framework.views import APIView

from region_builder.models import State
from region_builder.serializers import StateSerializer


class StateView(DetailView):
    template_name = "state.html"
    model = State


class StateAPIView(APIView):
    def get(self, request, format=None):
        obj_id = request.GET["id"]
        state = State.objects.prefetch_related("districts").get(id=obj_id)
        serializer = StateSerializer(state)
        return Response(serializer.data)
