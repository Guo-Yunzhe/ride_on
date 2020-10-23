import time 
import datetime 
import os 
import sys 


# get activities from strava
# manage loacal activities and update plan 
class activity_manager(object):
    '''

    '''
    def __init__(self, token_manager = None ):

        self.token_manager = token_manager
        self.local_update_record_path = None 
        self.local_activity_record_path = None  # `dict` is a unhashable type
        self.local_activity_list_path = None 
        self.has_path = False 

        # --------------------------------
        self.find_local_storage_path()
        assert self.check_path_exist() is True 
        pass

    def check_path_exist(self):
        c1 = os.path.exists(self.local_update_record_path)
        c2 = os.path.exists(self.local_activity_record_path)
        c3 = os.path.exists(self.local_activity_list_path)
        self.has_path = c1 and c2 and c3
        return self.has_path
    
    def check_token_manager(self):
        if self.token_manager is None: return False 
        self.token_manager.refresh_token()
        res = self.token_manager.check_token_avaiable()
        return res 
        
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
        self.local_update_record_path = res 
        self.local_activity_list_path = os.path.join( local_dir_name, 'activities_list.json')
        self.local_activity_record_path = os.path.join( local_dir_name, 'activities_raw_record.dat')
        if self.check_path_exist() is False:
            f1 = open(self.local_update_record_path, 'w+')
            f2 = open(self.local_activity_list_path, 'w+')
            f3 = open(self.local_activity_record_path, 'w+')
            f1.close()
            f2.close()
            f3.close()
            pass
        pass # end of the func 
    
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



