import time 
import datetime 
import os 



# get activities from strava
# manage loacal activities and update plan 
class activity(object):
    '''

    '''
    def find_update_record_path(self, file_name = 'update_record.json '):
        """Find the path of Activity Update Config File.
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
    



    pass 

