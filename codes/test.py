import os
import pandas as pd
import json
import xml.etree.ElementTree as ET
from sqlalchemy import create_engine
engine = create_engine('sqlite:///staging')
df = pd.read_sql_table('staging.Plant_hierarchy', con=engine)

print(df)

