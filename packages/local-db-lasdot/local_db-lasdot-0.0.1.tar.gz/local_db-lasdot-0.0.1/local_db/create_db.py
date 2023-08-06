import datetime
import gridfs
import json
import numpy as np
import os
import pandas as pd
from pymongo import MongoClient
import sys, traceback
from tqdm import tqdm
import time


class CreateDb():
    """
    Create database and populate with json data
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
        print(self.db)
    
    @staticmethod
    def encode_charset(val):
        '''
        @param val: some instance of np.int64
        @return: int value if int64 else returns value back
        '''
        if isinstance(val, np.int64):
            val = int(val)
        return val

    @staticmethod
    def parse_date(datetime_str):
        '''
        removes unwanted syntax in time object
        @param datatime_str: time string
        @return string
        '''
        datetime_arr = datetime_str.split(' ')
        time_component = datetime_arr[1]
        time_component = time_component.split('-')
        time_component = time_component[0]
        return datetime_arr[0] + ' ' + time_component


    @staticmethod    
    def parse_meta_data(metadata, dataid_list, time_collection, file_path):
        '''
        Writes a json object represent the metadata for all the cities 'newyork', 'austin', 'california'
        for a specific time interval
        [metadata_field] -> [] || [metadata_field] -> ['dataid': {value of metadata_field}]
        @param metadata: pandas dataframe for metadata
        @param dataid_list: list of dataid's in dataframes for specific time collection
        @param time_collection: name of time collection in database -- ['time_(1_min|15_min)']
        @param file_path: root directory for metadata file
        @return: None
        '''
        if not os.path.isdir(file_path):
            print(file_path + ' is not a valid directory')
            return

        metadata_obj = {}

        # get column types for metadata
        metadata_type = metadata.dtypes
        
        # get building types and initialize multidict object
        building_types_list = list(set(metadata['building_type']))
        for building_type in building_types_list:
            metadata_obj[building_type] = []

        for col in metadata.columns.to_list():
            if col != 'dataid' and col != 'building_type':
                metadata_obj[col] = []
        
        # slice metadata
        metadata_slice = metadata.loc[dataid_list, :].reset_index()
        dataid_col = metadata_slice.columns.get_loc('dataid')

        for row in tqdm(range(metadata_slice.shape[0]), desc='Creating metafile', ncols=100):
            dataid = CreateDb.encode_charset(metadata_slice.iloc[row, dataid_col])
            for col in range(metadata_slice.shape[1]):
                value = metadata_slice.iloc[row, col]
                # set building type
                if metadata_slice.columns[col] == 'building_type':
                    metadata_obj[value].append(dataid)
                col_name = metadata_slice.columns[col]

                if col_name != 'dataid' and col_name != 'building_type':
                    if metadata_type[col_name] == np.float64 and not pd.isnull(value):
                        if value != 0.0:
                            if col_name == 'house_construction_year':
                                value = int(value)
                            metadata_obj[col_name].append({ 
                                str(dataid): CreateDb.encode_charset(value)
                                })
                    else:
                        if not pd.isnull(value):
                            metadata_obj[col_name].append(dataid)
                            
        with open(os.path.join(file_path, time_collection + '_meta.json'), 'w') as write_file:
            json.dump(metadata_obj, write_file)

    @staticmethod
    def create_multidict(df, city_collection):
        '''
        creates a multidictionary object that is the json schema of the file to be 
        inserted into tha database --> [city_collection][dataid]
        @param df: pandas dataframe for pecan street dataset
        @city_collection: name of city collection in database -- 'newyork', 'austin', 'california'
        @return: multidictionary object
        '''
        data_dict = {city_collection: {}}
        dataid_col = df.columns.get_loc('dataid')

        for row_i in tqdm(range(df.shape[0]), desc='Creating database schema', ncols=100):
            dataid = str(CreateDb.encode_charset(df.iloc[row_i, dataid_col]))

            if dataid not in data_dict[city_collection]:
                data_dict[city_collection][dataid] = []

        return data_dict

    @staticmethod    
    def serialize_data(df, time_col_name, time_collection, city_collection, file_path):
        '''
        Creates a serialized json file with the data set by the predefined schema in 
        create_multidict()
        @param df: pandas dataframe for pecan street dataset
        @param time_col_name: time column name in dataframe
        @param time_collection: name of time collection in database -- ['time_(1_min|15_min)']
        @param city_collection: name of city collection in database -- 'newyork', 'austin', 'california'
        @param file_path: root file
        '''

        if not os.path.isdir(file_path):
            print('no such directory ' + file_path)
            return

        dataid_col = df.columns.get_loc('dataid')
        time_col = df.columns.get_loc(time_col_name)

        # Create multidict obj
        data = CreateDb.create_multidict(df, city_collection)

        for row_i in tqdm(range(df.shape[0]), desc='Creating serialized json data', ncols=100):
            data_dict = {}

            time_str = CreateDb.parse_date(df.iloc[row_i, time_col])
            time_obj = datetime.datetime.strptime(time_str, '%Y-%m-%d %H:%M:%S')

            dataid = str(CreateDb.encode_charset(df.iloc[row_i, dataid_col]))

            for col_i in range(df.shape[1]):
                if col_i != dataid_col and col_i != time_col:
                    if not pd.isna(df.iloc[row_i, col_i]):
                        data_dict[df.columns[col_i]] = CreateDb.encode_charset(df.iloc[row_i, col_i])
                if col_i == time_col:
                    data_dict["time"] = str(time_obj.date()) + ' ' + str(time_obj.time())

            data[city_collection][dataid].append(data_dict)

        with open(os.path.join(file_path, time_collection + '_' + city_collection + '.json'), 'w') as write_file:
            json.dump(data, write_file)


    def single_insert(self, time_collection, **kwargs):
        '''
        Insert a single file into the database: metadata or file
        @param time_collection: name of time collection in database -- ['time_(1_min|15_min)']
        @param city_collection: name of city collection in database -- 'newyork', 'austin', 'california'
        @param Keyword Arguments: 
                                  data_file_dir: root file directories
                                  meta_file_dir: root directory for metadata file
        '''
        acceptable_keys = ['data_file_dir', 'meta_file_dir', 'city_collection']

        if len(kwargs.keys()) == 0:
            raise KeyError('expected either [data_file_dir] or [meta_file_dir] got None')

        if not all(key in acceptable_keys for key in kwargs.keys()):
            raise KeyError('argument keys must be either [data_file_dir] or [meta_file_dir]')

        if 'city_collection' in kwargs.keys() and 'data_file_dir' not in kwargs.keys():
            raise KeyError('[city_collection] provided, while [data_file_dir] is missing')

        if 'data_file_dir' in kwargs.keys() and 'city_collection' not in kwargs.keys():
            raise KeyError('[data_file_dir] provided, while [city_collection] is missing')


        try:
            fs = gridfs.GridFS(self.db, collection=time_collection)

            if 'data_file_dir' in kwargs.keys():
                city_collection = kwargs.get('city_collection')
                if os.path.isdir(kwargs['data_file_dir']):
                    with open(os.path.join(kwargs['data_file_dir'], time_collection + '_' + city_collection + '.json'), 'rb') as data:
                        fs.put(data, filename=city_collection)
                    print(city_collection + ' inserted into database')
            if 'meta_file_dir' in kwargs.keys():
                if os.path.isdir(kwargs['meta_file_dir']):
                    with open(os.path.join(kwargs['meta_file_dir'], time_collection + '_meta.json'), 'rb') as data:
                        fs.put(data, filename='metadata')
                    print('metadata inserted into database')
        except:
            traceback.print_exc(file=sys.stdout)
            print('Could not insert file into database')

    def batch_insert(self, file_dir):
        '''
        Insert all json files in the directory provided
        @param file_dir: root file directory
        '''

        if os.path.isdir(file_dir):
            files = [file for file in os.listdir(file_dir) if os.path.isfile(os.path.join(file_dir, file))]
            for file in tqdm(files, desc='Inserting all files', ncols=100):
                if file.split('.')[-1] == 'json':
                    time_collection = file.split('_', 3)[:3]
                    city_collection = file.split('_')[-1].split('.')[0]
                    time_collection = '_'.join(time_collection)
                    if city_collection == 'meta':
                        self.single_insert(time_collection=time_collection, meta_file_dir=file_dir)
                    else:
                        self.single_insert(
                            time_collection=time_collection, 
                            city_collection=city_collection, 
                            data_file_dir=file_dir)
        else:
            print('no such directory ' + file_dir ) 



