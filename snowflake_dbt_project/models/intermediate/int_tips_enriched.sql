-- models/intermediate/int_superstore_sales.sql
select
    total_bill,
    tip,
    sex,
    smoker,
    day,
    time,
    size
from {{ ref('stg_tips') }}