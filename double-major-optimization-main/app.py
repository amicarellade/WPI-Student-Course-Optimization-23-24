from flask import Flask, render_template, request, redirect, url_for, jsonify, session
import user_functions as usr
import pandas as pd
import process_workday
import basic_data_funcs as bd
import setup_model as sm

ui = Flask(__name__)

# Set the secret key to enable Flask session
ui.secret_key = 'your_secret_key_here'



@ui.route('/', methods=['GET', 'POST'])
# this can definitely be cleaned up - we don't need to be storing all this stuff in session variables unless we see an ISP

def index():
    result = "Select at least one major and input and/or upload your courses!"
    if request.method == 'POST':
        #session['major'] = request.form['major']
        #session['second_major'] = request.form['second_major']
        session['courses'] = request.form['courses'].split(", ")
        if session['courses'] == ['']:
            session['courses'] = []
        #session['removed_courses'] = request.form['removed-courses'].split(", ")
        #session['masters'] = request.form['masters']

        #major = session['major']
        #second_major = session['second_major']
        courses = session['courses']
        #removed_courses = session['removed_courses']
        #masters = session['masters']

        major = request.form['major']
        second_major = request.form['second_major']
        removed_courses = request.form['removed-courses'].split(", ")
        masters = request.form['masters']

        programs_ref = bd.get_dict_from_json("Data/JSONs/programs_ref.json")
        if masters == "None":
            if major == "Select...":
                result = "Please select a primary major!"
                return render_template('index.html', result=result)

            elif major == second_major:
                result = "Please select two different majors or select \"None\" if you don't have a second major."
                return render_template('index.html', result=result)

            program_names = [major+"_MAJOR"]
            if second_major != "None":
                program_names.append(second_major+"_MAJOR")
            prog_name = sm.get_program_run_name(program_names)
            session['program_names'] = program_names
            print("WEEE "+str(session.get('program_names')))
            #print(prog_name)
            base_dict = programs_ref[prog_name].copy()
            base_dict.pop("ALL_MAJORS")
            base_dict.pop("Buckets")
            session['base_dict'] = base_dict
            print("the base dict we retrieved is: " + str(base_dict))
        else:
            if major == "Select..." and second_major != "None":
                result = "Please select a primary major!"
                return render_template('index.html', result=result)

            elif major == second_major:
                result = "Please select two different majors or select \"None\" if you don't have a second major."
                return render_template('index.html', result=result)

            elif major != "Select..." and second_major == "None":
                program_names = [major + "_" + masters + "_BSMS"]
                prog_name = sm.get_program_run_name(program_names)
                session['program_names'] = program_names
                # print(prog_name)
                base_dict = programs_ref[prog_name].copy()
                base_dict.pop("ALL_MAJORS")
                base_dict.pop("Buckets")
                session['base_dict'] = base_dict
                print("the base dict we retrieved is: " + str(base_dict))


        #print(request.files['FileStorage'])

        #TODO: consolidate running the model into some function that gets called twice, instead of copy/pasting all this code
        # for if a file was uploaded or not

        if 'file' in request.files and request.files['file'].filename != '':
            # Process Excel file if uploaded
            file = request.files['file']
            if file.filename != '':
                # Save the file temporarily
                # TODO: delete the file
                file_path = 'uploads/' + file.filename
                file.save(file_path)

                # Read the Excel file using pandas
                columns = ["Requirement", "Status", "Remaining", "Registrations Used", "Academic Period", "Credits",
                           "Grade"]
                for i in range(15):
                    df = pd.read_excel(file_path, header=i)
                    if "Registrations Used" in df.columns:
                        break

                course_list = process_workday.courses_from_excel(df, courses, removed_courses)

                # Check for independent studies
                independent_studies = [course for course in course_list if course.endswith('999')]
                for isp in independent_studies:
                    course_list.remove(isp)
                session['independent_studies'] = independent_studies
                session['ISPs'] = []

                if independent_studies:
                    session["courses"] = course_list
                    # Redirect to the first independent study form page
                    return redirect(url_for('independent_study_form'))


                print(course_list)
                if masters == "None":
                    if second_major == "None":
                        usr.run_model([str(major) + "_MAJOR"], course_list, write_output=True, output_name="test")
                        return redirect(url_for('result', result_filename='test.txt'))
                    else:
                        try:
                            usr.run_model([str(major) + "_MAJOR", str(second_major) + "_MAJOR"], course_list, write_output=True, output_name="test")
                            return redirect(url_for('result', result_filename='test.txt'))
                        except KeyError:
                            result = "This combination of majors is not currently supported. Please choose a different combination."
                            return render_template('index.html', result=result)
                else:
                    if major == "Select..." and second_major == "None":
                        usr.run_model([str(masters) + "_MASTER"],
                                      course_list, write_output=True, output_name="test")
                        return redirect(url_for('result', result_filename='test.txt'))
                    elif major != "Select..." and second_major == "None":
                        try:
                            usr.run_model([str(major) + "_" + str(masters) + "_BSMS"],
                                          course_list, write_output=True, output_name="test")
                            return redirect(url_for('result', result_filename='test.txt'))
                        except KeyError:
                            result = "This BS/MS combination is not currently supported. Please choose a different combination."
                            return render_template('index.html', result=result)
                    elif major != "Select..." and second_major != "None":
                        result = "Double majors with a BS/MS is not currently supported. Please choose a different combination of degrees."
                        return render_template('index.html', result=result)
                # # Encode the result dictionary as JSON
                # result_json = jsonify(result=solution)

                # # Save the JSON result to a text file
                # result_file_path = 'uploads/result.txt'
                # with open(result_file_path, 'w') as result_file:
                #     result_file.write(result_json.get_data(as_text=True))

                # Redirect to a new URL after form submission
                return redirect(url_for('result', result_filename='test.txt'))
        # else:
        #     print("true!")
        elif masters == "None":
            if major == "Select...":
                result = "Please select a primary major!"
                return render_template('index.html', result=result)
            if major != second_major and second_major != "None":
                try:
                    usr.run_model([str(major) + "_MAJOR", str(second_major) + "_MAJOR"], courses,
                                             write_output=True, output_name="test")
                    return redirect(url_for('result', result_filename='test.txt'))
                except KeyError:
                    result = "This combination of majors is not currently supported. Please choose a different combination."
                    return render_template('index.html', result=result)
        else:
            if major == "Select..." and second_major == "None":
                usr.run_model([str(masters) + "_MASTER"],
                              courses, write_output=True, output_name="test")
                return redirect(url_for('result', result_filename='test.txt'))
            if major != "Select..." and second_major == "None":
                try:
                    usr.run_model([str(major) + "_" + str(masters) + "_BSMS"],
                        courses, write_output=True, output_name="test")
                    return redirect(url_for('result', result_filename='test.txt'))
                except KeyError:
                    result = "This BS/MS combination is not currently supported. Please choose a different combination."
                    return render_template('index.html', result=result)
            elif major != "Select..." and second_major != "None":
                result = "Double majors with a BS/MS is not currently supported. Please choose a different combination of degrees."
                return render_template('index.html', result=result)
        # Check for independent studies
        independent_studies = [course for course in courses if course.endswith('999')]
        for isp in independent_studies:
            courses.remove(isp)
        session['independent_studies'] = independent_studies
        session['ISPs'] = []

        if independent_studies:
            # Redirect to the first independent study form page
            return redirect(url_for('independent_study_form'))

        elif second_major == "None":
            usr.run_model([str(major) + "_MAJOR"], courses, write_output=True, output_name="test")
            return redirect(url_for('result', result_filename='test.txt'))

        else:
            result = "You didn't account for this case, dummy."
            return render_template('index.html', result=result)

    return render_template('index.html', result=result)

@ui.route('/independent_study_form', methods=['GET', 'POST'])
def independent_study_form():
    independent_studies = session.get('independent_studies')
    program_names = session.get('program_names')
    print("YOOOO "+str(program_names))
    reqs = ["None"]
    sreqs = []
    isps = session.get('ISPs')
    if isps == None:
        isps = []

    if not independent_studies:
        if len(program_names) == 1:
            usr.run_model([str(program_names[0])], session['courses'], write_output=True,
                          output_name="test", ISPs=isps)
        else:
            usr.run_model([str(program_names[0]) , str(program_names[1])],
                          session['courses'],
                          write_output=True, output_name="test", ISPs=isps)
        return redirect(url_for('result', result_filename='test.txt'))

    current_study = independent_studies[0]  # Get the first independent study
    session['current_study'] = current_study
    base_dict = session.get('base_dict')

    for prog_name in program_names:
        print(prog_name)
        for req in base_dict[prog_name]['Reqs'].keys():
            #print(req)
            reqs.append((req, base_dict[prog_name]['Reqs'][req]['Req Description']))
        #print(dict(reqs))
        for sreq in base_dict[prog_name]['Sreqs'].keys():
            #print(sreq)
            sreqs.append((sreq, base_dict[prog_name]['Sreqs'][sreq]['Sreq Description']))
    #reqs = [(req, desc) for req in base_dict["DS_MAJOR"]['Reqs'].keys() for desc in base_dict["DS_MAJOR"]['Reqs']]
    # req_options = []
    if request.method == 'POST':
        # Store form data for the current independent study
        isps.append({
            'substitution': request.form['substitution'],
            'credits': request.form['credits'],
            'req': request.form['reqs'],
            'sreqs': request.form.getlist('sreqs')
            #'sreq': request.form['sreqs']
        })

        # Remove the current study from the list
        independent_studies.pop(0)
        session['independent_studies'] = independent_studies
        session['ISPs'] = isps

        # Check if there are more independent studies to process
        if independent_studies:
            return redirect(url_for('independent_study_form'))

        # No more independent studies, run the model
        if len(program_names) == 1:
            usr.run_model([str(program_names[0])], session['courses'], write_output=True, output_name="test", ISPs=isps)
        else:
            usr.run_model([str(program_names[0]), str(program_names[1])], session['courses'],
                          write_output=True, output_name="test", ISPs=isps)
        return redirect(url_for('result', result_filename='test.txt'))

    return render_template('independent_study_form.html', current_study=current_study, reqs=reqs, sreqs=sreqs)


@ui.route('/result/<result_filename>')
def result(result_filename):
    #result_path = 'uploads/' + result_filename
    with open(result_filename, 'r') as result_file:
        result_content = result_file.read()

    return render_template('result.html', result=result_content)

if __name__ == '__main__':
    ui.run(debug=True)
