# type: ignore
# the above line stops inline error detection 

import os
from db_connect import get_connection
from datetime import date

# here I have taken in consideration that the system is Windows or Mac/Linux
# cls for windows and clear for Mac/Linux
def clrscreen():
    os.system('cls' if os.name== 'nt' else 'clear')

def display():
    try:
        cnx= get_connection()
        cursor= cnx.cursor()
        cursor.execute("SELECT Bno, ISBN, Bname, auth, price, publ, category, total_qty, avail_qty, d_o_purchase FROM bookrecord")
        
        
        rows= cursor.fetchall()
        cursor.close
        cnx.close
        
        if not rows:
            print("No book records found.")
            return
        
        print(f"\n{'='*70}")
        print(f" {'Code':<8} {'ISBN':<14} {'Title':<22} {'Author':<16} {'Category':<12} {'Avail':<6} {'Total'} ")
        print(f"{'='*70}")
        for r in rows:
            print(f" {r[0]:<8} {str(r[1]):<14} {r[2][:20]:<22} {str(r[3])[:14]:<16} {str(r[6]):<12} {r[8]:<6} {r[7]}")
        print(f"{'='*70}\n")
    except Exception as e:
        print("Error:", e)
        
def insertData():
    try:
        cnx= get_connection()
        cursor= cnx.cursor()
        
        bno= input("Book Code       :").strip()
        isbn= input("ISBN           :").strip()
        bname= input("Book Name     :").strip()
        auth= input("Author Name    :").strip()
        price= int(input("Price (₹) :"))
        publ= input("Publisher      :").strip()
        
        print("Category options: english, hindi, mathematics, science, history, technology, other")
        category= input("Category   :").strip().lower()
        qty= int(input("Quantity    :"))
        
        print("Date of purchase     :")
        DD= int(input("Day (in DD)  :"))
        MM= int(input("Month (in MM):"))
        YY= int(input("Year(in YY)  :"))
        
        query= """INSERT INTO bookrecord
                    (Bno, ISBN, Bname, auth, price, publ, category, total_qty, avail_qty, d_o_purchase)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
        data= (bno, isbn, bname, auth, price, publ, category, qty, qty, date(YY, MM, DD))
        
        cursor.execute(query, data)
        cnx.commit()
        cursor.close()
        cnx.close()
        print("Book record inserted successfully.")
    
    except Exception as e:
        print(" Error:", e)
        

def deleteBook():
    try:
        cnx= get_connection()
        cursor= cnx.cursor()
        
        bno= input("Enter book code to delete:").strip()
        cursor.execute("DELETE FROM bookrecord WHERE Bno= %s", (bno,))
        cnx.commit()
        
        print(f" {cursor.rowcount} record(s) deleted.")
        
        cursor.close()
        cnx.close() 
    except Exception as e:
        print(" Error:", e)


def searchBook():
    try:
        cnx= get_connection()
        cursor= cnx.cursor()
        
        print("Search by: \n1. Book Code\n2.ISBN\n3.Title\n4.Author\n5.Category")
        choice= input("Choice:").strip()
        
        if (choice == '1'):
            val= input("Enter book code:").strip()
            cursor.execute("SELECT * FROM bookrecord WHERE Bno= %s", (val,))
        elif (choice == '2'):
            val= input("Enter ISBN:").strip()
            cursor.execute("SELECT * FROM bookrecord WHERE ISBN= %s", (val,))
        elif (choice == '3'):
            val= input("Enter the title:").strip()
            cursor.execute("SELECT * FROM bookrecord WHERE Bname LIKE %s", ('%'+val+'%',))
        elif (choice == '4'):
            val= input("Enter author name:").strip()
            cursor.execute("SELECT * FROM bookrecord WHERE auth LIKE %s", ('%'+val+'%',))
        elif (choice == '5'):
            val= input("Enter category:").strip()
            cursor.execute("SELECT * FROM bookrecord WHERE category = %s", (val,))
        else:
            print("Invalid choice.")
            return 
        
        rows= cursor.fetchall()
        cursor.close()
        cnx.close()
        
        if not rows:
            print("No matching records found.")
            return 

        for r in rows:
            print(f"\nBook Code    : {r[0]}")
            print(f"ISBN           : {r[1]}")
            print(f"Title          : {r[2]}")
            print(f"Author         : {r[3]}")
            print(f"Price          : ₹{r[4]}")
            print(f"Publisher      : {r[5]}")
            print(f"Category       : {r[6]}")
            print(f"Total quantity : {r[7]}")
            print(f"Available      : {r[8]}")
            print(f"Purchased      : {r[9]}")
        
        print(f"\n {len(rows)} record(s) found.")
    
    except Exception as e:
        print("Error!", e)

def updateBook():
    try:
        cnx= get_connection()
        cursor= cnx.cursor()
        
        bno= input("Enter book to update:").strip()
        cursor.execute("SELECT * FROM bookrecord WHERE Bno= %s", (bno,))
        
        if not cursor.fetchone():
            print("Book not found.")
            cursor.close()
            cnx.close()
            return
        
        print("Enter updated data:")
        bname= input("Book Name         :").strip()
        auth= input("Author             :").strip()
        price= int(input("Price         :"))
        publ= input("Publisher          :").strip()
        category= input("Category       :").strip().lower()
        qty= int(input("Total Quantity  :"))
        avail= int(input("Available Qty :"))
        
        query= """UPDATE bookrecord
                SET Bname= %s, auth= %s, price= %s, publ= %s, 
                category= %s, total_qty= %s, avail_qty= %s
                WHERE Bno= %s"""
        cursor.execute(query, (bname, auth, price, publ, category, qty, avail, bno))
        cursor.commit()
        print(f"{cursor.rowcount} record(s) updated.")
        
        cursor.close()
        cnx.close()
    
    except Exception as e:
        print("Error:", e)