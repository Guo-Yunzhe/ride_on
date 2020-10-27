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
        # now we have two managers
        self.client = StravaIO(access_token=self.token_manager.get_access_token() )
        # and other variables
        self.FETCH_INTERVAL = 6 # wait 6s between 2 fetch
        pass 

    # for now we only support *after* a time stamp
    def fetch_activities_after_year(self, year = None):
        assert year is not None 

        pass

    def fetch_activities_last_month(self, month_cnt):
        # assert type(month_cnt) == type(8) # we set month cnt can be float
        assert month_cnt > 0
        now = int(time.time())
        last_month = int( now -  month_cnt * (31 * 24 * 3600 ) )  # fix bug  
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

    def fetch_activities_after(self, input_timestamp = 1595161543):
        # the actual fetch method
        # TODO should update the `update config` in activity manager
        #   - last update time
        #   - update count
        #   - known earlist time stamp 
        list_activities = self.client.get_logged_in_athlete_activities(after = input_timestamp)
        fetched_activities = {}
        for a in list_activities: 
            if a.id in self.activity_manager.activity_list:
                print('Activity %d already stored in local, skip.' % a.id) 
                time.sleep(1 + random.random() * 3 )
                continue
            time.sleep(self.FETCH_INTERVAL + random.random() * 2)
            print('Fetching Activity, ID is  %d ...' % a.id)
            each_activity = self.client.get_activity_by_id(a.id)
            each_activity_dict = each_activity.to_dict()
            # activity.store_locally()
            # process each activity 
            fetched_activities[each_activity_dict['id']] = each_activity_dict
            pass
        # here the fetch operation is over 
        return fetched_activities  # end of method `fetch_activities_after`

    pass  # end of the class 


# test code 

try:
    from token_management import token_manager
    from activity_management import activity_manager
except:
    import sys 
    sys.exit()

cc = strava_client(token_manager= token_manager() , activity_manager= activity_manager() )

aa = cc.activity_manager

print('Before')
print(cc.activity_manager.activity_list)

cc.fetch_activities_last_month(2.5)

print('After')
print(cc.activity_manager.activity_list)

