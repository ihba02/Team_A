from sqlalchemy import create_engine, text


def Table_creation():
    engine = create_engine("sqlite:///staging")

# Each statement separately
    create_table_1 = """
    CREATE TABLE IF NOT EXISTS core_dim_asset (
    ASSET_KEY INTEGER PRIMARY KEY AUTOINCREMENT,
    ASSET TEXT,
    CATEGORY TEXT,
    MANUFACTURER TEXT,
    INSTALLDATE DATETIME,
    WARRANTYYEARS INTEGER
    );
    """

    create_table_2 = """
    CREATE TABLE IF NOT EXISTS core_dim_plant (
    PLANT_KEY INTEGER PRIMARY KEY AUTOINCREMENT,
    PLANT_NAME TEXT,
    REGION TEXT,
    MANAGER TEXT,
    ESTABLISHED_YEAR INTEGER
    );
    """

    create_table_3 = """
        CREATE TABLE IF NOT EXISTS core_fact_asset_performance (
    FACT_KEY INTEGER PRIMARY KEY AUTOINCREMENT,
    DATE DATETIME,
    ASSET TEXT,
    REGION TEXT,
    PLANT TEXT,
    TEMPERATURE FLOAT,
    VIBRATION FLOAT,
    HEALTH_SCORE FLOAT,
    FOREIGN KEY (PLANT) REFERENCES core_dim_plant(PLANT_NAME),
    FOREIGN KEY (ASSET) REFERENCES core_dim_asset(ASSET)
    );"""

    create_index_1 = """-- Create indexes to improve query performance
    CREATE INDEX IF NOT EXISTS idx_fact_asset_performance_asset ON core_fact_asset_performance(ASSET);
    """
    create_index_2 = """CREATE INDEX IF NOT EXISTS idx_fact_asset_performance_date ON core_fact_asset_performance(DATE);"""

# Execute each separately
    with engine.connect() as conn:
        for ddl in [create_table_1, create_table_2, create_table_3,create_index_1,create_index_2]:
            conn.execute(text(ddl))
        conn.commit()

Table_creation()