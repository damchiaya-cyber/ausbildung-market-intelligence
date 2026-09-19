# src/data_pipeline/etl_bibb.py
import pandas as pd
import numpy as np
from sqlalchemy import create_engine
import os

# Uses local SQLite file database (No Docker required)
DB_URI = os.getenv("DATABASE_URL", "sqlite:///ausbildung_db.sqlite")

def fetch_raw_bibb_data() -> pd.DataFrame:
    """
    Simulates / fetches BIBB contract statistical data.
    BIBB datasets record supply, demand, and unplaced numbers by state & trade.
    """
    print("📥 Fetching raw BIBB data...")
    
    states = [
        (1, 'BY', 'Bayern', 'Bavaria', 'München', 'South'),
        (2, 'NW', 'Nordrhein-Westfalen', 'North Rhine-Westphalia', 'Düsseldorf', 'West'),
        (3, 'BE', 'Berlin', 'Berlin', 'Berlin', 'East'),
        (4, 'BW', 'Baden-Württemberg', 'Baden-Württemberg', 'Stuttgart', 'South'),
        (5, 'SN', 'Sachsen', 'Saxony', 'Dresden', 'East'),
    ]
    
    professions = [
        (101, '43122', 'Fachinformatiker Anwendungsentwicklung', 'IT Specialist Software Dev', 'IT & Software'),
        (102, '26312', 'Mechatroniker', 'Mechatronics Technician', 'Industrie'),
        (103, '62102', 'Kaufmann im Einzelhandel', 'Retail Sales Specialist', 'Handel'),
        (104, '31102', 'Elektroniker Energie- und Gebäudetechnik', 'Electrician Energy Tech', 'Handwerk'),
    ]

    records = []
    np.random.seed(42)

    for year in range(2020, 2025):
        for state in states:
            for prof in professions:
                base_supply = np.random.randint(400, 1500)
                demand_modifier = 0.85 if state[1] in ['BY', 'BW'] else 1.15
                base_demand = int(base_supply * demand_modifier)
                
                filled = min(base_supply, base_demand) - np.random.randint(10, 50)
                unfilled = max(0, base_supply - filled)
                unplaced = max(0, base_demand - filled)

                records.append({
                    "year_id": year,
                    "region_id": state[0],
                    "state_code": state[1],
                    "state_name_de": state[2],
                    "state_name_en": state[3],
                    "capital_city": state[4],
                    "macro_region": state[5],
                    "profession_id": prof[0],
                    "kldb_code": prof[1],
                    "profession_name_de": prof[2],
                    "profession_name_en": prof[3],
                    "sector_category": prof[4],
                    "offered_positions": base_supply,
                    "applied_applicants": base_demand,
                    "filled_positions": filled,
                    "unfilled_positions": unfilled,
                    "unplaced_applicants": unplaced
                })

    return pd.DataFrame(records)


def run_etl():
    df = fetch_raw_bibb_data()
    engine = create_engine(DB_URI)

    print(f"⚙️ Populating database using engine: {engine.name}...")

    # Load into SQLite tables
    dim_region = df[['region_id', 'state_code', 'state_name_de', 'state_name_en', 'capital_city', 'macro_region']].drop_duplicates()
    dim_region.to_sql('dim_region', engine, if_exists='replace', index=False)

    dim_profession = df[['profession_id', 'kldb_code', 'profession_name_de', 'profession_name_en', 'sector_category']].drop_duplicates()
    dim_profession.to_sql('dim_profession', engine, if_exists='replace', index=False)

    dim_date = pd.DataFrame({'year_id': df['year_id'].unique(), 'reporting_period': 'Annual'})
    dim_date.to_sql('dim_date', engine, if_exists='replace', index=False)

    fact_table = df[['year_id', 'region_id', 'profession_id', 'offered_positions', 
                     'applied_applicants', 'filled_positions', 'unfilled_positions', 'unplaced_applicants']]
    fact_table.to_sql('fact_ausbildung_market', engine, if_exists='replace', index=False)

    print("✅ ETL Pipeline Completed Successfully! Database created at 'ausbildung_db.sqlite'.")

if __name__ == "__main__":
    run_etl()