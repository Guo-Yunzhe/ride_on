import json 

token_dict = {}
conf_file_path = 'strava_settings.json'
# start input 
strava_ID = input('Please input your Strava Client ID, then press ENTER:\n')
strava_secret = input('Please PASTE your Strava Client Secret, then press ENTER:\n')
access_token  = input('Please PASTE your Strava Access Token, then press ENTER:\n')
refresh_token = input('Please PASTE your Strava Refresh Token, then press ENTER:\n')

token_dict['STRAVA_ID'] = strava_ID 
token_dict['STRAVA_SECRET'] = strava_secret 
token_dict['ACCESS_TOKEN' ] = access_token 
token_dict['REFRESH_TOKEN'] = refresh_token 

json_str = json.dumps(token_dict, sort_keys= False)
with open(conf_file_path, 'w') as f:
    # f.seek(0)
    # f.truncate()
    f.write(json_str)
    pass
