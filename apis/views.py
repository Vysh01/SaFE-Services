from django.db.models import Count, F, Q
from django.shortcuts import render

# Create your views here.
from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response
from rest_framework.views import APIView

from apis.models import *
from apis.serializers import *


class GetReportGen(APIView):
    def get(self, request):
        detail_query_set = UserTbl.objects.all()
        response_query_set = ResponseTbl.objects.all()
        # age_groups = UsersSerializer(detail_query_set.annotate(age_groups=Count('user_age')).values('age_groups'), many=True)
        age_groups = detail_query_set.values('user_age').annotate(count=Count('user_age')).order_by('user_age')
        gender_groups = detail_query_set.values('user_sex').annotate(count=Count('user_sex'))
        user_types = detail_query_set.values('user_type').annotate(count=Count('user_type'))
        location_group = detail_query_set.values('current_country').annotate(count=Count('current_country'))
        percentages = detail_query_set.values('percent_comp').annotate(count=Count('percent_comp'))
        reg_dates = detail_query_set.values('percent_comp').annotate(count=Count('percent_comp'))
        redflags = response_query_set.values('question_id', 'question__question_step').filter(
            is_error='true').annotate(count=Count('question_id'))
        return Response(
            {'genders': gender_groups, 'ages': age_groups, 'user_types': user_types, 'locations': location_group,
             'percentages': percentages, 'regflags': redflags},
            status.HTTP_200_OK)


class GetAllMigrants(ListAPIView):
    serializer_class = UsersSerializer
    queryset = UserTbl.objects.filter(user_type='migrant')
    pagination_class = LimitOffsetPagination


class GetAllHelpers(ListAPIView):
    serializer_class = UsersSerializer
    queryset = UserTbl.objects.filter(user_type='helper')
    pagination_class = LimitOffsetPagination


# Getting User Responses
class GetUserResponses(ListAPIView):
    serializer_class = ResponseSerializer

    def get(self, request):
        queryset = ResponseTbl.objects.annotate(question_title=F('question__question_step')).values('question',
                                                                                                    'question_title',
                                                                                                    'response',
                                                                                                    'is_error',
                                                                                                    'tile_id',
                                                                                                    'question_query',
                                                                                                    'response_time').filter(
            user_id=self.request.GET['migrant']).order_by('tile_id')
        return Response({'data': queryset})


# Get Redflags
class GetRedflagQuestions(ListAPIView):
    serializer_class = QuestionsSerializer

    def get_queryset(self):
        return QuestionsTbl.objects.values('question_id', 'question_step', 'question_description').exclude(
            Q(question_condition=None) | Q(question_condition='')).order_by(
            'tiles_tbl_tile')


class GetRedflagUsers(ListAPIView):
    serializer_class = TestSerializer

    def get_queryset(self):
        return ResponseTbl.objects.filter(question_id=self.kwargs['question']).values('user__user_name')


# Get Migrants By Percent
class GetUsersByPercent(ListAPIView):
    serializer_class = UsersSerializer

    def get_queryset(self):
        return UserTbl.objects.filter(percent_comp__gte=self.request.GET['percent_min'],
                                      percent_comp__lte=self.request.GET['percent_max'])


# Get Users by Dest & Current Country
class GetUsersByCountry(ListAPIView):
    serializer_class = UsersSerializer

    def get_queryset(self):
        destination = self.request.GET['destination']
        current = self.request.GET['current']
        return ResponseTbl.objects.filter(response_variable='mg_destination', response__contains=destination,
                                          user__current_country__contains=current)


# Searching by Name or Number
class GetUserByQuery(ListAPIView):
    serializer_class = UsersSerializer

    def get_queryset(self):
        return UserTbl.objects.filter(
            Q(user_name__icontains=self.request.GET['query']) | Q(user_phone__icontains=self.request.GET['query']))
