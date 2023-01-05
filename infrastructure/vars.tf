variable "project" {
  type      = string
  sensitive = true
}

variable "project_name" {
  type      = string
  sensitive = true
}

variable "location" {
  type      = string
  sensitive = true
}

variable "zone" {
  type      = string
  sensitive = true
}

variable "owner_email" {
  type      = string
  sensitive = true
}

variable "user_email" {
  type      = list(string)
  sensitive = true
}

variable "escape" {
  type      = string
  sensitive = false
}

variable "deletion_protection" {
  type      = bool
  sensitive = false
}
