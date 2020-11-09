#  test code to fetch data from strava 
try:
    from token_management import token_manager
    from activity_management import activity_manager
    from strava_client import strava_client
except:
    import sys 
    sys.exit()

cc = strava_client(token_manager= token_manager() , activity_manager= activity_manager() )

aa = cc.activity_manager

print('Before')
print(cc.activity_manager.activity_list)

cc.fetch_activities_last_month(0.2)

print('After')
print(cc.activity_manager.activity_list)

