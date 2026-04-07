# type: ignore

import auth
import book
import member
import issue
import admin


def menu_book():
    
    while True:
        print("\n ---- Book Management ----")
        print(" 1. Add book")
        print(" 2. Display all books")
        print(" 3. Search a book")
        print(" 4. Delete book")
        print(" 5. Update book detail")
        print(" 6. Back")
        
        c= input("Choice:").strip()
        if c=='1': 
            book.insertData()
        elif c=='2':
            book.display()
        elif c=='3':
            book.searchBook()
        elif c=='4':
            book.deleteBook()
        elif c== '5':
            book.updateBook()
        elif c== '6':
            break
        else:
            print("Invalid Choice.")
        
        input("Press enter to continue :)")

def menu_member():
    while True:
        print("\n ---- Member Management ----")
        print(" 1. Add member")
        print(" 2. Display all member")
        print(" 3. Search member")
        print(" 4. Delete member")
        print(" 5. Update member detail")
        print(" 6. Back")
        
        c= input("Choice:").strip()
        if c=='1': 
            member.insertMember()
        elif c=='2':
            member.display()
        elif c=='3':
            member.searchMember()
        elif c=='4':
            member.deleteMember()
        elif c== '5':
            member.updateMember()
        elif c== '6':
            break
        else:
            print("Invalid Choice.")
        
        input("Press enter to continue :)")
        
def menu_issue():
    while True:
        print("\n ---- Book Issue/Return ----")
        print(" 1. Issue book")
        print(" 2. Return book")
        print(" 3. View all issued books")
        print(" 4. View overdue books")
        print(" 5. Back")
        
        c= input("Choice:").strip()
        if c=='1': 
            issue.issueBook()
        elif c=='2':
            issue.returnBook()
        elif c=='3':
            issue.showIssuedBooks()
        elif c=='4':
            issue.showOverdueBooks()
        elif c== '5':
            break
        else:
            print("Invalid Choice.")
        input(" Press enter to continue :)")
        
def menu_admin():
    while True:
        print("\n ---- Admin Panel ----")
        print(" 1. Add system user")
        print(" 2. List all users")
        print(" 3. Delete user")
        print(" 4. Back")
        c= input("Choice:").strip()
        if c=='1':
            admin.addUser()
        elif c=='2':
            admin.listUsers()
        elif c=='3':
            admin.deleteUser()
        elif c=='4':
            break
        
        else:
            print("Invalid Choice.")
        
        input("Press enter to continue. :)")
        
def main():
    if not auth.login():
        return 
    
    while True:
        print(f"\n ===== Library Management System =====")
        print(f"Logged in as : {auth.CURRENT_USER['username']} ({auth.CURRENT_USER['role']})")
        print(" 1. Book Management")
        print(" 2. Member Management")
        print(" 3. Issue/ Return Book")
        if auth.CURRENT_USER['role'] == 'admin':
            print(" 4. Admin Panel")
            print(" 5. Logout")
        else:
            print(" 4. Logout")
        
        c= input("Choice:").strip()
        
        if c== '1':
            menu_book()
        elif c== '2':
            menu_member()
        elif c==  '3':
            menu_issue()
        elif c =='4' and auth.CURRENT_USER['role'] == 'admin':
            menu_admin()
        elif c in ('4','5'):
            auth.logout()
            break
        else:
            print(" INVALID CHOICE.")

if __name__ == "__main__":
    main()