from django.apps import AppConfig
from scipy import spatial
import pandas as pd

us_location = []
us_lat_long_kd_tree = None
us_user_lat_long_detail = None

class ApiAppConfig(AppConfig):

    name = 'user_locator_cass.api'

    def ready(self):
        from user_locator_cass.api.models import UsLocation
        from cassandra.cqlengine.connection import get_session
        global us_location, us_lat_long_kd_tree, us_user_lat_long_detail
        print('**** Loading initial cities data')
        query = UsLocation.objects.all().limit(None)
        session = get_session()
        local_us_location = session.execute(str(query))
        us_location = list(local_us_location)
        print(us_location[0])
        lat_long_points = []
        lat_long_user_detail = []
        #lat_long_points = [((d['latitude'], d['longitude'])) for d in us_location]
        for d in us_location:
            lat_long_points.append((d['latitude'], d['longitude']))
            lat_long_user_detail.append(d)
        print('**** ' + str(lat_long_points[0]))
        us_lat_long_kd_tree = spatial.KDTree(lat_long_points)

        us_location_keys = us_location[0].keys()
        #us_user_lat_long_detail = pd.DataFrame([[d[c] for c in us_location_keys] for d in us_location], columns=us_location_keys)
        us_user_lat_long_detail = pd.DataFrame(lat_long_user_detail, columns=us_location_keys)
        #print(df.head())
        print('*** Loading initial cities data completed with # of cities : {}'.format(len(us_location)))