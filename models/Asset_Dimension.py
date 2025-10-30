
from sqlalchemy import text,create_engine
import pandas as pd

con = create_engine("sqlite:///Staging")
engine = create_engine("sqlite:///warehouse")



def validate_asset_metadata(con):
    """
    Validate staging_asset_metadata for missing or empty ASSET values.
    Raises ValueError if invalid records are found.
    """
    df = pd.read_sql("SELECT * FROM staging.Asset_Metadata", con=con)

    # Check if ASSET column exists
    if 'ASSET' not in df.columns:
        raise ValueError("Column 'ASSET' not found in staging_asset_metadata")

    # Find missing or empty ASSETs
    invalid_rows = df[df['ASSET'].isnull() | (df['ASSET'].astype(str).str.strip() == '')]

    if not invalid_rows.empty:
        print("Invalid rows found in staging_asset_metadata:")
        print(invalid_rows)
        raise ValueError(f"Found {len(invalid_rows)} record(s) with NULL or blank ASSET values.")
    else:
        print("✅ Validation passed: No NULL or blank ASSET values.")


def load_core_dim_asset(con,engine):
    # Step 1: Validate staging data
    validate_asset_metadata(con)

    # Step 2: Merge (Upsert) data into core_dim_asset
    merge_sql = """
    INSERT INTO core_dim_asset (ASSET, CATEGORY, MANUFACTURER, INSTALLDATE,WARRANTYYEERAS)
    SELECT Asset, Category, Manufacturer, InstallDate, WarrantyYears
    FROM staging.Asset_Metadata
    ON CONFLICT(Asset)
    DO UPDATE SET
        CATEGORY = excluded.Category,
        MANUFACTURER = excluded.Manufacturer,
        INSTALLDATE = excluded.InstallDate,
        WARRANTYYEERAS = excluded.WarrantyYears;
    """
    with engine.connect() as conn:
        conn.execute(text(merge_sql))
        conn.commit()

    print("✅ Merge completed successfully into core_dim_asset.")

# Run both steps
load_core_dim_asset(con,engine)