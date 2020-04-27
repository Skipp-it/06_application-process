from flask import Flask, render_template, request, url_for, redirect

import data_manager

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/mentors')
def mentors_list():
    mentor_name = request.args.get('mentor-last-name')
    city_name = request.args.get('city-name')
    if mentor_name:
        mentor_details = data_manager.get_mentors_by_last_name(mentor_name)
    elif city_name:
        mentor_details = data_manager.get_mentors_by_city(city_name)
    else:
        mentor_details = data_manager.get_mentors()

    # We get back a list of dictionaries from the data_manager (for details check 'data_manager.py')
    return render_template('mentors.html', mentors=mentor_details, city_name=city_name) #     city_name are rostul, aici, de a pastra ultima selectie pe buton


@app.route('/applicants-phone')
def applicants_phone():
    applicant_name = request.args.get('applicant-name')
    applicant_email = request.args.get('email-ending')
    if applicant_name:
        applicant_details = data_manager.get_applicant_data_by_name(applicant_name)
    elif applicant_email:
        applicant_details = data_manager.get_applicant_data_by_email(applicant_email)
    else:
        applicant_details = ""
    return render_template('applicant-phone.html', applicants=applicant_details)


@app.route('/applicants')
def applicants_list():
    applicants_details = data_manager.get_applicant()
    return render_template('applicants.html', applicants=applicants_details)


@app.route('/applicants/<code>', methods=['GET','POST'])
def applicant_code(code):
    if request.method == 'POST':
        phone_no = request.form['new-phone']
        data_manager.update_phone_number(phone_no, code)
        return redirect('/applicants/' + code)
    else:
        applicant_details = data_manager.get_applicant_by_code(code)
    return render_template('applicants-update.html', applicants=applicant_details, code=code)


@app.route('/applicants/<code>/delete')
def delete_applicant(code):
    data_manager.delete_applicant(code)
    return redirect('/applicants')


@app.route('/add-applicant', methods=['GET','POST'])
def add_applicant():
    if request.method == 'POST':
        first_name = request.form['first-name']
        last_name = request.form['last-name']
        phone_number = request.form['phone-number']
        email = request.form['email']
        data_manager.add_applicant(first_name, last_name, phone_number, email)
        code = data_manager.get_max_id()
        code_data = code[0].get('max','')
        app_code = data_manager.get_application_code_by_id(code_data)
        applicant_code = app_code[0].get('application_code', '')
        return redirect('/applicants/' + str(applicant_code))
    return render_template('add-applicant.html')


@app.route("/applicants/delete-by-email", methods=['GET','POST'])
def delete_by_email():
    if request.method == 'POST':
        email_domain = request.form['email-ending']
        data_manager.delete_applicant_by_email(email_domain)
        return redirect('/applicants')


if __name__ == '__main__':
    app.run(debug=True)
