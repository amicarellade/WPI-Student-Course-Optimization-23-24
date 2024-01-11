from flask import Flask, render_template, request, redirect, url_for
import user_functions as usr
import pandas as pd

ui = Flask(__name__)

@ui.route('/', methods=['GET', 'POST'])
def index():
    result = "Select at least one major and input your courses!"
    if request.method == 'POST':
        major = request.form['major']
        second_major = request.form['second_major']
        courses = request.form['courses']

        if 'file' in request.files:
            # Process Excel file if uploaded
            file = request.files['file']
            if file.filename != '':
                # Save the file temporarily
                file_path = 'uploads/' + file.filename
                file.save(file_path)

                # Read the Excel file using pandas
                df = pd.read_excel(file_path)

                # Call your script function here with DataFrame 'df'
                result = your_script.your_function_with_dataframe(major, second_major, df)

                # Redirect to a new URL after form submission
                return redirect(url_for('result', result=result))

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

@app.route('/result/<result>')
def result(result):
    return render_template('result.html', result=result)

if __name__ == '__main__':
    ui.run(debug=True)
