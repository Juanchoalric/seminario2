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
 "user_id": "2323454",
 "store_id": "6409cecd413d495796d7fe47fb6d4591"  
}

### /entry (GET)

example (local url) with postman: http://127.0.0.1:4032/entry?store_id=6409cecd413d495796d7fe47fb6d4591

example (heroku url) with postman: http://viralert2.herokuapp.com/entry?store_id=6409cecd413d495796d7fe47fb6d4591

response: 

{
    "_id": "106257b6b86c491f9038f97e73d1e441",
    "date": "17-Oct-2021",
    "store_id": "6409cecd413d495796d7fe47fb6d4591",
    "time": "11:33:58",
    "user_id": "2323454"
}