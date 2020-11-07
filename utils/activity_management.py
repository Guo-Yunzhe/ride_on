import time 
import datetime 
import os 
import sys 
import json 


# manage local acticity storage, update time
class activity_manager(object):
    '''

    '''
    def __init__(self): # , token_manager = None ):

        # self.token_manager = token_manager
        self.local_update_config_path = None 
        self.local_activity_record_path = None  # `dict` is a unhashable type
        self.local_activity_list_path = None 
        self.has_path = False 
        self.local_storage_loaded = False 
        # activity information 
        self.activity_list = None # a list of activity ID, keys of dict activity_storage
        self.activity_storage = None # a dict that store all activity information 
        # update information 
        self.update_info_loaded = False 
        self.last_update_timestamp = None # when fetch new activities, we use `after = self.last_update_timestamp`
        self.earliest_known_timestamp = None # usually, time between [[self.earliest_known_timestamp, self.last_update_timestamp]] is updated
        # for this dict, we use `time.strftime("%Y-%m-%d")` as key 
        self.update_record_dict = None # this dict record the API request count every day, Strava have request limit per day 
        # initialized operations
        # --------------------------------
        self.find_local_storage_path()
        assert self.check_path_exist() is True 
        # -------- load local storage 
        self.load_local_storage()
        pass
    
    # add one update record 
    def fetch_API_record_counter_click(self, cnt = 1 ):
        # cnt should be 1 in most cases 
        assert type(cnt) == type(101)
        key = time.strftime("%Y-%m-%d")
        value = self.update_record_dict.get(key, 0) + 1 
        self.update_record_dict[key] = value 
        # should we write to disk now ?
        pass 

    def check_earliest_latest_time(self):
        res_earliest = float('inf')
        res_latest   = 0 
        for aid in self.activity_list:
            each_activity_start_time_str = self.activity_storage[str(aid)]['start_date'] # we do not use local time here 
            each_timestamp = activity_manager.datetime_2_timestamp(each_activity_start_time_str)
            if each_timestamp < res_earliest:
                res_earliest = each_timestamp
            if each_timestamp > res_latest:
                res_latest   = each_timestamp
            pass
        # write to self, should be int 
        self.earliest_known_timestamp = res_earliest
        self.last_update_timestamp    = res_latest
        pass
    
    @staticmethod
    def datetime_2_timestamp(date_time_str):
        assert type(date_time_str) == type('2020-10-11T13:41:31Z')
        d = datetime.datetime.strptime(date_time_str, "%Y-%m-%dT%H:%M:%SZ")
        t = d.timetuple()
        time_stamp = int(time.mktime(t))
        return time_stamp
    
    # merge two dict into one dict 
    # but not update
    def merge_activity_storage(self, fetched_activities):
        assert self.local_storage_loaded is True
        assert type(fetched_activities) == type({})
        # get keys 
        key_list = list( fetched_activities.keys() ) 
        # update self.activity storage
        for each_key in key_list:
            if each_key not in self.activity_list:
                self.activity_storage[each_key] = fetched_activities[each_key]
                self.activity_list.append(each_key)
                pass
            pass
        pass # end of `merge_activity_storage` 

    def check_path_exist(self):
        c1 = os.path.exists(self.local_update_config_path)
        c2 = os.path.exists(self.local_activity_record_path)
        c3 = os.path.exists(self.local_activity_list_path)
        self.has_path = c1 and c2 and c3
        return self.has_path
    
        
    def find_local_storage_path(self, file_name = 'update_record.json'): # bug fix 
        """Find the path of Activity Update Config File.
        The config file should be a json file.
        This function exit when it failed to find the path.

        Args:
            file_name (str, optional): The path of Strava Token Config File. Defaults to 'strava_settings.json'.
        """
        res = None 
        if os.path.exists('local_storage/'):
            res = os.path.join(os.path.abspath('.'),'local_storage', file_name)
        elif os.path.exists(os.path.join(os.path.abspath('..'),'local_storage')):
            res = os.path.join(os.path.abspath('..'),'local_storage', file_name)
        else:
            # create DIR and related Files 
            os.mkdir('local_storage')
            with open('local_storage/readme.md', 'w') as f:
                f.writelines(activity_manager.get_readme() )
            res = os.path.join(os.path.abspath('.'),'local_storage', file_name)
            pass
        # print(res)
        local_dir_name = os.path.dirname(res)
        self.local_update_config_path = res 
        self.local_activity_list_path = os.path.join( local_dir_name, 'activities_list.json')
        self.local_activity_record_path = os.path.join( local_dir_name, 'activities_raw_record.json')
        if self.check_path_exist() is False:
            print('Creating Local Storage Files ...')
            f1 = open(self.local_update_config_path, 'w+')
            f2 = open(self.local_activity_list_path, 'w+')
            f3 = open(self.local_activity_record_path, 'w+')
            f1.close()
            f2.close()
            f3.close()
            pass
        pass # end of the func 

    def load_activity_list(self):
        with open(self.local_activity_list_path,'r') as f:
            activity_dict_str = f.read()
            pass
        activity_dict = json.loads(activity_dict_str) # json is a dict 
        self.activity_list = activity_dict['activities'] # key value is 'activities'
        pass

    def load_activity_record(self):
        with open(self.local_activity_record_path, 'r') as f:
            activity_record_str = f.read()
            pass 
        self.activity_storage = json.loads(activity_record_str)
        pass

    def load_local_storage(self):
        with open(self.local_update_config_path, 'r') as f :
            update_config_str = f.read()
            pass
        try:
            update_config = json.loads(update_config_str)
            FIRST_LOAD = False 
        except:
            update_config = {}
            update_config['last_update_time'] = 327 # means first load, no fetch yet 
            update_config['earliest_known_time'] = 327
            update_config['update_record_dict'] = {}
            FIRST_LOAD = True 
            pass 
        self.update_info_loaded = True 
        self.last_update_timestamp = update_config['last_update_time']
        self.earliest_known_timestamp = update_config['earliest_known_time']
        self.update_record_dict = update_config['update_record_dict']
        if not FIRST_LOAD:
            self.load_activity_list()
            self.load_activity_record()
        else: 
            self.activity_list = []
            self.activity_storage = {}
            pass
        self.local_storage_loaded = True  
        self.update_local_storage()   
        pass

    def update_local_storage(self):
        if self.local_storage_loaded == False:
            print('Local Storage NOT Loaded!')
            # print('Update Failed!')
            return False 
        self.update_activity_list()
        self.update_activity_record()
        # then modify the upload config 
        self.check_earliest_latest_time() 
        update_config = {}
        update_config['last_update_time'] = self.last_update_timestamp
        update_config['earliest_known_time'] = self.earliest_known_timestamp
        update_config['update_record_dict'] = self.update_record_dict
        update_config_str = json.dumps(update_config, indent= True)
        with open(self.local_update_config_path,'w') as f:
            f.seek(0)
            f.truncate()
            f.write(update_config_str)
            pass  
        pass

    def update_activity_list(self):
        # write activity list json to file 
        assert type(self.activity_list) == type([])
        activity_dict = {}
        activity_dict['activities'] = self.activity_list
        activity_dict_str = json.dumps(activity_dict, indent= True)
        with open(self.local_activity_list_path,'w') as f:
            f.seek(0)
            f.truncate()
            f.write(activity_dict_str)
            pass    
        pass 
    
    def update_activity_record(self):
        activity_record_str = json.dumps(
            self.activity_storage, \
            indent= True, \
            ensure_ascii=True # ensure ascii is very important 
            ) 
        with open(self.local_activity_record_path,'w') as f:
            f.seek(0)
            f.truncate()
            f.write(activity_record_str)
            pass    
        pass
    
    @staticmethod
    def get_readme():
        readme_list =[
            '# DIR Local Storage\n',
            '  \n',    
            'There are several files used to store local activities and other information:\n',
            '- activities_raw_record.json\n',
            '- activities_list.json\n',
            '- update_record.json\n',
        ]
        return readme_list
    pass 

# aa = activity_manager()



