# Create your views here.
from django.http import HttpResponse
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

		perc_list.append([user, points_total])

	perc_list.sort(user_compare, reverse=True)

	return render_to_response('Rank.html',
				{'users' : perc_list })

def rankUser(request, userName):
	user           = get_object_or_404(db.userInfo, psn_id=userName)
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
