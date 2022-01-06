# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from datetime import date
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

    @staticmethod
    def insert(id, last_name, first_name):
        opponent = Opponent(id, last_name, first_name)
        opponent.save()
        return Opponent.objects.get(pk=id)

    class Meta:
        managed = False
        db_table = 'pt_opponent'


class Note(models.Model):
    id = models.AutoField(primary_key=True, db_column='not_id')
    content = models.CharField(max_length=500, db_column='not_content')
    date = models.DateField(db_column='not_date')
    user = models.ForeignKey(User, models.DO_NOTHING, db_column='not_usr_id')

    @staticmethod
    def add_note(content):
        Note.objects.create(content=content, user_id=1, date=date.today())

    @staticmethod
    def get_notes_of_user(user):
        return Note.objects.all().order_by('-date')

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

    @staticmethod
    def insert(opponent, comment, match_date, status, rank):
        return Match.objects.create(user_id=1,
                                    comment=comment,
                                    opponent_id=opponent.id,
                                    date=match_date,
                                    rank_opponent=rank,
                                    status_id=status)

    @staticmethod
    def get_win_lose_ratio(user):
        win_lose_ratio = {
            StatusTypeString.VICTORY.value: Match.objects.filter(status__id=StatusType.VICTORY.value).count(),
            StatusTypeString.DEFEAT.value: Match.objects.filter(status__id=StatusType.DEFEAT.value).count()
        }
        return win_lose_ratio

    @staticmethod
    def get_matchs_of_user(user):
        matchs = Match.objects.all().order_by('-date')
        for match in matchs:
            match.get_sets_of_match()
        return matchs

    @staticmethod
    def add_match(opponent, user_scores, opponent_scores, comment, date, rank_opponent):
        victory_user = 0
        for i in range(len(user_scores)):
            user_scores[i] = int(user_scores[i])
            opponent_scores[i] = int(opponent_scores[i])
            if user_scores[i] > opponent_scores[i]:
                victory_user += 1
        match = Match.insert(opponent,
                             comment,
                             date,
                             StatusType.VICTORY.value if victory_user == 3 else StatusType.DEFEAT.value,
                             rank_opponent)
        for i in range(len(user_scores)):
            Set.insert(match, user_scores[i], opponent_scores[i], i + 1)

    class Meta:
        managed = False
        db_table = 'pt_match'


class Set(models.Model):
    id = models.AutoField(primary_key=True, db_column='set_id')
    match = models.ForeignKey(Match, models.DO_NOTHING, db_column='set_mat_id')
    score_user = models.DecimalField(max_digits=65535, decimal_places=65535, db_column='set_score_user')
    score_opponent = models.DecimalField(max_digits=65535, decimal_places=65535, db_column='set_score_opponent')
    number = models.DecimalField(max_digits=65535, decimal_places=65535, db_column='set_number')

    @staticmethod
    def get_fifth_set_ratio(user):
        win_fifth_set = 0
        lose_fifth_set = 0
        # @todo A filtrer par les matchs de l'utilisateur courant
        matchs = Match.objects.all()
        fifth_sets = Set.objects.filter(match__in=matchs, number=5)
        for set in fifth_sets:
            if set.score_user > set.score_opponent:
                win_fifth_set += 1
            else:
                lose_fifth_set += 1

        fifth_set_ratio = {
            StatusTypeString.VICTORY.value: win_fifth_set,
            StatusTypeString.DEFEAT.value: lose_fifth_set
        }
        return fifth_set_ratio

    @staticmethod
    def get_clutch_set_ratio(user):
        win_clutch_set = 0
        lose_clutch_set = 0
        # @todo A filtrer par les matchs de l'utilisateur courant
        matchs = Match.objects.all()
        sets = Set.objects.filter(match__in=matchs)
        for set in sets:
            if abs(set.score_user - set.score_opponent) <= 2:
                if set.score_user > set.score_opponent:
                    win_clutch_set += 1
                else:
                    lose_clutch_set += 1

        clutch_set_ratio = {
            StatusTypeString.VICTORY.value: win_clutch_set,
            StatusTypeString.DEFEAT.value: lose_clutch_set
        }
        return clutch_set_ratio

    class Meta:
        managed = False
        db_table = 'pt_set'

    @staticmethod
    def insert(match, score_user, score_opponent, number):
        return Set.objects.create(match_id=match.id,
                                  score_user=score_user,
                                  score_opponent=score_opponent,
                                  number=number)


class StatusType(Enum):
    VICTORY = 0
    DEFEAT = 1


class StatusTypeString(Enum):
    VICTORY = "Victoire(s)"
    DEFEAT = "Défaite(s)"
