import os
import pandas as pd
import json
import xml.etree.ElementTree as ET
from sqlalchemy import create_engine,text,inspect
engine = create_engine('sqlite:///staging')
#df = pd.read_sql_table('staging.Asset_Metadata', con=engine)

#print(df)
#with engine.connect() as conn:
#    conn.execute(text("DROP TABLE IF EXISTS core_fact_asset_performance;"))
#    conn.commit()

query = text("SELECT * FROM core_dim_asset;")

with engine.connect() as conn:
    result = conn.execute(query)
    for row in result:
        print(row)
#engine = create_engine("sqlite:///staging")
#inspector = inspect(engine)
#print("Tables in DB:", inspector.get_table_names())

