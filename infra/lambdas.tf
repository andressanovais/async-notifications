data "archive_file" "zip_lambda_connection_state_store" {
  output_path = "${path.module}/lambda_zip/lambda-connection-state-store.zip"
  source_dir  = "../${path.module}/connection-state-store/src"
  excludes    = ["__pycache__"]
  type        = "zip"
}

