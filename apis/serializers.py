from rest_framework import serializers

from apis.models import *


class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        exclude = ('user_img',)
        model = UserTbl


class ResponseSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ['question', 'response', 'is_error', 'tile_id', 'question_query', 'response_time']
        model = ResponseTbl


class QuestionsSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ['question_id', 'question_step', 'question_description']
        model = QuestionsTbl


class TestSerializer(serializers.Serializer):
    class Meta:
        fields = ['user_name']
