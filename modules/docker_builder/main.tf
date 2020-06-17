# local-exec for building the docker image and push it from terraform
resource "null_resource" "building_docker_image" {
  triggers = {
    image_id = var.image_id
  }
  provisioner "local-exec" {
    command = <<EOF
      docker build -t ${var.image_id} .
      docker push ${var.image_id}
    EOF
  }
}