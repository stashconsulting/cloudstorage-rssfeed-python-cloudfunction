import requests

file_name = "test.jpeg"

files = {file_name: open(file_name, "rb")}
data = {
  "title": 'test form data',
  "description": 'test form data',
  "creation_date": '12/12/2020',
}

r = requests.post(
    "https://getproperties-cvrukhkgjq-uc.a.run.app/insertData",
    data=data,
    files=files,
)


print(r.status_code)
