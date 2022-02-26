# CRYPTO

### Instructions
Follow step by step instruction below to setup CRYPTO-Project django application in local.

### Prerequisites

- Python 3.8
- MySql

### Recommended tools

Creating a virtual python environment dedicated for this application is strongly recommended to prevent your local system from breaking unexpectedly.

- [pyenv-virtualenv](https://github.com/pyenv/pyenv-virtualenv)

        $ virtualenv --python=python3.8 venv

- [PyCharm](https://www.jetbrains.com/pycharm/)

### Setting up

1. Prep MySQL user for this application.

    my.cnf

        [client]
        default-character-set = utf8mb4

        [mysql]
        default-character-set = utf8mb4

        [mysqld]
        character-set-client-handshake = FALSE
        character-set-server = utf8mb4
        collation-server = utf8mb4_unicode_ci
        innodb_file_format = Barracuda
        innodb_file_per_table = 1
        innodb_large_prefix

    mysql

        mysql> CREATE SCHEMA crypto_db CHARACTER SET utf8mb4;
        mysql> CREATE USER 'crypto_admin'@'localhost' IDENTIFIED BY 'CryptoAdmin!123';
        mysql> GRANT ALL PRIVILEGES ON crypto_db.* TO 'crypto_admin'@'localhost';
        mysql> FLUSH PRIVILEGES;

2. Clone this repository and confirm if virtual env is activated.

        $ git clone https://github.com/Dhruvil-Gajjar/Crypto.git 
        $ cd crypto
        $ python --version
        Python 3.8

3. Run `pip install -r requirements.txt`

4. Export below commands for development.

        $ export DJANGO_SECRET_KEY='(eh44==a$@wt1h#t4$zf(dz)6seixy6tw$l4aunzt&rpsf3y7w'
        $ export DJANGO_SETTINGS_MODULE=project.settings.development
        $ export DB_NAME='crypto_db'
        $ export DB_USERNAME='crypto_admin'
        $ export DB_PASSWORD='CryptoAdmin!123'
        $ export DB_HOST='localhost'
        $ export DB_PORT='3306' 

5. Run following django **management** commands.

        $ python manage.py makemigrations     
        $ python manage.py migrate     

6. Run following command to start the **server**.

        $ python manage.py runserver     

### Enjoy !!