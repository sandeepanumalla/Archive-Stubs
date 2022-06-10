import json
import os
import sys
import ast
import time
from functools import wraps
from tkinter import Tk, filedialog, Button
from auth import rest_api
from flask_login import login_required
import tkinter.ttk as ttk
from tkinter.filedialog import askdirectory
import win32api

from forms import LoginForm
from stubs import STALE
# from STALE import getListOfFiles, getCount, getListOfFilesOneLevel
from flask import Flask, render_template, url_for, redirect, send_from_directory, request, jsonify, session, flash, \
    Response

app = Flask(__name__, template_folder='templates', static_url_path='', static_folder='static')
cls = STALE()
app.config['SECRET_KEY']='91a52a9fdbb83c1762f518c62c9b8924'

driveIndexes = [];
def showDrives():
    drives = win32api.GetLogicalDriveStrings()
    drives = drives.split('\000')[:-1]
    for i in drives:
        driveIndexes.append(i)

    ##driveIndexes = drives
    return drives

def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            print("session")
            return f(*args, **kwargs)
        else:
            print("session not found")
            flash("You need to login first", "danger")
            return redirect(url_for('login'))
    return wrap

@app.route('/')
@login_required
def index():
    drives = showDrives();
    return render_template('home.html', msg='Archived Stubs', connected = drives)

@app.route('/get')
def get():
    return redirect(url_for('index'))

usercredentials = {
    "username": "testuser@stubs.com",
    "password":"testing"
}
print(usercredentials);

@app.route('/login',methods=["POST","GET"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'admin@stubs.com' and form.password.data == 'password':
            print("logged in")
            flash('You have been logged in!', 'success')
            session['logged_in'] = True
            return redirect(url_for('index'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route('/logout')
def logout():
    session.pop('logged_in',None)
    return redirect(url_for('login'))

@app.route('/check')
@login_required
def checkindex():
    return render_template('check.html')

@app.route("/counter",methods=["POST","GET"])
@login_required
def ajaxfilecounter():
    if request.method == 'POST':
        data = request.form['data']
        res = ast.literal_eval(data)
        return render_template('prereport.html', rowdata=res)


@app.route("/ajaxmovestubs",methods=["POST","GET"])
@login_required
def ajaxmovestubs():
    if request.method == 'POST':
        
        folderPath = request.form['folderPath']
        optProc = request.form['optProc']
        try:
            noSubFolders = request.form['noSubFolders']
        except KeyError as e:
            noSubFolders = 'NO'
            
        # folderPath = 'C:\python\zurich\stubs\Destination'
        start = time.time()
        if noSubFolders == 'YES':
            FileData =  cls.getListOfFilesOneLevel(folderPath, optProc)
        else:
            FileData =  cls.getListOfFiles(folderPath, optProc)
        end = time.time()
        processTime = end-start 
        # FileData =  getStubsStale(folderPath)
        CountData = cls.getCount(FileData, folderPath, optProc)
        CountData.update({'ptime' : processTime, 'noSubFolders' : noSubFolders})
        
        msg = f'{CountData}'
    return jsonify(msg)

##confirmation call
@app.route("/stubsconfirm",methods=["POST","GET"])
@login_required
def stubsconfirm():
    if request.method == 'POST':
        folderPath = request.form['folderPath']
        optProc = request.form['optProc']
        try:
            noSubFolders = request.form['noSubFolders']
        except KeyError as e:
            noSubFolders = 'NO'
            
        start = time.time()
        if noSubFolders == 'YES':
            CountData =  cls.getListOfFilesOneLevel(folderPath, optProc, 'Yes')
        else:
            CountData =  cls.getListOfFiles(folderPath, optProc, 'Yes')
        msg = f'{CountData}'
    return jsonify(msg)

@app.route("/opendialog/<driveIndex>",methods=["POST","GET"])
def opendialog(driveIndex):
    open_folder = 'Select Folder Path'
    
    if request.method == 'POST': 
        # name = request.form['name']
        # if (name == 'SelectFolder'):
        # selectedDrive = document.getElementById("#option").textValue
        content = request.get_json(silent=True)
        #selected = content['selectedDrive']


        selectedDrive = driveIndexes[(int)(driveIndex) - 1]
        print("the selected drive is -> ", selectedDrive);
        root = Tk()
        root.withdraw()
        root.attributes('-topmost', True)
        open_folder = filedialog.askdirectory(initialdir=selectedDrive)
        root.iconify()
        root.deiconify()
        root.destroy()
        root.mainloop()
    return jsonify(open_folder)

def main():
    app.run(debug=True, port=5000, host='0.0.0.0')

if __name__ == '__main__':
    main()