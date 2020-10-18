# RIDE ON ! 

# todo: add log info 

class token(object):
    '''Strava V3 API Token Management.
    '''

    def __init__(self):
        self.oauth_dict = None
        pass

    def parse_oauth_info(self):
        """Extract tokens and other important info from oauth dict.
        """
        assert self.oauth_dict is not None 
        assert type(self.oauth_dict) == type({})


        pass
    
    def get_strava_oauth_from_file(self, response_path = 'Strava.json'):
        """Get Strava response json from disk. Add it to self.oauth_dict .

        Args:
            response_path (str, optional): the json path. Defaults to 'Strava.json'.
        """
        import os 
        assert os.path.exists(response_path)
        f = open(response_path,'r')
        response_str = f.read()
        f.close()
        try:
            self.oauth_dict = eval(response_str)
        except SyntaxError:
            print('Wrong Strava OAuth Response File!')
            import sys 
            sys.exit(1)
            pass
        pass


    def get_token(self, OAuth_response):

        pass

    # 
    def test_token_avaiable(self):


        pass

    # 
    def refresh_token(self):


        pass


x = token()
x.get_strava_oauth_from_file()

