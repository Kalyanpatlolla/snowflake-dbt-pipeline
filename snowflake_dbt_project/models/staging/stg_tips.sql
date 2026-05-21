select
    "total_bill" as total_bill,
    "tip" as tip,
    "sex" as sex,
    "smoker" as smoker,
    "day" as day,
    "time" as time,
    "size" as size,
    current_timestamp as loaded_at
from {{ source('raw', 'superstore') }}