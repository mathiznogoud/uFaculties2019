from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from . import api
from flask_mysqldb import MySQL
from .. import app
import pymysql

mysql = MySQL(app)


@api.route('/api')
def Index():
    cur = mysql.connection.cursor()
    cur.execute("SELECT  id, name FROM departments")
    data = cur.fetchall()
    cur.close()

    return render_template('api/index.html', departments=data )



@api.route('/api/insert', methods = ['POST'])
def insert():

    if request.method == "POST":
        flash("Data Inserted Successfully")
        name = request.form['name']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO departments (name) VALUES (%s)", (name,))
        mysql.connection.commit()
        return redirect(url_for('api.Index'))




@api.route('/api/delete/<string:id_data>', methods = ['GET'])
def delete(id_data):
    flash("Record Has Been Deleted Successfully")
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM departments WHERE id=%s", (id_data,))
    mysql.connection.commit()
    return redirect(url_for('api.Index'))



@api.route('/api/update',methods=['POST','GET'])
def update():

    if request.method == 'POST':
        id_data = request.form['id']
        name = request.form['name']
        cur = mysql.connection.cursor()
        cur.execute("""
               UPDATE departments
               SET name=%s
               WHERE id=%s
            """, (name, id_data))
        flash("Data Updated Successfully")
        mysql.connection.commit()
        return redirect(url_for('api.Index'))

@api.route('/researchfields')
def TreeView():
    db1 = pymysql.connect("localhost","uf_admin","uF_admin2019#","uFaculties_db")
    cursor = db1.cursor()
    query = "select * from researchfields"
    cursor.execute(query)
    result = cursor.fetchall()
    cur = db1.cursor()

    keys = ["Id", "Title", "ParentId"]
    
    answer = [{k: v for k, v in zip(keys, tup)} for tup in result]

    return render_template("api/TreeView.html", answer=answer)