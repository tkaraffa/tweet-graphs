resource "google_service_account" "tweet-graphs" {
  account_id   = "tweet-graphs"
  display_name = "tweet-graphs"
  project      = var.project
  description  = "Service account for Tweet-graphs project."
}

resource "time_rotating" "key_rotation" {
  rotation_minutes = 5
}

resource "google_service_account_key" "tweet-graphs-key" {
  service_account_id = google_service_account.tweet-graphs.id

  keepers = {
    rotation_time = time_rotating.key_rotation.rotation_minutes
  }
}

data "google_service_account_key" "tweet-graphs-key" {
  name            = google_service_account_key.tweet-graphs-key.name
  public_key_type = "TYPE_X509_PEM_FILE"
}

resource "local_file" "tweets-account" {
  content  = base64decode(google_service_account_key.tweet-graphs-key.private_key)
  filename = "../serviceaccount.json"
}
