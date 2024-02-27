from flask import Flask, render_template, request, redirect, url_for, jsonify
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
        courses = request.form['courses'].split(", ")
        removed_courses = request.form['removed-courses'].split(", ")
        if major == "Select...":
            result = "Please select a primary major!"
        
        elif major == second_major:
            result = "Please select two different majors or select \"None\" if you don't have a second major."
            return render_template('index.html', result=result)

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
                for i in range(15):
                    df = pd.read_excel(file_path, header=i)
                    print("BRUHHHHHHHHHHHHHHHHHHHHHHhhh " + str(df.columns))
                    if "Registrations Used" in df.columns:
                        break
                        # print("BROOOOOOOOOOOOOOOOOOO")
                        # df = pd.read_excel(file_path, header=9)  # names=columns,

                course_list = process_workday.courses_from_excel(df, courses, removed_courses)
                print(course_list)
                solution = usr.run_model([str(major).upper() + "_MAJOR"], course_list, write_output=True, output_name="test")

                # # Encode the result dictionary as JSON
                # result_json = jsonify(result=solution)

                # # Save the JSON result to a text file
                # result_file_path = 'uploads/result.txt'
                # with open(result_file_path, 'w') as result_file:
                #     result_file.write(result_json.get_data(as_text=True))

                # Redirect to a new URL after form submission
                return redirect(url_for('result', result_filename='test.txt'))

        elif major != second_major and second_major != "None":
            solution = usr.run_model([str(major).upper() + "_MAJOR", str(second_major).upper() + "_MAJOR"], courses,
                                     write_output=True, output_name="test")
            return redirect(url_for('result', result_filename='test.txt'))

        elif second_major == "None":
            solution = usr.run_model([str(major).upper() + "_MAJOR"], courses, write_output=False, output_name="test")
            return redirect(url_for('result', result_filename='test.txt'))




        
        else:
            result = "You didn't account for this case, dummy."
            return render_template('index.html', result=result)

    return render_template('index.html', result=result)

@ui.route('/result/<result_filename>')
def result(result_filename):
    #result_path = 'uploads/' + result_filename
    with open(result_filename, 'r') as result_file:
        result_content = result_file.read()

    return render_template('result.html', result=result_content)

if __name__ == '__main__':
    ui.run(debug=True)
