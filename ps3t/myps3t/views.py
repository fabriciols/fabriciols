# Create your views here.
from django.http import HttpResponse
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.shortcuts import get_list_or_404
from django.shortcuts import render_to_response
import ps3t.myps3t.models as db
import pprint

def user_compare(user_a, user_b):
	return user_a[1] - user_b[1]

def rank(request):
	
	BRONZE_VALUE   = 15
	SILVER_VALUE   = 30
	GOLD_VALUE     = 90
	PLATINUM_VALUE = 180

	users  = get_list_or_404(db.userTrophy.objects.all())

	perc_list = []

	for user in users:
		points_total  = user.platinum + user.gold + user.silver + user.bronze

		points_total = ( user.platinum * PLATINUM_VALUE
							+ user.gold     * GOLD_VALUE
							+ user.silver   * SILVER_VALUE 
							+ user.bronze   * BRONZE_VALUE)

		setUserDif(user)

		perc_list.append([user, points_total])

	perc_list.sort(user_compare, reverse=True)

	return render_to_response('Rank.html',
				{'users' : perc_list })

def setUserDif(user):

	user.last_trophy.platinum   = user.platinum   - user.last_trophy.platinum
	user.last_trophy.gold       = user.gold       - user.last_trophy.gold
	user.last_trophy.silver     = user.silver     - user.last_trophy.silver
	user.last_trophy.bronze     = user.bronze     - user.last_trophy.bronze
	user.last_trophy.total      = user.total      - user.last_trophy.total
	user.last_trophy.level      = user.level      - user.last_trophy.level
	user.last_trophy.perc_level = user.perc_level - user.last_trophy.perc_level


def rankUser(request, userName):

	try:
		user = db.userInfo.objects.get(psn_id=userName)
	except db.userInfo.DoesNotExist:

		queue = db.updateQueue.objects.all()

		return render_to_response('noUserRank.html',
								{'user'  : userName,
								'queue'  : queue})

	user_trophy    = get_object_or_404(db.userTrophy, user=user)
	user_game_info = get_list_or_404(db.userGameInfo, user=user)

	perc_list = []

	for gameInfo in user_game_info:
		perc =  (( 202 * gameInfo.perc_done ) / 100)
		trophy_total = gameInfo.platinum + gameInfo.gold + gameInfo.silver + gameInfo.bronze

		if gameInfo.platinum is 0 and gameInfo.perc_done is 100:
			type = 1
		else:
			type = 0
				
		perc_list.append([gameInfo, perc, trophy_total, type])

	return render_to_response('userRank.html',
				{'user'          : user,
				 'user_trophy'   : user_trophy,
				 'user_game_info': perc_list,
				})
