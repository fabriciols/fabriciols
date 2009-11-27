from django.db import models
from datetime import datetime

# ---------------------------
# Definicao das tabelas do BD
# ---------------------------

class userInfo(models.Model):
	psn_id = models.CharField(max_length=30)
	email  = models.CharField(max_length=50)
	pic_url= models.CharField(max_length=150)

# A ultima vez que o sv atualizou a base inteira
class userLastTrophy(models.Model):
	platinum = models.IntegerField(default=0)
	gold    = models.IntegerField(default=0)
	silver  = models.IntegerField(default=0)
	bronze  = models.IntegerField(default=0)
	total   = models.IntegerField(default=0)
	level   = models.IntegerField(default=0)
	perc_level = models.IntegerField(default=0)
	date_update = models.DateTimeField(default=datetime.now, blank=True)

class userTrophy(models.Model):
	user     = models.ForeignKey(userInfo)
	platinum = models.IntegerField()
	gold    = models.IntegerField()
	silver  = models.IntegerField()
	bronze  = models.IntegerField()
	total   = models.IntegerField()
	level   = models.IntegerField()
	perc_level  = models.IntegerField()
	date_update = models.DateTimeField(default=datetime.now, blank=True)

	last_trophy = models.ForeignKey(userLastTrophy, blank=True)

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

class updateQueue(models.Model):
	psn_id  = models.CharField(max_length=30, blank=True, default="0")
	type	  = models.IntegerField()
	date    = models.DateTimeField(default=datetime.now, blank=True)
	
