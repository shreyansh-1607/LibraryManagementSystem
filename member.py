# type: ignore

import re
from db_connect import get_connection
from datetime import date

def validate_email(email):
    pattern= r'^[\w\.-]+@[\w\.-]+\.\w{2,}$'
    return re.match(pattern, email) is not None

def validate_mobile(mob):
    return mob.isdigit() and len(mob) == 10

def display():
    try:
        cnx= get_connection()
        cursor= cnx.cursor()
        cursor.execute("SELECT * FROM member")
        rows= cursor.fetchall()
        cursor.close()
        cnx.close()
        
        if not rows:
            print("No member records found.")
            return
        
        print(f"\n{'='*75}")
        print(f"  {'Code':<8} {'Name':<20} {'Mobile':<12} {'Type':<10} {'Email':<25}")
        print(f"\n{'='*75}")
        
        for r in rows:
            print(f"  {r[0]:<8} {r[1][:18]:<20} {str(r[2]):<12} {str(r[4]):<10} {str(r[3])[:23]:<25}")
        print(f"\n{'='*75}")
        
    except Exception as e:
        print("Error:", e)

def insertMember():
    try:
        cnx= get_connection()
        cursor= cnx.cursor()
        
        mno= input("Member Code :").strip()
        mname= input("Member Name:").strip()
        
        mob= input("Mobile No   :").strip()
        if not validate_mobile(mob):
            print("Invalid mobile number.")
            cursor.close()
            cnx.close()
            return
        
        email= input("Email address :").strip()
        if not validate_email(email):
            print("Invalid email id.")
            cursor.close()
            cnx.close()
            return
        
        print("Membership type:\n1.Student\n2.Faculty")
        t= input("Choice    :").strip()
        mem_type= "faculty" if t=='2' else "student"
        
        print("Date of membership   :")
        DD= int(input("Day  :"))
        MM= int(input("Month:"))
        YY= int(input("Year :"))
        
        addr= input("Address    :").strip()
        
        query= """INSERT INTO member (Mno, Mname, mob, email, mem_type, DOP, ADR)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)"""
        cursor.execute(query, (mno, mname, mob, email, mem_type, date(YY, MM, DD), addr))
        cnx.commit()
        
        print("Member record successfully inserted.")
        cursor.close()
        cnx.close()
        
    except Exception as e:
        print("Error:", e)

def deleteMember():
    try:
        cnx= get_connection()
        cursor= cnx.cursor()
        mno= input("Enter the member number to delete:").strip()
        
        cursor.execute("DELETE FROM member WHERE Mno= %s", (mno,))
        cnx.commit()
        
        print(f"{cursor.rowcount} record(s) deleted.")
        cursor.close()
        cnx.close()
        
    except Exception as e:
        print("Error:", e)

def searchMember():
    try:
        cnx= get_connection()
        cursor= cnx.cursor()
        
        name= input("Enter member name as you may recall:").strip()
        cursor.execute("SELECT * FROM member WHERE Mname LIKE %s", ('%'+ name+ '%',)) 
        rows= cursor.fetchall()
        
        cursor.close()
        cnx.close()
        
        if not rows:
            print("No matching member found.")
            return
        
        for r in rows:
            print(f"\nMember Code   : {r[0]}")
            print(f"Name            : {r[1]}")
            print(f"Mobile          : {r[2]}")
            print(f"Email id        : {r[3]}")
            print(f"Member-Type     : {r[4]}")
            print(f"Joined          : {r[5]}")
            print(f"Address         : {r[6]}")
        
        print(f"\n {len(rows)} record(s) found.")
    
    except Exception as e:
        print("Error:", e)

#  probable error in update function== must check again
def updateMember():
    try:
        cnx= get_connection()
        cursor= cnx.cursor()
        
        mno= input("Enter the member code to update :").strip()
        
        cursor.execute("SELECT * FROM member WHERE Mno= %s", (mno,))
        
        if not cursor.fetchone():
            print("Member not found.")
            cursor.close()
            cnx.close()
            return
        
        print("Enter new data   :")
        
        mname= input("Name          :").strip()
        mob= input("Mobile number   :").strip()
        if not validate_mobile(mob):
            print("Invalid mobile number.")
            cursor.close()
            cnx.close()
            return 
        
        email= input("Enter email id:").strip()
        if not validate_email(email):
            print("Invalid email id.")
            cursor.close()
            cnx.close()
            return 
        
        print("Type:\n1.Student\n2.Faculty")
        t= input("Choice:").strip()
        mem_type= 'faculty' if t=='2' else 'student'
        
        addr= input("Address         :").strip()
        
        query= """ UPDATE member
                    SET Mname= %s, mob= %s, email= %s, mem_type= %s, ADR= %s
                    WHERE Mno= %s"""
        
        cursor.execute(query, (mname, mob, email, mem_type, addr, mno))
        cursor.commit()
        
        print(f" {cursor.rowcount} record(s) updated.")
        cursor.close()
        cnx.close()
    
    except Exception as e:
        print("Error:", e)
    