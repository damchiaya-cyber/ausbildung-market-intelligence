CREATE TABLE IF NOT EXISTS dim_region (
    region_id INT PRIMARY KEY,
    state_code VARCHAR(2) NOT NULL UNIQUE,
    state_name_de VARCHAR(50),
    state_name_en VARCHAR(50),
    capital_city VARCHAR(50),
    macro_region VARCHAR(20) CHECK (macro_region IN ('North', 'South', 'East', 'West'))
);

CREATE TABLE IF NOT EXISTS dim_profession (
    profession_id INT PRIMARY KEY,
    kldb_code VARCHAR(10) NOT NULL UNIQUE,
    profession_name_de VARCHAR(150) NOT NULL,
    profession_name_en VARCHAR(150) NOT NULL,
    sector_category VARCHAR(50) NOT NULL
);

CREATE TABLE IF NOT EXISTS dim_date (
    year_id INT PRIMARY KEY,
    reporting_period VARCHAR(10) DEFAULT 'annual'
);

CREATE TABLE IF NOT EXISTS fact_ausbildung_market (
    fact_id SERIAL PRIMARY KEY,
    year_id INT NOT NULL REFERENCES dim_date(year_id),
    region_id INT NOT NULL REFERENCES dim_region(region_id),
    profession_id INT NOT NULL REFERENCES dim_profession(profession_id),

    offered_posistions INT NOT NULL CHECK (offered_position >= 0),
    applied_applicants INT NOT NULL CHECK (applied_applicants >= 0),
    filled_applicants INT NOT NULL CHECK (filled_positions >=0),
    unfilled_positions INT NOT NULL CHECK (unfilled_positions >=0),
    unplaced_applicants INT NOT NULL CHECK (inplaced_applicants >=0)

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT unique_market_entry UNIQUE (year_id, region_id, profession_id)
);
