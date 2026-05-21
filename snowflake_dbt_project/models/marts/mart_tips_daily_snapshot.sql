{{
    config(
        materialized='incremental',
        unique_key=['snapshot_date', 'day']
    )
}}

select
    cast(loaded_at as date)   as snapshot_date,
    day,
    count(*)                  as num_orders,
    round(sum(tip), 2)        as total_tips,
    round(avg(tip), 2)        as avg_tip,
    round(sum(total_bill), 2) as total_revenue

from {{ ref('stg_tips') }}

{% if is_incremental() %}

    -- This block only runs on incremental runs (not first run)
    -- Only process rows newer than what's already in the table
    where loaded_at > (select max(snapshot_date) from {{ this }})

{% endif %}

group by cast(loaded_at as date), day