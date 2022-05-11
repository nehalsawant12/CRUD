from flask import Flask, redirect,render_template,request,redirect,url_for
import pymysql

con=None
cur=None
app=Flask(__name__)
 
def connectToDb():
    global con,cur
    con=pymysql.connect(host="localhost",user="root",password="",database="article")
    cur=con.cursor()

def disconnectDB():
    cur.close()
    con.close()

def getAllPersonData():
    connectToDb()
    selectquery="Select*from per_info;"
    cur.execute(selectquery)
    data=cur.fetchall()
    disconnectDB()
    return data
        

def insertTopersonTable(per_name,per_mob,per_email,per_city,per_dob=None):
    try:
        connectToDb()
        insertQuery="insert into per_info(per_name,per_mob,per_email,per_city,per_dob) values (%s,%s,%s,%s,%s);"
        cur.execute(insertQuery,(per_name,per_mob,per_email,per_city,per_dob))
        con.commit()
        disconnectDB()
        return True
    except:
        disconnectDB()
        return False

def getOnePerson(per_id):
    connectToDb()
    selectquery="Select*from per_info where per_id=%s;"
    cur.execute(selectquery,(per_id,))
    data=cur.fetchone()
    disconnectDB()
    return data

@app.route("/update/",methods=['GET','POST'])
def updatePersonToTable(per_name,per_mob,per_email,per_city,per_id,per_dob=None):
    try:
        connectToDb()
        updateQuery="update per_info set per_name=%s,per_mob=%s,per_email=%s,per_city=%s,per_dob=%s where per_id=%s;"
        cur.execute(updateQuery,(per_name,per_mob,per_email,per_city,per_dob,per_id))
        con.commit()
        disconnectDB()
        return True
    except:
        disconnectDB()
        return False


def deletePersonTable(per_id):
    try:
        connectToDb()
        deleteQuery="delete from per_info where per_id=%s;"
        cur.execute(deleteQuery,(per_id,))
        con.commit()
        disconnectDB()
        return True
    except:
        disconnectDB()
        return False

@app.route("/")
@app.route("/index/")
def index():
    data=getAllPersonData()
    #tuple of tuple
    return render_template("index.html",data=data)

@app.route("/add/",methods=['GET','POST'])
def addPerson():
    if request.method == "POST":
         data=request.form
         if insertTopersonTable(data["txtName"],data["txtMob"],
         data["txtemail"],data["txtcity"],data["txtDOB"]):
            message = "Record inserted successfully"
         else:
            message = "Due to some issue could not insert record"
         return render_template("insert.html",message=message)
    return render_template("insert.html")



@app.route("/edit/",methods=["GET","POST"])
def updatePerson():
    per_id=request.args.get('id',type=int,default=1)
    data=getOnePerson(per_id)
    if request.method == "POST":
         fdata=request.form
         if updatePersonToTable(fdata["txtName"],fdata["txtMob"],
         fdata["txtemail"],fdata["txtcity"],per_id,fdata["txtDOB"]):
            message = "Record updated successfully"
         else:
            message = "Due to some issue could not update record"
         return render_template("update.html",message=message)
    return render_template("update.html",data=data)


@app.route("/delete/")
def deleteperson():
    per_id=request.args.get('id',type=int,default=1)
    deletePersonTable(per_id)
    return redirect(url_for("index"))

if __name__== '__main__':
    app.run(debug=True)

