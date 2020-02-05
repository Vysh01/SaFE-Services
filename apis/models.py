# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.db.models.signals import post_save


class ContactsTbl(models.Model):
    country = models.ForeignKey('CountriesTbl', models.DO_NOTHING)
    title = models.CharField(max_length=2000, blank=True, null=True)
    title_en = models.CharField(max_length=2000, blank=True, null=True)
    description = models.CharField(max_length=2000, blank=True, null=True)
    description_en = models.CharField(max_length=2000, blank=True, null=True)
    phone = models.CharField(max_length=500, blank=True, null=True)
    address = models.CharField(max_length=500, blank=True, null=True)
    address_en = models.CharField(max_length=500, blank=True, null=True)
    website = models.CharField(max_length=200, blank=True, null=True)
    email = models.CharField(max_length=200, blank=True, null=True)
    contact_id = models.AutoField(primary_key=True)


class Meta:
    managed = False
    db_table = 'contacts_tbl'


class CountriesTbl(models.Model):
    country_id = models.CharField(primary_key=True, max_length=45)
    country_name = models.CharField(unique=True, max_length=100)
    country_status = models.IntegerField()
    country_blacklist = models.IntegerField()
    country_order = models.IntegerField(blank=True, null=True)
    country_name_en = models.CharField(unique=True, max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'countries_tbl'


class DefaultContactsTbl(models.Model):
    id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=45, blank=True, null=True)
    title_en = models.CharField(max_length=45, blank=True, null=True)
    description = models.CharField(max_length=45, blank=True, null=True)
    description_en = models.CharField(max_length=45, blank=True, null=True)
    phone = models.CharField(max_length=45, blank=True, null=True)
    address = models.CharField(max_length=45, blank=True, null=True)
    address_en = models.CharField(max_length=45, blank=True, null=True)
    website = models.CharField(max_length=45, blank=True, null=True)
    email = models.CharField(max_length=45, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'default_contacts_tbl'


class FeedbackQuestionsResponseTable(models.Model):
    user = models.ForeignKey('MigrantTbl', models.DO_NOTHING)
    feedback_question = models.ForeignKey('FeedbackQuestionsTable', models.DO_NOTHING)
    response = models.CharField(max_length=100)
    response_feedback = models.CharField(max_length=2000)
    response_id = models.AutoField(primary_key=True)
    opt_response = models.CharField(max_length=5000, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'feedback_questions_response_table'
        unique_together = (('feedback_question', 'user'),)


class FeedbackQuestionsTable(models.Model):
    question_id = models.AutoField(primary_key=True)
    question_title = models.CharField(max_length=2000)
    question_option = models.CharField(max_length=2000)
    question_title_en = models.CharField(max_length=2000)
    question_option_en = models.CharField(max_length=2000)

    class Meta:
        managed = False
        db_table = 'feedback_questions_table'


class ManpowersTbl(models.Model):
    manpower_name = models.CharField(max_length=455)

    class Meta:
        managed = False
        db_table = 'manpowers_tbl'


class MigrantTbl(models.Model):
    migrant_id = models.AutoField(primary_key=True)
    migrant_name = models.CharField(max_length=200)
    migrant_phone = models.CharField(max_length=100)
    migrant_sex = models.CharField(max_length=100)
    user_tbl_user = models.ForeignKey('UserTbl', models.DO_NOTHING)
    migrant_age = models.IntegerField()
    fb_id = models.CharField(unique=True, max_length=200, blank=True, null=True)
    current_country = models.CharField(max_length=200, blank=True, null=True)
    inactive_date = models.CharField(max_length=45, blank=True, null=True)
    migrant_img = models.TextField(blank=True, null=True)
    migrant_tblcol = models.CharField(max_length=45, blank=True, null=True)
    percent_comp = models.PositiveIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'migrant_tbl'


class OptionsTbl(models.Model):
    option_id = models.AutoField(primary_key=True)
    option_text = models.CharField(max_length=200)
    questions_tbl_question = models.ForeignKey('QuestionsTbl', models.DO_NOTHING)
    option_text_en = models.CharField(max_length=200)

    class Meta:
        managed = False
        db_table = 'options_tbl'
        unique_together = (('option_id', 'questions_tbl_question'),)


class QuestionsTbl(models.Model):
    question_id = models.AutoField(primary_key=True)
    question_step = models.CharField(max_length=500)
    question_description = models.TextField()
    question_condition = models.CharField(max_length=500, blank=True, null=True)
    response_type = models.IntegerField()
    tiles_tbl_tile = models.ForeignKey('TilesTbl', models.DO_NOTHING)
    question_title = models.CharField(max_length=500)
    order = models.IntegerField(blank=True, null=True)
    variable = models.CharField(max_length=200, blank=True, null=True)
    conflict_description = models.CharField(max_length=2000)
    question_title_en = models.CharField(max_length=500, blank=True, null=True)
    question_step_en = models.CharField(max_length=500)
    question_description_en = models.TextField()
    conflict_description_en = models.CharField(max_length=2000, blank=True, null=True)
    question_call = models.CharField(max_length=45, blank=True, null=True)
    question_video = models.CharField(max_length=45, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'questions_tbl'


class ResponseTbl(models.Model):
    id = models.IntegerField(primary_key=True)
    user = models.ForeignKey('UserTbl', models.DO_NOTHING, related_name='responses')
    question = models.ForeignKey(QuestionsTbl, models.DO_NOTHING)
    response = models.CharField(max_length=500, blank=True, null=True)
    response_variable = models.CharField(max_length=50, blank=True, null=True)
    is_error = models.CharField(max_length=50, blank=True, null=True)
    tile = models.ForeignKey('TilesTbl', models.DO_NOTHING)
    question_query = models.CharField(max_length=2000, blank=True, null=True)
    response_time = models.CharField(max_length=45, blank=True, null=True)
    query_followback = models.CharField(max_length=10, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'response_tbl'
        unique_together = (('user', 'question'),)


class TilesTbl(models.Model):
    tile_id = models.AutoField(primary_key=True)
    tile_title = models.CharField(max_length=100)
    tile_type = models.CharField(max_length=100)
    tile_description = models.CharField(max_length=500)
    tile_order = models.IntegerField()
    tile_title_en = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'tiles_tbl'


class UserTbl(models.Model):
    user_id = models.AutoField(primary_key=True)
    user_name = models.CharField(max_length=200)
    user_phone = models.CharField(unique=True, max_length=100)
    user_sex = models.CharField(max_length=100)
    fb_id = models.CharField(unique=True, max_length=200, blank=True, null=True)
    user_age = models.IntegerField()
    user_type = models.CharField(max_length=20, blank=True, null=True)
    user_img = models.TextField(blank=True, null=True)
    percent_comp = models.FloatField(blank=True, null=True)
    current_country = models.CharField(max_length=45, blank=True, null=True)
    registered_country = models.CharField(max_length=50, blank=True, null=True)
    last_active = models.CharField(max_length=45, blank=True, null=True)
    parent_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'user_tbl'


class UserSafeTbl(models.Model):
    user_id = models.AutoField(primary_key=True)
    user_name = models.CharField(max_length=200)
    user_phone = models.CharField(unique=True, max_length=100)
    user_sex = models.CharField(max_length=100)
    user_email = models.CharField(max_length=100)
    social_network = models.CharField(max_length=20)
    social_id = models.CharField(unique=True, max_length=200, blank=True, null=True)
    user_age = models.IntegerField()
    user_type = models.CharField(max_length=20, blank=True, null=True)
    user_img = models.TextField(blank=True, null=True)
    percent_comp = models.FloatField(blank=True, null=True)
    current_country = models.CharField(max_length=45, blank=True, null=True)
    registered_country = models.CharField(max_length=50, blank=True, null=True)
    last_active = models.CharField(max_length=45, blank=True, null=True)
    parent_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'user_safe_tbl'


# This receiver handles token creation immediately a new user is created.
@receiver(post_save, sender=UserTbl)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
