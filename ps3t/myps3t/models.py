from django.db import models

# Definicao das tabelas do BD

class usersInfo(models.Model):
	name   = models.CharField(max_length=50)
	email  = models.CharField(max_length=50)
	passwd = models.CharField(max_length=50)
	type   = models.IntegerField()

class usersStats(models.Model):
	user   = models.ForeignKey(usersInfo)
	name   = models.CharField(max_length=50)
	platinum  = models.IntegerField()
	gold    = models.IntegerField()
	silver  = models.IntegerField()
	bronze  = models.IntegerField()
	level   = models.IntegerField()
	percent = models.IntegerField()
	last_update = models.DateTimeField()

	# Informacoes do ultimo update
	# Esta nesta tabela para ter mais agilidade
	# na hora de mostrar o Rank
	last_plat = models.IntegerField()
	last_gold = models.IntegerField()
	last_silv = models.IntegerField()
	last_bron = models.IntegerField()
	last_lvl  = models.IntegerField()
	last_perc = models.IntegerField()
