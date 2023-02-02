from django.db import models


class Boosted(models.Model):
    boosted_id = models.AutoField(db_column='Boosted_id', primary_key=True)  # Field name made lowercase.
    name = models.CharField(max_length=50, blank=True, null=True)
    image_url = models.CharField(max_length=100, blank=True, null=True)
    type = models.CharField(max_length=15, blank=True, null=True)
    date_time = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'boosted'


class Character(models.Model):
    id_char = models.AutoField(primary_key=True)
    name = models.CharField(max_length=45, blank=True, null=True)
    world = models.ForeignKey('World', models.DO_NOTHING)
    voc = models.ForeignKey('Vocation', models.DO_NOTHING)

    class Meta:
        managed = True
        db_table = 'character'
        unique_together = (('id_char', 'world', 'voc'),)


class Highscores(models.Model):
    exp_rank = models.IntegerField(blank=True, null=True)
    exp_rank_change = models.IntegerField(blank=True, null=True)
    id_char = models.ForeignKey('Character', models.DO_NOTHING, db_column='id_char')
    voc = models.ForeignKey('Vocation', models.DO_NOTHING)
    world = models.ForeignKey('World', models.DO_NOTHING)
    level = models.IntegerField(blank=True, null=True)
    level_change = models.IntegerField(blank=True, null=True)
    exp_value = models.BigIntegerField(blank=True, null=True)
    exp_diff = models.BigIntegerField(blank=True, null=True)
    charm_rank = models.IntegerField(blank=True, null=True)
    charm_rank_change = models.IntegerField(blank=True, null=True)
    charm_value = models.IntegerField(blank=True, null=True)
    charm_diff = models.IntegerField(blank=True, null=True)
    date = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'highscores'
        unique_together = (('id', 'id_char', 'voc', 'world'),)


class HighscoresHistory(models.Model):
    exp_rank = models.IntegerField(blank=True, null=True)
    exp_rank_change = models.IntegerField(blank=True, null=True)
    id_char = models.ForeignKey(Character, models.DO_NOTHING, db_column='id_char')
    voc = models.ForeignKey('Vocation', models.DO_NOTHING)
    world = models.ForeignKey('World', models.DO_NOTHING)
    level = models.IntegerField(blank=True, null=True)
    level_change = models.IntegerField(blank=True, null=True)
    exp_value = models.BigIntegerField(blank=True, null=True)
    exp_diff = models.BigIntegerField(blank=True, null=True)
    charm_rank = models.IntegerField(blank=True, null=True)
    charm_rank_change = models.IntegerField(blank=True, null=True)
    charm_value = models.IntegerField(blank=True, null=True)
    charm_diff = models.IntegerField(blank=True, null=True)
    date = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'highscores_history'
        unique_together = (('id', 'id_char', 'voc', 'world'),)


class NameChange(models.Model):
    name_change_id = models.AutoField(primary_key=True)
    id_char = models.ForeignKey(Character, models.DO_NOTHING, db_column='id_char')
    level = models.IntegerField(blank=True, null=True)
    old_name = models.CharField(max_length=45, blank=True, null=True)
    new_name = models.CharField(max_length=45, blank=True, null=True)
    traded = models.IntegerField(blank=True, null=True)
    date = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'name_change'
        unique_together = (('name_change_id', 'id_char'),)


class News(models.Model):
    news_id = models.AutoField(primary_key=True)
    id_on_tibiacom = models.SmallIntegerField(blank=True, null=True)
    url_tibiacom = models.CharField(unique=True, max_length=255, blank=True, null=True)
    type = models.CharField(max_length=20, blank=True, null=True)
    content = models.TextField(blank=True, null=True)
    content_html = models.TextField(blank=True, null=True)
    date_added = models.DateTimeField()
    news_title = models.CharField(max_length=150, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'news'


class RecordsHistory(models.Model):
    exp_rank = models.IntegerField(blank=True, null=True)
    exp_rank_change = models.IntegerField(blank=True, null=True)
    id_char = models.ForeignKey(Character, models.DO_NOTHING, db_column='id_char')
    voc = models.ForeignKey('Vocation', models.DO_NOTHING)
    world = models.ForeignKey('World', models.DO_NOTHING)
    level = models.IntegerField(blank=True, null=True)
    level_change = models.IntegerField(blank=True, null=True)
    exp_value = models.BigIntegerField(blank=True, null=True)
    exp_diff = models.BigIntegerField(blank=True, null=True)
    charm_rank = models.IntegerField(blank=True, null=True)
    charm_rank_change = models.IntegerField(blank=True, null=True)
    charm_value = models.IntegerField(blank=True, null=True)
    charm_diff = models.IntegerField(blank=True, null=True)
    record_type = models.CharField(max_length=45, blank=True, null=True)
    event = models.CharField(max_length=20, blank=True, null=True)
    date = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'records_history'
        unique_together = (('id', 'id_char', 'voc', 'world'),)


class Tasks(models.Model):
    task = models.AutoField(primary_key=True)
    task_name = models.CharField(max_length=30, blank=True, null=True)
    status = models.CharField(max_length=15, blank=True, null=True)
    date = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'tasks'


class Vocation(models.Model):
    voc_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=45, blank=True, null=True)
    premium = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'vocation'


class World(models.Model):
    world_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=45, blank=True, null=True)
    name_value = models.CharField(max_length=45, blank=True, null=True)
    pvp_type = models.CharField(max_length=30, blank=True, null=True)
    pvp_type_value = models.IntegerField(blank=True, null=True)
    battleye_protected = models.CharField(max_length=45, blank=True, null=True)
    battleye_date = models.DateField(blank=True, null=True)
    battleye_value = models.IntegerField(blank=True, null=True)
    location = models.CharField(max_length=45, blank=True, null=True)
    location_value = models.IntegerField(blank=True, null=True)
    creation_date = models.DateField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'world'


class WorldOnlineHistory(models.Model):
    id_online = models.AutoField(primary_key=True)
    world = models.ForeignKey(World, models.DO_NOTHING)
    players_online = models.SmallIntegerField(blank=True, null=True)
    date = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'world_online_history'


class WorldTransfers(models.Model):
    world_transfer_id = models.AutoField(primary_key=True)
    id_char = models.ForeignKey(Character, models.DO_NOTHING, db_column='id_char')
    old_world = models.CharField(max_length=45, blank=True, null=True)
    oldid = models.SmallIntegerField(blank=True, null=True)
    new_world = models.CharField(max_length=45, blank=True, null=True)
    newid = models.SmallIntegerField(blank=True, null=True)
    level = models.IntegerField(blank=True, null=True)
    traded = models.IntegerField(blank=True, null=True)
    date = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'world_transfers'
        unique_together = (('world_transfer_id', 'id_char'),)

