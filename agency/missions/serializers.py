from rest_framework import serializers
from missions.models import Target, Mission


class TargetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Target
        fields = ['id', 'name', 'country', 'notes', 'is_complete']
        read_only_fields = ['id']


class TargetUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Target
        fields = ['notes', 'is_complete']


class MissionSerializer(serializers.ModelSerializer):
    targets = TargetSerializer(many=True)

    class Meta:
        model = Mission
        fields = ['id', 'cat', 'targets', 'is_complete']
        read_only_fields = ['id']

    def validate(self, attrs):
        targets = attrs.get('targets', [])
        if not targets or not (1 <= len(targets) <= 3):
            raise serializers.ValidationError({'targets': 'Provide 1 to 3 targets.'})

        # Validate mission completion consistency with targets
        is_complete = attrs.get('is_complete', False)
        if is_complete and any(not t.get('is_complete', False) for t in targets):
            raise serializers.ValidationError(
                {'is_complete': 'Mission can be completed only if all targets are complete.'}
            )

        # Validate cat availability for active missions
        cat = attrs.get('cat')
        if cat and Mission.objects.filter(cat=cat, is_complete=False).exists():
            raise serializers.ValidationError({'cat': 'Cat already has an active mission.'})
        return attrs

    def create(self, validated_data):
        targets_data = validated_data.pop('targets')
        mission = Mission.objects.create(**validated_data)
        for target_data in targets_data:
            Target.objects.create(mission=mission, **target_data)
        return mission


class MissionUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Mission
        fields = ['is_complete', 'cat']

    def validate(self, attrs):
        mission: Mission = self.instance

        # Validate cat assignment availability if cat is being set/changed
        new_cat = attrs.get('cat', mission.cat)
        if new_cat and Mission.objects.filter(cat=new_cat, is_complete=False).exclude(pk=mission.pk).exists():
            raise serializers.ValidationError({'cat': 'Cat already has an active mission.'})

        # If resulting mission state is complete, ensure all targets are already complete
        resulting_complete = attrs.get('is_complete', mission.is_complete)
        if resulting_complete and not all(t.is_complete for t in mission.targets.all()):
            raise serializers.ValidationError({'is_complete': 'All targets must be complete to complete mission.'})
        return attrs
