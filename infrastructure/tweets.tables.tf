resource "google_bigquery_table" "raw_tweets" {
  dataset_id          = google_bigquery_dataset.tweet-graphs.dataset_id
  table_id            = "raw_tweets"
  deletion_protection = var.deletion_protection

  external_data_configuration {
    autodetect      = false
    max_bad_records = 0
    source_format   = "NEWLINE_DELIMITED_JSON"
    source_uris = [
      "${google_storage_bucket.tweets.url}/*.jsonl"
    ]
    ignore_unknown_values = true
    schema = jsonencode(
      local.raw_tweet_columns
    )


  }
  labels = {}
}

resource "google_bigquery_table" "tweets" {
  dataset_id          = google_bigquery_dataset.tweet-graphs.dataset_id
  table_id            = "tweets"
  deletion_protection = var.deletion_protection

  schema = jsonencode(
    concat(
      local.meta_columns,
      local.raw_tweet_columns
    )
  )

}
