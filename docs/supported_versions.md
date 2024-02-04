# Compatibility table

### Python versions

- Python 3.11, 3.12

### Supported databases

- PostgreSQL: 9.0.23+ (tested with 9.0.23, 16.1 (latest))

- MySql: 8.0.0+ (tested with 8.0.0, 8.3.0 (latest))

- MariaDB: 10.4.0+ (tested with 10.4.0, 11.2.2 (latest))

### Supported packages

- SQLAlchemy: 2.0.0+ (tested with 2.0.0, 2.0.25 (latest))

- psygopg: 3.0.18+ (tested with 3.0.18, 3.1.17 (latest))

- PyMySQL: 1.0.2+ (tested with 1.0.2, 1.1.0 (latest))
 
- alembic: 1.8.0+ (tested with 1.8.0, 1.13.1 (latest))

### Compatibility status

Each version of RedBeanPython has been tested with a full suite of tests against the following versions of Python, databases and packages:

Tests results:

| database | python | packages | status |
|----------|--------|----------|--------|
| postgres (postgres:16.1) | 3.12 | latest (2024) ['SQLAlchemy==2.0.25', 'psycopg==3.1.17', 'PyMySQL==1.1.0', 'alembic==1.13.1'] | :material-check: OK |
| postgres (postgres:16.1) | 3.12 | legacy (2022) ['SQLAlchemy==2.0.0', 'psycopg==3.0.18', 'PyMySQL==1.0.2', 'alembic==1.8.0'] | :material-check: OK |
| postgres (postgres:16.1) | 3.11 | latest (2024) ['SQLAlchemy==2.0.25', 'psycopg==3.1.17', 'PyMySQL==1.1.0', 'alembic==1.13.1'] | :material-check: OK |
| postgres (postgres:16.1) | 3.11 | legacy (2022) ['SQLAlchemy==2.0.0', 'psycopg==3.0.18', 'PyMySQL==1.0.2', 'alembic==1.8.0'] | :material-check: OK |
| postgres (postgres:9.0.23) | 3.12 | latest (2024) ['SQLAlchemy==2.0.25', 'psycopg==3.1.17', 'PyMySQL==1.1.0', 'alembic==1.13.1'] | :material-check: OK |
| postgres (postgres:9.0.23) | 3.12 | legacy (2022) ['SQLAlchemy==2.0.0', 'psycopg==3.0.18', 'PyMySQL==1.0.2', 'alembic==1.8.0'] | :material-check: OK |
| postgres (postgres:9.0.23) | 3.11 | latest (2024) ['SQLAlchemy==2.0.25', 'psycopg==3.1.17', 'PyMySQL==1.1.0', 'alembic==1.13.1'] | :material-check: OK |
| postgres (postgres:9.0.23) | 3.11 | legacy (2022) ['SQLAlchemy==2.0.0', 'psycopg==3.0.18', 'PyMySQL==1.0.2', 'alembic==1.8.0'] | :material-check: OK |
| mysql (mysql:8.3.0) | 3.12 | latest (2024) ['SQLAlchemy==2.0.25', 'psycopg==3.1.17', 'PyMySQL==1.1.0', 'alembic==1.13.1'] | :material-check: OK |
| mysql (mysql:8.3.0) | 3.12 | legacy (2022) ['SQLAlchemy==2.0.0', 'psycopg==3.0.18', 'PyMySQL==1.0.2', 'alembic==1.8.0'] | :material-check: OK |
| mysql (mysql:8.3.0) | 3.11 | latest (2024) ['SQLAlchemy==2.0.25', 'psycopg==3.1.17', 'PyMySQL==1.1.0', 'alembic==1.13.1'] | :material-check: OK |
| mysql (mysql:8.3.0) | 3.11 | legacy (2022) ['SQLAlchemy==2.0.0', 'psycopg==3.0.18', 'PyMySQL==1.0.2', 'alembic==1.8.0'] | :material-check: OK |
| mysql (mysql:8.0.0) | 3.12 | latest (2024) ['SQLAlchemy==2.0.25', 'psycopg==3.1.17', 'PyMySQL==1.1.0', 'alembic==1.13.1'] | :material-check: OK |
| mysql (mysql:8.0.0) | 3.12 | legacy (2022) ['SQLAlchemy==2.0.0', 'psycopg==3.0.18', 'PyMySQL==1.0.2', 'alembic==1.8.0'] | :material-check: OK |
| mysql (mysql:8.0.0) | 3.11 | latest (2024) ['SQLAlchemy==2.0.25', 'psycopg==3.1.17', 'PyMySQL==1.1.0', 'alembic==1.13.1'] | :material-check: OK |
| mysql (mysql:8.0.0) | 3.11 | legacy (2022) ['SQLAlchemy==2.0.0', 'psycopg==3.0.18', 'PyMySQL==1.0.2', 'alembic==1.8.0'] | :material-check: OK |
| mysql (mariadb:11.2.2) | 3.12 | latest (2024) ['SQLAlchemy==2.0.25', 'psycopg==3.1.17', 'PyMySQL==1.1.0', 'alembic==1.13.1'] | :material-check: OK |
| mysql (mariadb:11.2.2) | 3.12 | legacy (2022) ['SQLAlchemy==2.0.0', 'psycopg==3.0.18', 'PyMySQL==1.0.2', 'alembic==1.8.0'] | :material-check: OK |
| mysql (mariadb:11.2.2) | 3.11 | latest (2024) ['SQLAlchemy==2.0.25', 'psycopg==3.1.17', 'PyMySQL==1.1.0', 'alembic==1.13.1'] | :material-check: OK |
| mysql (mariadb:11.2.2) | 3.11 | legacy (2022) ['SQLAlchemy==2.0.0', 'psycopg==3.0.18', 'PyMySQL==1.0.2', 'alembic==1.8.0'] | :material-check: OK |
| mysql (mariadb:10.4.0) | 3.12 | latest (2024) ['SQLAlchemy==2.0.25', 'psycopg==3.1.17', 'PyMySQL==1.1.0', 'alembic==1.13.1'] | :material-check: OK |
| mysql (mariadb:10.4.0) | 3.12 | legacy (2022) ['SQLAlchemy==2.0.0', 'psycopg==3.0.18', 'PyMySQL==1.0.2', 'alembic==1.8.0'] | :material-check: OK |
| mysql (mariadb:10.4.0) | 3.11 | latest (2024) ['SQLAlchemy==2.0.25', 'psycopg==3.1.17', 'PyMySQL==1.1.0', 'alembic==1.13.1'] | :material-check: OK |
| mysql (mariadb:10.4.0) | 3.11 | legacy (2022) ['SQLAlchemy==2.0.0', 'psycopg==3.0.18', 'PyMySQL==1.0.2', 'alembic==1.8.0'] | :material-check: OK |
| sqlite (build-in) | 3.12 | latest (2024) ['SQLAlchemy==2.0.25', 'psycopg==3.1.17', 'PyMySQL==1.1.0', 'alembic==1.13.1'] | :material-check: OK |
| sqlite (build-in) | 3.12 | legacy (2022) ['SQLAlchemy==2.0.0', 'psycopg==3.0.18', 'PyMySQL==1.0.2', 'alembic==1.8.0'] | :material-check: OK |
| sqlite (build-in) | 3.11 | latest (2024) ['SQLAlchemy==2.0.25', 'psycopg==3.1.17', 'PyMySQL==1.1.0', 'alembic==1.13.1'] | :material-check: OK |
| sqlite (build-in) | 3.11 | legacy (2022) ['SQLAlchemy==2.0.0', 'psycopg==3.0.18', 'PyMySQL==1.0.2', 'alembic==1.8.0'] | :material-check: OK |

#
# ___