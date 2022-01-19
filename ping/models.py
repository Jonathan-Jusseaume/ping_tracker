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
from django.db import connection, models


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
    def add_note(user, content):
        Note.objects.create(user=user, content=content, date=date.today())

    @staticmethod
    def get_notes_of_user(user):
        return Note.objects.filter(user=user).order_by('-date')

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
    def insert(user, opponent, comment, match_date, status, rank):
        return Match.objects.create(user=user,
                                    comment=comment,
                                    opponent_id=opponent.id,
                                    date=match_date,
                                    rank_opponent=rank,
                                    status_id=status)

    @staticmethod
    def get_matchs_of_user(user):
        matchs = Match.objects.filter(user=user).order_by('-date')
        for match in matchs:
            match.get_sets_of_match()
        return matchs

    @staticmethod
    def add_match(user, opponent, user_scores, opponent_scores, comment, date, rank_opponent):
        victory_user = 0
        for i in range(len(user_scores)):
            user_scores[i] = int(user_scores[i])
            opponent_scores[i] = int(opponent_scores[i])
            if user_scores[i] > opponent_scores[i]:
                victory_user += 1
        match = Match.insert(user,
                             opponent,
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

    class Meta:
        managed = False
        db_table = 'pt_set'

    @staticmethod
    def insert(match, score_user, score_opponent, number):
        return Set.objects.create(match_id=match.id,
                                  score_user=score_user,
                                  score_opponent=score_opponent,
                                  number=number)


class UserStats(models.Model):
    id = models.AutoField(primary_key=True, db_column='uss_id')
    user = models.OneToOneField(User, models.DO_NOTHING, db_column='uss_usr_id')
    victory = models.IntegerField(default=0, db_column='uss_number_victory')
    defeat = models.IntegerField(default=0, db_column='uss_number_defeat')
    fifth_set_victory = models.IntegerField(default=0, db_column='uss_fifth_set_victory')
    fifth_set_defeat = models.IntegerField(default=0, db_column='uss_fifth_set_defeat')
    decisive_victory = models.IntegerField(default=0, db_column='uss_decisive_victory')
    decisive_defeat = models.IntegerField(default=0, db_column='uss_decisive_defeat')

    def get_win_lose_ratio(self):
        return {
            StatusTypeString.VICTORY.value: self.victory,
            StatusTypeString.DEFEAT.value: self.defeat
        }

    def get_fifth_set_ratio(self):
        return {
            StatusTypeString.VICTORY.value: self.fifth_set_victory,
            StatusTypeString.DEFEAT.value: self.fifth_set_defeat
        }

    def get_clutch_set_ratio(self):
        return {
            StatusTypeString.VICTORY.value: self.decisive_victory,
            StatusTypeString.DEFEAT.value: self.decisive_defeat
        }

    def get_average_opponents(self):
        with connection.cursor() as c:
            c.execute("SELECT cast(trunc(mat_rank_opponent / 100) as integer) AS ranking,"
                      "sum(CASE WHEN mat_mas_id = 0 THEN 1 ELSE 0 END) AS victory, "
                      "sum(CASE WHEN mat_mas_id = 1 THEN 1 ELSE 0 END) AS defeat "
                      "FROM pt_match WHERE mat_usr_id = " + str(
                self.user.id) + " GROUP BY trunc(mat_rank_opponent / 100);")
            return c.fetchall()

    class Meta:
        managed = False
        db_table = 'pt_user_stats'


class StatusType(Enum):
    VICTORY = 0
    DEFEAT = 1


class StatusTypeString(Enum):
    VICTORY = "Victoire(s)"
    DEFEAT = "Défaite(s)"
