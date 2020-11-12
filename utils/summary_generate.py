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

        pass


    def find_summary_dir_path(self):


        pass 


#  test code  
ss = summary_generator(activity_manager= activity_manager() )
example_ID = '4322397441'
a = ss.activity_dict[example_ID]


