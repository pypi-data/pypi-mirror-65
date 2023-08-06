# -*- coding: UTF-8 -*-
from datetime import datetime
from StringIO import StringIO
import pandas as pd
from utils import get_station


class PlcProfilesParser(object):

    def __init__(self, profiles_file, cnc_name):
        """Creates a dictionary with data from PLC800"""
        # Support for files or raw string
        if isinstance(profiles_file, str):
            profiles_file = StringIO(profiles_file)
        if not hasattr(profiles_file, 'read'):
            raise TypeError('Must be file pointer or basestring')
        # read file
        self.cnc_name = cnc_name
        self.df_profiles = pd.read_csv(profiles_file, header=None, sep=';',
                                       names=['name', 'timestamp', 'flag', 'ai', 'ae', 'r1', 'r2', 'r3', 'r4'],
                                       dtype={'name': str, 'timestamp': str, 'ai': float, 'ae': float,
                                              'r1': float, 'r2': float, 'r3': float, 'r4': float})

    @property
    def profiles(self):
        df = self.df_profiles.drop(columns=['flag'])
        df['cnc_name'] = self.cnc_name
        df['magn'] = 1
        df['ai'] = df['ai'].apply(lambda x: int(x * 1000))
        df['ae'] = df['ae'].apply(lambda x: int(x * 1000))
        df['r1'] = df['r1'].apply(lambda x: int(x * 1000))
        df['r2'] = df['r2'].apply(lambda x: int(x * 1000))
        df['r3'] = df['r3'].apply(lambda x: int(x * 1000))
        df['r4'] = df['r4'].apply(lambda x: int(x * 1000))
        df['timestamp'] = df['timestamp'].apply(
            lambda x: datetime.strptime(x, '%d/%m/%Y %H:%M:%S').strftime('%Y-%m-%d %H:%M:%S'))
        df['season'] = df['timestamp'].apply(lambda x: get_station(x))
        return df.T.to_dict().values()
