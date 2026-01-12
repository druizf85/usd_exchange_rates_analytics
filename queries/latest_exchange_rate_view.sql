CREATE OR REPLACE VIEW latest_exchange_rate_view AS

WITH date_ranking AS (

    SELECT exchange_rate, 
			values, 
			time_last_update_utc, 
			ROW_NUMBER() OVER(PARTITION BY exchange_rate ORDER BY CAST(time_last_update_utc AS date) DESC) AS rn
    FROM "Exchange_Rates_Silver_Table"
	WHERE values <> 0
	AND values IS NOT NULL
	AND exchange_rate IS NOT NULL
	
	),

last_update_values AS (

	SELECT exchange_rate, 
			values,
			time_last_update_utc
	FROM date_ranking
		WHERE rn = 1
	)

SELECT m.continent,
		m.country,
		lv.exchange_rate, 
		lv.values,
		lv.time_last_update_utc 
FROM last_update_values lv
JOIN currency_metadata m ON lv.exchange_rate = m.currency_code