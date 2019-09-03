from census import Census
import pandas as pd
import json
from sqlalchemy import create_engine
with open('credentials.json') as creds:
    credentials = json.load(creds)
api_key = credentials['api_key']   # CGR's API key
pg_username = credentials['pg_username']
pg_password = credentials['pg_password']

engine = create_engine(f"postgresql://{pg_username}:{pg_password}@localhost/wsosfairhousing")
c = Census(api_key)

block_data = pd.DataFrame()
tract_data = pd.DataFrame()
county_fips = {'Lucas':'39095','Wood':'39173'}
for county in county_fips:
    temp_block = pd.DataFrame(c.sf1.get(
        ('NAME','GEO_ID','P001001'),
        geo={'for':'block:*',
        'in': f'state:39 county:{county_fips[county][2:]}'},
        year=2010
    ))
    print(temp_block)
    block_data = block_data.append(temp_block,sort=False)
    
    temp_ct_df = pd.DataFrame(c.acs5.state_county_tract(acs_dict,county_fips[county][:2], county_fips[county][2:],'*', year = 2017))
    tract_data = tract_data.append(temp_ct_df,sort=False)
block_data.to_sql('block_2010',engine, if_exists='replace')
tract_data.to_sql('tract_2017',engine, if_exists='replace')
