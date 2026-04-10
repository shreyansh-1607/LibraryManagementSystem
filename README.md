# Library Management System 

A robust, CLI-based Library Management System built with Python and MySQL. This system handles everything from user authentication and role-based access to book inventory management, issuing logic and automated fine calculations.

## Features

- **Role-Based Access Control**: Distinct functionalities for Admin and Librarian roles.
- **Inventory Management**: Full CRUD (Create, Read, Update, Delete) operations for Books and Members.
- **Transaction Tracking**:
  * Issue and Return books.
  * Automatic Book Count updates (decrements on issue, increments on return).
  * Maintains a record of books issued by specific members.
- **Financial Logic**: Built-in Fine Calculation for overdue returns.
- **User Management**: Secure user list maintenance, restricted to Admin access only.
- **Database Integration**: Persistent storage using MySQL with a dedicated connection module.

## Tech Stacks:

* *Language*: Python 3.11.4

* *Database*: MySQL

* *Connector*: mysql-connector-python

* *Interface*: Command Line Interface (CLI) [can be extended with UI support in future surely]

## Project Structure

| File | Description |
| :--- | :--- |
| `main.py` | The main entry point of the application. Contains connection to different files across  |
| `auth.py` | Handles login, logout and session authentication. |
| `admin.py` | Admin-only features (admin panel) and system-wide user management. |
| `book.py` | Manages book's function of display, delete, searching a book and updating its records . |
| `member.py` | Manages library member's profile, mail/phone validation. Also supports display, delete, searching member profile and updating their record. |
| `issue.py` | Logic for issuing/returning books and calculating fines. Also displays issued/ overdue books  |
| `db_connect.py` | Centralized MySQL database connection configuration. |
| `LibraryManagementSQL_database.sql` | SQL script to initialize the database structure and tables. |

## Getting Started

### Prerequisites

Python: Ensure Python 3.11.4 is installed.

MySQL: A running MySQL server instance.

Dependencies: 
Install the required Python-MySQL connector: mysql-connector-python 9.6.0
  ```bash
  pip install mysql-connector-python
  ```

### Database Setup

1. Open your MySQL Command Line or Workbench.

2. Execute the commands within the SQL file: *LibraryManagementSQL_database.SQL*

3. Open db_connect.py and update the credentials to match your local setup:

  ```bash
db_connect.py
host="localhost",
user="your_username",
password="your_password",
database="library_db"

  ```


### Installation

1. Clone the repository:

      git clone [https://github.com/shreyansh-1607/LibraryManagementSystem.git](https://github.com/shreyansh-1607/LibraryManagementSystem.git)


1. Navigate to the project directory:

```bash
# Move into the folder created by the clone command
cd LibraryManagement
```

### Usage

Run the application using the following command:
```bash
python main.py
```

### Flow:

* Login: Enter your (user) credentials (configured in the database).

* Admin: Access user management and full system reports.

* Librarian: Perform daily tasks like issuing books and adding members of library managing.

## Roadmap

 - Transition from CLI to a Graphical User Interface (GUI) using Tkinter or PyQt.

 - Implement a search feature for books by Title/Author/ISBN.

 - Add an automated email notification system for overdue fines.

## Author

Shreyansh Shashwat

GitHub: [@shreyansh-1607](https://github.com/shreyansh-1607)

Email: shashwat.shreyansh16@gmail.com

LinkedIn: [https://www.linkedin.com/in/shreyansh-shashwat/](https://www.linkedin.com/in/shreyansh-shashwat/)

## License

This project is licensed under the MIT License - see the [LICENSE] file for details.
