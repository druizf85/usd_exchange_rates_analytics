# %%
import os
import requests
from dotenv import load_dotenv
import pandas as pd
import s3fs
from sqlalchemy import create_engine
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

query = F""" 
SELECT MAX(DATE(time_last_update_utc)) FROM {db_table}
"""
last_update = pd.read_sql(query, engine).iloc[0, 0]
print(f'Last update: {last_update}')

# %%
apy_key = os.getenv('APY_KEY')
url = f'https://v6.exchangerate-api.com/v6/{apy_key}/latest/USD'
response = requests.get(url)
data = response.json()
date_extract = pd.to_datetime(data['time_last_update_utc'])
file_date = date_extract.strftime('%Y-%m-%d')
df = pd.json_normalize(data)

# %%
if date_extract <= last_update:
    print(f'Process Stopped: date_extract ({date_extract}) older or equal to last_update.')
    sys.exit(0)
else:
    print('Initializing loading process')

# %%
# -------------------------------------------------------  RAW OBJECT STORE ---------------------------------------------#

# %%
minio_url = os.getenv('MINIO_BASE_URL')
minio_key = os.getenv('MINIO_KEY')
minio_secret = os.getenv('MINIO_SECRET')

# %%
fs = s3fs.S3FileSystem(key=minio_key, secret=minio_secret, client_kwargs={"endpoint_url": minio_url})
fs.ls("/")

# %%
bucket = 'testdr'
raw_key = f'{bucket}/bronze/{file_date}'
raw_path = f's3://{raw_key}.parquet'
raw_path

# %%
try:
    df.to_parquet(raw_path, filesystem=fs, engine="pyarrow", index=False)
    print(f'File from date {file_date} loaded successfully')
except Exception as e:
    print(f'Error: {e}')

# %%
silver_file = 'fullexchange_rates'
silver_key = f'{bucket}/silver/{silver_file}'
silver_path = f's3://{silver_key}.parquet'

# %%
try:
    df_silver = pd.read_parquet(silver_path, filesystem=fs, engine="pyarrow")
    consolidated_df = pd.concat([df_silver, df], ignore_index=True)
    consolidated_df.to_parquet(silver_path, filesystem=fs, engine='pyarrow', index=False)
    print(f'DataFrame "{silver_file}" successfully loaded, total rows: {len(consolidated_df)}.')
except Exception as e:
    print(f'Error: {e}')


