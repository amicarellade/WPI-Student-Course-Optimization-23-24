from flask import Flask, render_template, request, redirect, url_for, session
import user_functions as usr
import pandas as pd
import process_txt as pt
import process_workday
import basic_data_funcs as bd
import setup_model as sm
import mapping_buckets as mb
import json

ui = Flask(__name__)
ui.secret_key = 'your_secret_key_here'




@ui.route('/', methods=['GET', 'POST'])
def index():
    result = "Select at least one major and input and/or upload your courses!"
    
    if request.method == 'POST':
        # Process form inputs
        courses = request.form['courses'].split(", ")
        courses = [] if courses == [''] else courses

        major = request.form['major']
        second_major = request.form['second_major']
        removed_courses = request.form['removed-courses'].split(", ")
        masters = request.form['masters']

        if not validate_major_selection(major, second_major, masters):
            return render_template('index.html', result=result)

        # Load program references
        programs_ref = bd.get_dict_from_json("Data/JSONs/programs_ref.json")
        
        try:
            # Determine the program name
            program_names, base_dict, prog_name = determine_program(programs_ref, major, second_major, masters)
        except ValueError as e:
            result = str(e)  # Error message for invalid combinations
            return render_template('index.html', result=result)

        session['program_names'] = program_names
        session['base_dict'] = base_dict
        session['prog_name'] = prog_name

        # Validate course codes
        if not validate_course_format(courses):
            result = "Taken course with an invalid format detected - please format course codes according to the example above."
            return render_template('index.html', result=result)

        # Process uploaded file if present
        if 'file' in request.files and request.files['file'].filename != '':
            file = request.files['file']
            file_path = f'uploads/{file.filename}'
            file.save(file_path)

            df = pd.read_excel(file_path, header=None)
            for i in range(15):
                if "Registrations Used" in df.columns:
                    break

            courses = process_workday.courses_from_excel(df, courses, removed_courses)
            independent_studies = [course for course in courses if course.endswith('999')]

            if independent_studies:
                session["courses"] = [course for course in courses if course not in independent_studies]
                session['independent_studies'] = independent_studies
                session['ISPs'] = []
                return redirect(url_for('independent_study_form'))

        # Run the model
        if not run_model(major, second_major, masters, courses, program_names):
            result = "This combination of majors is not currently supported. Please choose a different combination."
            return render_template('index.html', result=result)

        return redirect(url_for('result', result_filename='test.txt'))

    return render_template('index.html', result=result)



@ui.route('/independent_study_form', methods=['GET', 'POST'])
def independent_study_form():
    independent_studies = session.get('independent_studies', [])
    program_names = session.get('program_names', [])
    isps = session.get('ISPs', [])
    base_dict = session.get('base_dict', {})

    if not independent_studies:
        run_model(None, None, None, session['courses'], program_names, isps)
        return redirect(url_for('result', result_filename='test.txt'))

    current_study = independent_studies[0]
    reqs, sreqs = extract_reqs(base_dict, program_names)

    if request.method == 'POST':
        isps.append({
            'substitution': request.form['substitution'],
            'credits': request.form['credits'],
            'req': request.form['reqs'],
            'sreqs': request.form.getlist('sreqs')
        })

        independent_studies.pop(0)
        session['independent_studies'] = independent_studies
        session['ISPs'] = isps

        if independent_studies:
            return redirect(url_for('independent_study_form'))

        run_model(None, None, None, session['courses'], program_names, isps)
        return redirect(url_for('result', result_filename='test.txt'))

    return render_template('independent_study_form.html', current_study=current_study, reqs=reqs, sreqs=sreqs)


@ui.route('/result/<result_filename>')
def result(result_filename):
    # Open and read the result file
    with open(result_filename, 'r') as result_file:
        result_content = result_file.read()
    
    # Extract the courses dictionary from the result data
    results_dict = pt.parse_template(result_content)
    print(results_dict)

    prog_name = session.get('prog_name', '')
    print(prog_name)

    programs_ref = bd.get_dict_from_json("Data/JSONs/programs_ref.json")
    program_ref = programs_ref[prog_name]
    print(program_ref)

    #merge courses buckets to courses
    courses = mb.augment_courses_with_buckets(results_dict, program_ref)
    print(courses)


    #read json file
    with open("Data/Oscar+RP_Ddata/CS_courses.json", "r") as file:
        OscarAndRP_data = json.load(file)



    #open csv merged_courses.csv
    courses_data = pd.read_csv("merged_courses.csv")

    # Pass the courses_dict and program_names to the HTML template
    return render_template(
        # You can change the template file to 'result.html', 'table.html', or 'piechart.html' if you want
        'course_results.html',   
        results=courses,
        json_data=OscarAndRP_data,
    )

def validate_major_selection(major, second_major, masters):
    if major == "Select...":
        return False
    if major == second_major:
        return False
    if masters != "None" and second_major != "None":
        return False
    return True


def validate_course_format(courses):
    return all("_" in course and " " not in course for course in courses)


def determine_program(programs_ref, major, second_major, masters):
    if masters == "None":
        program_names = [f"{major}_MAJOR"]
        if second_major != "None":
            program_names.append(f"{second_major}_MAJOR")
    else:
        program_names = [f"{major}_{masters}_BSMS"]

    prog_name = sm.get_program_run_name(program_names)

    # Check if the program exists in the JSON reference
    if prog_name not in programs_ref:
        raise ValueError(f"Program combination '{prog_name}' does not exist.")

    base_dict = programs_ref[prog_name].copy()
    base_dict.pop("ALL_MAJORS", None)
    base_dict.pop("Buckets", None)
    return program_names, base_dict, prog_name


def extract_reqs(base_dict, program_names):
    reqs = []
    sreqs = []
    for prog_name in program_names:
        reqs.extend([(req, desc) for req, desc in base_dict[prog_name]['Reqs'].items()])
        sreqs.extend([(sreq, desc) for sreq, desc in base_dict[prog_name]['Sreqs'].items()])
    return reqs, sreqs


def run_model(major, second_major, masters, courses, program_names, isps=[]):
    try:
        if masters == "None":
            usr.run_model(program_names, courses, write_output=True, output_name="test", ISPs=isps)
        else:
            usr.run_model(program_names, courses, write_output=True, output_name="test", ISPs=isps)
        return True
    except KeyError:
        return False



if __name__ == '__main__':
    ui.run(debug=True)
