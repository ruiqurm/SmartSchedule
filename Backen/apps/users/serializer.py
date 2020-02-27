from rest_framework import serializers
from apps.users.models import OrgProfile,UserProfile
from friendship.models import Friend
import json

class OrgSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrgProfile
        fields = ("pk","verified_name")

class OrgDetailField(serializers.RelatedField):
    """
    如果是org，返回更具体的参数
    """
    def to_representation(self, value):
        if value is None:
            return None
        else:
            return OrgSerializer(value).data

class UserSerializer(serializers.ModelSerializer):
    org = OrgDetailField(read_only=True)
    class Meta:
        model = UserProfile
        fields = ("pk","username","org")
    # class Meta:
    #     model = User
    #     fields = ("id","username","is_org")
#



class FridenshipSerializer(serializers.Serializer):
    to_user = serializers.PrimaryKeyRelatedField(read_only=True)
    from_user = serializers.PrimaryKeyRelatedField(read_only=True)



