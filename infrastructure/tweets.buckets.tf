resource "google_storage_bucket" "tweets" {
  name                        = "tweets-raw"
  project                     = var.project
  location                    = var.location
  uniform_bucket_level_access = true
}
