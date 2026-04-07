# type: ignore
from db_connect import get_connection
from datetime import date, timedelta

FINE_PER_DAY= 2

def calculate_fine(issue_date, return_date, due_date):
    if return_date > due_date :
        overdue_days= (return_date - due_date).days
        return overdue_days * FINE_PER_DAY
    return 0

def issueBook():
    
    try:
        cnx= get_connection()
        cursor= cnx.cursor()
        
        bno= input("Enter book code to be issued    :").strip()
        mno= input("Enter your member code          :").strip()
        
        # should check once if there is such book or not. 
        # also if there is such member or not
        # else first insertMember() should be done by librarian
        # book check >>
        cursor.execute("SELECT Bname, avail_qty FROM bookrecord WHERE Bno= %s", (bno,))
        book= cursor.fetchone()
        
        if not book:
            print("Book not found in records.")
            cursor.close()
            cnx.close()
            return
        if book[1] <= 0:
            print(f" Regret to inform but the '{book[0]}' is currently not available. ")
            cursor.close()
            cnx.close()
            return
        
        # member check >>
        cursor.execute("SELECT Mname, mem_type FROM member WHERE Mno= %s", (mno,))
        member= cursor.fetchone()
        
        if not member:
            print("Member not found.")
            cursor.close()
            cnx.close()
            return
        
        issue_date= date.today()
        due_date= issue_date + timedelta(days= 7) #7days due
        
        cursor.execute("INSERT INTO issue (Bno, Mno, d_o_issue, due_date) VALUES (%s, %s, %s, %s)", 
            (bno, mno, issue_date, due_date))
        
        # reduce the avail-qty of the book taken
        cursor.execute("UPDATE bookrecord SET avail_qty = avail_qty - 1 WHERE Bno= %s", (bno,))
        cnx.commit()
    # why cnx.commit() and not cursor.commit() here?? I am confused here ....

        print(f"\nBook issued successfully.")
        print(f"Book     :{book[0]}")
        print(f"Member   : {member[0]} ({member[1]})")
        print(f"Issued   : {issue_date}")
        print(f"Due by   : {due_date}")
        
        cursor.close()
        cnx.close()
        
    except Exception as e:
        print("Error:", e)

def returnBook():
    try:
        cnx= get_connection()
        cursor= cnx.cursor()
        
        bno= input("Book code to be returned:").strip()
        mno= input("Enter your member code:").strip()
        
        cursor.execute(
            """SELECT issue_id, d_o_issue, due_date
            FROM issue 
            WHERE Bno= %s AND Mno= %s AND d_o_ret IS NULL
            ORDER BY d_o_issue DESC LIMIT 1""", (bno, mno))
        
        record= cursor.fetchone()
        
        if not record:
            print("No active issue found for this book and member.")
            cursor.close()
            cnx.close()
            return 
        
        issue_id= record[0]
        issue_date= record[1]
        due_date= record[2]
        return_date= date.today()
        
        fine= calculate_fine(issue_date, return_date, due_date)
        
        #to set the return date and fine
        cursor.execute(
            "UPDATE issue SET d_o_ret= %s, fine= %s, WHERE issue_id= %s", (return_date, fine, issue_id))
        
        #count avail_qty+1
        cursor.execute(
            "UPDATE bookrecord SET avail_qty= avail_qty+1 WHERE Bno= %s", (bno,))
        
        cnx.commit()
        
        print(f"\nBook returned successfully.")
        print(f"Issue Date  : {issue_date}")
        print(f"Due date    : {due_date}" )
        print(f"Return date : {return_date}")
        
        if fine>0:
            overdue= (return_date - due_date).days
            print(f"Overdue     : {overdue} day(s)")
            print(f"Fine        : {fine} (Rs.{FINE_PER_DAY}*{overdue} days)")
        else:
            print("Fine     : Rs 0 (returned within time)")
        
        cursor.close()
        cnx.close()
    
    except Exception as e:
        print("Error:", e)


def showIssuedBooks():
    try:
        cnx= get_connection()
        cursor= cnx.cursor()
        
        cursor.execute(
            """SELECT B.Bno, B.Bname, M.Mname, I.d_o_issue, I.due_date, I.d_o_ret, I.fine
            FROM bookrecord B 
            JOIN issue I ON B.Bno= I.Bno
            JOIN member M ON M.Mno= I.Mno
            ORDER BY I.d_o_issue DESC"""
        )
        
        rows= cursor.fetchall()
        cursor.close()
        cnx.close()
        
        if not rows:
            print("No issue records found.")
            return 
        
        print(f"\n{'='*80}")
        print(f"  {'BookCode':<10} {'Title':<22} {'MemberCode':<12} {'Member':<18} {'Due':<12} {'Status'}")
        print(f"{'='*80}")
        
        for r in rows:
            status= "Returned" if r[6] else ("OVERDUE" if r[5]< date.today() else "Issued")
            fine_info= f"  Fine:₹{r[7]}" if r[7] else ""
            print(f"{r[0]:<10} {r[1][:20]:<22} {r[2]:<12} {r[3][:16]:<18} {str(r[5]):<12} {status}{fine_info}")
        print(f"{'='*80}\n")
    
    except Exception as e:
        print("  Error:", e)

def showOverdueBooks():
    try:
        cnx= get_connection()
        cursor= cnx.cursor()
        cursor.execute(
            """SELECT B.Bname, M.mob, M.email, I.d_o_issue, I.due_date,
            DATEDIFF(CURDATE(), I.due_date) AS overdue_days,
            DATEDIFF(CURDATE(), I.due_date)* %s AS projected_fine
            FROM issue I
            JOIN bookrecord B ON B.Bno= I.Bno
            JOIN member M ON M.Mno= I.Mno
            WHERE I.d_o_ret IS NULL AND I.due_date < CURDATE()
            ORDER BY overdue_days DESC""", (FINE_PER_DAY,)
        )
        
        rows= cursor.fetchall()
        cursor.close()
        cnx.close()
        
        if not rows:
            print("No overdue books found.")
            return 
        
        print(f"\n *** OVERDUE BOOKS REPORT ***")
        print(f"{'='*70}")
        
        for r in rows:
            print(f"Book        : {r[0]}")
            print(f"Member      : {r[1]}  | Mobile: {r[2]}  |  Email: {r[3]}")
            print(f"Due         : {r[5]}  | Overdue: {r[6]} day(s)")
            print(f"Projected Fine: ₹{r[7]}")
            print(f" {'-'*50}")
            
        print(f"{'='*70}")
    
    except Exception as e:
        print("Error:", e)     