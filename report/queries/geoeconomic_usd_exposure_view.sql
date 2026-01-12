CREATE OR REPLACE VIEW geoeconomic_usd_exposure_view AS

SELECT m.continent,
		m.country,
	    er.exchange_rate,
	    AVG(er.values) AS avg_usd_rate,
	    STDDEV(er.values) AS volatility_usd,
	    (MAX(er.values) - MIN(er.values)) AS usd_range_movement
FROM "Exchange_Rates_Silver_Table" er
JOIN currency_metadata m ON er.exchange_rate = m.currency_code
GROUP BY m.continent, m.country, er.exchange_rate
ORDER BY m.continent, m.country