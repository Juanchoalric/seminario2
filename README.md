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

example (local url) with postman: http://127.0.0.1:4032/entry?user_id=12345678

example (heroku url) with postman: http://viralert2.herokuapp.com/entry?user_id=12345678

response: 

[
 {"store_id": "ad0f32ac14b148d68ce3626e856baaf2", "date": "17-Oct-2021", "time": "21:16:35", 
 "store_name": "Casa"},
 {"store_id": "ad0f32ac14b148d68ce3626e856baaf2", "date": "17-Oct-2021", "time": "22:07:42", 
 "store_name": "Casa"}
]