# Local Database

## Description: 
Popluate and query local mongo server with 
energy api data
<hr>

# Populate Database Section
## Sample Usage

### Batch insertion:
~~~~
create_db = CreateDb(db_name='example_db')
create_db.batch_insert('folder_path')
~~~~

### Single insert:
~~~~
create = CreateDb(db_name='example_db')
create.single_insert(time_collection='time_(1_sec|1_min|15_min)', data_file_dir='data folder path', meta_file_dir='metadata folder path')
~~~~

# Query Database Section
## Sample Usage

### Query with filter
~~~
query = QueryDb(db_name='example_db')
query_param = ['nest', 'grid', 'solar', 'clotheswasher1', 'dishwasher1']
data, id_list = query.query_df(query_param, 'time_15_min', db_op='OR', city=['all'])
try:
    data = QueryDb.filter_by(data, dataid='6139', city='austin')
except Exception as e:
    print(e)
~~~

### Query with dictionary parameter
~~~
query = QueryDb(db_name='example_db')
query_param = ['air1', 'nest', {'first_floor_square_footage': 2148}]

data, id_list = query.query_df(
    query_param,
    time_collection='time_15_min',
    db_op='AND',
    city=['all']
    first_floor_sqft_tol=0
)
~~~

### Test scripts
Must have test json files to implement this.
<br>
<b>note: </b> commands must be implemented from command line ./local_db directory

~~~
python -m unittest tester.TestCreateDbClass.test_db_server

python -m unittest tester.TestCreateDbClass.test_batch_insert

python -m unittest tester.TestCreateDbClass.test_query_error_check

python -m unittest tester.TestCreateDbClass.test_query_empty

python -m unittest tester.TestCreateDbClass.test_query_db_op
~~~



