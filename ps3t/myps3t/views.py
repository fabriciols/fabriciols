# Create your views here.
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import get_list_or_404
from django.shortcuts import render_to_response
import ps3t.myps3t.models as db

def rank(request):

	users  = get_list_or_404(db.userTrophy.objects.all())

	perc_list = []

	for user in users:
		print user.user.psn_id
		print user.user.pic_url
		perc =  (( 202 * user.perc_level) / 100)
		perc_list.append([user, perc])

	return render_to_response('Rank.html',
				{'users' : perc_list })

def rankUser(request, userName):
	user           = get_object_or_404(db.userInfo, psn_id=userName)
	user_trophy    = get_object_or_404(db.userTrophy, user=user)
	user_game_info = get_list_or_404(db.userGameInfo, user=user)

	perc_list = []

	for gameInfo in user_game_info:
		perc =  (( 202 * gameInfo.perc_done ) / 100)
		perc_list.append([gameInfo, perc])

	return render_to_response('userRank.html',
				{'user'          : user,
				 'user_trophy'   : user_trophy,
				 'user_game_info': perc_list,
				})
