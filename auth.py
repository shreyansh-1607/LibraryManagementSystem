# type: ignore
from db_connect import get_connection

CURRENT_USER = { 'username': None, 'role': None}

def login():
    print("\n========== Library Management System ==========")
    print("               Please Log In")
    print("================================================")
    
    for attempts in range(3):
        username= input("Username: ").strip()
        password= input("Password: ").strip()
        
        try:
            cnx= get_connection()
            cursor= cnx.cursor()
            cursor.execute(
                "SELECT username, role FROM users WHERE username= %s AND password= %s", (username, password)
            )
            # not written as username = {username} and password= {password} 
            # as it is vulnerable to being hacked 
            # so I am using the old C way to use parameter in between
            
            result= cursor.fetchone() #fetchone-- retrieves one row from the query as tuple
            
            cursor.close()
            cnx.close() #connection closed here
            
            if result:
                CURRENT_USER['username']= result[0]
                CURRENT_USER['role']= result[1]
                print(f"\n Welcome, {result[0]}!! You are logged in as: {result[1].upper()}")
                return True
            else:
                print(f" Invalid credentials. {2 - attempts} attempt(s) left.")
        
        except Exception as e:
            print("Database error:", e)
            return False
        
    print("Too many failed attempts. Try later :)\n Exiting")
    return False

def require_admin():
    if CURRENT_USER['role']!= 'admin':
        print("  Access denied. Admin only authorised.")
        return False
    return True

def logout():
    CURRENT_USER['username']= None
    CURRENT_USER['role']= None
    print("\nLogged Out Successfully.")
    