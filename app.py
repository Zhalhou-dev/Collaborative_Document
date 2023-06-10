import os

from flask import Flask, request, jsonify, render_template, redirect, url_for,send_file
from faker import Faker
from twilio.jwt.access_token import AccessToken
from twilio.jwt.access_token.grants import SyncGrant
from werkzeug.utils import secure_filename

app = Flask(__name__)
fake = Faker()


@app.route('/')
def index():
    return render_template('index.html')

# Add your Twilio credentials
@app.route('/token')
def generate_token():
    TWILIO_ACCOUNT_SID = 'AC2a4e0722722d55ace198db1858312dd9'
    TWILIO_SYNC_SERVICE_SID = 'MG6dc80686c99b266be9c7e7786eeb6dee'
    TWILIO_API_KEY="SK4c0e1ddcb69010198dec2568c34e88a4"
    TWILIO_API_SECRET="wgTiTMsMGfGEkUSejcaINp5HzViY7cZR"


    username = request.args.get('username', fake.user_name())

    # create access token with credentials
    token = AccessToken(TWILIO_ACCOUNT_SID, TWILIO_API_KEY, TWILIO_API_SECRET, identity=username)
    # create a Sync grant and add to token
    sync_grant_access = SyncGrant(TWILIO_SYNC_SERVICE_SID)
    token.add_grant(sync_grant_access)
    return jsonify(identity=username, token=token.to_jwt().decode())

# Write the code here
@app.route('/', methods=['POST'])
def download_text():
    text_from_notepad=request.form['text']
    with open("Downloaded_Document.txt","w") as f:
        f.write(text_from_notepad)
    path="Downloaded_Document.txt"
    return send_file(path,as_attachment=True)


    
        

    

    


if __name__ == "__main__":
    app.run(host='localhost', port='5001', debug=True)
