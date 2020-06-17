# cloud-storage-rssfeed-python

This infraestructure create an application that generates a RSS Feed file each time that a file is uploaded into a bucket, there’s another function that shows the file generated in JSON.

If you are interested in seeing the blog regarding this project I’m glad to share it! in [Medium](https://medium.com/stash-media/troubleshooting-terraform-on-a-serverless-world-b4c2a6019f54). 
I’m going to cover the problems I had during the implementation and the decision I made to fix those.

## Before you begin

### Google SDK

It’s important to make sure that Cloud SDK is authorized to access your data and services.

```
gcloud auth login
```

On the new browser tab that opens by running the command, choose an account that has the Editor or Owner role in the Google Cloud project.

### Configuring the Google Provider

If you don’t specify the credentials in the file we can supply the key to Terraform using the environment variable setting the value to the location of the file. If you are in Windows use set instead of export.

```
export GOOGLE_CLOUD_KEYFILE_JSON={{path}}
```

If you have any problems with this step check this [Issue](https://github.com/hashicorp/terraform/issues/8493)

## Getting started

### Usage

We initialize a working directory containing Terraform configuration files.

```
terraform init
```

Run the following command that scans the current directory for the `.tf` files and applies the changes appropriately.

```
terraform apply
```

## Built With 🛠️

* [Docker 19.03.8](https://docs.docker.com/engine/release-notes/) -  To create the image Kongdbless.

## Contributing 🖇️

There are a few ways to contribute to the `RSS Feed generator` repo. Please read [CONTRIBUTING.md](https://github.com/stashconsulting/cloudstorage-rssfeed-python-cloudfunction/blob/master/CONTRIBUTING.md) for additional information.

## Versioning. 📌

For the versions available, see the [tags on this repository](https://github.com/stashconsulting/cloudstorage-rssfeed-python-cloudfunction/tags).

## Authors ✒️

* **Genesis Alvarez** - *Initial work* - [stashconsulting](https://github.com/stashconsulting)

* **Shailyn Ortiz** - *Maintainer* - [stashconsulting](https://github.com/stashconsulting)

## License 📄

RSS Feed generator is licensed under the Server Side Public License (SSPL). 
Please read the [LICENSE](https://github.com/stashconsulting/cloudstorage-rssfeed-python-cloudfunction/blob/master/LICENSE) file.

## Acknowledgments
This project was born when [*Shailyn Ortiz*](https://github.com/sjortiz) wanted to generate a RSS Feed for his podcasts called **Not another AWS Podcasts** where he and his partner shows the latest cloud news.

Please tell others about this project. 📢

---
⌨️ with ❤️ by [Alvarez](https://github.com/UsernameAlvarez)
