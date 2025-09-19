from rest_framework import viewsets, status, mixins
from rest_framework.response import Response
from django.core.exceptions import ValidationError

from missions.serializers import (
    MissionSerializer,
    MissionUpdateSerializer,
    TargetUpdateSerializer,
)
from missions.models import Mission, Target


class MissionViewSet(viewsets.ModelViewSet):
    queryset = Mission.objects.all()
    serializer_class = MissionSerializer

    def create(self, request, *args, **kwargs):
        serializer = MissionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        mission_instance = self.get_object()
        serializer = MissionUpdateSerializer(mission_instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        mission = self.get_object()
        try:
            mission.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except ValidationError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class TargetViewSet(mixins.UpdateModelMixin, viewsets.GenericViewSet):
    queryset = Target.objects.all()
    serializer_class = TargetUpdateSerializer

    def update(self, request, *args, **kwargs):
        target = self.get_object()
        # Block any updates if either the target or mission is already complete
        if target.is_complete or target.mission.is_complete:
            return Response({"error": "Cannot update Notes as the target or mission is completed."},
                            status=status.HTTP_400_BAD_REQUEST)

        partial = kwargs.pop('partial', False)
        serializer = self.get_serializer(target, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        # If all targets are complete after this update, mark mission as complete
        target.refresh_from_db()
        mission = target.mission
        if mission.targets.filter(is_complete=False).count() == 0:
            if not mission.is_complete:
                mission.is_complete = True
                mission.save(update_fields=["is_complete"])

        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
