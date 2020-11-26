try:
    from utils.activity_management import activity_manager
except ModuleNotFoundError:
    from activity_management import activity_manager

# import other packets 
import time 

class summary_generator(object):
    '''
    Generate Summary Markdown Files.
    '''

    def __init__(self,\
        activity_manager = None):
        # initialize of summary_generator
        assert activity_manager is not None
        self.activity_manager = activity_manager # an initialized activity manager 
        self.activity_dict = self.activity_manager.activity_storage 
        self.activity_month = None  # the key of this dict is like '2020-10', '2020-03'
        pass


    def find_summary_dir_path(self):
        # this dir is the output path 

        pass 

    def split_activities_by_month(self):


        pass

    def get_activity_info(self, activity_ID):
        assert type(activity_ID) == str 
        a = self.activity_dict[activity_ID]
        # what is the return type ? 

        pass 

    

#  test code  
ss = summary_generator(activity_manager= activity_manager() )
example_ID = '3836008439'
a = ss.activity_dict[example_ID]

'''
In [4]: a['distance']
Out[4]: 17603.7

In [5]: a['elapsed_time']
Out[5]: 3645

In [6]: a['timezone']
Out[6]: '(GMT+08:00) Asia/Shanghai'

In [7]: a['calories']
Out[7]: 339.0

In [8]: a['total_elevation_gain']
Out[8]: 44.0

In [9]: a['startdate']
---------------------------------------------------------------------------
KeyError                                  Traceback (most recent call last)
<ipython-input-9-92d40b0218f1> in <module>
----> 1 a['startdate']

KeyError: 'startdate'

In [10]: a['start_date_local']
Out[10]: '2020-11-11T20:57:40Z'

''' 

