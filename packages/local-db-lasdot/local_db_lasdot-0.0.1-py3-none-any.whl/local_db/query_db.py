import datetime
import gridfs
import json
import math
import os
import pandas as pd 
from pymongo import MongoClient
import sys, traceback
from tqdm import tqdm


class QueryDb():
    """
    Query local database with AND and OR db operations
    """
    def __init__(self, db_name="pecan_street"):

        def test_db_conn():
            '''
            Test mongodb server connection
            '''
            try:
                client = MongoClient('mongodb://localhost:27017/')
                client.server_info()
                print('now connected to mongodb at port 27017')
            except:
                print('Cannot connect to mongodb server')
                exit(-1)

        test_db_conn()
    
        def init_db_client(db_name):
            '''
            @param db_name: name of database, default [pecan_street]
            @return: database client
            '''
            try:
                client = MongoClient('mongodb://localhost:27017/')
                db = client[db_name]
                return db
            except:
                print('Cannot connect to mongodb server')
                exit(-1)

        self.db = init_db_client(db_name)
        self.meta_file='metadata'
        self.query_tolerance = 5  # query tolerance for 1 second time intervals

        self.building_types = ['Single-Family Home', 'Mobile Home', 'Town Home', 'Apartment', 'Sales']

        # Kewyord Arguments and their corresponding tol parameters
        self.tol_dict = {
            'total_amount_of_pv': 'total_pv_tol',
            'house_construction_year': 'year_tol',
            'total_square_footage' : 'total_sqft_tol',
            'first_floor_square_footage' : 'first_floor_sqft_tol',
            'second_floor_square_footage' : 'second_floor_sqft_tol',
            'third_floor_square_footage' : 'third_floor_sqft_tol',
            'half_floor_square_footage' : 'half_floor_sqft_tol',
            'lower_level_square_footage' : 'lower_level_sqft_tol'
            }
        
        self.file_params = ['air1', 'air2', 'air3', 'airwindowunit1',
                            'aquarium1', 'bathroom1', 'bathroom2', 'bedroom1', 'bedroom2',
                            'bedroom3', 'bedroom4', 'bedroom5', 'battery1', 'car1', 'car2',
                            'circpump1', 'clotheswasher1', 'clotheswasher_dryg1', 'diningroom1',
                            'diningroom2', 'dishwasher1', 'disposal1', 'drye1', 'dryg1', 'freezer1',
                            'furnace1', 'furnace2', 'garage1', 'garage2', 'grid', 'heater1',
                            'heater2', 'heater3', 'housefan1', 'icemaker1', 'jacuzzi1', 'kitchen1',
                            'kitchen2', 'kitchenapp1', 'kitchenapp2', 'lights_plugs1',
                            'lights_plugs2', 'lights_plugs3', 'lights_plugs4', 'lights_plugs5',
                            'lights_plugs6', 'livingroom1', 'livingroom2', 'microwave1', 'office1',
                            'outsidelights_plugs1', 'outsidelights_plugs2', 'oven1', 'oven2',
                            'pool1', 'pool2', 'poollight1', 'poolpump1', 'pump1', 'range1',
                            'refrigerator1', 'refrigerator2', 'security1', 'sewerpump1', 'shed1',
                            'solar', 'solar2', 'sprinkler1', 'sumppump1', 'utilityroom1',
                            'venthood1', 'waterheater1', 'waterheater2', 'wellpump1', 'winecooler1',
                            'leg1v', 'leg2v']
        print(self.db)

    def read_file(self, time_collection, city_collection):
        '''
        Read file from time collection in database
        @param time_collection: name of time collection in database -- ['time_(1_min|15_min)']
        @city_collection: name of city collection in database -- 'newyork', 'austin', 'california'
        @return: file from database
        '''
        try:
            fs = gridfs.GridFS(self.db, collection=time_collection)
            file = fs.get_last_version(filename=city_collection)
            return json.loads(file.read())
        except:
            print('file not found in database')

    def read_meta(self, time_collection):
        '''
        Read metadata file from time collection in database
        @param time_collection: name of time collection in database -- ['time_(1_min|15_min)']
        @return: metadata file from database
        '''
        try:
            fs = gridfs.GridFS(self.db, collection=time_collection)
            file = fs.get_last_version(filename=self.meta_file)
            return json.loads(file.read())
        except:
            print('metadata not in database')

    def check_tol_param(self, query_param, args):
        '''
        Check if dictionary query parameter has corresponding tol parameter
        @param query_param: list of query parameters
        @return: list item containing [True] || [False, string: missing tol parameter]
        '''
        for query in query_param:
            if isinstance(query, dict):
                query_key = [key for key in query.keys()][0]
                if self.tol_dict[query_key] not in args.keys():
                    return [False, self.tol_dict[query_key]]
        return [True]

    @staticmethod
    def stringify_list(multi_list):
        new_list = []
        for list_item in multi_list:
            temp_list = []
            for item in list_item:
                temp_list.append(str(item))
            new_list.append(temp_list)
        return new_list

    def get_dataids(self, query_param, metadata, args):
        '''
        Filters dataids based on the type of db_op and query parameters
        @param query_param: list of query parameters
        @param metadata: metadata for a specific time collection
        @param args: Keyword Arguments
        @return: list of dataids
        '''
        dataid_list = [metadata[query] for query in query_param if isinstance(query, str) and query != 'nest']

        if 'nest' in query_param:
            nests = []
            for val in metadata['number_of_nests']:
                for key in val.keys():
                    nests.append(key)
            dataid_list.append(nests)

        for query in query_param:
            if isinstance(query, dict):
                dataid = []
                query_key = [key for key in query.keys()][0]
                for values in metadata[query_key]:
                    for meta_key, meta_val in values.items():
                        if math.fabs(meta_val  - query[query_key]) <= args[self.tol_dict[query_key]]:
                            dataid.append(meta_key)
                dataid_list.append(dataid)

        if len(dataid_list) > 1:
            dataid_list = QueryDb.stringify_list(dataid_list)
            if args['db_op'] == 'AND':
                dataid = dataid_list[0]
                for i in range(1, len(dataid_list), 1):
                    dataid = set(dataid).intersection(set(dataid_list[i]))
                dataid_list = list(dataid)
            else:
                dataid = dataid_list[0]
                for i in range(1, len(dataid_list), 1):
                    dataid = set(dataid).union(set(dataid_list[i]))
                dataid_list = list(dataid)
            return dataid_list
        return dataid_list[0]

    @staticmethod
    def get_datetime_obj(timestr):
        return datetime.datetime.strptime(timestr, '%Y-%m-%d %H:%M:%S')

    @staticmethod
    def filter_time(df, from_, to_):
        datetime.datetime.strptime(from_, '%Y-%m-%d')
        datetime.datetime.strptime(to_, '%Y-%m-%d')
        start = from_
        end = to_
        mask = (df['time'] > start) & (df['time'] <= end)
        return df.loc[mask]

    @staticmethod
    def filter_by(df, **kwargs):
        '''
        Filter dataframe by city, dataid, time
        @param df: dataframe returned from query 
        @param Keyword Arguments:
                                 city (list, string): ['newyork', 'austin', 'california'] || 'newyork'
                                 dataid (list, string): ['5679', '5989'] || '5679'
                                 from_ (string): datetime string '%Y-%m-%d'
                                 to_ (string): datetime string '%Y-&m-&d'
        @return: filtered dataframe or empty list
        '''
        if 'from_' in kwargs and 'to_' not in kwargs:
            raise KeyError('[to_] argument is missing')
        if 'to_' in kwargs and 'from_' not in kwargs:
            raise KeyError('[from_] argument is missing')

        if 'city' in kwargs:
            if isinstance(kwargs.get('city'), list):
                df = df.loc[df['city'].isin(kwargs.get('city')), :]
            else:
                df = df.loc[df['city'] == kwargs.get('city'), :]

        if 'dataid' in kwargs:
            if isinstance(kwargs.get('dataid'), list):
                df = df.loc[df['dataid'].isin(kwargs.get('dataid')), :]
            else:
                df = df.loc[df['dataid'] == kwargs.get('dataid'), :]
        
        if 'from_' in kwargs:
            df = QueryDb.filter_time(df, kwargs.get('from_'), kwargs.get('to_'))

        if df.shape[0] == 0:
            return []
        return df

    def query_df(self, query_param, time_collection, **kwargs):
        '''
        @param query_param: list of query parameters
        @param time_collection: name of time collection in database -- ['time_(1_min|15_min)']
        @return: dataframe that matches query description
        @param Keyword Arguments:
                                  db_op (string): 'AND' || 'OR',
                                  year_tol (number): house_construction_year + tol,
                                  total_pv_tol (number): total_amount_pv + tol,
                                  total_sqft_tol (number): total_square_foot + tol,
                                  first_floor_sqft_tol (number): first_floor_square_footage + tol,
                                  second_floor_sqft_tol (number): second_floor_square_footage + tol
                                  third_floor_sqft_tol (number): third_floor_square_footage + tol
                                  half_floor_sqft_tol (number): half_floor_square_footage + tol,
                                  lower_level_sqft_tol (number): lower_level_square_footage + tol
        @return: dataframe or empty list
        '''
        assert len(query_param) > 0, 'must have at least one query item'

        if not isinstance(query_param, list):
            raise TypeError('query_param arguments should be type list')

        if len(query_param) == 1 and isinstance(query_param[0], dict):
            raise ValueError('at least one non-dictionary metadata parameter must be included in query')

        if len(query_param) > 1:
            count = 0
            for query in query_param:
                if isinstance(query, str) and query not in self.building_types:
                    count += 1
            if count == 0:
                raise ValueError('at least one non-dictionary metadata parameter must be included in query')

        if 'city' not in kwargs.keys():
            raise KeyError('[city] missing from arguments')

        if not isinstance(kwargs['city'], list):
            raise TypeError('[city] argument must be of type list')

        if len(query_param) > 1 and 'db_op' not in kwargs.keys():
            raise KeyError('multiple query parameters needs [dp_op]=[AND, OR]')

        for query in query_param:
            if not isinstance(query, str) and not isinstance(query, dict):
                raise TypeError('arguments to query_param must be of type string or dictionary')

        if 'pv' in query_param:
            raise ValueError('[pv] should be either [solar] or [solar2] or both')

        if len(query_param) == 1 and query_param[0] in self.building_types:
            raise ValueError('bulding type cannot be the only query parameter')

        #check for tol parameter in query
        tol_check = self.check_tol_param(query_param, kwargs)
        if not tol_check[0]:
            raise KeyError(tol_check[1] + ' is missing from Keyword Arguments')

        data_obj = []

        metadata = self.read_meta(time_collection)

        # return empty list if no value found for single query
        if len(query_param) == 1:
            if isinstance(query_param[0], dict):
                for key in query_param[0].keys():
                    if len(metadata[key]) == 0:
                        return data_obj
            else:
                if len(metadata[query_param[0]]) == 0:
                    return data_obj
        
        dataid_list = self.get_dataids(query_param, metadata, kwargs)

        cities = []

        cities = kwargs.get('city')

        if kwargs.get('city')[0] == 'all':
            cities = ['newyork', 'california', 'austin']

        for city in tqdm(cities, desc='fetching data from local server', ncols=100):
            data_file = self.read_file(time_collection, city)
            if not any(str(dataid) in data_file[city] for dataid in dataid_list):
                continue
            else:
                for dataid in dataid_list:
                    dataid = str(dataid)
                    if dataid in data_file[city].keys():
                        data_values = data_file[city][dataid]
                        for data_value in data_values:
                            value = {}
                            value['dataid'] = dataid
                            value['time'] = QueryDb.get_datetime_obj(data_value.get('time'))
                            value['city'] = city

                            for query in query_param:
                                if isinstance(query, str):
                                    if query in self.file_params:
                                        value[query] = data_value.get(query)
                                if query == 'nest':
                                    value['air1'] = data_value.get('air1')
                            data_obj.append(value)

        if len(data_obj) != 0:
            data_obj = pd.DataFrame(data_obj)
            print(data_obj.info(verbose=False, memory_usage='deep'))   

        return data_obj, dataid_list


        

        
        
        
            
        

