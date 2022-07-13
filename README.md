# Blog_Web_App_REST

# API Endpoints

### **1. Register Users [POST]** 
**endpoint:** http://127.0.0.1:8000/api/v1/users/ 

**Authorization:** AllowAny

**Request Body:** 
```
{
    "email": "khair.ahammed0868@outlook.com", 
    "name": "khair", 
    "password": "khair123", 
    "password2": "khair123" 
}
```

**Sample Response:**  
```
{
    "message": "OTP has been sent to your email. Please check your mail"
}
```

### **2. Token Generate/ Login Credential [POST]**
**Endpoint:** http://127.0.0.1:8000/api/v1/token/ 

**Authorization:** AllowAny

**Request Body:**

```
{
    "email": "khairahmad@gmail.com",
    "password": "khair2255"
}
```
**Sample Response:**
```
{
    "token": {
        "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTY1Nzc5MTgxMSwiaWF0IjoxNjU3NzA1NDExLCJqdGkiOiJiMGZjOWU0OTM4ZjY0OTIxYTRiZGUwYTdjY2Q1YWI2ZiIsInVzZXJfaWQiOjMzfQ.loDlrNXEETMPT9ikzycfsKFkCQrFzQv7VBwH9TVANNA",
        "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjU3NzkxODExLCJpYXQiOjE2NTc3MDU0MTEsImp0aSI6IjE5NGEwYjFkNzM1YTQ2NTY5ZDgyNjljZDI4NTcxOWVmIiwidXNlcl9pZCI6MzN9.2n6aqPROMNKqZMxoZzid5enbFdIm0Yx97-0Rv1GGX-0"
    },
    "message": "Login Success"
}
```

### **3. Token Refresh [POST]**
**Endpoint:** http://127.0.0.1:8000/api/v1/token/refresh/ 

**Authorization:** AllowAny

**Request Body:**

```
{
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTY1Nzc5MTgxMSwiaWF0IjoxNjU3NzA1NDExLCJqdGkiOiJiMGZjOWU0OTM4ZjY0OTIxYTRiZGUwYTdjY2Q1YWI2ZiIsInVzZXJfaWQiOjMzfQ.loDlrNXEETMPT9ikzycfsKFkCQrFzQv7VBwH9TVANNA" 
}
```
**Sample Response**
```
{
    "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjU3NzkyMDgyLCJpYXQiOjE2NTc3MDU0MTEsImp0aSI6IjQwYmM1OTAyMmYzMzQ1Zjg4MDM4MDExODA0ODdlMWFkIiwidXNlcl9pZCI6MzN9.gDE07ugnTGzQ-f2RW0TvYjKJ5k-8XFWuz4pbAsW1DZA"
}
```


### **4. Account verify [POST]**
**Endpoint:** http://127.0.0.1:8000/api/v1/account_active/<EncodedEmail\>/

**Authorization:** AllowAny

**Request Body:**

```
{
    "otp" : 435343
}
```
**Sample Response:**

```
{
    "message": "Account Created Successfully"
}
```
**instructions:** The endpoint link will be found on Email 

### **5. View User List [GET]**

**Endpoint:** http://127.0.0.1:8000/api/v1/users/

**Authorization:** Admin or Stuff

**Request Body:**
```

```
**Sample Response:**
```
[
    {
        "id": 47,
        "name": "khair",
        "email": "khair.ahammed088@outlook.com"
    },
    {
        "id": 4,
        "name": "Hasan",
        "email": "hasan3@gmail.com"
    },
    {
        "id": 1,
        "name": "Mizan",
        "email": "mizan2@gmail.com"
    },
    {
        "id": 44,
        "name": "khair",
        "email": "khai.ahammed07@outlook.com"
    }
]
```
**Instructions:**  Have to provde the authorization header [Access Token]


### **6. Update User Info [PUT]**

**Endpoint:** http://127.0.0.1:8000/api/v1/users/<user id\>/ 

**Authorization:** Exact Authenticated User or Admin

**Request Body:**
```
{
    "name":"Khair Ahammed"
}
```
**Sample Response:**

```
{
    "name": "Khair Ahammed",
    "email": "khai.ahammed07@outlook.com"
}
```
**Instructions:**  Have to provde the authorization header [Access Token]


### **7. Partial Update User Info [PATCH]**
**Endpoint:** http://127.0.0.1:8000/api/v1/users/<user id\>/ 

**Authorization:** Exact Authenticated User or Admin

**Request Body:**
```
{
    "name":"Khair Ahammed"
}
```
**Sample Response:**

```
{
    "name": "Khair Ahammed",
    "email": "khai.ahammed07@outlook.com"
}
```
**Instructions:**  Have to provde the authorization header [Access Token]

### **7. Delete User [DELETE]**
**Endpoint:** http://127.0.0.1:8000/api/v1/users/<user id\>/ 

**Authorization:** Exact Authenticated User or Admin

**Request Body:**
```

```
**Sample Response:**

```
{
    "message": "User has been deleted!"
}
```
**Instructions:**  Have to provde the authorization header [Access Token]


### **8. Password Reset Mail [POST]**
**Endpoint:** http://127.0.0.1:8000/api/v1/password-reset/

**Authorization:** AllowAny

**Request Body:**
```
{
    "email":"khair.ahammed07@outlook.com"
}
```
**Sample Response:**

```
{
    "message": "Password Reset link has been send. Please check your Email"
}
```

### **9. Password Reset Verify Mail [POST]**
**Endpoint:** http://127.0.0.1:8000/api/v1/account_active_reset/<Encoded Mail\>/

**Authorization:** AllowAny

**Request Body:**

```
{
    "otp": 302417
}
```
**Sample Response:**

```
{
    "message": "Reset Password by going to this link: http://localhost:3000/api/v1/user/reset/a2hhaXIuYWhhbW1lZDUyQG91dGxvb2suY29t/302417"
}
```
**instructions:** The endpoint link will be found on Email 

### **10. Reset Password [POST]**
**Endpoint:** http://127.0.0.1:8000/api/v1/account_active_reset/<Encoded Mail\>/<otp\>/

**Authorization:** AllowAny

**Request Body:**

```
{
    "password": "khair456",
    "password2": "khair456"
}

```
**Sample Response:**

```
{
    "msg": "Password Reset Successfully"
}
```


### **11. Post List [GET]**
**Endpoint:** http://127.0.0.1:8000/api/v1/blogs/

**Authorization:** AllowAny

**Request Body:**

```

```
**Sample Response:**

```
{
    "count": 5,
    "next": "http://127.0.0.1:8000/api/v1/blogs/?page=2",
    "previous": null,
    "results": [
        {
            "id": 5,
            "title": "Blog 3",
            "description": "This is my 3rd Blog",
            "status": "draft",
            "created": "2022-07-06T07:11:40.860273Z",
            "modified": "2022-07-06T07:11:40.860273Z",
            "created_by": 4
        },
        {
            "id": 7,
            "title": "Blog 4",
            "description": "This is my 4th Blog",
            "status": "draft",
            "created": "2022-07-06T07:27:20.937126Z",
            "modified": "2022-07-06T07:27:20.937126Z",
            "created_by": 3
        }
    ]
}
```
**Instructions:** Searching and Filering are Available. Also pagination is implemented.  

### **12. Post Detail View [GET]**
**Endpoint:** http://127.0.0.1:8000/api/v1/blogs/<Post ID\>/

**Authorization:** AllowAny

**Request Body:**

```

```
**Sample Response:**

```
{
    "id": 2,
    "title": "Demo",
    "description": "Demo Demo Demo",
    "status": "published",
    "created": "2022-07-06T05:34:59.275908Z",
    "modified": "2022-07-06T10:08:31.054270Z",
    "created_by": 28
}
```

### **13. Create Blog Post [POST]**
**Endpoint:** http://127.0.0.1:8000/api/v1/blogs/

**Authorization:** Authenticated User

**Request Body:**

```
{
    "title": "Rest API V2",
    "description": "Django Rest FrameWork",
    "status": "published"
}
```
**Sample Response:**

```
{
    "message": "Post has been published!"
}
```
**Instructions:** Authorization header should be included




### **14. Update Blog Post [PUT]**
**Endpoint:**  http://127.0.0.1:8000/api/v1/blogs/<Post ID\>/

**Authorization:** Author of the Post or Admin

**Request Body:**

```
{
    "title": "Rest API V2",
    "description": "Django Rest FrameWork",
    "status": "published"
}
```
**Sample Response:**

```
{
    "message": "Post has been published!"
}
```
**Instructions:** Authorization header should be included


### **15. Partial Update Blog Post [PUT]**
**Endpoint:**  http://127.0.0.1:8000/api/v1/blogs/<Post ID\>/

**Authorization:** Author of the Post or Admin

**Request Body:**

```
{
    "title": "Rest API V2",
    "description": "Django Rest FrameWork",
    "status": "published"
}
```
**Sample Response:**

```
{
    "message": "Post has been published!"
}
```
**Instructions:** Authorization header should be included

### **16. Delete Blog Post [PUT]**
**Endpoint:**  http://127.0.0.1:8000/api/v1/blogs/<Post ID\>/

**Authorization:** Author of the Post or Admin

**Request Body:**

```
{
    "title": "Rest API V2",
    "description": "Django Rest FrameWork",
    "status": "published"
}
```
**Sample Response:**

```
{
    "message": "Post has been published!"
}
```
**Instructions:** Authorization header should be included

### **17. Add Comment [POST]**
**Endpoint:**  http://127.0.0.1:8000/api/v1/blogs/<Post ID\>/comments/

**Authorization:** AllowAny

**Request Body:**

```
{
    "body": "Another Comment",
    "post": 32
}
```
**Sample Response:**

```
{
    "id": 6,
    "body": "Another Comment",
    "created": "2022-07-13T14:09:58.827290Z"
}
```



### **18. View Comments [GET]**
**Endpoint:**  http://127.0.0.1:8000/api/v1/blogs/<Post ID\>/comments/

**Authorization:** AllowAny

**Request Body:**

```

```
**Sample Response:**

```
[
    {
        "id": 1,
        "body": "Informative",
        "created": "2022-07-07T10:05:10.010430Z",
        "modified": "2022-07-07T10:05:10.010430Z",
        "comment_by": 8,
        "post": 9
    },
    {
        "id": 6,
        "body": "Another Comment",
        "created": "2022-07-13T14:09:58.827290Z",
        "modified": "2022-07-13T14:09:58.827290Z",
        "comment_by": 32,
        "post": 9
    }
]
```

### **19. Update Comments [PUT]**
**Endpoint:**  http://127.0.0.1:8000/api/v1/blogs/<Post ID\>/comments/

**Authorization:** AllowAny

**Request Body:**

```

```
**Sample Response:**

```
[
    {
        "id": 1,
        "body": "Informative",
        "created": "2022-07-07T10:05:10.010430Z",
        "modified": "2022-07-07T10:05:10.010430Z",
        "comment_by": 8,
        "post": 9
    },
    {
        "id": 6,
        "body": "Another Comment",
        "created": "2022-07-13T14:09:58.827290Z",
        "modified": "2022-07-13T14:09:58.827290Z",
        "comment_by": 32,
        "post": 9
    }
]
```





# Models

#### User
![image](https://user-images.githubusercontent.com/41924102/178666733-c61489f5-b7fd-43e7-95bd-6fd7be8f1c0c.png)

#### Post
![image](https://user-images.githubusercontent.com/41924102/178666929-20caecce-e82e-42b0-b3fa-8b757e62c618.png)

#### Comment
![image](https://user-images.githubusercontent.com/41924102/178667097-0b3ac6b1-cf59-4ffc-aa4d-b5e040816011.png)

#### OTP
