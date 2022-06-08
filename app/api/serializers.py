from rest_framework import serializers
from ..models import MainTask, SubTask


class MainTaskSerializer(serializers.ModelSerializer):
    user_email = serializers.SerializerMethodField()

    class Meta:
        model = MainTask
        fields = '__all__'

    def get_user_email(self, obj):
        return obj.created_by.email


class SubTaskSerializer(serializers.ModelSerializer):
    user_email = serializers.SerializerMethodField()
    maintask_title = serializers.SerializerMethodField()

    class Meta:
        model = SubTask
        fields = '__all__'

    def get_user_email(self, obj):
        return obj.created_by.email
    
    def get_maintask_title(self, obj):
        return obj.maintask.title