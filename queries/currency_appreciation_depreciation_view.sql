CREATE OR REPLACE VIEW currency_appreciation_depreciation_view AS

WITH diffs AS (
    SELECT
        exchange_rate,
        CAST(time_last_update_utc AS date),
        values,
        values - LAG(values) OVER (PARTITION BY CAST(time_last_update_utc AS date) ORDER BY CAST(time_last_update_utc AS date) DESC) AS daily_delta
    FROM "Exchange_Rates_Silver_Table"
	)
	
--SELECT * FROM diffs -- STILL DON'T GET GET THIS ONE

SELECT
    exchange_rate,
    AVG(daily_delta) AS avg_daily_change_usd,
    SUM(daily_delta) AS total_change_usd,
    COUNT(*) AS periods
FROM diffs
--WHERE exchange_rate IN ('COP')
GROUP BY exchange_rate
ORDER BY avg_daily_change_usd DESC



--Cómo interpretarlo:
--avg_daily_change_usd > 0 → moneda se deprecia (USD más caro en esa moneda)
--avg_daily_change_usd < 0 → moneda se aprecia
