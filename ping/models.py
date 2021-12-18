# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.contrib.auth.models import User
from django.db import models


class MatchStatus(models.Model):
    id = models.DecimalField(primary_key=True, max_digits=65535, decimal_places=65535, db_column='mas_id')
    name = models.CharField(max_length=10, db_column='mas_name')

    class Meta:
        managed = False
        db_table = 'pt_match_status'


class Opponent(models.Model):
    id = models.CharField(primary_key=True, max_length=7, db_column='opp_id')
    last_name = models.CharField(max_length=50, db_column='opp_last_name')
    first_name = models.CharField(max_length=50, db_column='opp_first_name')

    class Meta:
        managed = False
        db_table = 'pt_opponent'


class Note(models.Model):
    id = models.AutoField(primary_key=True, db_column='not_id')
    content = models.CharField(max_length=500, db_column='not_content')
    usr = models.ForeignKey(User, models.DO_NOTHING, db_column='not_usr')

    class Meta:
        managed = False
        db_table = 'pt_note'
