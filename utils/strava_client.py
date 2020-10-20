import time 

# TODO demo http://developers.strava.com/docs/reference/#api-Activities-getLoggedInAthleteActivities

class strava_client(object):
    '''
        Strava Client 
    '''
    def __init__(self, token_manager):
        self.token = token_manager()
        self.last_update_time = None # <int>, time stamp 
        self.activity_list = []

        
        pass

    def get_activity_by_month(self, year, month):
        # some assertion
        assert year > 2000
        assert year <= time.gmtime().tm_year + 1 
        assert month > 0
        assert month < 13 
        # time stamps 


        pass


    pass 