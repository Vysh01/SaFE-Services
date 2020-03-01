from rest_framework import serializers

from apis.models import *


class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        exclude = ('user_img',)
        model = UserSafeTbl


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

class ExportMigrantSerializer(serializers.Serializer):
    user_name = serializers.CharField(max_length=50)
    user_phone = serializers.CharField(max_length=20)
    user_age = serializers.IntegerField()
    user_sex = serializers.CharField(max_length=10)
    percent_comp = serializers.CharField(max_length=10)
    current_country = serializers.CharField(max_length=20)
    registered_country = serializers.CharField(max_length=20)


class ExportHelperSerializer(serializers.Serializer):
    user_name = serializers.CharField(max_length=50)
    user_phone = serializers.CharField(max_length=20)
    user_email = serializers.CharField(max_length=10)

class ExportRedflagMigrantSerializer(serializers.Serializer):
    question = serializers.CharField(max_length=500)
    response = serializers.CharField(max_length=500)
    question_query = serializers.CharField(max_length=500)
    user_name = serializers.CharField(max_length=50)
    user_phone = serializers.CharField(max_length=20)
    user_age = serializers.IntegerField()
    user_sex = serializers.CharField(max_length=10)
    percent_comp = serializers.CharField(max_length=10)
    current_country = serializers.CharField(max_length=20)
    registered_country = serializers.CharField(max_length=20)

