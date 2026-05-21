-- Custom test: tip should never exceed total_bill
-- This test FAILS if ANY row is returned
-- (i.e., if any row has a tip greater than the bill — which would be weird)

select
    total_bill,
    tip,
    sex,
    day
from {{ ref('stg_tips') }}
where tip > total_bill