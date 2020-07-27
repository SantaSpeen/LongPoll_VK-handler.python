import json
def token():
	with open('./configs/token.json', 'r') as f:
		data = json.load(f)
	group_token = data['token']
	return group_token