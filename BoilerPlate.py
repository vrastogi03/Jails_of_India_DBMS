import subprocess as sp
import pymysql
import pymysql.cursors
import getpass
import re

regex = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'


def check(email):
    if (re.search(regex, email)):
        return 1

    else:
        return 0


def prisoner(jid):
    print("1. Insert a tuple")
    print("2. Delete a tuple")
    print("3. Update a tuple")
    print("4. Calculate the age of the prisoner")
    print("5. Calculate the period of captivity left for a prisoner")
    print("6. Calculate the monthly wage of a prisoner")

    val = int(input("Choose the query you want to execute> "))
    if val == 1:
        try:
            row = {}
            print("Enter new prisoner's details: ")
            row["PId"] = int(input("Prisoner Id: "))
            name = (input("Name (Fname Lname): ")).split(' ')
            row["Fname"] = name[0]
            row["Lname"] = name[1]
            row["jid"] = int(input("Jail id: "))
            row["dname"] = input("Department name: ")
            row["Add"] = input("Address: ")
            row["confperiod"] = int(input("ConfinementPeriod(in years): "))
            row["DOB"] = input("Birth Date (YYYY-MM-DD): ")
            row["DOI"] = input("DateofImprisonment (YYYY-MM-DD): ")

            if (row["jid"] == jid):

                dob = str(row["DOB"])
                doi = str(row["DOI"])
                listdob = dob.split("-")
                listdoi = doi.split("-")
                dobint = int(listdob[0])
                doiint = int(listdoi[0])
                # print(dobint,doiint);
                if (doiint - dobint >= 16):

                    query = "INSERT INTO PRISONER VALUES('%d', '%s', '%s', '%d', '%s', '%s', '%d', '%s', '%s')" % (
                    row["PId"], row["Fname"], row["Lname"], row["jid"], row["dname"], row["Add"], row["confperiod"],
                    row["DOB"], row["DOI"])
                    cur.execute(query)
                    con.commit()

                    query = "INSERT INTO PWORKSFOR VALUES('%d','%d','%s')" % (row["PId"], row["jid"], row["dname"])
                    cur.execute(query)
                    con.commit()

                    query = "SELECT DHeadId FROM DEPARTMENT WHERE DJailId='%d' AND DName='%s' " % (
                    row["jid"], row["dname"])
                    cur.execute(query);
                    result = cur.fetchall()
                    poid = result[0]['DHeadId']
                    # print(poid)
                    # print(cur.fetchall())

                    # ***************************************************************************************
                    query = "SELECT COUNT(*) FROM JWORKSFOR WHERE JId='%d' AND DName='%s'" % (row["jid"], row["dname"])
                    cur.execute(query)
                    result = cur.fetchall()
                    cnt = result[0]['COUNT(*)']
                    if (cnt == 0):
                        query = "INSERT INTO JWORKSFOR VALUES('%d','%s','%d')" % (row["jid"], row["dname"], poid)
                        cur.execute(query)
                        con.commit()
                    # ***************************************************************************************

                    print("Inserted into Database")
                    print("")

                else:
                    print("Age must be greater than 16 years at time of imprisonment \n")

            else:
                print("You can insert only in your jail")
                print("")

        except Exception as e:
            con.rollback()
            print("Failed to insert into database")
            print("***", e, "***")

    if val == 2:
        try:
            pid = int(input("Please Enter the Prisoner id you want to delete> "))
            query = "SELECT PJailId FROM PRISONER WHERE (PId = '%d')" % (pid)
            cur.execute(query)
            result = cur.fetchall()
            if result[0]['PJailId'] == jid:
                query = "DELETE FROM PRISONER WHERE (PId = '%d')" % (pid)
                cur.execute(query)
                con.commit()

                print("Deleted from Database")
                print("")
            else:
                print("You can delete only in your jail")
                print("")

        except Exception as e:
            con.rollback()
            print("Failed to delete from database")
            print("***", e, "***")

    if val == 3:
        pid = int(input("Please Enter the Prisoner id whose attribute you want to modify> "))
        print("1. Prisoner Id")
        print("2. Prisoner First Name")
        print("3. Prisoner Last Name")
        print("4. Prisoner Jail Id")
        print("5. Prisoner Department Name")
        print("6. Prisoner Add")
        print("7. Prisoner Confinement Period")
        print("8. Prisoner DOB")
        print("9. Prisoner Date of Imprisonment")
        valu = int(input("Choose the Attribute you want to modify> "))
        try:
            query = "SELECT PJailId FROM PRISONER WHERE (PId = '%d')" % (pid)
            cur.execute(query)
            result = cur.fetchall()
            if result[0]['PJailId'] == jid:
                if valu == 1:
                    inp = int(input("Please enter the new value> "))

                    query = "SET FOREIGN_KEY_CHECKS=0;"
                    cur.execute(query)
                    con.commit()

                    query = "UPDATE PRISONER SET PId = '%d' WHERE PId = '%d'" % (inp, pid)
                    cur.execute(query)
                    con.commit()

                    query = "UPDATE CRIME SET CPId = '%d' WHERE CPId = '%d'" % (inp, pid)
                    cur.execute(query)
                    con.commit()

                    query = "UPDATE VISITOR SET VPId = '%d' WHERE VPId = '%d'" % (inp, pid)
                    cur.execute(query)
                    con.commit()

                    query = "UPDATE VISITORCONTACT SET VPId = '%d' WHERE VPId = '%d'" % (inp, pid)
                    cur.execute(query)
                    con.commit()

                    query = "UPDATE PWORKSFOR SET PId = '%d' WHERE PId = '%d'" % (inp, pid)
                    cur.execute(query)
                    con.commit()

                    query = "SET FOREIGN_KEY_CHECKS=1;"
                    cur.execute(query)
                    con.commit()

                    print("Udated in Database")
                    print("")

                if valu == 2:
                    inp = input("Please enter the new value> ")
                    query = "UPDATE PRISONER SET PFirstName = '%s' WHERE PId = '%d'" % (inp, pid)
                    cur.execute(query)
                    con.commit()

                    print("Udated in Database")
                    print("")

                if valu == 3:
                    inp = input("Please enter the new value> ")
                    query = "UPDATE PRISONER SET PLastName = '%s' WHERE PId = '%d'" % (inp, pid)
                    cur.execute(query)
                    con.commit()

                    print("Udated in Database")
                    print("")

                if valu == 4:
                    inp = int(input("Please enter the new value> "))

                    query = "SET FOREIGN_KEY_CHECKS=0;"
                    cur.execute(query)
                    con.commit()

                    query = "UPDATE PRISONER SET PJailId = '%d' WHERE PId = '%d'" % (inp, pid)
                    cur.execute(query)
                    con.commit()

                    query = "UPDATE PWORKSFOR SET JId = '%d' WHERE PId = '%d'" % (inp, pid)
                    cur.execute(query)
                    con.commit()

                    query = "SELECT PDname FROM PRISONER WHERE PId ='%d' " % (pid)
                    cur.execute(query)
                    result = cur.fetchall()
                    dname = result[0]['PDname']

                    query = "SELECT DHeadId FROM DEPARTMENT WHERE DJailId='%d' AND DName='%s' " % (inp, dname)
                    cur.execute(query);
                    result = cur.fetchall()
                    poid = result[0]['DHeadId']
                    # print(poid)
                    # print(cur.fetchall())

                    # ***************************************************************************************
                    query = "SELECT COUNT(*) FROM JWORKSFOR WHERE JId='%d' AND DName='%s'" % (inp, dname)
                    cur.execute(query)
                    result = cur.fetchall()
                    cnt = result[0]['COUNT(*)']
                    if (cnt == 0):
                        query = "INSERT INTO JWORKSFOR VALUES('%d','%s','%d')" % (inp, dname, poid)
                        cur.execute(query)
                        con.commit()
                    # ***************************************************************************************

                    query = "SET FOREIGN_KEY_CHECKS=1;"
                    cur.execute(query)
                    con.commit()

                    print("Udated in Database")
                    print("")
                # *****************
                if valu == 5:
                    inp = input("Please enter the new value> ")

                    query = "SET FOREIGN_KEY_CHECKS=0;"
                    cur.execute(query)
                    con.commit()

                    query = "UPDATE PRISONER SET PDname = '%s' WHERE PId = '%d'" % (inp, pid)
                    cur.execute(query)
                    con.commit()

                    query = "UPDATE PWORKSFOR SET DName = '%s' WHERE PId = '%d'" % (inp, pid)
                    cur.execute(query)
                    con.commit()

                    query = "SET FOREIGN_KEY_CHECKS=1;"
                    cur.execute(query)
                    con.commit()

                    print("Udated in Database")
                    print("")

                if valu == 6:
                    inp = input("Please enter the new value> ")
                    query = "UPDATE PRISONER SET PAdd = '%s' WHERE PId = '%d'" % (inp, pid)
                    cur.execute(query)
                    con.commit()

                    print("Udated in Database")
                    print("")

                if valu == 7:
                    inp = int(input("Please enter the new value> "))
                    query = "UPDATE PRISONER SET PConfinementPeriod = '%d' WHERE PId = '%d'" % (inp, pid)
                    cur.execute(query)
                    con.commit()

                    print("Udated in Database")
                    print("")

                if valu == 8:
                    inp = input("Please enter the new value> ")
                    query = "UPDATE PRISONER SET PDOB = '%s' WHERE PId = '%d'" % (inp, pid)
                    cur.execute(query)
                    con.commit()

                    print("Udated in Database")
                    print("")

                if valu == 9:
                    inp = input("Please enter the new value> ")
                    query = "UPDATE PRISONER SET PDateofImprisonment = '%s' WHERE PId = '%d'" % (inp, pid)
                    cur.execute(query)
                    con.commit()

                    print("Udated in Database")
                    print("")
            else:
                print("You can modify only in your jail")
                print("")
        except Exception as e:
            con.rollback()
            print("Failed to update in database")
            print("***", e, "***")

    if val == 4:
        try:
            pid = int(input("Please Enter the Prisoner's id whose age you want to Calculate > "))
            query = "SELECT PJailId FROM PRISONER WHERE (PId = '%d')" % (pid)
            cur.execute(query)
            result = cur.fetchall()
            if result[0]['PJailId'] == jid:

                query = "SELECT TIMESTAMPDIFF (YEAR, PDOB, CURDATE()) FROM PRISONER WHERE PId = '%d'" % (pid)
                cur.execute(query)
                age = cur.fetchall()
                print("The age is ", end='')
                print(age[0]['TIMESTAMPDIFF (YEAR, PDOB, CURDATE())'])
                print("")
            else:
                print("You can access only in your jail")
                print("")

        except Exception as e:
            con.rollback()
            print("Failed to find from database")
            print("***", e, "***")

    if val == 5:
        try:
            pid = int(
                input("Please Enter the Prisoner's id whose the period of captivity left you want to find out > "))
            query = "SELECT PJailId FROM PRISONER WHERE (PId = '%d')" % (pid)
            cur.execute(query)
            result = cur.fetchall()
            if result[0]['PJailId'] == jid:
                query = "SELECT TIMESTAMPDIFF (YEAR, PDateofImprisonment, CURDATE()) FROM PRISONER WHERE PId = '%d'" % (
                    pid)
                cur.execute(query)
                spend = cur.fetchall()

                query = "SELECT PConfinementPeriod FROM PRISONER WHERE PId = '%d'" % (pid)
                cur.execute(query)
                Confinement_Period = cur.fetchall()

                print("The period of captivity left is ", end="")
                print(Confinement_Period[0]['PConfinementPeriod'] - spend[0][
                    'TIMESTAMPDIFF (YEAR, PDateofImprisonment, CURDATE())'])
                print("")
            else:
                print("You can access only in your jail")
                print("")

        except Exception as e:
            con.rollback()
            print("Failed to find from database")
            print("***", e, "***")
    if val == 6:
        try:
            pid = int(input("Please Enter the Prisoner's id whose monthly wage you want to find out > "))
            query = "SELECT PJailId,DWorkHours,DWage FROM PRISONER,DEPARTMENT WHERE (PDname=DName AND PJailId=DJailId AND PId = '%d')" % (
                pid)
            cur.execute(query)
            result = cur.fetchall()
            if result[0]['PJailId'] == jid:

                hrs = result[0]['DWorkHours']
                wage = result[0]['DWage']
                print("Monthly wage of the asked prisoner with PId->", pid, " is>> ", 4 * hrs * wage)
                print("")

            else:

                print("You can access only in your jail")
                print("")

        except Exception as e:
            con.rollback()
            print("Failed to find from database")
            print("***", e, "***")

    a = input("<< press any key to continue >> \n")
    temp = sp.call('clear', shell=True)


def crime(jid):
    print("1. Insert a tuple")
    print("2. Delete a tuple")
    print("3. Update a tuple")
    val = int(input("Choose the query you want to execute> "))

    if val == 1:
        try:
            row = {}
            print("Enter new crime details: ")
            row["CPId"] = int(input("Prisoner Id: "))
            row["CType"] = input("Crime Type: ")
            row["CDate"] = input("Crime Date (YYYY-MM-DD): ")
            row["CLocation"] = input("Crime Location: ")

            query = "SELECT PJailId FROM PRISONER WHERE (PId = '%d')" % (row["CPId"])
            cur.execute(query)
            result = cur.fetchall()
            if result[0]['PJailId'] == jid:
                query = "INSERT INTO CRIME VALUES('%d', '%s', '%s', '%s')" % (
                row["CPId"], row["CType"], row["CDate"], row["CLocation"])
                cur.execute(query)
                con.commit()

                print("Inserted into Database")
                print("")

            else:
                print("You can insert only in your jail")
                print("")

        except Exception as e:
            con.rollback()
            print("Failed to insert into database")
            print("***", e, "***")

    if val == 2:
        try:
            cpid = int(input("Please Enter the Prisoner's id whose crime data you want to delete> "))
            ctype = input("Please Enter the corresponding crime type> ")

            query = "SELECT PJailId FROM PRISONER WHERE (PId = '%d')" % (cpid)
            cur.execute(query)
            result = cur.fetchall()
            if result[0]['PJailId'] == jid:
                query = "DELETE FROM CRIME WHERE (CPId = '%d' AND CType = '%s')" % (cpid, ctype)
                cur.execute(query)
                con.commit()

                print("Deleted from Database")
                print("")
            else:
                print("You can delete only in your jail")
                print("")

        except Exception as e:
            con.rollback()
            print("Failed to delete from database")
            print("***", e, "***")

    if val == 3:
        cpid = int(input("Please Enter the Prisoner id whose attribute you want to modify> "))
        ctype = input("Please Enter the corresponding crime type> ")

        print("1. Crime Type")
        print("2. Crime Date")
        print("3. Crime Location")
        valu = int(input("Choose the Attribute you want to modify> "))
        try:
            query = "SELECT PJailId FROM PRISONER WHERE (PId = '%d')" % (cpid)
            cur.execute(query)
            result = cur.fetchall()
            if result[0]['PJailId'] == jid:
                if valu == 1:
                    inp = input("Please enter the new value> ")

                    query = "UPDATE CRIME SET CType = '%s' WHERE (CPId = '%d' AND CType = '%s')" % (inp, cpid, ctype)
                    cur.execute(query)
                    con.commit()

                    print("Updated in Database")
                    print("")

                if valu == 2:
                    inp = input("Please enter the new value> ")

                    query = "UPDATE CRIME SET CDate = '%s' WHERE (CPId = '%d' AND CType = '%s')" % (inp, cpid, ctype)
                    cur.execute(query)
                    con.commit()

                    print("Udated in Database")
                    print("")

                if valu == 3:
                    inp = input("Please enter the new value> ")

                    query = "UPDATE CRIME SET CLocation = '%s' WHERE (CPId = '%d' AND CType = '%s')" % (
                    inp, cpid, ctype)
                    cur.execute(query)
                    con.commit()

                    print("Udated in Database")
                    print("")

            else:
                print("You can update only in your jail")
                print("")

        except Exception as e:
            con.rollback()
            print("Failed to update from database")
            print("***", e, "***")
    a = input("<< press any key to continue >> \n")
    temp = sp.call('clear', shell=True)


def jail():
    print("1. Insert a tuple")
    print("2. Delete a tuple")
    print("3. Update a tuple")
    print("4. Find monthly expenditure of a particular jail ")
    val = int(input("Choose the query you want to execute> "))
    if val == 1:
        try:
            row = {}
            print("Enter new Jail's details: ")
            row["JId"] = int(input("Jail Id: "))
            row["Jname"] = input("Jail name: ")
            row["JAdd"] = input("Jail Address: ")
            row["JCapacity"] = int(input("Jail Capacity: "))

            query = "INSERT INTO JAIL VALUES('%d', '%s', '%s', '%d')" % (
            row["JId"], row["Jname"], row["JAdd"], row["JCapacity"])
            cur.execute(query)
            con.commit()

            print("Inserted into Database")
            print("")


        except Exception as e:
            con.rollback()
            print("Failed to insert into database")
            print("***", e, "***")

    if val == 2:
        try:
            jid = int(input("Please Enter the Jail id you want to delete> "))
            query = "DELETE FROM JAIL WHERE (JId = '%d')" % (jid)
            cur.execute(query)
            con.commit()

            print("Deleted from Database")
            print("")

        except Exception as e:
            con.rollback()
            print("Failed to delete from database")
            print("***", e, "***")

    if val == 3:
        jid = int(input("Please Enter the Jail id whose attribute you want to modify> "))
        print("1. Jail Id")
        print("2. Jail Name")
        print("3. Jail Address")
        print("4. Jail Capacity")
        valu = int(input("Choose the Attribute you want to modify> "))
        try:
            if valu == 1:
                inp = int(input("Please enter the new value> "))

                query = "SET FOREIGN_KEY_CHECKS=0;"
                cur.execute(query)
                con.commit()

                query = "UPDATE JAIL SET JId = '%d' WHERE JId = '%d'" % (inp, jid)
                cur.execute(query)
                con.commit()

                query = "UPDATE POLICEOFFICER SET POJailId = '%d' WHERE POJailId = '%d'" % (inp, jid)
                cur.execute(query)
                con.commit()

                query = "UPDATE DEPARTMENT SET DJailId = '%d' WHERE DJailId = '%d'" % (inp, jid)
                cur.execute(query)
                con.commit()

                query = "UPDATE PRISONER SET PJailId = '%d' WHERE PJailId = '%d'" % (inp, jid)
                cur.execute(query)
                con.commit()

                query = "UPDATE PWORKSFOR SET JId = '%d' WHERE JId = '%d'" % (inp, jid)
                cur.execute(query)
                con.commit()

                query = "UPDATE JWORKSFOR SET JId = '%d' WHERE JId = '%d'" % (inp, jid)
                cur.execute(query)
                con.commit()

                query = "SET FOREIGN_KEY_CHECKS=1;"
                cur.execute(query)
                con.commit()

                print("Udated in Database")
                print("")

            if valu == 2:
                inp = input("Please enter the new value> ")

                query = "UPDATE JAIL SET JName = '%s' WHERE JId = '%d'" % (inp, jid)
                cur.execute(query)
                con.commit()

                print("Udated in Database")
                print("")

            if valu == 3:
                inp = input("Please enter the new value> ")

                query = "UPDATE JAIL SET JAdd = '%s' WHERE JId = '%d'" % (inp, jid)
                cur.execute(query)
                con.commit()

                print("Udated in Database")
                print("")

            if valu == 4:
                inp = int(input("Please enter the new value> "))

                query = "UPDATE JAIL SET JCapacity = '%s' WHERE JId = '%d'" % (inp, jid)
                cur.execute(query)
                con.commit()

                print("Udated in Database")
                print("")

        except Exception as e:
            con.rollback()
            print("Failed to delete from database")
            print("***", e, "***")

    if val == 4:
        try:
            expenditure = 0;
            jid = int(input("Please Enter the Jails's id whose monthly expenditure you want to find out > "))
            query = "SELECT JName from JAIL WHERE JId='%d'" % (jid)
            cur.execute(query)
            result = cur.fetchall()
            jname = result[0]['JName']
            # print(jname)
            print(result)
            query = "SELECT PId,DWorkHours,DWage FROM PRISONER,DEPARTMENT WHERE (PDname=DName AND PJailId=DJailId AND PJailId = '%d')" % (
                jid)
            cur.execute(query)
            result = cur.fetchall()

            for prisoner in result:
                hrs = prisoner['DWorkHours']
                wage = prisoner['DWage']
                expenditure += 4 * hrs * wage;

            query = "SELECT SUM(POSalary) FROM POLICEOFFICER WHERE POJailId= '%d' " % (jid)
            cur.execute(query)
            result = cur.fetchall()
            # print(result[0]['SUM(POSalary)'])
            expenditure += result[0]['SUM(POSalary)']
            print("Total expenditure for the", jname, "with id=", jid, "is ->", expenditure)
            print("")
        # print(prisoner['PId'],hrs,wage)

        except Exception as e:
            con.rollback()
            print("Failed to find from database")
            print("***", e, "***")
    a = input("<< press any key to continue >> \n")
    temp = sp.call('clear', shell=True)


def policeofficer():
    print("1. Insert a tuple")
    print("2. Delete a tuple")
    print("3. Update a tuple")
    print("4. Calculate Age of Police Officer")

    val = int(input("Choose the query you want to execute> "))
    if val == 1:
        try:
            row = {}
            print("Enter new Police Officer's details: ")
            row["POId"] = int(input("Prisoner Id: "))
            name = (input("Name (Fname Lname): ")).split(' ')
            row["Fname"] = name[0]
            row["Lname"] = name[1]
            row["POJailId"] = int(input("Jail id: "))
            row["POAdd"] = input("Address: ")
            row["PODOB"] = input("Birth Date (YYYY-MM-DD): ")
            row["POSalary"] = int(input("Salary: "))
            row["DOP"] = input("DateofPosting (YYYY-MM-DD): ")
            row["JobType"] = input("JobType (Jailer or Guard): ")

            if (row["JobType"] == "Jailer" or row["JobType"] == "Guard"):
                query = "INSERT INTO POLICEOFFICER VALUES('%d', '%s', '%s', '%d', '%s', '%s', '%d', '%s', '%s')" % (
                row["POId"], row["Fname"], row["Lname"], row["POJailId"], row["POAdd"], row["PODOB"], row["POSalary"],
                row["DOP"], row["JobType"])
                cur.execute(query)
                con.commit()

                print("Inserted into Database")
                print("")
            else:
                print("INVALID JOB TYPE\n")


        except Exception as e:
            con.rollback()
            print("Failed to insert into database")
            print("***", e, "***")

    if val == 2:
        try:
            poid = int(input("Please Enter the Police Officer id you want to delete> "))
            query = "DELETE FROM POLICEOFFICER WHERE (POId = '%d')" % (poid)
            cur.execute(query)
            con.commit()

            print("Deleted from Database")
            print("")


        except Exception as e:
            con.rollback()
            print("Failed to delete from database")
            print("***", e, "***")

    if val == 3:
        poid = int(input("Please Enter the Police Officer id whose attribute you want to modify> "))
        print("1. Police Officer Id")
        print("2. Police Officer First Name")
        print("3. Police Officer Last Name")
        print("4. Police Officer Add")
        print("5. Police Officer DOB")
        print("6. Police Officer Salary")
        print("7. Police Officer Date of Posting")
        print("8. Police Officer Job Type")
        valu = int(input("Choose the Attribute you want to modify> "))
        try:
            if valu == 1:
                inp = int(input("Please enter the new value> "))

                query = "SET FOREIGN_KEY_CHECKS=0;"
                cur.execute(query)
                con.commit()

                query = "UPDATE POLICEOFFICER SET POId = '%d' WHERE POId = '%d'" % (inp, poid)
                cur.execute(query)
                con.commit()

                query = "UPDATE DEPARTMENT SET DHeadId = '%d' WHERE DHeadId = '%d'" % (inp, poid)
                cur.execute(query)
                con.commit()

                query = "UPDATE JWORKSFOR SET POId = '%d' WHERE POId = '%d'" % (inp, poid)
                cur.execute(query)
                con.commit()

                query = "UPDATE POLICEOFFICERCONTACT SET POId = '%d' WHERE POId = '%d'" % (inp, poid)
                cur.execute(query)
                con.commit()

                query = "UPDATE POLICEOFFICEREMAIL SET POId = '%d' WHERE POId = '%d'" % (inp, poid)
                cur.execute(query)
                con.commit()

                query = "SET FOREIGN_KEY_CHECKS=1;"
                cur.execute(query)
                con.commit()

                print("Udated in Database")
                print("")

            if valu == 2:
                inp = input("Please enter the new value> ")
                query = "UPDATE POLICEOFFICER SET POFName = '%s' WHERE POId = '%d'" % (inp, poid)
                cur.execute(query)
                con.commit()

                print("Udated in Database")
                print("")

            if valu == 3:
                inp = input("Please enter the new value> ")
                query = "UPDATE POLICEOFFICER SET POLName = '%s' WHERE POId = '%d'" % (inp, poid)
                cur.execute(query)
                con.commit()

                print("Udated in Database")
                print("")

            if valu == 4:
                inp = input("Please enter the new value> ")

                query = "UPDATE POLICEOFFICER SET POAdd = '%s' WHERE POId = '%d'" % (inp, poid)
                cur.execute(query)
                con.commit()

                print("Udated in Database")
                print("")

            if valu == 5:
                inp = input("Please enter the new value> ")
                query = "UPDATE POLICEOFFICER SET PODOB = '%s' WHERE POId = '%d'" % (inp, poid)
                cur.execute(query)
                con.commit()

                print("Udated in Database")
                print("")

            if valu == 6:
                inp = int(input("Please enter the new value> "))
                query = "UPDATE POLICEOFFICER SET POSalary = '%d' WHERE POId = '%d'" % (inp, poid)
                cur.execute(query)
                con.commit()

                print("Udated in Database")
                print("")

            if valu == 7:
                inp = input("Please enter the new value> ")
                query = "UPDATE POLICEOFFICER SET PODateofPosting = '%s' WHERE POId = '%d'" % (inp, poid)
                cur.execute(query)
                con.commit()

                print("Udated in Database")
                print("")

            if valu == 8:
                inp = input("Please enter the new value> ")
                if (inp == "Jailer" or inp == "Guard"):

                    query = "UPDATE POLICEOFFICER SET JobType = '%s' WHERE POId = '%d'" % (inp, poid)
                    cur.execute(query)
                    con.commit()

                    print("Updated in Database")
                    print("")
                else:
                    print("INVALID INPUT\n")

        except Exception as e:
            con.rollback()
            print("Failed to update in database")
            print("***", e, "***")

    if val == 4:
        try:
            poid = int(input("Please Enter the Police Officer's id whose age you want to Calculate > "))
            query = "SELECT TIMESTAMPDIFF (YEAR, PODOB, CURDATE()) FROM POLICEOFFICER WHERE POId = '%d'" % (poid)
            cur.execute(query)
            age = cur.fetchall()
            print("The age is ", end="")
            print(age[0]['TIMESTAMPDIFF (YEAR, PODOB, CURDATE())'])
            print("")


        except Exception as e:
            con.rollback()
            print("Failed to find from database")
            print("***", e, "***")
    a = input("<< press any key to continue >> \n")
    temp = sp.call('clear', shell=True)


def policeofficercontact():
    print("1. Insert a tuple")
    print("2. Delete a tuple")
    print("3. Update a tuple")
    val = int(input("Choose the query you want to execute> "))

    if val == 1:
        try:
            row = {}
            print("Enter new police officer's contact details: ")

            row["POId"] = int(input("Police Officer Id: "))
            row["POContact"] = input(" Police Officer Contact: ")
            num = int(row["POContact"]);
            # print(num);
            if (num >= 6000000000 and num < 10000000000):
                query = "INSERT INTO POLICEOFFICERCONTACT VALUES('%d', '%s')" % (row["POId"], row["POContact"])
                cur.execute(query)
                con.commit()

                print("Inserted into Database")
                print("")
            else:
                print("INVALID CONTACT NUMBER\n")


        except Exception as e:
            con.rollback()
            print("Failed to insert into database")
            print("***", e, "***")

    if val == 2:
        try:
            poid = int(input("Please Enter the police officer's id whose data you want to delete> "))
            pocontact = input("Please Enter the corresponding contact> ")

            query = "DELETE FROM POLICEOFFICERCONTACT WHERE (POId = '%d' AND POContact = '%s')" % (poid, pocontact)
            cur.execute(query)
            con.commit()

            print("Deleted from Database")
            print("")

        except Exception as e:
            con.rollback()
            print("Failed to delete from database")
            print("***", e, "***")

    if val == 3:

        try:
            poid = int(input("Please Enter the police officer's id whose data you want to update> "))
            pocontact = input("Please Enter the corresponding contact> ")

            inp = input("Please enter the new contact> ")
            num = int(inp)
            if (num >= 6000000000 and num < 10000000000):
                query = "UPDATE POLICEOFFICERCONTACT SET POContact = '%s' WHERE (POId = '%d' AND POContact = '%s')" % (
                inp, poid, pocontact)
                cur.execute(query)
                con.commit()

            else:
                print("INVALID CONTACT NUMBER")

            print("Updated in Database")
            print("")


        except Exception as e:
            con.rollback()
            print("Failed to update from database")
            print("***", e, "***")

    a = input("<< press any key to continue >> \n")
    temp = sp.call('clear', shell=True)


def policeofficeremail():
    print("1. Insert a tuple")
    print("2. Delete a tuple")
    print("3. Update a tuple")
    val = int(input("Choose the query you want to execute> "))

    if val == 1:
        try:
            row = {}
            print("Enter new police officer's email details: ")
            row["POId"] = int(input("Police Officer Id: "))
            row["POEmail"] = input(" Police Officer Email: ")
            email = row["POEmail"]
            if check(email) == 1:
                query = "INSERT INTO POLICEOFFICEREMAIL VALUES('%d', '%s')" % (row["POId"], row["POEmail"])
                cur.execute(query)
                con.commit()

                print("Inserted into Database")
                print("")
            else:
                print("Wrong email format")


        except Exception as e:
            con.rollback()
            print("Failed to insert into database")
            print("***", e, "***")

    if val == 2:
        try:
            poid = int(input("Please Enter the police officer's id whose data you want to delete> "))
            poemail = input("Please Enter the corresponding email> ")

            query = "DELETE FROM POLICEOFFICEREMAIL WHERE (POId = '%d' AND POEmail = '%s')" % (poid, poemail)
            cur.execute(query)
            con.commit()

            print("Deleted from Database")
            print("")


        except Exception as e:
            con.rollback()
            print("Failed to delete from database")
            print("***", e, "***")

    if val == 3:

        try:
            poid = int(input("Please Enter the police officer's id whose data you want to update> "))
            poemail = input("Please Enter the corresponding email> ")

            inp = input("Please enter the new contact> ")
            email = inp

            if check(email) == 1:

                query = "UPDATE POLICEOFFICERCONTACT SET POEmail = '%s' WHERE (POId = '%d' AND POEmail = '%s')" % (
                inp, poid, poemail)
                cur.execute(query)
                con.commit()

                print("Udated in Database")
                print("")
            else:
                print("Wrong email format")


        except Exception as e:
            con.rollback()
            print("Failed to update from database")
            print("***", e, "***")
    a = input("<< press any key to continue >> \n")
    temp = sp.call('clear', shell=True)


def avgexpense():
    try:

        expenditure = 0;
        query = "SELECT JId from JAIL";
        cur.execute(query);
        result = cur.fetchall()
        for jail in result:
            jid = jail['JId']
            # print(jid)
            query = "SELECT PId,DWorkHours,DWage FROM PRISONER,DEPARTMENT WHERE (PDname=DName AND PJailId=DJailId AND PJailId = '%d')" % (
                jid)
            cur.execute(query)
            result2 = cur.fetchall()
            for prisoner in result2:
                hrs = prisoner['DWorkHours']
                wage = prisoner['DWage']
                expenditure += 4 * hrs * wage;

            query = "SELECT SUM(POSalary) FROM POLICEOFFICER WHERE POJailId= '%d' " % (jid)
            cur.execute(query)
            result2 = cur.fetchall()
            expenditure += result2[0]['SUM(POSalary)']

        query = "SELECT COUNT(*) FROM PRISONER"
        cur.execute(query)
        result = cur.fetchall()
        cnt = result[0]['COUNT(*)']

        print("Average Government expenditure per prisoner -> ", expenditure / cnt)
        print("")


    except Exception as e:
        con.rollback()
        print("Failed to find from database")
        print("***", e, "***")

    a = input("<< press any key to continue >> \n")
    temp = sp.call('clear', shell=True)


def access(ch, Id):
    cur = con.cursor()
    if ch == 1:
        query = "SELECT POJailId FROM POLICEOFFICER WHERE (POId = '%d')" % (Id)
        cur.execute(query)
        result = cur.fetchall()
        jid = result[0]['POJailId']
        print(
            "You have access only to the tuples that are related to your Jail with JailId '%d' in the database" % (jid))
        while (1):
            print("1. PRISONER")
            print("2. CRIME")
            print("3. DEPARTMENT")
            print("4. VISITOR")
            print("5. VISITORCONTACT")
            print("6. Exit")

            val = int(input("Choose the Table you want to edit> "))
            if val == 1:
                prisoner(jid)
            if val == 2:
                crime(jid)
            if val == 3 or val == 4 or val == 5:
                print("\n******UNDER CONSTRUCTION :(********");
                print()
            if val == 6:
                break
            else:
                print("Please Enter a valid input")

    elif ch == 2:
        while (1):
            print("1. JAIL")
            print("2. POLICEOFFICER")
            print("3. POLICEOFFICERCONTACT")
            print("4. POLICEOFFICEREMAIL")
            print("5. Average expenditure of a prisoner")
            print("6. Exit")
            val = int(input("Choose the Table you want to edit> "))
            if val == 1:
                jail()
            if val == 2:
                policeofficer()
            if val == 3:
                policeofficercontact()
            if val == 4:
                policeofficeremail()
            if val == 5:
                avgexpense()
            if val == 6:
                break
            else:
                print("Please Enter a valid input")


def formulate(ch):
    cur = con.cursor()

    if ch == 1:
        Id = int(input("Please enter your Id>> "))
        query = "SELECT COUNT(*) FROM POLICEOFFICER WHERE (POId = '%d' AND JobType = 'Jailer')" % (Id)
        cur.execute(query)
        result = cur.fetchall()
        if result[0]["COUNT(*)"] == 1:
            passw = getpass.getpass("Password for accessing database>>")
            if passw == 'p':
                print("Access granted")
                print("")
                access(ch, Id)
            else:
                print("Wrong Password")
        else:
            print("Id not found or the Id does not corresponds to a Jailer")

    if ch == 2:
        passw = getpass.getpass("Password for accessing database>>")
        if passw == 'p':
            print("Access granted")
            print("")
            access(ch, -1)
        else:
            print("Wrong Password")


while (1):
    temp = sp.call('clear', shell=True)
    username = input("Username for accessing MySQL:")
    password = getpass.getpass("Password for accessing MySQL:")
    # print(password)
    ch = 0

    try:
        con = pymysql.connect(host='localhost',
                              user='root',
                              password='vibhu8587921009',
                              db='JAILDB',
                              cursorclass=pymysql.cursors.DictCursor
                              )
        temp = sp.call('clear', shell=True)

        if (con.open):
            print("Connected")
        else:
            print("Failed to connect")

        with con:
            cur = con.cursor()
            while (1):
                temp = sp.call('clear', shell=True)
                print("1.Enter as a Jailer")
                print("2.Enter as a Government Official")
                print("3.Logout")
                ch = int(input("Enter choice> "))
                temp = sp.call('clear', shell=True)

                if ch == 1 or ch == 2:
                    formulate(ch)
                elif ch == 3:
                    break
                else:
                    print("Please Enter a valid input")

        if ch == 3:
            break


    except:
        temp = sp.call('clear', shell=True)
        print("Connection Refused: Either username or password is incorrect or user doesn't have access to database")