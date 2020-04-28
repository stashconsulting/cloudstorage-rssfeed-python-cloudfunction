import requests

file_name = "test.jpeg"

files = {file_name: open(file_name, "rb")}
data = {
  "title": 'test form data',
  "description": 'test form data',
  "creation_date": '12/12/2019 10:20 PM',
}

r = requests.post(
    "https://cloudrunsrv-cvrukhkgjq-uc.a.run.app/insertData",
    data=data,
    files=files,
)


print(r.status_code)
