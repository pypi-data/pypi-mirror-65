'''
Python class to make easier to use Konker REST API
'''
import json
#from pprint import pprint
import os
import sys
import urllib.parse
from oauthlib.oauth2 import BackendApplicationClient, MissingTokenError
from requests_oauthlib import OAuth2Session


# data handling libraries
import arrow
#import numpy as np
from pandas.io.json import json_normalize
import pandas as pd

class Client:
    '''
    Base class to handle client connection to KONKER API and abstract
    the use of handling OAUTH HTTP requests
    '''
    base_api = 'https://api.prod.konkerlabs.net'
    application = 'default'
    token = None
    client = None
    oauth = None
    username = None

    def login(self, cid='', username='', password=''):
        ''' use this function to connect to the platform using predefined credentials
            on "credentials.json" file or given explicity username and password
            '''

        if cid != '':
            # lookup for credential file
            if os.path.isfile('credentials.json'):
                with open('credentials.json') as file:
                    credentials = json.load(file)
            else:
                print('"credentials.json" found. You must define the '+\
                    'username and password by yourself')
                credentials = {}

            try:
                username = credentials[cid]['username']
                password = credentials[cid]['password']
                print('connected')
            except KeyError:
                raise KeyError('"{}" not found on credentials file'.format(cid))
        else:
            # must have informed username and password ....
            if (len(username) == 0 or len(password) == 0):
                print('invalid username or password')
                return None, None


        # try to login on the platform ...

        self.client = BackendApplicationClient(client_id=username)
        self.oauth = OAuth2Session(client=self.client)
        try:
            self.token = self.oauth.fetch_token(token_url='{}/v1/oauth/token'.format(self.base_api),
                                                client_id=username,
                                                client_secret=password)

            # log the username
            self.username = username
        except MissingTokenError:
            # print(error)
            print('Invalid credentials')

        return self.oauth, self.token

    def set_application(self, _name):
        '''
        define the application to be used this point forward
        '''
        self.application = _name

    def check_connection(self):
        '''
        raise an exception if current class is not connected to the server
        '''
        if not self.oauth:
            raise Exception('not connected. login first')

    def get_all_devices_for_application(self, application, size=None):
        '''
        returns a list of devices for a specified application
        '''
        self.check_connection()
        #print('application = {}'.format(application))
        #print('API = {}'.format(self.base_api))
        url = "{}/v1/{}/devices/".format(self.base_api, application)
        if size:
            url = "{}&size={}".format(url, size)
        result = self.oauth.get(url).json()
        #print(result)
        if result['code'] == 200:
            devices = result['result']
        else:
            print('ERROR')
            print(result)
            devices = None
        return devices

    def get_all_devices(self, size=None):
        '''
        retrieve a list of all devices connected to this application, visible to your user
        '''
        return self.get_all_devices_for_application(self.application, size)

    def get_locations_for_application(self, application):
        '''
        retrieve a list of all locations for refered application
        '''
        self.check_connection()
        result = self.oauth.get("{}/v1/{}/locations/".format(self.base_api, application)).json()
        if result['code'] == 200:
            devices = result['result']
        else:
            print('ERROR')
            print(result)
            devices = None
        return devices

    def get_locations(self):
        '''
        return a list of locations for current defined application
        '''
        return self.get_locations_for_application(self.application)

    def get_device_credentials(self, guid):
        '''
        get credentials for a device
        '''
        self.check_connection()
        info = self.oauth.get("{}/v1/{}/deviceCredentials/{}".format(
            self.base_api, self.application, guid)).json()
        return info

    def get_applications(self):
        '''
        retrieve a list of all applications
        '''
        self.check_connection()
        result = self.oauth.get("{}/v1/applications/".format(
            self.base_api)).json()
        print(result)
        if 'error' in result and result['error'] == 'unauthorized':
            applications = None
        else:
            applications = result['result']
        return applications



    def get_all_devices_for_location(self, store, size=None):
        '''
        retrieve a list of all devices for a given STORE.
        give just the store # as a parameter, for instance:
        app.getAllDevicesForStore(1234)
        '''
        self.check_connection()
        url = "{}/v1/{}/devices/?locationName={}".format(
            self.base_api, self.application, store)
        if size:
            url = "{}&size={}".format(url, size)
        devices = self.oauth.get(url).json()['result']
        return devices

    def read_data(self, guid, channel=None, delta=-10, start_date=None):
        '''
        read data from a given device for a specific period of time (default 10 days)
        and a starting date (if not informed return last X days)

        the final returning is a Pandas Dataframe that can be used for further processing
        '''
        self.check_connection()
        stats_dfa = []
        interval = 2 if abs(delta) > 1 else 1

        if start_date:
            dt_start = start_date
        else:
            dt_start = arrow.utcnow().to('America/Sao_Paulo').floor('day')

        dt_start = dt_start.shift(days=delta)
        sys.stdout.write('Reading channel({}.{}) from {} '.format(guid, channel, dt_start))

        for _ in range(0, int((delta*-1) / interval)+1):
            dt_end = dt_start.shift(days=interval)

            query = 'device:{}{}timestamp:>{} timestamp:<{}'.format(
                guid,
                ' channel:{} '.format(channel) if channel else ' ',
                dt_start.isoformat(),
                dt_end.isoformat()
            )
            query = urllib.parse.quote(query)

            #print('')
            #print('q={}'.format(q))
            #print('application = {}'.format(self.application))

            statsx = self.oauth.get(
                "{}/v1/{}/incomingEvents?q={}&sort=newest&limit=10000".format(
                    self.base_api,
                    self.application,
                    query
                )
            )

            stats = statsx.json()['result']
            if (stats and len(stats) > 0):
                sys.stdout.write('.')
                #stats_dfx = json_normalize(stats).set_index('timestamp')
                stats_dfx = stats
                #stats_dfx = stats_dfx[3:]
                #stats_dfa.append(stats_dfx)
                stats_dfa.extend(stats_dfx)
            else:
                sys.stdout.write('X')
                #print('ERROR = {}'.format(statsx.json()))
            dt_start = dt_end
        print('\nDone')
        #return pd.concat(stats_dfa) if len(stats_dfa) > 0 else pd.DataFrame()
        return stats_dfa


    @staticmethod
    def look_for(name, devices):
        '''
        look for a specific device in a given list of devices
        can inform a partial name to return ...
        return all elements that matches
        '''
        data = []
        for device in devices:
            if name in device['name']:
                data.append(device)
        return data
