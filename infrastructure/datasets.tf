resource "google_bigquery_dataset" "tweet-graphs" {
  dataset_id                  = "tweets"
  project                     = var.project
  friendly_name               = "tweets"
  description                 = "Tweets in raw and transformed formats"
  location                    = var.location
  default_table_expiration_ms = 36000000

  labels = {
    env = "default"
  }
}
