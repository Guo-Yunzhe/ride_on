# RIDE ON ! 

import os 
import sys 
import time 
import json 
import subprocess
# todo: add log info 

class token(object):
    '''Token Management.
    '''

    def __init__(self):
        self.oauth_dict = None
        self.conf_file_path = None 
        self.strava_ID = None 
        self.strava_secret = None 
        self.access_token = None 
        self.refresh_token = None 
        self.expire_time = None 
        self.INVALID_REFRESH_TOKEN = False # if True, the access token are can not use
        # initialize 
        self.find_config_file_path()
        self.find_token_from_config_file()
        pass

    def test_internet_connection(self):
        internet_test = self.refresh_access_token()
        if internet_test is not True:
            return False 
        else:
            return True 
        pass
    
    def find_config_file_path(self, file_name = 'strava_settings.json'):
        """Find the path of Strava Token Config File.
        The config file should be a json file.
        This function exit when it failed to find the path.

        Args:
            file_name (str, optional): The path of  Strava Token Config File. Defaults to 'strava_settings.json'.
        """
        res = None 
        if os.path.exists(file_name):
            res = os.path.join(os.path.abspath('.'), file_name)
        elif os.path.exists(os.path.join(os.path.abspath('..'), file_name)):
            res = os.path.join(os.path.abspath('..'), file_name)
        elif os.path.exists(os.path.join(os.path.abspath('..'), 'conf',file_name)):
            res = os.path.join(os.path.abspath('..'), file_name)
            pass
        else:
            print('Strava Setting File NOT Exist!')
            sys.exit(1)
        self.conf_file_path = res 
        pass

    def find_token_from_config_file(self):
        self.find_config_file_path()
        f = open(self.conf_file_path, 'r')
        token_json = f.read()
        f.close()
        token_dict = json.loads(token_json)
        try:
            self.strava_ID = token_dict['STRAVA_ID']
            self.strava_secret = token_dict['STRAVA_SECRET']
            self.access_token  = token_dict['ACCESS_TOKEN' ]
            self.refresh_token = token_dict['REFRESH_TOKEN']
        except KeyError:
            print('Corrupted Strava Config File!')
            sys.exit(1)
            pass
        pass

    def get_access_token(self):
        curr_time = time.time()
        if self.expire_time is not None:
            if curr_time < self.expire_time - 40: # still not expired
                return self.access_token
            else: # has or about to expire 
                time.sleep(60)
                self.refresh_access_token()
                return self.access_token
        else: # self.expire_time is None 
            self.refresh_access_token()
            return self.access_token

        pass 

    def check_token_avaiable(self, input_token = 'DEFAULT_INPUT'):
        """Check out if the token is avaliable.

            CURL: curl -G https://www.strava.com/api/v3/athlete -H "Authorization: Bearer ReplaceWithAccessToken"
        """
        curr_time = time.time()
        if self.expire_time is not None and 'DEFAULT' in input_token:
            if curr_time > self.expire_time:
                # expired
                return False 
            else:
                return True 
            pass 
        # Now self.expire_time is None 
        if 'DEFAULT' in input_token:
            test_token = self.access_token
        else:
            test_token = input_token
            pass
        res = None 
        # A success_msg_example = '''{"id":xxxxx,"username":"xxx","resource_state":2,"firstname":"Yunzhe","lastname":"Guo","city":"北京市","state":"北京市","country":"中国","sex":"M","premium":true,"summit":true,"created_at":"2018-12-29T02:48:44Z","updated_at":"2020-10-17T09:44:20Z","badge_type_id":1,"profile_medium":"https://xxx","profile":"https://xxx","friend":null,"follower":null}'''
        # A failed_msg_example  = '''{"message":"Authorization Error","errors":[{"resource":"Athlete","field":"access_token","code":"invalid"}]}'''
        ret = subprocess.run(\
            ['curl', '-G', 'https://www.strava.com/api/v3/athlete', \
            '-H', 'Authorization: Bearer %s'%(test_token)
            ],\
            shell=True,stdout=subprocess.PIPE,\
            stderr=subprocess.PIPE,encoding="utf-8",\
            timeout=15) # usually 15s is enough
        if ret.returncode == 0:
            msg = ret.stdout 
        else:
            return res # Query Failed 
        # then check the response 
        if "Authorization Error" in msg:
            res = False  # Token NOT Avaliable 
        elif 'id' in msg and 'username' in msg:
            res = True   # Token Avaliable 
            # print('Access Token Avaliable!')
        else: 
            # other case ? 
            # the code here should never be executed
            pass 
        return res 

    # 
    def refresh_access_token(self):
        """Get New Access Token from Strava. 
        An CURL example is given:

        curl -X POST https://www.strava.com/api/v3/oauth/token \
          -d client_id=ReplaceWithClientID \
          -d client_secret=ReplaceWithClientSecret \
          -d grant_type=refresh_token \
          -d refresh_token=ReplaceWithRefreshToken
        """ 
        ret = subprocess.run(\
            ['curl', '-X', 'POST', 'https://www.strava.com/api/v3/oauth/token', \
            '-d', 'client_id=%s'%(str(self.strava_ID)),
            '-d', 'client_secret=%s'%(self.strava_secret),
            '-d', 'grant_type=refresh_token', 
            '-d', 'refresh_token=%s'%(self.refresh_token)
            ],\
            shell=True,stdout=subprocess.PIPE,\
            stderr=subprocess.PIPE,encoding="utf-8",\
            timeout=15) # usually 15s is enough
        if ret.returncode == 0:
            msg = ret.stdout 
        else:
            return None # Internet Problem
        # print(msg)
        try: 
            msg_dict = eval(msg)
            self.refresh_token = msg_dict['refresh_token']
            self.access_token  = msg_dict['access_token' ]
            self.expire_time   = msg_dict['expires_at'   ]
            # update to file 
            self.write_tokens_to_config_file()
            return True
        except KeyError: # query Failed
            print('Key Error when refresh access token!')
            return False 
        pass

    def write_tokens_to_config_file(self):
        token_dict = {}
        token_dict['STRAVA_ID'] = self.strava_ID 
        token_dict['STRAVA_SECRET'] = self.strava_secret 
        token_dict['ACCESS_TOKEN' ] = self.access_token 
        token_dict['REFRESH_TOKEN'] = self.refresh_token 
        json_str = json.dumps(token_dict)
        # print(json_str)
        with open(self.conf_file_path, 'w') as f:
            f.seek(0)
            f.truncate()
            f.write(json_str)
            pass
        # end
        pass



def test_token_management():
    t = token()
    print( t.get_access_token() ) 
    pass 

# test_token_management()




''' test code in history
# x.get_strava_oauth_dict_from_file()
# x.find_config_file_path()

# command = 'curl -G https://www.strava.com/api/v3/athlete -H "Authorization: Bearer ~ReplaceWithYourToken"'
# d = os.popen(command).readlines()

print( t.check_token_avaiable() )
print(t.access_token)
t.refresh_access_token()
print(t.access_token)
'''



