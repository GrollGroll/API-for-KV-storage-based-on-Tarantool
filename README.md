# Run
### Project
In the root folder of the project:
  ```
  docker-compose up -d --build
  ```
### Tests
  ```
  docker exec -it FastAPI sh
  pytest src/test_app.py
  ```
_____________
# API Documentation
## Base URL
  ```
  http://<ip_address>:8080/api
  ```
## Authentication
### 1. Login
**Endpoint:** POST /api/login

**Description:** Authenticates a user and returns an authorization token.

**Request**
   - **Body Parameters:**
        - 'username' (string, required)
        - 'password' (string, required)

**Example Request:**

  ```
  {
   "username": "admin",
   "password": "presale"
  }
  ```
**Example CURL:**

  ```
  curl -X 'POST' \
    'http://<ip_address>:8080/api/login' \
    -H 'Content-Type: application/x-www-form-urlencoded' \
    -d 'username=admin&password=presale'
  ```
**Response**
   - **Success Response:**

   ```
   {
     "access_token": "<token>"
   }
   ```
   - **Possible Errors:**
        - **400 Bad Request:** Invalid username or password.
        - **401 Unauthorized:** Missing or invalid credentials.
_____________
## Data Storage
### 2. Write Data
**Endpoint:** POST /api/write

**Description:** Stores key-value pairs in the database.

**Authentication Required:** Yes (Bearer Token)

**Request**
   - **Headers:**
        - Authorization: Bearer <token>
   - **Body Parameters:**
        - **'data'** (object, required): An object containing key-value pairs to be stored.

**Example Request:**

  ```
  {
    "data": {
      "key1": "value1",
      "key2": "value2",
      "key3": 12345
    }
  }
  ```
**Example CURL:**

  ```
  curl -X 'POST' \
    'http://<ip_address>:8080/api/write' \
    -H 'Authorization: Bearer <token>' \
    -H 'Content-Type: application/json' \
    -d '{
      "data": {
        "key1": "value1",
        "key2": "value2",
        "key3": 12345
      }
    }'
  ```
**Response**
   - **Success Response:**

  ```
  {
     "status": "success"
  }
  ```
   - **Possible Errors:**
        - **401 Unauthorized:** Missing or invalid token.
        - **500 Internal Server Error:** Failed to store data due to server issues or incorrect data format.
_____________
### 3. Read Data
**Endpoint:** POST /api/read

**Description:** Retrieves values for a batch of keys from the database.

**Authentication Required:** Yes (Bearer Token)

**Request**
   - **Headers:**
        - Authorization: Bearer <token>
   - **Body Parameters:**
        - **'keys'** (array of strings, required): A list of keys for which values need to be fetched.

**Example Request:**

  ```
  {
    "keys": ["key1", "key2", "key3"]
  }
  ```
**Example CURL:**

  ```
  curl -X 'POST' \
    'http://<ip_address>:8080/api/read' \
    -H 'Authorization: Bearer <token>' \
    -H 'Content-Type: application/json' \
    -d '{
      "keys": ["key1", "key2", "key3"]
    }'
  ```
**Response**
   - **Success Response:**

   ```
   {
     "data": {
       "key1": "value1",
       "key2": "value2",
       "key3": null  // if the key is not found
     }
   }
   ```
   - **Possible Errors:**
        - **401 Unauthorized:** Missing or invalid token.
        - **500 Internal Server Error:** Failed to retrieve data due to server issues or incorrect data format.
_____________
### Error Codes
   - **400 Bad Request:** The request could not be understood or was missing required parameters.
   - **401 Unauthorized:** Authentication failed or user does not have permissions for the desired action.
   - **404 Not Found:** The requested resource could not be found.
   - **500 Internal Server Error:** An error occurred on the server. Possible reasons include database connectivity issues, unexpected input, or internal server errors.


































    
