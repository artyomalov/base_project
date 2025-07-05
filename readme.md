To run project you need python 3.12.2 or higher, PostgreSQL and OpneSSL to be installed on your pc.

1. Create virtual environment.
   - Navigate to the root folder of the project
   - Run "python -m venv .venv".

2. Activate created virtual environment.
   Run:
   For Linux:
   ". .venv/bin/activate" / "source .venv/bin/activate"
   For WIndows:
   ". .venv/Scripts/activate" / source .venv/Scripts/activate

   (For Windows better to install bash terminal from Git).

3. Install project's dependencies.
   Run "pip install -r requirements.txt".

4. Generate OpenSSL keys for JWT token generation.
   Run the following commands:

   - "mkdir certs"
   - "openssl genrsa -out ./config/certs/jwt-private.pem 2048"
   - "openssl rsa -in ./config/certs/jwt-private.pem -pubout -out ./config/certs/jwt-public.pem".

5. Create projects's databases (working and test) on your postgres local server.

6. Create env file
   Run python generate_env.py

7. Make migrations and create all nesessary tables.
   Run "alembic upgrade head"

8. Create root user.
   Run "python create_root_user_script.py".
   Insert username and password for your root user (dafault: root - root)

9. Start app.
   Run "python main.py"
