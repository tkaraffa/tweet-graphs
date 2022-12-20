locals {
  tweet_columns = <<EOF
    {
      "name": "test",
      "type": "STRING",
      "comment": "test data"
    },
    {
      "name": "test2",
      "type": "STRING",
      "comment": "test data"
    }
  EOF
}

resource "google_bigquery_table" "raw_tweets" {
  dataset_id = google_bigquery_dataset.tweet-graphs.dataset_id
  table_id   = "raw_tweets"

  external_data_configuration {
    autodetect    = true
    source_format = "NEWLINE_DELIMITED_JSON"
    source_uris = [
      "${google_storage_bucket.tweets.url}/*.jsonl"
    ]
    ignore_unknown_values = true
    schema                = <<EOF
    [
      ${join(",", [local.tweet_columns])}
    ]
   EOF
  }
}

resource "google_bigquery_table" "tweets" {
  dataset_id = google_bigquery_dataset.tweet-graphs.dataset_id
  table_id   = "tweets"
  schema     = <<EOF
  [
    ${join(",", [local.meta_columns, local.tweet_columns])}
  ]
 EOF
}
