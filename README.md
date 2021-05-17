# PythonChallenge
Jobsity Challenge - Argenis Aroche 

# Requirements
- Docker
- Docker compose

# How to run?
- docker-compose up
- Go to http://localhost:5000 and log in it with any of the follow users:
```json
[
  { "username": "Argenis", "password": "abcd1234" },
  { "username": "Aldair", "password": "abcd1234" }
]
```

- Create a user
```bash
curl --header "Content-Type: application/json" --request POST --data '{"username":"user1","password":"abcd"}' http://localhost:5000/newuser
```