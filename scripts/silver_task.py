# %%
from dotenv import load_dotenv
import pandas as pd
import os
from sqlalchemy import create_engine
import s3fs
import sys

# %%
load_dotenv()
folder_path = os.getcwd()

# %%
def engine_postgre(user, password, host, port, database):
    engine = create_engine(f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{database}")
    return engine

# %%
postgres_user = os.getenv('POSTGRES_USER')
postgres_password = os.getenv('POSTGRES_PASSWORD')
postgres_host = os.getenv('POSTGRES_HOST')
postgres_host_local = os.getenv('POSTGRES_HOST_LOCAL')
postgres_port = os.getenv('POSTGRES_PORT')
postgres_port_local = os.getenv('POSTGRES_PORT_LOCAL')
postgres_database = os.getenv('POSTGRES_DB')

# %%
engine = engine_postgre(postgres_user, postgres_password, postgres_host, postgres_port, postgres_database)

# %%
db_table = '"Exchange_Rates_Silver_Table"'

# %%
minio_url = os.getenv('MINIO_BASE_URL')
minio_key = os.getenv('MINIO_KEY')
minio_secret = os.getenv('MINIO_SECRET')

# %%
fs = s3fs.S3FileSystem(key=minio_key, secret=minio_secret, client_kwargs={"endpoint_url": minio_url})
fs.ls("/")

# %%
bucket = 'testdr'
silver_file = 'fullexchange_rates'
silver_key = f'{bucket}/silver/{silver_file}'
silver_path = f's3://{silver_key}.parquet'

# %%
query = f""" 
SELECT MAX(DATE(time_last_update_utc)) FROM {db_table}
"""
last_update = pd.read_sql(query, engine).iloc[0, 0]

# %%
try:
    df_silver = pd.read_parquet(silver_path, filesystem=fs, engine="pyarrow")
    df_silver['time_last_update_utc_compare'] = pd.to_datetime(df_silver['time_last_update_utc']).dt.date
    df_to_load = df_silver[df_silver['time_last_update_utc_compare'] > last_update]
except Exception as e:
    print(f'Error: {e}')

# %%
if len(df_to_load) >0 :
    print(f'Including {len(df_to_load)} new rows in DB.')
else:
    print('No new data to load')
    sys.exit(0)

# %%
df_to_load = df_to_load.drop(columns=('time_last_update_utc_compare'))

# %%
df_to_load = df_to_load.melt(id_vars=['result', 'documentation', 'terms_of_use', 'time_last_update_unix', 'time_last_update_utc', 'time_next_update_unix', 'time_next_update_utc', 'base_code'],  value_vars=None, var_name='exchange_rate', value_name='values')
df_to_load['exchange_rate'] = df_to_load['exchange_rate'].str.replace('conversion_rates.', '')

# %%
try:
    df_to_load.to_sql('Exchange_Rates_Silver_Table', engine, if_exists='append', index=False)
    print(f'New data in {db_table}')
except Exception as e:
    print({e})

# %%
last_update_silver = pd.read_sql(query, engine).iloc[0, 0]
print(f'Last update: {last_update_silver}')


