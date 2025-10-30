import os
import pandas as pd
import json
import xml.etree.ElementTree as ET
from sqlalchemy import create_engine,text
engine = create_engine('sqlite:///staging')
df = pd.read_sql_table('staging.Asset_Metadata', con=engine)

print(df)
#with engine.connect() as conn:
#    conn.execute(text("DROP TABLE IF EXISTS core_fact_asset_performance;"))
#    conn.commit()

