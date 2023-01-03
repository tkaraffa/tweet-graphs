locals {
  meta_columns = [
    {
      "name" : "_id",
      "type" : "STRING",
      "description" : "Unique identifier for this row!"
    },
    {
      "name" : "_created_at",
      "type" : "DATETIME",
      "description" : "The timestamp at which this row was added..."
    },
    {
      "name" : "_filename",
      "type" : "STRING",
      "description" : "The filename from which this row was derived."
    }
  ]
}
