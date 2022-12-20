locals {
  meta_columns = <<EOF
    {
      "name": "id",
      "type": "STRING",
      "comment": "Unique identifier for this row."
    },
    {
      "name": "created_at",
      "type": "TIMESTAMP",
      "comment": "The timestamp at which this row was added."
    },
    {
      "name": "filename",
      "type": "STRING",
      "comment": "The filename from which this row was derived."
    }
  EOF
}
