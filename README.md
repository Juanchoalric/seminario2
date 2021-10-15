# seminario2

## POST

### /register/user

{
 "document": "2323454",
 "name": "jose",
 "surname": "pepe",
 "email": "pepe@gmail.com",
 "password": "loquesea"
}

### /register/local

{
 "name": "jose2",
 "email": "pepe2@gmail.com",
 "password": "loquesea"
}

{
 "name": "GeneralStore",
 "email": "generalstore@gmail.com",
 "password": "loquesea"
}

### /login

#### usuario
{
 "email": "pepe@gmail.com",
 "password": "loquesea"
}

#### local
{
 "email": "pepe2@gmail.com",
 "password": "loquesea"
}

{
 "email": "generalstore@gmail.com",
 "password": "loquesea"
}

### /entry (POST)

{
 "user_name": jose,
 "store_name": "GeneralStore"
}

### /entry (GET)

example (local url) with postman: http://127.0.0.1:4032/entry?store_name=GeneralStore
example (heroku url) with postman: http://viralert2.herokuapp.com/entry?store_name=GeneralStore

response: 

{
    "_id": "028171f5896c4aca9c067e363b186870",
    "date": "14-Oct-2021",
    "store_name": "GeneralStore",
    "time": "19:52:07",
    "user_name": "jose"
}