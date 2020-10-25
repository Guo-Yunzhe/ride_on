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
        # activity information 
        self.activity_list = None # a list of activity ID 
        self.activity_record = None # a dict storage all activity information 
        # update information 
        self.update_info_loaded = False 
        self.last_update_timestamp = None # when fetch new activities, we use `after = self.last_update_timestamp`
        self.earliest_known_timestamp = None # we sure that time between [[self.earliest_known_timestamp, self.last_update_timestamp]] is updated
        self.update_record_dict = None # this dict record the API request count every day, Strava have request limit per day and per hour
        # initialized operations
        # --------------------------------
        self.find_local_storage_path()
        assert self.check_path_exist() is True 
        pass

    def check_path_exist(self):
        c1 = os.path.exists(self.local_update_config_path)
        c2 = os.path.exists(self.local_activity_record_path)
        c3 = os.path.exists(self.local_activity_list_path)
        self.has_path = c1 and c2 and c3
        return self.has_path
    
        
    def find_local_storage_path(self, file_name = 'update_record.json '):
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
        self.local_activity_record_path = os.path.join( local_dir_name, 'activities_raw_record.dat')
        if self.check_path_exist() is False:
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
        self.activity_record = json.loads(activity_record_str)
        pass

    def load_local_storage(self):
        # todo: load the update config json 
        with open(self.local_update_config_path, 'r') as f :
            update_config_str = f.read()
            pass
        try:
            update_config = json.loads(update_config_str)
            FIRST_LOAD = False 
        except:
            update_config = {}
            update_config['last_update_time'] = 327 # means first load, no fetch yet 
            update_config['earliest_known_time'] = int(time.time())
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
            return 
        else: 
            self.activity_list = []
            self.activity_record = {}
            return 

        pass

    def update_local_storage(self):
        self.update_activity_list()
        self.update_activity_record()
        # then modify the upload config  
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
        activity_record_str = json.dumps(self.activity_record, indent= False)
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
            '- activities_raw_record.dat\n',
            '- activities_list.json\n',
            '- update_record.json\n',
        ]
        return readme_list
    pass 

aa = activity_manager()



