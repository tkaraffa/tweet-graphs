
insert into tweets.tweets (
    _id,
    _created_at,
    _filename,
    data,
    includes,
    errors,
    meta
)

select
    generate_uuid() as _id,
    current_datetime("UTC") as _created_at,
    _file_name as _filename,
    data,
    includes,
    errors,
    meta
from
    `tweet-graphs-330003`.tweets.raw_tweets
where
    contains_substr(_file_name, :datetime_input)
