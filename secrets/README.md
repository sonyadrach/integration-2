1. Generate db_password:
   openssl rand -base64 24 > secrets/db_password
2. Generate jwt_secret_key:
   openssl rand -base64 48 > secrets/jwt_secret_key
3. Secret files shall be stored in the secrets/ directory with permissions 0600:
   chmod 600 secrets/db_password secrets/jwt_secret_key