select
    sex,
    round(avg(tip), 2) as avg_tip,
    round(avg(total_bill), 2) as avg_bill,
    count(*) as total_customers
from {{ ref('stg_tips') }}
group by sex