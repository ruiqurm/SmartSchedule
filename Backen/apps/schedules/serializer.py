from rest_framework import serializers
from apps.schedules.models import Schedule,ScheduleTable,Todo


class ScheduleSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    class Meta:
        model = Schedule
        fields = ("pk","title","add_time","description","start_time","end_time",
                  "weight","user","table")

class ScheduleTableSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    class Meta:
        model = ScheduleTable
        fields = ("pk","title","description","add_time","user","permission")
class TodoSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    class Meta:
        model = Todo
        fields = ("pk","title","add_time","user","is_finished")