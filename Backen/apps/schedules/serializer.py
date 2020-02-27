from rest_framework import serializers
from apps.schedules.models import Schedule,ScheduleTable,Todo,Post,Activity
from apps.users.models import OrgProfile

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

class PostObjectRelatedField(serializers.RelatedField):
    """
    依据https://www.django-rest-framework.org/api-guide/relations/#generic-relationships改写的
    一个Field，用于序列化GenericRelation Field
    """
    def to_representation(self, value):
        """
        Serialize tagged objects to a simple textual representation.
        """
        print(type(value))
        if isinstance(value, Schedule):
            return ScheduleSerializer(value).data
        elif isinstance(value, Todo):
            return TodoSerializer(value).data
        elif isinstance(value,Activity):
            raise #TODO： 添加Acitivity的序列化
        raise Exception('Unexpected type of tagged object')


class PostSerializer(serializers.ModelSerializer):
    content_object = PostObjectRelatedField(read_only=True)
    class Meta:
        model = Post
        fields = ('pk','user','add_time','content_object')