from django.db import models
from datetime import datetime

# Definicao das tabelas do BD

class userInfo(models.Model):
	psn_id = models.CharField(max_length=30)
	email  = models.CharField(max_length=50)
	pic_url= models.CharField(max_length=150)

class userTrophy(models.Model):
	user     = models.ForeignKey(userInfo)
	platinum = models.IntegerField()
	gold    = models.IntegerField()
	silver  = models.IntegerField()
	bronze  = models.IntegerField()
	level   = models.IntegerField()
	total   = models.IntegerField()
	perc_level  = models.IntegerField()
	date_update = models.DateField(default=datetime.now, blank=True)

class userLastTrophy(models.Model):
	user     = models.ForeignKey(userInfo)
	platinum = models.IntegerField()
	gold    = models.IntegerField()
	silver  = models.IntegerField()
	bronze  = models.IntegerField()
	total   = models.IntegerField()
	level   = models.IntegerField()
	percent = models.IntegerField()
	date_update = models.DateField(default=datetime.now, blank=True)

class gameInfo(models.Model):
	psn_id = models.CharField(max_length=30)
	name   = models.CharField(max_length=100)
	pic_url= models.CharField(max_length=150)

class userGameInfo(models.Model):
	user      = models.ForeignKey(userInfo)
	game      = models.ForeignKey(gameInfo)
	perc_done = models.IntegerField()
	platinum  = models.IntegerField()
	gold    = models.IntegerField()
	silver  = models.IntegerField()
	bronze  = models.IntegerField()
