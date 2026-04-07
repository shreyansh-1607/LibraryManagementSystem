# type: ignore

from db_connect import get_connection
from auth import require_admin

def addUser():
    if not require_admin():
        return
    
    try:
        cnx= get_connection()
        cursor= cnx.cursor()
        
        uname= input("New Username  :").strip()
        pwd= input("Password      :").strip()
        
        print("Role:\n1.Admin\n2.Librarian")
        role= 'admin' if input("Choice:").strip() == '1' else 'librarian'
        
        cursor.execute("INSERT INTO users VALUES (%s, %s, %s)", (uname, pwd, role))
        cnx.commit()
        
        print("User added successfully.")
        cursor.close()
        cnx.close()
    
    except Exception as e:
        print("Error:", e)

def listUsers():
    
    if not require_admin():
        return
    
    try:
        cnx= get_connection()
        cursor= cnx.cursor()
        cursor.execute("SELECT username, role FROM users")
        
        rows= cursor.fetchall()
        print(f"\n {'Username':<20} {'Role'}")
        print(" " + "-"*30)
        
        for r in rows:
            print(f" {r[0]: <20} {r[1]}")
        
        cursor.close()
        cnx.close()
    
    except Exception as e:
        print("Error:", e)

def deleteUser():
    if not require_admin():
        return 
    
    try:
        cnx= get_connection()
        cursor= cnx.cursor()
        uname= input("Username to delete: ").strip()
        cursor.execute("DELETE FROM users WHERE username= %s", (uname,))
        cnx.commit()
        print(f"{cursor.rowcount} user(s) removed.")
        cursor.close()
        cnx.close()
    except Exception as e:
        print("Error:", e)