{{ config(materialized='table') }}

with daily_totals as (

    select
        day,
        round(sum(tip), 2)        as total_tips,
        round(sum(total_bill), 2) as total_revenue,
        count(*)                  as num_orders
    from {{ ref('stg_tips') }}
    group by day

)

select
    day,
    total_tips,
    total_revenue,
    num_orders,

    rank() over (order by total_tips desc) as tip_rank,
    lag(total_tips) over (order by total_tips desc) as prev_day_tips,
    total_tips - max(total_tips) over () as gap_from_best_day

from daily_totals
order by tip_rank