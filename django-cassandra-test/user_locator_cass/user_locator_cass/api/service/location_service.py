import numpy as np
from user_locator_cass.api.apps import us_lat_long_kd_tree, us_user_lat_long_detail
import pandas as df

def find_k_closet(lat, long, k):

    global us_lat_long_kd_tree, us_user_lat_long_detail

    '''Find the k nearest points from the specified lat, long.
       Paramsters:
            lat : float
            long : float
            k : int number of closet neighbor to retrieve

       Returns:
             list of at least k indexes in points that closest to point
    '''

    result = us_lat_long_kd_tree.query((lat, long), k)

    if not isinstance(result[0], np.ndarray):
        result = ([result[0]], [result[1]])
    print('********')
    print(us_user_lat_long_detail.iloc[result[1]])

    return result