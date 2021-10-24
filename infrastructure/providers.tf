provider "google" {
  project = var.project
  region  = var.location
  zone    = var.zone
  scopes  = ["cloud-platform"]
}
