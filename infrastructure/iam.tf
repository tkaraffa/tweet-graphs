resource "google_project_iam_policy" "project" {
  project     = var.project
  policy_data = data.google_iam_policy.admin.policy_data
}

data "google_iam_policy" "admin" {
  binding {
    role = "roles/owner"

    members = [
      var.user_email
    ]
  }
  binding {
    role = "roles/editor"
    members = [
      "serviceAccount:${google_service_account.tweet-graphs.email}",
    ]
  }
}
