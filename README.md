# django-user-management


The User Management App is a Django application that provides user registration and management functionality. It allows users to create an account and update their profile information

- JWT Authentication: The app uses JSON Web Tokens (JWT) for user authentication and authorization.
- Image Upload: Users can upload a profile picture, which is stored in the server's media storage.


## Installation and Usage

1. Clone the repository and navigate to the project directory.
2. Install the project dependencies using `pip install -r requirements.txt`.
3. Apply the database migrations using `python manage.py migrate`.
4. Start the development server using `python manage.py runserver`.
5. Access the app in your web browser at `http://localhost:8000/`.

## API Endpoints

`POST /users/`: Register a new user by providing the required user details.
```
curl --location 'http://localhost:8000/user/' \
--header 'Content-Type: application/json' \
--form 'password="password"' \
--form 'full_name="Aryan Gupta"' \
--form 'bio="bio"' \
--form 'profile_picture=@"/C:/Users/aryan2/Downloads/github_avatar.png"' \
--form 'email="aryan@company.com"'
```
`PATCH /users/`: Update the profile information of a user.
```
curl --location --request PATCH 'http://localhost:8000/user/' \
--header 'Authorization: Bearer token' \
--header 'Content-Type: application/json' \
--data '{
    "full_name": "New Name",
    "bio": "updated bio"
}'
```



