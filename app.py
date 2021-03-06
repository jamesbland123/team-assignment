# app.py
import os
import boto3
import simplejson as json
from flask import Flask, jsonify, request, render_template, make_response, url_for, redirect
from flask_cors import CORS

app = Flask(__name__)
# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})

users = {
    "admin" : "abc123sisboombah"
}

TABLE = os.environ['DB_TABLE']
ENDPOINT = os.environ['ENDPOINT']
dynamodb = boto3.resource('dynamodb')
db_tbl = dynamodb.Table(TABLE)
team_size = 1

@app.route("/")
def main_page():
    if 'hash_provided' in request.cookies:
        return render_template('hash_provided.html')

    else:
        return render_template('register.html', endpoint=ENDPOINT)    

@app.route("/member", methods=['POST'])
def add_member():
    if 'hash_provided' in request.cookies:
        return render_template('hash_provided.html')

    name = request.form.get('name')
    if not name:
        return render_template('msg.html', message='Please provide userId and name')
    
    teams = get_db_items()
    sorted_teams = sort_teams(teams)

    for team in sorted_teams:
        if int(team['members_count']) < team_size: 
            team['members_count'] = int(team['members_count']) + 1
            team['members'].append(name)
            db_tbl.put_item(Item=team)
            
            resp = make_response(render_template('hash.html', hash_code=team['team_hash_login']))
            resp.set_cookie('hash_provided', value='YES', max_age=1800 )
            return resp
    
    return render_template('no_hashes.html', name=name)    

@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if check_password(username, password):
            resp = make_response(redirect(url_for('admin')))
            resp.set_cookie('username', value=username, max_age=3600)
            return resp

        else: 
            return render_template('msg.html', message='Login failed')

    if 'username' in request.cookies:
        return redirect(url_for('admin'))   

    return render_template('login.html', endpoint=ENDPOINT)

@app.route("/logout")
def logout():
    message = "User has been logged out." 
    resp = make_response(render_template('logout.html', message=message))
    resp.set_cookie('username', '', expires=0)
    return resp

@app.route("/admin")
def admin():
    if 'username' in request.cookies:
        return render_template('admin.html')
    
    return redirect(url_for('login'))

@app.route("/list_edit_teams")
def list_edit_teams():
    if 'username' in request.cookies:
        return render_template('list_edit_teams.html', endpoint=ENDPOINT)
    
    return redirect(url_for('login'))

@app.route("/list_teams")
def list_teams():
    if (request.headers.get('setJson') == "true"):
        teams = get_db_items()
        sorted_teams = sort_teams(teams)

        response = make_response(json.dumps(sorted_teams))
        response.headers['Content-Type'] = 'application/json'
        return response

    if 'username' in request.cookies:
        teams = get_db_items()
        sorted_teams = sort_teams(teams)
        
        return render_template('list_teams.html', items=sorted_teams)
    


    return redirect(url_for('login'))

@app.route("/delete_all")
def delete_all():
    if 'username' in request.cookies:
        
        data = get_db_items()

        with db_tbl.batch_writer() as batch:
            for each in data:
                batch.delete_item(Key={
                                    'row_number': each['row_number'],
                                    'team_hash': each['team_hash']
                                    }
                                )
        
        return jsonify({'success': 'data deleted'})     
        
        
    return redirect(url_for('login'))
    
@app.route("/upload", methods=['POST'])
def upload():
      if request.method == 'POST':
        f = request.files['file']
        print(f.filename)
        delete_all()
        
        #store the file contents as a string
        fstring = f.read().decode("utf-8")
        print(fstring)
        myreader = csv.reader(fstring.splitlines())
        line_count = 0
        for row in myreader:
            if line_count == 0:
                print(f'Column names are {row}')
                line_count += 1
            else:
                db_tbl.put_item(Item={'row_number': int(row[3]), 'team_hash':row[4], 'team_hash_login':row[5], 'members_count': 0, 'members': [] })
                print( row[3], row[4], row[5])
                line_count += 1
                
        print(line_count)
        return redirect(url_for('login'))    

@app.route("/update_row", methods=['POST'])
def update_row():
    req_data = request.get_json()
    row_number = int(req_data['row_number'])
    
    response = db_tbl.update_item(
        Key={
            'row_number': row_number,
            'team_hash': req_data['team_hash']
        },
        UpdateExpression="set team_hash_login=:t, members=:m, members_count=:c",
        ExpressionAttributeValues={
            ':t': req_data['team_hash_login'],
            ':m': req_data['members'],
            ':c': req_data['members_count']
        },
        ReturnValues="NONE"
    )
    return jsonify({
        "status": "success",
        "row_number": row_number,
        "team_hash_login": req_data['team_hash_login'],
        "members": req_data['members'],
        "members_count": int(req_data['members_count'])
        })           

def sort_teams(team_list):
    sorted_teams = sorted(team_list, key=lambda item: item['row_number'])
    return sorted_teams

def get_db_items():
    response = db_tbl.scan()
    data = response['Items']

    # Retrieve data records beyond 1MB dynamodb response
    while 'LastEvaluatedKey' in response:
        response = db_tbl.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
        data.extend(response['Items'])

    return data

def check_password(username, password):
    if username in users and users.get(username) == password:
        return True
    return False

if __name__ == "__main__":
    main_page()