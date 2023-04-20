# Yatube REST API


### Requirements & Compatibility
* Django==3.2.16
* pytest==6.2.4
* pytest-pythonpath==0.7.3
* pytest-django==4.4.0
* djangorestframework==3.12.4
* djangorestframework-simplejwt==4.7.2
* Pillow==9.3.0
* PyJWT==2.1.0
* requests==2.26.0

### Installation:

To copy the project, run the following commands:

```
git clone https://github.com/TatianaBelova333/api_final_yatube.git
```
```
cd api_final_yatube
```

Create and activate a virtual environment:

```
python3 -m venv env
```
```
source env/bin/activate
```

Install the packages according to the configuration file `requirements.txt`:

```
python3 -m pip install --upgrade pip
```
```
pip install -r requirements.txt
```

Execute migrations:
```
python3 manage.py migrate
```

Run the project:

```
python3 manage.py runserver
```

# SOME REST API EXAMPLES
### Get list of Posts

`GET /api/v1/posts/`

```
HTTP/1.1 200 OK
Content-Type: application/json

{
  "count": 123,
  "next": "http://api.example.org/accounts/?offset=400&limit=100",
  "previous": "http://api.example.org/accounts/?offset=200&limit=100",
  "results": [
    {
      "id": 0,
      "author": "string",
      "text": "string",
      "pub_date": "2021-10-14T20:41:29.648Z",
      "image": "string",
      "group": 0
    }
  ]
}
```
### Get a specific Post

`GET /api/v1/posts/{id}/`
```
HTTP/1.1 200 OK
Content-Type: application/json

{
  "id": 0,
  "author": "string",
  "text": "string",
  "pub_date": "2019-08-24T14:15:22Z",
  "image": "string",
  "group": 0
}
```
### Get a non-existent Post
`GET /api/v1/posts/{id}/`
```
HTTP/1.1 404 Not Found
Content-Type: application/json

{
    "detail": "Not found."
}
```
### Create a new Post
```
POST /api/v1/posts/{id}/
Content-Type: application/json
{
  "text": "string",
  "image": "string",
  "group": 0
}
```
```
Content-Type: application/json
HTTP/1.1 201 Created

{
"id": 0,
"author": "string",
"text": "string",
"pub_date": "2019-08-24T14:15:22Z",
"image": "string",
"group": 0
}

```
### Attempt to create a Post by an authorised user

```
HTTP/1.1 401 Unauthorised
{
    "detail": "Authentication credentials were not provided."
}
```
