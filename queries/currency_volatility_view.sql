CREATE OR REPLACE VIEW currency_volatility_view AS

WITH oct_25_vol AS (
	SELECT exchange_rate,
		    COALESCE(STDDEV(values), 0) AS volatility,
		    AVG(values)    AS avg_value,
		    MAX(values)    AS max_value,
		    MIN(values)    AS min_value
	FROM "Exchange_Rates_Silver_Table"
		WHERE EXTRACT(MONTH FROM CAST(time_last_update_utc AS date)) = 10
		AND EXTRACT(YEAR FROM CAST(time_last_update_utc AS date)) = 2025
	GROUP BY exchange_rate
	),

nov_25_vol AS (
	SELECT exchange_rate,
		    COALESCE(STDDEV(values), 0) AS volatility,
		    AVG(values)    AS avg_value,
		    MAX(values)    AS max_value,
		    MIN(values)    AS min_value
	FROM "Exchange_Rates_Silver_Table"
		WHERE EXTRACT(MONTH FROM CAST(time_last_update_utc AS date)) = 11
		AND EXTRACT(YEAR FROM CAST(time_last_update_utc AS date)) = 2025
	GROUP BY exchange_rate
	),

dec_25_vol AS (
	SELECT exchange_rate,
		    COALESCE(STDDEV(values), 0) AS volatility,
		    AVG(values)    AS avg_value,
		    MAX(values)    AS max_value,
		    MIN(values)    AS min_value
	FROM "Exchange_Rates_Silver_Table"
		WHERE EXTRACT(MONTH FROM CAST(time_last_update_utc AS date)) = 12
		AND EXTRACT(YEAR FROM CAST(time_last_update_utc AS date)) = 2025
	GROUP BY exchange_rate
	),

all_2025_vol AS(
	SELECT exchange_rate,
		    COALESCE(STDDEV(values), 0) AS volatility,
		    AVG(values)    AS avg_value,
		    MAX(values)    AS max_value,
		    MIN(values)    AS min_value
	FROM "Exchange_Rates_Silver_Table"
		WHERE EXTRACT(YEAR FROM CAST(time_last_update_utc AS date)) = 2025
	GROUP BY exchange_rate
	)

SELECT m.continent,
		m.country,
		y_25.exchange_rate as exchange_rate,
		o_25.min_value AS min_value_october, 
		o_25.max_value AS max_value_october,
		o_25.avg_value AS avg_value_october,
		o_25.volatility AS volatility_value_october,
		n_25.min_value AS min_value_november, 
		n_25.max_value AS max_value_november,
		n_25.avg_value AS avg_value_november,
		n_25.volatility AS volatility_value_november,
		d_25.min_value AS min_value_december, 
		d_25.max_value AS max_value_december,
		d_25.avg_value AS avg_value_december,
		d_25.volatility AS volatility_value_december,
		y_25.min_value AS min_value_2025_all, 
		y_25.max_value AS max_value_2025_all,
		y_25.avg_value AS avg_value_2025_all,
		y_25.volatility AS volatility_2025_all

FROM all_2025_vol y_25
JOIN oct_25_vol o_25 ON o_25.exchange_rate = y_25.exchange_rate
JOIN nov_25_vol n_25 ON n_25.exchange_rate = y_25.exchange_rate
JOIN dec_25_vol d_25 ON d_25.exchange_rate = y_25.exchange_rate
JOIN currency_metadata m ON y_25.exchange_rate = m.currency_code

ORDER BY volatility_2025_all DESC

