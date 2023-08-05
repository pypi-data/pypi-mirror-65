import pyproj
import numpy as np
import pkg_resources
import re
import logging
import sys

# Get the version
version_file = pkg_resources.resource_filename('pylatlon','VERSION')
# Setup logging module
logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)
logger = logging.getLogger('pylatlon')
with open(version_file) as version_f:
   version = version_f.read().strip()

geod = pyproj.Geod(ellps='WGS84')

class dlatlon(object):
    """ A delta position object
    """
    def __init__(self, distance, azimuth, azimuth_back):
        self.distance = distance
        self.azimuth  = azimuth
        self.azimuth_back  = azimuth_back

class latlon(object):
    """ A position object
    """
    def __init__(self, lon, lat):
        self.dlon = lon
        self.dlat = lat
        dms = self.calc_dms(lon,lat)
        self.lon = dms['deg_lon']
        self.lat = dms['deg_lat']
        #self.dlon = dms['lon']
        #self.dlat = dms['lat']
        self.minutes_lon = dms['min_lon']
        self.minutes_lat = dms['min_lat']
        self.dminutes_lon = dms['dmin_lon']
        self.dminutes_lat = dms['dmin_lat']
        self.seconds_lon = dms['sec_lon']
        self.seconds_lat = dms['sec_lat']
        self.easting = dms['EW']
        self.northing = dms['NS']
        print(dms)
    def calc_dms(self,lon,lat):
        """ Calculate degrees, minutes, seconds, east, west, north south out of
        floating point longitude and latitude.
        """
        dms = {}
        dms['lon'] = lon
        dms['lat'] = lat
        dms['deg_lat']   = int(lat)
        dms['deg_lon']   = int(lon)
        # Minutes
        dms['dmin_lon'] = (lon - int(lon))*60
        dms['min_lon']  = int(dms['dmin_lon'])
        dms['dmin_lat'] = (lat - int(lat)) * 60
        dms['min_lat']  = int(dms['dmin_lat'])
        # Seconds
        dms['sec_lat']  = (dms['dmin_lat'] - dms['min_lat']) * 60
        dms['sec_lon']  = (dms['dmin_lon'] - dms['min_lon']) * 60
        if(dms['deg_lon']<0):
            dms['deg_lon'] = - dms['deg_lon']
            dms['EW'] = 'W'
        else:
            dms['EW'] = 'E'
        if(dms['deg_lat']<0):
            dms['deg_lat'] = - dms['deg_lat']
            dms['NS'] = 'S'
        else:
            dms['NS'] = 'N'

        return dms
    def strf(self,format=1,separator=' ', prec_deg=4):
        """
        dlon/dlat: Decimal longitude, latitude (e.g. 12.20)
        EW/NS: Northing/Easting
        Format 1: dlon dlat
        Format 2: abs(dlon)EW abs(dlat)NS
        """
        retstr = None
        if(type(format) == int):
            print('Having a format number')
            if(format==1):
                print('Format 1')
                print(self.dlon)
                print(self.lon)
                retstr = "{:3.4f}".format(self.dlon)
                retstr += separator + "{:2.4f}".format(self.dlat)
            elif(format==2):
                print('Format 2')
                retstr = "{:3.4f}".format(abs(self.dlon)) + self.easting
                retstr += separator + "{:2.4f}".format(abs(self.dlat))  + self.northing

        return retstr
    def strp(pstr,format='%dlon %dlat',dec_separator='.'):
        """ Parses a string containing longitude and latitude
        dec_separator: The separator character between the whole and fractional part
        %dlon, %dlat: Degrees (either negative, positive, or with extension %NS %EW)
        %mlon, %mlat: Minutes
        %slon, %slat: Seconds
        %EW, %NS:
        %?:
        %*:

        """
        print(pstr)
        ind_pos = []
        #integer https://stackoverflow.com/questions/8586346/python-regex-for-integer
        #
        if False:
            regex_int = '([-+]?[0-9]+)'
            #regex_int = '[0-9]+'
            #regex_int = 'd+'
        #format += ' ' # A white space in the end, making find easier
        regex_format = format[:]

        # Replace anychar with regex version
        ind_anychar = format.find('%?') # Anychar
        regex_format = regex_format.replace('%?','(.)')

        ind_anychar = format.find('%*') # Anychar
        regex_format = regex_format.replace('%*','(.*)')

        #https://docs.python.org/3/library/re.html#simulating-scanf
        ind_dlon = format.find('%dlon')
        if(ind_dlon > -1):
            print('ind_dlon',ind_dlon)
            regex_dlon = r'(?P<dlon>[-+]?(\d+[.,]?\d+))'
            regex_format = regex_format.replace('%dlon',regex_dlon)

        ind_dlat = format.find('%dlat')
        if(ind_dlat > -1):
            print('ind_dat',ind_dlat)
            regex_dlat = r'(?P<dlat>[-+]?(\d+[.,]?\d+))'
            regex_format = regex_format.replace('%dlat',regex_dlat)

        # Minutes
        ind_mlon = format.find('%mlon')
        if(ind_mlon > -1):
            print('ind_mlon',ind_mlon)
            regex_mlon = r'(?P<mlon>[-+]?(\d+[.,]?\d+))'
            regex_format = regex_format.replace('%mlon',regex_mlon)

        ind_mlat = format.find('%mlat')
        if(ind_mlat > -1):
            print('ind_dat',ind_mlat)
            regex_mlat = r'(?P<mlat>[-+]?(\d+[.,]?\d+))'
            regex_format = regex_format.replace('%mlat',regex_mlat)

        # Seconds
        ind_slon = format.find('%slon')
        if(ind_slon > -1):
            print('ind_slon',ind_slon)
            regex_slon = r'(?P<slon>[-+]?(\d+[.,]?\d+))'
            regex_format = regex_format.replace('%slon',regex_slon)

        ind_slat = format.find('%slat')
        if(ind_slat > -1):
            print('ind_dat',ind_slat)
            regex_slat = r'(?P<slat>[-+]?(\d+[.,]?\d+))'
            regex_format = regex_format.replace('%slat',regex_slat)

        ind_EW = format.find('%EW')
        if(ind_EW > -1):
            print('ind_EW',ind_EW)
            regex_EW = r'(?P<EW>[EW])'
            regex_format = regex_format.replace('%EW',regex_EW)

        ind_NS = format.find('%NS')
        if(ind_NS > -1):
            print('ind_NS',ind_NS)
            regex_NS = r'(?P<NS>[NS])'
            regex_format = regex_format.replace('%NS',regex_NS)

        print('regex_format','"' + regex_format + '"')
        print('A')
        searchObj = re.search(regex_format,pstr)
        print(searchObj)
        print('B')
        searchObj = re.findall(regex_format,pstr)
        print(searchObj)
        print('C')
        searchObj = re.match(regex_format,pstr)
        print('Match',searchObj)
        print('Group',searchObj.group(1))
        print('Group',searchObj.group(2))
        print('Group',searchObj.groupdict())
        parse_dict = searchObj.groupdict()
        # Checking first if we have degrees
        try:
            lat = float(parse_dict['dlat'])
            logger.debug('strp(): Adding degrees (Latitude): ' + str(lat))
        except:
            logger.error('strp(): No Latitude specified, aborting')
            return None

        try:
            lon = float(parse_dict['dlon'])
            logger.debug('strp(): Adding degrees (Longitude): ' + str(lon))
        except:
            logger.error('strp(): No Longitude specified, aborting')
            return None

        # Checking for minutes/seconds.
        try:
            mlon = float(parse_dict['mlon'])
            lon = lon + mlon /60
            logger.debug('strp(): Adding minutes (Longitude): ' + str(mlon))
        except:
            pass

        try:
            slon = float(parse_dict['slon'])
            lon = lon + slon /60/60
            logger.debug('strp(): Adding seconds (Longitude): ' + str(slon))
        except:
            pass

        try:
            mlat = float(parse_dict['mlat'])
            lat = lat + mlat /60
            logger.debug('strp(): Adding minutes (Latitude): ' + str(mlat))
        except:
            pass

        try:
            slat = float(parse_dict['slat'])
            lat = lat + slat /60/60
            logger.debug('strp(): Adding seconds (Latitude): ' + str(slat))
        except:
            pass


        try:
            EW = parse_dict['EW']
            if(EW=='W'):
                lon = -abs(lon)
            else:
                lon = abs(lon)
            logger.debug('strp(): Adding easting: '+ EW)
        except:
            pass


        try:
            NS = parse_dict['NS']
            if(NS=='S'):
                lat = -abs(lat)
            else:
                lat = abs(lat)
            logger.debug('strp(): Adding northing: ' +NS)
        except:
            pass

        return latlon(lon,lat)



    def __add__(self, other):
        """
        """
        [lon,lat] = geod.fwd(self.lon,self.lat,other.azimuth)
        pos = latlon(lon,lat)
        return pos

    def __sub__(self, other):
        """ Subtracting gives the difference between the two points in m on a WGS84 ellipsoid
        """
        azimuth11, azimuth22, distance = geod.inv(self.lon, self.lat, other.lon, other.lat)
        dpos = dlatlon(distance,azimuth12,azimuth21)
        return dpos
