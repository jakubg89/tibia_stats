from django.db import models


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


class Boosted(models.Model):
    boosted_id = models.AutoField(db_column='Boosted_id', primary_key=True)  # Field name made lowercase.
    name = models.CharField(max_length=50, blank=True, null=True)
    image_url = models.CharField(max_length=100, blank=True, null=True)
    type = models.CharField(max_length=15, blank=True, null=True)
    date_time = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'boosted'


class WorldOnlineHistory(models.Model):
    id_online = models.AutoField(primary_key=True)
    world = models.ForeignKey(World, models.DO_NOTHING)
    players_online = models.SmallIntegerField(blank=True, null=True)
    date = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'world_online_history'


class Highscores(models.Model):
    category = models.CharField(max_length=45, blank=True, null=True)
    rank = models.IntegerField(blank=True, null=True)
    name = models.CharField(max_length=45, blank=True, null=True)
    vocation = models.CharField(max_length=45, blank=True, null=True)
    world_id = models.CharField(max_length=45, blank=True, null=True)
    level = models.IntegerField(blank=True, null=True)
    value = models.BigIntegerField(blank=True, null=True)
    date = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'highscores'

