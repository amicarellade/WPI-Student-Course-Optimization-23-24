from flask import Flask, render_template, request, redirect, url_for
import user_functions as usr
import pandas as pd
import process_workday

ui = Flask(__name__)

@ui.route('/', methods=['GET', 'POST'])
def index():
    result = "Select at least one major and input your courses!"
    if request.method == 'POST':
        major = request.form['major']
        second_major = request.form['second_major']
        courses = request.form['courses']
        #return render_template('index.html', result=request.files['file'])
        if 'file' in request.files:
            # Process Excel file if uploaded
            file = request.files['file']
            if file.filename != '':
                # Save the file temporarily
                file_path = 'uploads/' + file.filename
                file.save(file_path)

                # Read the Excel file using pandas
                columns = ["Requirement", "Status", "Remaining", "Registrations Used", "Academic Period", "Credits",
                           "Grade"]
                df = pd.read_excel(file_path, names=columns)

                courses = process_workday.courses_from_excel(df)
                solution = usr.run_model([str(major).upper()+"_MAJOR"], courses, write_output=True, output_name="test")

                # Redirect to a new URL after form submission
                return redirect(url_for('result', result=solution))
        else:
            return render_template('index.html', result=request.files)
        if major == "Select...":
            result = "Please select a primary major!"

        elif major != second_major and second_major != "None":
            solution = usr.run_model([str(major).upper()+"_MAJOR", str(second_major).upper()+"_MAJOR"], [courses], write_output=True, output_name="test")
            return render_template('index.html', result=solution)

        elif second_major == "None":
            result = usr.run_model([str(major).upper()+"_MAJOR"], [courses], write_output=False, output_name="test")
            return render_template('index.html', result=result)

        elif major == second_major:
            result = "Please select two different majors or select \"None\" if you don't have a second major."
            return render_template('index.html', result=result)

        else:
            result = "You didn't account for this case, dummy"
            return render_template('index.html', result=result)

    return render_template('index.html', result=result)

@ui.route('/result/<result>')
def result(result):
    return render_template('result.html', result=result)

if __name__ == '__main__':
    ui.run(debug=True)
