# Python URL Shortener

A CLI-based URL Shortener built with **Python and PostgreSQL**.

The application generates a unique short code for a long URL, stores the URL in PostgreSQL, and allows users to retrieve the original URL using the short code. It also maintains click records for shortened URLs.

---

## Features

* Generate random 6-character short codes
* Store shortened URLs in PostgreSQL
* Retrieve original URLs using short codes
* Track URL clicks
* Relational database design using primary and foreign keys
* Database indexes for frequently queried columns
* SQL JOIN and aggregation queries
* Transaction handling using `COMMIT` and `ROLLBACK`
* Database configuration using environment variables

---

## Technologies Used

* **Python**
* **PostgreSQL**
* **SQL**
* **psycopg2**
* **python-dotenv**
* **Git & GitHub**

---

## Project Structure

```text
Python_URL_Shortener/
│
├── main.py
├── database.sql
├── seed.sql
├── requirements.txt
├── .env
├── .gitignore
└── README.md
```

### File Description

| File               | Purpose                                                         |
| ------------------ | --------------------------------------------------------------- |
| `main.py`          | Main Python application                                         |
| `database.sql`     | Creates database tables, relationships, constraints and indexes |
| `seed.sql`         | Inserts sample users, URLs and click data                       |
| `requirements.txt` | Python dependencies                                             |
| `.env`             | Local PostgreSQL connection configuration                       |
| `.gitignore`       | Prevents sensitive/local files from being committed             |
| `README.md`        | Project documentation                                           |

> `venv/` is created locally but is not included in the repository.

---

# Database Design

The application uses three related tables:

```text
┌─────────────┐
│    users    │
└──────┬──────┘
       │
       │ 1 : N
       ▼
┌─────────────┐
│    urls     │
└──────┬──────┘
       │
       │ 1 : N
       ▼
┌─────────────┐
│   clicks    │
└─────────────┘
```

### Users

Stores information about users.

Important fields:

* `id` — Primary Key
* `name`
* `email` — Unique
* `created_at`

### URLs

Stores shortened URLs.

Important fields:

* `id` — Primary Key
* `short_code` — Unique
* `original_url`
* `user_id` — Foreign Key
* `created_at`

Relationship:

```text
urls.user_id → users.id
```

One user can have multiple URLs.

### Clicks

Stores click information for shortened URLs.

Important fields:

* `id` — Primary Key
* `url_id` — Foreign Key
* `ip_address`
* `clicked_at`

Relationship:

```text
clicks.url_id → urls.id
```

One URL can have multiple clicks.

---

# How the Application Works

## Shorten a URL

```text
User enters long URL
        ↓
Python generates 6-character code
        ↓
Python sends INSERT query
        ↓
PostgreSQL stores the URL
        ↓
Short code is returned to user
```

Example:

```text
Long URL:
https://github.com

Short Code:
X7kP2a
```

---

## Retrieve a URL

```text
User enters short code
        ↓
Python queries PostgreSQL
        ↓
URL ID + original URL are found
        ↓
Click is recorded
        ↓
Original URL is returned
```

Example:

```text
Short Code:
X7kP2a

Original URL:
https://github.com
```

---

# PostgreSQL Setup

## Requirements

Install the following before running the project:

* Python
* Git
* PostgreSQL

Check Python:

```powershell
python --version
```

Check Git:

```powershell
git --version
```

Check PostgreSQL:

```powershell
psql --version
```

---

# Installation

## 1. Clone the Repository

```powershell
git clone https://github.com/sunaina156/Python_URL_Shortener.git
```

Move into the project directory:

```powershell
cd Python_URL_Shortener
```

---

## 2. Create a Virtual Environment

```powershell
python -m venv venv
```

Activate it:

```powershell
.\venv\Scripts\Activate.ps1
```

The terminal should now show:

```text
(venv)
```

---

## 3. Install Dependencies

```powershell
pip install -r requirements.txt
```

---

# Database Configuration

## 4. Open PostgreSQL

From PowerShell:

```powershell
psql -U postgres
```

Enter your PostgreSQL password.

---

## 5. Create the Database

Inside the PostgreSQL terminal:

```sql
CREATE DATABASE url_shortener;
```

Connect to the database:

```sql
\c url_shortener
```

Verify the connection:

```sql
SELECT current_database();
```

Expected result:

```text
url_shortener
```

---

## 6. Create Tables and Indexes

Run:

```sql
\i database.sql
```

This creates:

* `users`
* `urls`
* `clicks`
* Primary keys
* Foreign keys
* Unique constraints
* Indexes

Check the tables:

```sql
\dt
```

---

## 7. Insert Sample Data

Run:

```sql
\i seed.sql
```

This inserts sample:

* Users
* URLs
* Click records

Verify the data:

```sql
SELECT * FROM users;
```

```sql
SELECT * FROM urls;
```

```sql
SELECT * FROM clicks;
```

---

# Environment Configuration

Create a `.env` file in the project root:

```text
Python_URL_Shortener/
│
├── main.py
├── database.sql
├── seed.sql
├── requirements.txt
├── .env
└── README.md
```

Add your **own PostgreSQL credentials**:

```env
DB_HOST=localhost
DB_NAME=url_shortener
DB_USER=postgres
DB_PASSWORD=YOUR_POSTGRES_PASSWORD
DB_PORT=5432
```

Replace:

```text
YOUR_POSTGRES_PASSWORD
```

with the PostgreSQL password configured on your computer.

> **Never commit `.env` to GitHub.**

---

# Run the Application

Make sure the virtual environment is active:

```text
(venv)
```

Run:

```powershell
python main.py
```

The application will display:

```text
==============================
          URL SHORTENER
==============================
1. Shorten URL
2. Retrieve Original URL
3. Exit
```

---

# Using the Application

## Shorten URL

Select:

```text
1
```

Enter a URL:

```text
https://github.com
```

The application generates a short code:

```text
Short Code: X7kP2a
```

The URL is stored in PostgreSQL.

---

## Retrieve Original URL

Select:

```text
2
```

Enter the short code:

```text
X7kP2a
```

The application returns:

```text
Original URL: https://github.com
```

A click record is also stored in the `clicks` table.

---

# Useful SQL Queries

## View Users

```sql
SELECT * FROM users;
```

## View URLs

```sql
SELECT * FROM urls;
```

## Find a URL using a Short Code

```sql
SELECT original_url
FROM urls
WHERE short_code = 'abc123';
```

## Find URLs Created by a User

```sql
SELECT *
FROM urls
WHERE user_id = 1;
```

---

# SQL JOINs

Get users and the URLs they created:

```sql
SELECT
    u.name,
    url.short_code,
    url.original_url
FROM users u
JOIN urls url
    ON u.id = url.user_id;
```

Get URLs and their click information:

```sql
SELECT
    url.short_code,
    c.ip_address,
    c.clicked_at
FROM urls url
JOIN clicks c
    ON url.id = c.url_id;
```

---

# Click Analytics

Count clicks for each URL:

```sql
SELECT
    url_id,
    COUNT(*) AS total_clicks
FROM clicks
GROUP BY url_id;
```

Include URLs that have no clicks:

```sql
SELECT
    url.short_code,
    COUNT(c.id) AS total_clicks
FROM urls url
LEFT JOIN clicks c
    ON url.id = c.url_id
GROUP BY url.id, url.short_code;
```

---

# Indexes

The project includes indexes on commonly queried foreign-key columns:

```sql
CREATE INDEX idx_urls_user_id
ON urls(user_id);

CREATE INDEX idx_clicks_url_id
ON clicks(url_id);
```

View indexes:

```sql
\di
```

Analyze a query:

```sql
EXPLAIN ANALYZE
SELECT *
FROM urls
WHERE user_id = 1;
```

---

# Transactions

The database can be tested using PostgreSQL transactions.

### Rollback

```sql
BEGIN;

INSERT INTO users (name, email)
VALUES ('Test User', 'test@example.com');

SELECT * FROM users;

ROLLBACK;
```

The inserted record will be removed.

### Commit

```sql
BEGIN;

INSERT INTO users (name, email)
VALUES ('Committed User', 'committed@example.com');

COMMIT;
```

The inserted record will remain in the database.

---

# Database Constraints

The database uses constraints to maintain data integrity.

### Primary Keys

Each table has a unique identifier:

```text
users.id
urls.id
clicks.id
```

### Foreign Keys

```text
urls.user_id → users.id

clicks.url_id → urls.id
```

### Unique Constraints

The following values must be unique:

```text
users.email
urls.short_code
```

These constraints prevent invalid or duplicate data.

---

# Error Handling

The application handles cases such as:

* Invalid short codes
* Database connection through environment variables
* Foreign-key constraints
* Unique-value constraints

If a short code does not exist, the application displays:

```text
Short code not found!
```

---

# Project Flow

```text
                    ┌───────────────┐
                    │     User      │
                    └───────┬───────┘
                            │
                            ▼
                    ┌───────────────┐
                    │ Python App    │
                    └───────┬───────┘
                            │
                     SQL Queries
                            │
                            ▼
                    ┌───────────────┐
                    │  PostgreSQL   │
                    └───────┬───────┘
                            │
                ┌───────────┼───────────┐
                ▼           ▼           ▼
             users         urls       clicks
```

---

# Concepts Demonstrated

This project demonstrates practical understanding of:

* Python functions
* Random string generation
* CLI application development
* PostgreSQL
* SQL
* Database schema design
* Primary keys
* Foreign keys
* One-to-many relationships
* Referential integrity
* Unique constraints
* Indexes
* SQL filtering
* JOINs
* Aggregation with `COUNT`
* `GROUP BY`
* Transactions
* `COMMIT`
* `ROLLBACK`
* Python-to-PostgreSQL connectivity
* Environment variables
* Git and GitHub

---

# Future Improvements

Possible future improvements include:

* Convert the CLI application into a REST API using FastAPI
* Add URL validation
* Add user authentication
* Add URL expiration
* Improve click analytics
* Add automated tests
* Dockerize the application
* Add CI/CD
* Deploy the application to AWS
