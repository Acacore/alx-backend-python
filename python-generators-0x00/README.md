# MySQL Database Seeder for ALX_prodev

## 📌 Project Overview
This project is a Python-based utility that sets up and populates a MySQL database named **`ALX_prodev`** with user data. It is designed as part of the ALX Professional Development backend program to demonstrate working with databases, schema creation, and CSV data ingestion.

The project consists of:
- `seed.py` → Contains helper functions to connect to MySQL, create the database, create tables, and insert CSV data.  
- `user_data.csv` → Sample dataset containing user information.  

---

## 🗄️ Database Schema

The project creates a database named **`ALX_prodev`** with the following table:

### `user_data`
| Field     | Type         | Constraints                    |
|-----------|--------------|--------------------------------|
| user_id   | CHAR(36)     | Primary Key (UUID), Indexed    |
| name      | VARCHAR(100) | NOT NULL                       |
| email     | VARCHAR(100) | NOT NULL, UNIQUE               |
| age       | DECIMAL(3,0) | NOT NULL                       |

- **`user_id`** → Generated automatically in Python using `uuid.uuid4()`.  
- **`email`** → Enforced as unique to prevent duplicate records.  
- **`name`** and **`age`** → Required fields but duplicates are allowed.  

---

## 📊 ERD (Entity Relationship Diagram)

Below is the simple ERD representation of the `ALX_prodev` schema:

```mermaid
erDiagram
    USER_DATA {
        CHAR(36) user_id PK
        VARCHAR(100) name
        VARCHAR(100) email UNIQUE
        DECIMAL(3,0) age
    }
⚙️ Setup Instructions
1. Install MySQL
Download and install MySQL Community Server from the official MySQL website.
During setup, note down:

Host (default: 127.0.0.1)

Port (default: 3306)

Root username and password

2. Install Python Dependencies
Make sure Python 3.10+ is installed. Then install required libraries:

bash
Copy code
pip install mysql-connector-python
3. Project Structure
Copy code
python-generator-0x00/
│── seed.py
│── user_data.csv
│── README.md
4. Configure Database Connection
In seed.py, update the credentials in connect_db() and connect_to_prodev():

python
Copy code
user="root",
password="your_mysql_password",
host="127.0.0.1",
port=3306
▶️ Usage
Run the script:

bash
Copy code
python3 seed.py
Expected output:

nginx
Copy code
CSV file path: C:\Users\...\user_data.csv
Table user_data created successfully
Database ALX_prodev is present
[('uuid1', 'John Doe', 'johndoe@gmail.com', 34),
 ('uuid2', 'Jane Smith', 'janesmith@yahoo.com', 28),
 ('uuid3', 'Mike Johnson', 'mikej@hotmail.com', 45)]
🛡️ Duplicate Handling
The email field is declared UNIQUE.

The INSERT IGNORE SQL clause ensures duplicate emails are not inserted when reseeding.

If the same CSV is imported multiple times, only new unique records are added.

📂 Functions in seed.py
Function	Description
connect_db()	Connects to the MySQL server (without specifying a database).
create_database(conn)	Creates the ALX_prodev database if it does not already exist.
connect_to_prodev()	Connects directly to the ALX_prodev database.
create_table(conn)	Creates the user_data table with required fields and constraints.
insert_data(conn, csv)	Inserts CSV data into user_data with UUID as user_id. Skips duplicates.

📊 Sample Data (CSV)
Example rows from user_data.csv:

csv
Copy code
name,email,age
John Doe,johndoe@gmail.com,34
Jane Smith,janesmith@yahoo.com,28
Mike Johnson,mikej@hotmail.com,45
🚀 Future Improvements
Add logging for insert operations.

Extend schema with more fields (e.g., created_at, updated_at).

Support seeding multiple tables from different CSV files.

Add Docker support for quick environment setup.

