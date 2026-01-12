CREATE OR REPLACE VIEW continent_usd_strength_view AS

SELECT
    m.continent,
    AVG(er.values) AS avg_usd_exchange_rate,
    STDDEV(er.values) AS continent_volatility_usd,
    COUNT(DISTINCT er.exchange_rate) AS currency_count
FROM "Exchange_Rates_Silver_Table" er
JOIN currency_metadata m ON er.exchange_rate = m.currency_code
GROUP BY m.continent
ORDER BY avg_usd_exchange_rate ASC