from flask import Flask, redirect, url_for, request, render_template
from mysql.connector import errorcode
import mysql.connector

app = Flask(__name__)

@app.route('/result', methods=['POST', 'GET'])
def result_page(item_list):
    print item_list
    return render_template('result.html')


@app.route('/login', methods=['POST', 'GET'])
def login_page():
    username = request.form.get('uname')
    password = request.form.get('psw')
    # return str(username) + " " + str(password)
    try:
        connector = mysql.connector.connect(user='test', password='123', host='127.0.0.1', database='sh')
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            return "Something is wrong with your db user name or password!"
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            return "Database does not exist1"
        else:
            return "Another exception, returning!"
    else:
        # connector.close()
        print 'Connection to DB is ready!'
    try:
        cursor = connector.cursor()
        sql_command = "Select * From UserInfos Where firstname = '%s' And password = '%s'" % (username, password)
        cursor.execute(sql_command)
        result = cursor.fetchall()
        print 'username: %s, password: %s' % (username, password)
        print result
        if result and len(result) != 0:
            return_value = "<h1>DB Entries</h1>"
            for i in result:
                return_value += " <p> "
                return_value += str(i)
                return_value += " </p>"
            print return_value
            return "Successfully Logged In, Welcome! %s " % return_value
        else:
            return "Wrong username or password. Or you are attacking us?"

        # return redirect(url_for('result_page', item_list=result))
    except:
        return "Error!"

@app.route('/')
def home_page():
    return render_template('login.html')

if __name__ == '__main__':
   app.run("0.0.0.0")

