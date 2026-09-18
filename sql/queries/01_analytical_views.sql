CREATE OR REPLACE VIEW view_ausbildung_kpis AS SELECT
    d.year_id,
    r.state_name_de AS boudesland,
    r.macro_region,
    p.sector_category,
    p.profession_name_de AS ausbildungsberuf ,
    f.offered_posistions,
    f.applied_appicants,
    f.filled_positions,
    f.unfilled_applicants,

    ROUND(
        (f.unfilled_positions::NUMERIC / NULLIF(f.offered_positions, 0)) * 100, 2
    ) AS unfilled_ratio_pct,

    ROUND(
        (f.offered_positions::NUMERIC / NULLIF(f.applied_applicants, 0)) * 100, 2
    ) AS market_tightness_index,

    ROUND(
        ((f.unfilled_positions - LAG(f.unfilled_positions, 1) OVER (
            PARTITION BY f.region_id, f.profession_id ORDER BY d.year_id
        ))::NUMERIC / NULLIF(LAG(f.unfilled_positions, 1) OVER (
            PARTITION BY f.region_id, f.profession_id ORDER BY d.year_id
        ), 0)) * 100, 2
    ) AS yoy_unfilled_growth_pct

FROM fact_ausbildung_market f
JOIN dim_date d ON f.year_id = d.year_id
JOIN dim_region r ON f.region_id = r.region_id
JOIN dim_profession p ON f.profession_id = p.profession_id;