# fetch activities from strava
# manage update plan 
# currently we use stravaio 

import time 
import random
import requests

from stravaio import StravaIO

class strava_client(object):
    '''
        Strava Client 
    '''

    def __init__(self, \
            token_manager = None,\
            activity_manager = None):
        # First we load and test the Token Manager 
        assert token_manager is not None 
        self.token_manager = token_manager
        token_manager_test = self.token_manager.test()
        if token_manager_test is False:
            print('There is an ERROR when testing Token Manager!')
            pass 
        # Second we load the Activity Manager
        assert activity_manager is not None
        self.activity_manager = activity_manager
        if self.activity_manager.local_storage_loaded is False:
            print('There is an ERROR when load Local Storage!')
            pass
        # the client's access token should get from token manager every fetch event, not once 
        # self.client = StravaIO(access_token=self.token_manager.get_access_token() )
        # and other variables
        self.FETCH_INTERVAL = 10.24 # wait interval should > 9s, because strava limits 100 queries every 15 mins 
        pass 

    # for now we only support *after* a time stamp
    def fetch_activities_after_year(self, year = None):
        assert year is not None # year = 2020 or 2019
        # need datetime -> timestamp 
        # 2017.1.1 -> time stamp xxx 

        pass

    def fetch_activities_last_month(self, month_cnt = 2):
        # assert type(month_cnt) == type(8) # we set month cnt can be float
        assert month_cnt > 0
        now = int(time.time())
        last_month = int( now -  month_cnt * (31 * 24 * 3600 ) )   
        fetched_activities = self.fetch_activities_after(last_month)
        self.activity_manager.merge_activity_storage(fetched_activities)
        print('Activity after Last %g Month(%d) Fetched.' % (month_cnt, last_month) )
        self.activity_manager.update_local_storage()
        pass
    
    def fetch_activities_last_year(self, year_cnt = 1):
        now = int(time.time())
        last_year = int(now - 366 * 24 * 3600 * year_cnt)
        fetched_activities = self.fetch_activities_after(last_year)
        self.activity_manager.merge_activity_storage(fetched_activities)
        print('Activity after Last %g Year(%d) Fetched.' % (year_cnt, last_year))
        self.activity_manager.update_local_storage()
        pass

    def fetch_last_update(self): # use this for every day update
        last_update_TS = self.activity_manager.last_update_timestamp
        fetched_activities = self.fetch_activities_after(last_update_TS)
        self.activity_manager.merge_activity_storage(fetched_activities)
        print('Activity after Last Time Stamp %d Fetched.' % (last_update_TS) )
        self.activity_manager.update_local_storage()
        pass 

    def fetch_activities_after(self, input_timestamp = 1595161543, update_local_every_fetch = True):
        # the actual fetch method
        #==========================================
        # this line of code query activities list, but not fetch exact activity infomation
        tmp_strava_client = StravaIO(access_token=self.token_manager.get_access_token() )
        list_activities = tmp_strava_client.get_logged_in_athlete_activities(after = input_timestamp)
        self.activity_manager.fetch_API_record_counter_click()
        fetched_activities = {}
        # this loop fetch exact activity information
        for a in list_activities: 
            if str(a.id) in self.activity_manager.activity_list:
                print('Activity %d already stored in disk, skip.' % a.id) 
                time.sleep(0.327 + random.random() * 3 )
                continue
            time.sleep(self.FETCH_INTERVAL + random.random() * 2)
            print('Fetching Activity, ID is %d ...' % a.id)
            # initialize client and fetch 
            try:
                tmp_strava_client = StravaIO(access_token=self.token_manager.get_access_token() )
                each_activity = tmp_strava_client.get_activity_by_id(a.id)
                self.activity_manager.fetch_API_record_counter_click()
                each_activity_dict = each_activity.to_dict()
                fetched_activities[str(each_activity_dict['id'])] = each_activity_dict
            except: # TODO we need expand more error and handle method here !
                print('An ERROR occured when fetching activity %d'%(a.id))
                continue # go to fetch next activity
            # write to disk every fetch
            if update_local_every_fetch == True:
                self.activity_manager.merge_activity_storage(fetched_activities)
                self.activity_manager.update_local_storage()
                pass
            pass
        # here the fetch operation is over 
        return fetched_activities  # end of method `fetch_activities_after`

    pass  # end of the class 
