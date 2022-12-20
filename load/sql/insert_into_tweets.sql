
insert into tweets.tweets (
    id,
    created_at,
    filename,
    test, 
    test2
)

select
    generate_uuid() as id,
    current_datetime("UTC") as created_at,
    _file_name as filename,
    test,
    test2
from
    `tweet-graphs-330003`.tweets.raw_tweets
