resource "google_bigquery_table" "raw-tweets" {
  dataset_id = google_bigquery_dataset.tweet-graphs.dataset_id
  table_id   = "raw_tweets"
  schema     = <<EOF
  [
    {
        "name": "source",
        "type": "string",
        "mode": "NULLABLE",
        "description": "The source of this data."
    },
    {
        "name": "filename",
        "type": "string",
        "description": "The filename from which this data was loaded"
    },
    {
        "name": "json_text",
        "type": "string",
        "comment": "raw json data"
    }
  ]
 EOF
}

resource "google_bigquery_table" "tweets" {
  dataset_id = google_bigquery_dataset.tweet-graphs.dataset_id
  table_id   = "tweets"
  schema     = <<EOF
  [
    {
        "name": "id",
        "type": "integer",
        "mode": "REQUIRED",
        "description": "Artificially added ID."
    }
  ]
  EOF
}
