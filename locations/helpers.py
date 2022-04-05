from math import cos, asin, sqrt

def get_distance_from_coordinates(lat1, lon1, lat2, lon2):
    """
    Get distance in km from GPS location using Haversine formula
    cf: https://stackoverflow.com/questions/41336756/find-the-closest-latitude-and-longitude
    """
    p = 0.017453292519943295 # pi/180 to convert ° to rad
    hav = 0.5 - cos((lat2-lat1)*p)/2 + cos(lat1*p)*cos(lat2*p) * (1-cos((lon2-lon1)*p)) / 2
    return 2 * 6371 * asin(sqrt(hav)) # 6371 -> earth radius

def sort_to_closest(coordinates_list, target, res_len):
    """
    Get closest locations to v from data using GPS coordinates
    \param: data is a list of dict with 2 keys: 'lon' 6 'lat' as decimals
    \param: v is the location to compare from, a dict with 2 keys: 'lon' 6 'lat' as decimals
    \param: reslen is an integer for the max size of the resulting list
    Example: 
        tempDataList = [{'latitude': 39.7612992, 'longitude': -86.1519681}, 
                        {'latitude': 39.762241,  'longitude': -86.158436 }, 
                        {'latitude': 39.7622292, 'longitude': -86.1578917}]

        v = {'latitude': 39.7622290, 'longitude': -86.1519750}
        print(closest(tempDataList, v))
    """
    res = sorted(coordinates_list, key=lambda p: get_distance_from_coordinates(float(target['latitude']),float(target['longitude']),float(p.latitude),float(p.longitude)))
    if res_len < len(res) and res_len > 0:
        res = res[:res_len]
    return res


