locals {
  meta_columns = [
    {
      "name" : "id",
      "type" : "STRING",
      "description" : "Unique identifier for this row!"
    },
    {
      "name" : "created_at",
      "type" : "DATETIME",
      "description" : "The timestamp at which this row was added..."
    },
    {
      "name" : "filename",
      "type" : "STRING",
      "description" : "The filename from which this row was derived."
    }
  ]
}
