# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from enum import Enum

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
    date = models.DateField(db_column='not_date')
    user = models.ForeignKey(User, models.DO_NOTHING, db_column='not_usr')

    class Meta:
        managed = False
        db_table = 'pt_note'


class Match(models.Model):
    id = models.AutoField(primary_key=True, db_column='mat_id')
    user = models.ForeignKey(User, models.DO_NOTHING, db_column='mat_usr_id')
    status = models.ForeignKey(MatchStatus, models.DO_NOTHING, db_column='mat_mas_id')
    opponent = models.ForeignKey(Opponent, models.DO_NOTHING, db_column='mat_opp_id')
    rank_opponent = models.DecimalField(max_digits=65535, decimal_places=65535, db_column='mat_rank_opponent')
    date = models.DateField(db_column='mat_date')
    comment = models.CharField(max_length=500, blank=True, null=True, db_column='mat_comment')
    sets = []

    def get_sets_of_match(self):
        self.sets = Set.objects.filter(match=self)

    def __str__(self):
        return "Match de:" + self.opponent.last_name

    class Meta:
        managed = False
        db_table = 'pt_match'


class Set(models.Model):
    id = models.AutoField(primary_key=True, db_column='set_id')
    match = models.ForeignKey(Match, models.DO_NOTHING, db_column='set_mat_id')
    score_user = models.DecimalField(max_digits=65535, decimal_places=65535, db_column='set_score_user')
    score_opponent = models.DecimalField(max_digits=65535, decimal_places=65535, db_column='set_score_opponent')
    number = models.DecimalField(max_digits=65535, decimal_places=65535, db_column='set_number')

    class Meta:
        managed = False
        db_table = 'pt_set'


class StatusType(Enum):
    VICTORY = 0
    DEFEAT = 1
