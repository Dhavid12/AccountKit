from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from urllib.parse import urlencode
from urllib.request import urlopen
import requests
import json

# Create your views here.
@csrf_exempt
def login(request):

	app_id = "YOUR_APP_ID"
	version = "v1.0"
	app_secret = "YOUR_ACCOUNT_KIT_SECRET_KEY"
	me_endpoint_base_url = 'https://graph.accountkit.com/v1.0/me'
	token_exchange_base_url = 'https://graph.accountkit.com/v1.0/access_token'
	template_post_login = 'login/postlogin.html'
	template_login = 'login/login.html'
	context = {
		'app_id' : app_id,
		'api_version' : version
	}

	if request.method == 'POST':
		code = request.POST.get('code')
		params = {
			'grant_type': 'authorization_code',
			'code': code,
			'access_token': 'AA|' + app_id + '|' + app_secret
		}
		token_exchange_url = token_exchange_base_url + '?' + urlencode(params)
		jsonData = json.loads(urlopen(token_exchange_url).readall().decode('utf-8'))	
		print(jsonData)
		me_endpoint_url = me_endpoint_base_url + '?access_token=' + jsonData.get('access_token')
		jsonData = json.loads(urlopen(me_endpoint_url).readall().decode('utf-8'))
		print(jsonData)
		if(jsonData.get('phone')):
			context = {
				'method' : 'SMS',
				'user_id' : jsonData.get('id'),
				'identity' : jsonData.get('phone').get('number')
			}
		elif(jsonData.get('email')):
			context = {
				'method' : 'Email',
				'user_id' : jsonData.get('id'),
				'identity' : jsonData.get('email').get('address')
			}
		return render(request, template_post_login, context)
	return render(request, template_login, context)