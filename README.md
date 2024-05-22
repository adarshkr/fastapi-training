
# FastAPI Application

This application demonstrates several features of FastAPI:

## Features

### File Upload

The application includes routes for both single and multiple file uploads. The single file upload route is at `/file/` and accepts a single file in the request body. The multiple file upload route is at `/files/` and accepts multiple files in the request body.


### HTTP Methods

The application includes examples of several HTTP methods, including `GET`, `POST`, and `PUT`.

## Setup and Running the Application in a Virtual Environment

1. First, you need to create a virtual environment. You can do this with the `venv` module:

```bash
python3 -m venv env
```

2. Then, activate the virtual environment.

On macOS and Linux, use:
```bash
source env/bin/activate
```

On Windows, use:
```bash
.\env\Scripts\activate
```

3. Once the virtual environment is activated, you can install the application's dependencies:
```bash
pip install -r requirements.txt
```

<!-- 4. Finally, you can run the application:
```bash
uvicorn main:app --reload
``` -->

4. Finally, you can run the application:
```bash
docker compose build --no-cache
docker compose up -d
```

5. Access the swagger docs at http://localhost:8000/docs

6. Access the PgAdmin at http://localhost:8080 

7. Deactivate  virtual environment
```bash
deactivate
```