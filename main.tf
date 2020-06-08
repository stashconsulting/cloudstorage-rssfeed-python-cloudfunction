locals {
  region  = "us-central1"
  zone    = "us-central1-c"
}

# Specify the GCP Provider
provider "google" {
  project     = var.project
  region      = local.region
  zone        = local.zone
}

# zip up our source code
data "archive_file" "insert_data" {
 type        = "zip"
 output_path = "${path.module}/insert_data.zip"

 source {
    content  = file("${path.module}/source_code/insert_data.py")
    filename = "main.py"
  }

  source {
    content  = file("${path.module}/source_code/requirements.txt")
    filename = "requirements.txt"
  }
}

data "archive_file" "generate_rssfeed" {
 type        = "zip"
 output_path = "${path.module}/generate_rssfeed.zip"

 source {
    content  = file("${path.module}/source_code/generate_rssfeed.py")
    filename = "main.py"
  }

  source {
    content  = file("${path.module}/source_code/requirements.txt")
    filename = "requirements.txt"
  }
}

data "archive_file" "convert_xml_to_json" {
 type        = "zip"
 output_path = "${path.module}/convert_xml_to_json.zip"

 source {
    content  = file("${path.module}/source_code/convert_xml_to_json.py")
    filename = "main.py"
  }

  source {
    content  = file("${path.module}/source_code/requirements.txt")
    filename = "requirements.txt"
  }
}

# cloud storage service
resource "google_storage_bucket" "source_code_file" {
  name    = "source_code_file"
  location  = local.region
  force_destroy = true
}

resource "google_storage_bucket_access_control" "public_rule" {
  bucket = google_storage_bucket.bucket_file.name
  role   = "READER"
  entity = "allUsers"
}

resource "google_storage_bucket" "bucket_file" {
  name    = "bucket_file_tf"
  location  = local.region
  force_destroy = true
}

# place the zip-ed code in the bucket
resource "google_storage_bucket_object" "insert_data" {
 name   = "insert_data.zip"
 bucket = google_storage_bucket.source_code_file.name
 source = "${path.module}/insert_data.zip"
}

resource "google_storage_bucket_object" "generate_rssfeed" {
 name   = "generate_rssfeed.zip"
 bucket = google_storage_bucket.source_code_file.name
 source = "${path.module}/generate_rssfeed.zip"
}

resource "google_storage_bucket_object" "convert_xml_to_json" {
 name   = "convert_xml_to_json.zip"
 bucket = google_storage_bucket.source_code_file.name
 source = "${path.module}/convert_xml_to_json.zip"
}


# cloud functions service
resource "google_cloudfunctions_function" "function_insert_data" {
  name        = "function_insert_data"
  description = "My function"
  runtime     = "python37"

  available_memory_mb   = 128
  source_archive_bucket = google_storage_bucket.source_code_file.name
  source_archive_object = google_storage_bucket_object.insert_data.name
  trigger_http          = true
  entry_point           = "main"
  environment_variables = {
    collection = "image_file_details"
    DESTINATION_BUCKET = "bucket_file_tf"
  }
}

resource "google_cloudfunctions_function" "function_generate_rssfeed" {
  name        = "function_generate_rssfeed"
  description = "My function"
  runtime     = "python37"

  available_memory_mb   = 128
  source_archive_bucket = google_storage_bucket.source_code_file.name
  source_archive_object = google_storage_bucket_object.generate_rssfeed.name
  entry_point           = "main"
  event_trigger {
    event_type = "providers/cloud.firestore/eventTypes/document.write"
    resource = "image_file_details/{document}"
  }
  environment_variables = {
    collection = "image_file_details"
    DESTINATION_BUCKET = "bucket_file_tf"
  }
}

resource "google_cloudfunctions_function" "function_convert_xml_to_json" {
  name        = "function_convert_xml_to_json"
  description = "My function"
  runtime     = "python37"

  available_memory_mb   = 128
  source_archive_bucket = google_storage_bucket.source_code_file.name
  source_archive_object = google_storage_bucket_object.convert_xml_to_json.name
  trigger_http          = true
  entry_point           = "convert"
  environment_variables = {
    DESTINATION_BUCKET = "bucket_file_tf"
  }
}

resource "google_cloudfunctions_function_iam_binding" "insert_data" {
  cloud_function = google_cloudfunctions_function.function_insert_data.name
  role = "roles/cloudfunctions.invoker"
  members = [
    "allUsers",
  ]
}

resource "google_cloudfunctions_function_iam_binding" "generate_rssfeed" {
  cloud_function = google_cloudfunctions_function.function_generate_rssfeed.name
  role = "roles/cloudfunctions.invoker"
  members = [
    "allUsers",
  ]
}

resource "google_cloudfunctions_function_iam_binding" "convert_xml_to_json" {
  cloud_function = google_cloudfunctions_function.function_convert_xml_to_json.name
  role = "roles/cloudfunctions.invoker"
  members = [
    "allUsers",
  ]
}

# cloud run service
resource "google_cloud_run_service" "cloudrunsrv" {
  name     = "kongapi"
  location = local.region

  template {
    spec {
      containers {
        image = var.image_id
      }
    }
  }

  traffic {
    percent         = 100
    latest_revision = true
  }
  depends_on = [
    null_resource.building_docker_image,
  ]
}

# local-exec for building the docker image and push it from terraform
resource "null_resource" "building_docker_image" {
  triggers = {
    image_id = var.image_id
  }
  provisioner "local-exec" {
    command = <<EOF
      docker build -t kongdbless:latest .
      docker tag kongdbless:latest ${var.image_id}
      docker push ${var.image_id}
    EOF
  }
}
