from flask import Flask, render_template, request, jsonify, session
from datetime import datetime
import csv
import os

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'a_default_secret_key')

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    if email and email.endswith("@gmail.com"):
        session['email'] = email
        return jsonify({'status': 'success', 'message': 'Login successful'}), 200
    return jsonify({'status': 'error', 'message': 'Login failed. Please use a Gmail address.'}), 401

@app.route('/submit-form', methods=['POST'])
def submit_form():
    if 'email' not in session:
        return jsonify({'status': 'error', 'message': 'Session expired or invalid. Please log in again.'}), 401
    
    email = session['email']
    business_name = request.form['businessName']
    contact_address = request.form['contactAddress']
    mobile = request.form['mobile']
    remark = request.form.get('remark', '')
    business_type = request.form['businessType']
    agree_enroll = request.form['agreeEnroll']
    virtual_account = request.form['virtualAccount']
    merchant_business_name = request.form['merchantBusinessName']
    date_created = request.form['dateCreated']
    latitude = request.form.get('latitude', '')
    longitude = request.form.get('longitude', '')
    timestamp = request.form.get('timestamp', datetime.utcnow().isoformat())

    csv_file_path = os.path.join(app.root_path, 'submissions.csv')

    try:
        with open(csv_file_path, mode='a', newline='') as f:
            csv_writer = csv.writer(f)
            csv_writer.writerow([
                email, business_name, contact_address, mobile, remark,
                business_type, agree_enroll, virtual_account,
                merchant_business_name, date_created, latitude, longitude, timestamp
            ])
        return jsonify({'status': 'success', 'message': 'Form submitted successfully'}), 200
    except Exception as e:
        print(f"Failed to write to CSV: {e}")
        return jsonify({'status': 'error', 'message': 'Failed to save form data'}), 500

@app.route('/logout', methods=['GET'])
def logout():
    session.pop('email', None)
    return redirect(url_for('index'))

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html', email=session.get('email'))

if __name__ == '__main__':
    app.run(debug=True)  # Turn off debug mode in production
