from operator import attrgetter
from urllib import request
import sqlalchemy
import pytest
from flask import current_app

from asyncio.windows_events import NULL
from flask_login import login_user, current_user, logout_user, login_required
from Teacher import app
from flask import (
    render_template,
    redirect,
    url_for,
    flash,
    session,
    request,
    send_from_directory,
    send_file,
)
from Teacher import db
from Teacher.forms import (
    LoginForm,
    RegistrationForm,
    uploadcsv,
    addcourse,
    quiz_mapping,
    test_mapping,
    uploadsem,
    all_co,
    single_phase,
    all_phases,
    number_phases,
    uploadassign,
    uploadstudent,
    main_stid_cc as msc,
    large_crsend,
    small_crsend,
    labfile_upload,
    large_talk,
    po_form_upload, 
    staffid_coursecode,
    add_grade_mapping
)
from Teacher.models import (
    User,
    course,
    internal_co,
    quiz1,
    quiz2,
    quiz3,
    student_co,
    subject_co,
    test1,
    test1_mapping,
    test2,
    test2_mapping,
    test3,
    test3_mapping,
    quiz1_mapping,
    quiz2_mapping,
    quiz3_mapping,
    assignment_mapping as am,
    assignment,
    student,
    staffid_cc,
    courseend_survey,
    co_info,
    lab_co,
    talk,
    level, 
    threshold, 
    po_mapping, 
    po_attainment,
    grade_marks
)
from werkzeug.utils import secure_filename
import os
import csv


    
######################################################################################
######################################################################################
##############       MAIN


@app.route("/")
def home_page():
    # return redirect(url_for('labco_calc'))
    # return redirect(url_for('upload_assign'))
    # return redirect(url_for('subjectco_calc'))
    # return redirect(url_for('quizmappingco'))
    # return redirect(url_for('numberphases'))
    return render_template("index.html")
    # return redirect(url_for('sem_gradetomarks'))


@app.route("/displaymain")
def disp_main():
    session["staffid"] = ""
    session["coursecode"] = ""
    return render_template("newmain.html")


@app.route("/setmainwithouttrefresh")
def set_main_without_refresh():
    return render_template("newmain.html")


@app.route("/setstaffidandcoursecode", methods=["GET", "POST"])
def set_id_cc():
    form = msc()

    if request.method == "POST":
        the_coursecode = request.form["coursecode"]
        the_staffid = request.form["staffid"]

        print(the_coursecode, the_staffid)
        cc = staffid_cc.query.filter_by(
            coursecode=the_coursecode, staffid=the_staffid
        ).first()

        if cc:
            session["coursecode"] = the_coursecode
            session["staffid"] = the_staffid
            return render_template("newmain.html")

        else:
            flash(
                "Staff ID and Course Code are not mapped together, please check the values!",
                category="danger",
            )
            return render_template("newmain.html")

    else:
        return render_template("newmain.html")


###################################################################################################
###################################################################################################
# Register, Login, Logout


@app.route("/register", methods=["POST", "GET"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data)
        user.set_password(form.password1.data)
        db.session.add(user)
        db.session.commit()

        flash(f"Success! You have registered as : {user.username}", category="success")
        return redirect(url_for("login1"))

    if form.errors != {}:
        for err_msg in form.errors.values():
            flash(f"There was an error : {err_msg}", category="danger")

    return render_template("registration.html", form=form)


@app.route("/login", methods=["GET", "POST"])
def login1():
    form = LoginForm()
    if form.validate_on_submit():
        attempted_user = User.query.filter_by(username=form.username.data).first()
        print(attempted_user)
        if attempted_user is not None and attempted_user.check_password(
            form.password.data
        ):
            login_user(attempted_user)
            flash(
                f"Success! You are logged in as : {attempted_user.username}",
                category="success",
            )
            # return redirect(url_for('market_page'))
            return redirect(url_for("disp_main"))
        else:
            flash(
                f"Username and Password are not matching ! Please check again !",
                category="danger",
            )

    return render_template("user_login.html", form=form)


@app.route("/logout")
@login_required
def logout_function():
    session["coursecode"] = ""
    session["staffid"] = ""
    logout_user()
    return redirect(url_for("home_page"))


################################################################################################
################################################################################################
# Add course and dynamic co's


@app.route("/addcodetails", methods=["GET", "POST"])
def co_details():
    course_c = session["coursecode"]
    print(course_c)
    the_instance = course.query.filter_by(coursecode=course_c).first()
    countt = the_instance.numberco
    l = []
    for i in range(1, countt + 1):
        l.append({"name": ""})

    form = all_co(cos=l)

    count = 1
    if form.validate_on_submit():
        for i in form.cos:
            co_det = i.details.data
            co_check = co_info.query.filter_by(coursecode=course_c, co_number=count).first()
            if co_check == None:
                new_co = co_info(coursecode=course_c, co_number=count, co_details=co_det)
                db.session.add(new_co)
            else:
                co_update = co_info.query.filter_by(coursecode=course_c, co_number=count).update(dict(co_details=co_det))
                
            count += 1
        db.session.commit()
        flash(
            "The course has been created and the COs' have been updated !",
            category="success",
        )
        return render_template("newmain.html")

    if form.errors != {}:
        for err_msg in form.errors.values():
            flash(f"There was an error : {err_msg}", category="danger")

    return render_template("co_details.html", form=form)


@app.route("/addcourse", methods=["GET", "POST"])
def add_course():
    form = addcourse()

    if form.validate_on_submit():
        name = form.coursename.data
        code = form.coursecode.data
        number = form.co_number.data
        semester = form.sem.data
        lab_ = form.lab.data
        d1 = form.dicop1.data
        d2 = form.dicop2.data
        s1 = form.scop1.data
        s2 = form.scop2.data
        t = form.ciet.data
        q = form.cieq.data
        assi = form.assign.data
        
        target = form.target.data
        level_1 = form.level1.data
        level_2 = form.level2.data
        level_3 = form.level3.data
        
        
        dico = d1/d2
        sco = s1/s2

        if lab_ == "choice1":
            lab_ = "Y"
        else:
            lab_ = "N"

        session["coursecode"] = code
        print("1-courseocde", session["coursecode"])

        new_course = course(
            coursename=name,
            coursecode=code,
            numberco=number,
            semester=semester,
            labyorn=lab_,
            dicop = dico, 
            scop=sco, 
            internal_cie=t, 
            internal_quiz=q, 
            internal_assign = assi, 
            target = target, 
            level1 = level_1, 
            level2 = level_2, 
            level3 = level_3
        )
        db.session.add(new_course)
        db.session.commit()
        flash(f"The course was added, now moving to CO's", category="success")
        return redirect(url_for("co_details"))

    if form.errors != {}:
        for err_msg in form.errors.values():
            flash(f"There was an error : {err_msg}", category="danger")

    return render_template("admin.html", form=form)

@app.route('/setgrade', methods=['GET', 'POST'])
def set_grade():
    form = add_grade_mapping()
    print("first")
    if form.validate_on_submit():
        print("second")
        filename = secure_filename(form.file.data.filename)
        
        file_path = app.config["UPLOAD_FOLDER"] + filename
        print(file_path)
        form.file.data.save(file_path)
        
        with open(file_path, 'r', newline="") as f:
            r = csv.DictReader(f)
            
            schemeyear = form.scheme_year.data
            
            for i in r:
                
                grade_marks_access = grade_marks.query.filter_by(scheme=schemeyear, alloted_grade=i['GRADE']).first()
                if grade_marks_access:
                    print("Notherr", i['GRADE'])
                    grade_marks_update = grade_marks.query.filter_by(scheme=schemeyear, alloted_grade=i['GRADE']).update(dict(max_marks=i['MAXMARKS'], min_marks=i['MINMARKS'], gpoint=i['GPOINT']))
                    db.session.commit()
                else:
                    print(i['GRADE'])
                    new_grade_marks = grade_marks(scheme=schemeyear, max_marks=i['MAXMARKS'], min_marks=i['MINMARKS'], alloted_grade=i['GRADE'], gpoint=i['GPOINT'])
                    db.session.add(new_grade_marks)
                    db.session.commit()
                    
                
        
        flash(
            "The grade was mapped to the marks!",
            category="success",
        )

        return redirect(url_for("set_main_without_refresh"))
    
    if form.errors != {}:
        
        for err_msg in form.errors.values():
            flash(f"There was an error : {err_msg}", category="danger")

    return render_template("grademarksmapping.html", form=form)
    
        
        
    
    
##############################################################################################
###############################################################################################
##All mappings input and display


@app.route("/quizmappingwithco", methods=["GET", "POST"])
def quizmappingco():
    form = quiz_mapping()

    def ans_co(num):
        return int(num) if num in range(1, 11) else 0

    def ans_marks(num):
        return int(num) if (num) else sqlalchemy.null()

    final = []

    course_code = session["coursecode"]
    if course_code == "":
        flash("Please enter an appropriate Course Code!", category="danger")
        return render_template("newmain.html")

    if form.validate_on_submit():
        the_quiz_number = form.quiz_number.data

        versionn = form.quizversion.data

        l = [
            ans_co(form.q1.data),
            ans_co(form.q2.data),
            ans_co(form.q3.data),
            ans_co(form.q4.data),
            ans_co(form.q5.data),
            ans_co(form.q6.data),
            ans_co(form.q7.data),
            ans_co(form.q8.data),
            ans_co(form.q9.data),
            ans_co(form.q10.data),
            ans_co(form.q11.data),
            ans_co(form.q12.data),
            ans_co(form.q13.data),
            ans_co(form.q14.data),
            ans_co(form.q15.data),
        ]

        lm = [
            ans_co(form.q1m.data),
            ans_co(form.q2m.data),
            ans_co(form.q3m.data),
            ans_co(form.q4m.data),
            ans_co(form.q5m.data),
            ans_co(form.q6m.data),
            ans_co(form.q7m.data),
            ans_co(form.q8m.data),
            ans_co(form.q9m.data),
            ans_co(form.q10m.data),
            ans_co(form.q11m.data),
            ans_co(form.q12m.data),
            ans_co(form.q13m.data),
            ans_co(form.q14m.data),
            ans_co(form.q15m.data),
        ]

        marks_per_co = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

        for i in range(0, 10):
            for j in range(15):
                if l[j] == i + 1:
                    marks_per_co[i] += lm[j]

        if the_quiz_number == 1:
            check = quiz1_mapping.query.filter_by(
                coursecode=course_code, version=versionn
            ).first()
            if check:
                check1 = quiz1_mapping.query.filter_by(
                    coursecode=course_code, version=versionn
                ).update(
                    dict(
                        q1=l[0],
                        q2=l[1],
                        q3=l[2],
                        q4=l[3],
                        q5=l[4],
                        q6=l[5],
                        q7=l[6],
                        q8=l[7],
                        q9=l[8],
                        q10=l[9],
                        q11=l[10],
                        q12=l[11],
                        q13=l[12],
                        q14=l[13],
                        q15=l[14],
                        q1m=lm[0],
                        q2m=lm[1],
                        q3m=lm[2],
                        q4m=lm[3],
                        q5m=lm[4],
                        q6m=lm[5],
                        q7m=lm[6],
                        q8m=lm[7],
                        q9m=lm[8],
                        q10m=lm[9],
                        q11m=lm[10],
                        q12m=lm[11],
                        q13m=lm[12],
                        q14m=lm[13],
                        q15m=lm[14],
                        q1_bt = 0,
                        q2_bt = 0,
                        q3_bt = 0,
                        q4_bt = 0,
                        q5_bt = 0,
                        q6_bt = 0,
                        q7_bt = 0,
                        q8_bt = 0,
                        q9_bt = 0,
                        q10_bt = 0,
                        q11_bt = 0,
                        q12_bt = 0,
                        q13_bt = 0,
                        q14_bt = 0,
                        q15_bt = 0,
                        total_co1_marks=marks_per_co[0],
                        total_co2_marks=marks_per_co[1],
                        total_co3_marks=marks_per_co[2],
                        total_co4_marks=marks_per_co[3],
                        total_co5_marks=marks_per_co[4],
                        total_co6_marks=marks_per_co[5],
                        total_co7_marks=marks_per_co[6],
                        total_co8_marks=marks_per_co[7],
                        total_co9_marks=marks_per_co[8],
                        total_co10_marks=marks_per_co[9],
                    )
                )
            else:
                new_quiz = quiz1_mapping(
                    coursecode=course_code,
                    version=versionn,
                    q1=l[0],
                    q2=l[1],
                    q3=l[2],
                    q4=l[3],
                    q5=l[4],
                    q6=l[5],
                    q7=l[6],
                    q8=l[7],
                    q9=l[8],
                    q10=l[9],
                    q11=l[10],
                    q12=l[11],
                    q13=l[12],
                    q14=l[13],
                    q15=l[14],
                    q1m=lm[0],
                    q2m=lm[1],
                    q3m=lm[2],
                    q4m=lm[3],
                    q5m=lm[4],
                    q6m=lm[5],
                    q7m=lm[6],
                    q8m=lm[7],
                    q9m=lm[8],
                    q10m=lm[9],
                    q11m=lm[10],
                    q12m=lm[11],
                    q13m=lm[12],
                    q14m=lm[13],
                    q15m=lm[14],
                    q1_bt = 0,
                    q2_bt = 0,
                    q3_bt = 0,
                    q4_bt = 0,
                    q5_bt = 0,
                    q6_bt = 0,
                    q7_bt = 0,
                    q8_bt = 0,
                    q9_bt = 0,
                    q10_bt = 0,
                    q11_bt = 0,
                    q12_bt = 0,
                    q13_bt = 0,
                    q14_bt = 0,
                    q15_bt = 0,
                    total_co1_marks=marks_per_co[0],
                    total_co2_marks=marks_per_co[1],
                    total_co3_marks=marks_per_co[2],
                    total_co4_marks=marks_per_co[3],
                    total_co5_marks=marks_per_co[4],
                    total_co6_marks=marks_per_co[5],
                    total_co7_marks=marks_per_co[6],
                    total_co8_marks=marks_per_co[7],
                    total_co9_marks=marks_per_co[8],
                    total_co10_marks=marks_per_co[9],
                )
                db.session.add(new_quiz)
            db.session.commit()
            flash(f"The mappings of quiz 1 were uploaded !", category="success")

            # return redirect(url_for('quizmappingco'))
            return render_template("newmain.html")

        elif the_quiz_number == 2:
            check = quiz2_mapping.query.filter_by(
                coursecode=course_code, version=versionn
            ).first()
            if check:
                check1 = quiz2_mapping.query.filter_by(
                    coursecode=course_code, version=versionn
                ).update(
                    dict(
                        q1=l[0],
                        q2=l[1],
                        q3=l[2],
                        q4=l[3],
                        q5=l[4],
                        q6=l[5],
                        q7=l[6],
                        q8=l[7],
                        q9=l[8],
                        q10=l[9],
                        q11=l[10],
                        q12=l[11],
                        q13=l[12],
                        q14=l[13],
                        q15=l[14],
                        q1m=lm[0],
                        q2m=lm[1],
                        q3m=lm[2],
                        q4m=lm[3],
                        q5m=lm[4],
                        q6m=lm[5],
                        q7m=lm[6],
                        q8m=lm[7],
                        q9m=lm[8],
                        q10m=lm[9],
                        q11m=lm[10],
                        q12m=lm[11],
                        q13m=lm[12],
                        q14m=lm[13],
                        q15m=lm[14],
                        q1_bt = 0,
                        q2_bt = 0,
                        q3_bt = 0,
                        q4_bt = 0,
                        q5_bt = 0,
                        q6_bt = 0,
                        q7_bt = 0,
                        q8_bt = 0,
                        q9_bt = 0,
                        q10_bt = 0,
                        q11_bt = 0,
                        q12_bt = 0,
                        q13_bt = 0,
                        q14_bt = 0,
                        q15_bt = 0,
                        total_co1_marks=marks_per_co[0],
                        total_co2_marks=marks_per_co[1],
                        total_co3_marks=marks_per_co[2],
                        total_co4_marks=marks_per_co[3],
                        total_co5_marks=marks_per_co[4],
                        total_co6_marks=marks_per_co[5],
                        total_co7_marks=marks_per_co[6],
                        total_co8_marks=marks_per_co[7],
                        total_co9_marks=marks_per_co[8],
                        total_co10_marks=marks_per_co[9],
                    )
                )
            else:
                new_quiz = quiz2_mapping(
                    coursecode=course_code,
                    version=versionn,
                    q1=l[0],
                    q2=l[1],
                    q3=l[2],
                    q4=l[3],
                    q5=l[4],
                    q6=l[5],
                    q7=l[6],
                    q8=l[7],
                    q9=l[8],
                    q10=l[9],
                    q11=l[10],
                    q12=l[11],
                    q13=l[12],
                    q14=l[13],
                    q15=l[14],
                    q1m=lm[0],
                    q2m=lm[1],
                    q3m=lm[2],
                    q4m=lm[3],
                    q5m=lm[4],
                    q6m=lm[5],
                    q7m=lm[6],
                    q8m=lm[7],
                    q9m=lm[8],
                    q10m=lm[9],
                    q11m=lm[10],
                    q12m=lm[11],
                    q13m=lm[12],
                    q14m=lm[13],
                    q15m=lm[14],
                    q1_bt = 0,
                    q2_bt = 0,
                    q3_bt = 0,
                    q4_bt = 0,
                    q5_bt = 0,
                    q6_bt = 0,
                    q7_bt = 0,
                    q8_bt = 0,
                    q9_bt = 0,
                    q10_bt = 0,
                    q11_bt = 0,
                    q12_bt = 0,
                    q13_bt = 0,
                    q14_bt = 0,
                    q15_bt = 0,
                    total_co1_marks=marks_per_co[0],
                    total_co2_marks=marks_per_co[1],
                    total_co3_marks=marks_per_co[2],
                    total_co4_marks=marks_per_co[3],
                    total_co5_marks=marks_per_co[4],
                    total_co6_marks=marks_per_co[5],
                    total_co7_marks=marks_per_co[6],
                    total_co8_marks=marks_per_co[7],
                    total_co9_marks=marks_per_co[8],
                    total_co10_marks=marks_per_co[9],
                )
                db.session.add(new_quiz)
            db.session.commit()
            flash(f"The mappings of quiz 2 were uploaded !", category="success")

            # return redirect(url_for('quizmappingco'))
            return render_template("newmain.html")

        elif the_quiz_number == 3:
            check = quiz3_mapping.query.filter_by(
                coursecode=course_code, version=versionn
            ).first()
            if check:
                check1 = quiz3_mapping.query.filter_by(
                    coursecode=course_code, version=versionn
                ).update(
                    dict(
                        q1=l[0],
                        q2=l[1],
                        q3=l[2],
                        q4=l[3],
                        q5=l[4],
                        q6=l[5],
                        q7=l[6],
                        q8=l[7],
                        q9=l[8],
                        q10=l[9],
                        q11=l[10],
                        q12=l[11],
                        q13=l[12],
                        q14=l[13],
                        q15=l[14],
                        q1m=lm[0],
                        q2m=lm[1],
                        q3m=lm[2],
                        q4m=lm[3],
                        q5m=lm[4],
                        q6m=lm[5],
                        q7m=lm[6],
                        q8m=lm[7],
                        q9m=lm[8],
                        q10m=lm[9],
                        q11m=lm[10],
                        q12m=lm[11],
                        q13m=lm[12],
                        q14m=lm[13],
                        q15m=lm[14],
                        q1_bt = 0,
                        q2_bt = 0,
                        q3_bt = 0,
                        q4_bt = 0,
                        q5_bt = 0,
                        q6_bt = 0,
                        q7_bt = 0,
                        q8_bt = 0,
                        q9_bt = 0,
                        q10_bt = 0,
                        q11_bt = 0,
                        q12_bt = 0,
                        q13_bt = 0,
                        q14_bt = 0,
                        q15_bt = 0,
                        total_co1_marks=marks_per_co[0],
                        total_co2_marks=marks_per_co[1],
                        total_co3_marks=marks_per_co[2],
                        total_co4_marks=marks_per_co[3],
                        total_co5_marks=marks_per_co[4],
                        total_co6_marks=marks_per_co[5],
                        total_co7_marks=marks_per_co[6],
                        total_co8_marks=marks_per_co[7],
                        total_co9_marks=marks_per_co[8],
                        total_co10_marks=marks_per_co[9],
                    )
                )
            else:

                new_quiz = quiz3_mapping(
                    coursecode=course_code,
                    version=versionn,
                    q1=l[0],
                    q2=l[1],
                    q3=l[2],
                    q4=l[3],
                    q5=l[4],
                    q6=l[5],
                    q7=l[6],
                    q8=l[7],
                    q9=l[8],
                    q10=l[9],
                    q11=l[10],
                    q12=l[11],
                    q13=l[12],
                    q14=l[13],
                    q15=l[14],
                    q1m=lm[0],
                    q2m=lm[1],
                    q3m=lm[2],
                    q4m=lm[3],
                    q5m=lm[4],
                    q6m=lm[5],
                    q7m=lm[6],
                    q8m=lm[7],
                    q9m=lm[8],
                    q10m=lm[9],
                    q11m=lm[10],
                    q12m=lm[11],
                    q13m=lm[12],
                    q14m=lm[13],
                    q15m=lm[14],
                    q1_bt = 0,
                    q2_bt = 0,
                    q3_bt = 0,
                    q4_bt = 0,
                    q5_bt = 0,
                    q6_bt = 0,
                    q7_bt = 0,
                    q8_bt = 0,
                    q9_bt = 0,
                    q10_bt = 0,
                    q11_bt = 0,
                    q12_bt = 0,
                    q13_bt = 0,
                    q14_bt = 0,
                    q15_bt = 0,
                    total_co1_marks=marks_per_co[0],
                    total_co2_marks=marks_per_co[1],
                    total_co3_marks=marks_per_co[2],
                    total_co4_marks=marks_per_co[3],
                    total_co5_marks=marks_per_co[4],
                    total_co6_marks=marks_per_co[5],
                    total_co7_marks=marks_per_co[6],
                    total_co8_marks=marks_per_co[7],
                    total_co9_marks=marks_per_co[8],
                    total_co10_marks=marks_per_co[9],
                )
                db.session.add(new_quiz)
            db.session.commit()
            flash(f"The mappings of quiz 3 were uploaded !", category="success")

            # return redirect(url_for('quizmappingco'))
            return render_template("newmain.html")

    if form.errors != {}:
        for err_msg in form.errors.values():
            flash(f"There was an error : {err_msg}", category="danger")

    return render_template("quiz_co_mapping.html", form=form)


@app.route("/testmappingwithco", methods=["GET", "POST"])
def testmappingco():
    form = test_mapping()

    def ans_co(num):
        return int(num) if num in range(1, 11) else 0

    d = {}

    the_course_code = session["coursecode"]
    if the_course_code == "":
        flash("Please enter an appropriate Course Code!", category="danger")
        return render_template("newmain.html")

    if form.validate_on_submit():

        the_cie_number = form.test_number.data

        l = [
            ans_co(form.q1a.data),
            ans_co(form.q1b.data),
            ans_co(form.q1c.data),
            ans_co(form.q2a.data),
            ans_co(form.q2b.data),
            ans_co(form.q2c.data),
            ans_co(form.q3a.data),
            ans_co(form.q3b.data),
            ans_co(form.q3c.data),
            ans_co(form.q4a.data),
            ans_co(form.q4b.data),
            ans_co(form.q4c.data),
            ans_co(form.q5a.data),
            ans_co(form.q5b.data),
            ans_co(form.q5c.data),
        ]

        lm = [
            ans_co(form.q1am.data),
            ans_co(form.q1bm.data),
            ans_co(form.q1cm.data),
            ans_co(form.q2am.data),
            ans_co(form.q2bm.data),
            ans_co(form.q2cm.data),
            ans_co(form.q3am.data),
            ans_co(form.q3bm.data),
            ans_co(form.q3cm.data),
            ans_co(form.q4am.data),
            ans_co(form.q4bm.data),
            ans_co(form.q4cm.data),
            ans_co(form.q5am.data),
            ans_co(form.q5bm.data),
            ans_co(form.q5cm.data),
        ]

        final = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

        for i in range(0, 10):
            for j in range(15):
                if l[j] == i + 1:
                    final[i] += lm[j]

        if the_cie_number == 1:
            check = test1_mapping.query.filter_by(coursecode=the_course_code).first()
            if check:
                check1 = test1_mapping.query.filter_by(
                    coursecode=the_course_code
                ).update(
                    dict(
                        q1a=l[0],
                        q1b=l[1],
                        q1c=l[2],
                        q2a=l[3],
                        q2b=l[4],
                        q2c=l[5],
                        q3a=l[6],
                        q3b=l[7],
                        q3c=l[8],
                        q4a=l[9],
                        q4b=l[10],
                        q4c=l[11],
                        q5a=l[12],
                        q5b=l[13],
                        q5c=l[14],
                        q1am=lm[0],
                        q1bm=lm[1],
                        q1cm=lm[2],
                        q2am=lm[3],
                        q2bm=lm[4],
                        q2cm=lm[5],
                        q3am=lm[6],
                        q3bm=lm[7],
                        q3cm=lm[8],
                        q4am=lm[9],
                        q4bm=lm[10],
                        q4cm=lm[11],
                        q5am=lm[12],
                        q5bm=lm[13],
                        q5cm=lm[14],
                        q1a_bt = 1,
                        q1b_bt = 2,
                        q1c_bt = 0,
                        q2a_bt = 2,
                        q2b_bt = 3,
                        q2c_bt = 0,
                        q3a_bt = 2,
                        q3b_bt = 1,
                        q3c_bt = 0,
                        q4a_bt = 3,
                        q4b_bt = 2,
                        q4c_bt = 0,
                        q5a_bt = 2,
                        q5b_bt = 4,
                        q5c_bt = 0,
                        total_co1_marks=final[0],
                        total_co2_marks=final[1],
                        total_co3_marks=final[2],
                        total_co4_marks=final[3],
                        total_co5_marks=final[4],
                        total_co6_marks=final[5],
                        total_co7_marks=final[6],
                        total_co8_marks=final[7],
                        total_co9_marks=final[8],
                        total_co10_marks=final[9],
                    )
                )

            else:

                new_test = test1_mapping(
                    coursecode=the_course_code,
                    q1a=l[0],
                    q1b=l[1],
                    q1c=l[2],
                    q2a=l[3],
                    q2b=l[4],
                    q2c=l[5],
                    q3a=l[6],
                    q3b=l[7],
                    q3c=l[8],
                    q4a=l[9],
                    q4b=l[10],
                    q4c=l[11],
                    q5a=l[12],
                    q5b=l[13],
                    q5c=l[14],
                    q1am=lm[0],
                    q1bm=lm[1],
                    q1cm=lm[2],
                    q2am=lm[3],
                    q2bm=lm[4],
                    q2cm=lm[5],
                    q3am=lm[6],
                    q3bm=lm[7],
                    q3cm=lm[8],
                    q4am=lm[9],
                    q4bm=lm[10],
                    q4cm=lm[11],
                    q5am=lm[12],
                    q5bm=lm[13],
                    q5cm=lm[14],
                    q1a_bt = 1,
                    q1b_bt = 2,
                    q1c_bt = 0,
                    q2a_bt = 2,
                    q2b_bt = 3,
                    q2c_bt = 0,
                    q3a_bt = 2,
                    q3b_bt = 1,
                    q3c_bt = 0,
                    q4a_bt = 3,
                    q4b_bt = 2,
                    q4c_bt = 0,
                    q5a_bt = 2,
                    q5b_bt = 4,
                    q5c_bt = 0,
                    total_co1_marks=final[0],
                    total_co2_marks=final[1],
                    total_co3_marks=final[2],
                    total_co4_marks=final[3],
                    total_co5_marks=final[4],
                    total_co6_marks=final[5],
                    total_co7_marks=final[6],
                    total_co8_marks=final[7],
                    total_co9_marks=final[8],
                    total_co10_marks=final[9],
                )

                db.session.add(new_test)
            db.session.commit()

            flash(f"The mappings of test 1 were uploaded !", category="success")
            # return redirect(url_for('testmappingco'))
            return render_template("newmain.html")

        elif the_cie_number == 2:
            check = test2_mapping.query.filter_by(coursecode=the_course_code).first()
            if check:
                check1 = test2_mapping.query.filter_by(
                    coursecode=the_course_code
                ).update(
                    dict(
                        q1a=l[0],
                        q1b=l[1],
                        q1c=l[2],
                        q2a=l[3],
                        q2b=l[4],
                        q2c=l[5],
                        q3a=l[6],
                        q3b=l[7],
                        q3c=l[8],
                        q4a=l[9],
                        q4b=l[10],
                        q4c=l[11],
                        q5a=l[12],
                        q5b=l[13],
                        q5c=l[14],
                        q1am=lm[0],
                        q1bm=lm[1],
                        q1cm=lm[2],
                        q2am=lm[3],
                        q2bm=lm[4],
                        q2cm=lm[5],
                        q3am=lm[6],
                        q3bm=lm[7],
                        q3cm=lm[8],
                        q4am=lm[9],
                        q4bm=lm[10],
                        q4cm=lm[11],
                        q5am=lm[12],
                        q5bm=lm[13],
                        q5cm=lm[14],
                        q1a_bt = 1,
                        q1b_bt = 2,
                        q1c_bt = 0,
                        q2a_bt = 2,
                        q2b_bt = 3,
                        q2c_bt = 0,
                        q3a_bt = 2,
                        q3b_bt = 1,
                        q3c_bt = 0,
                        q4a_bt = 3,
                        q4b_bt = 2,
                        q4c_bt = 0,
                        q5a_bt = 2,
                        q5b_bt = 4,
                        q5c_bt = 0,
                        total_co1_marks=final[0],
                        total_co2_marks=final[1],
                        total_co3_marks=final[2],
                        total_co4_marks=final[3],
                        total_co5_marks=final[4],
                        total_co6_marks=final[5],
                        total_co7_marks=final[6],
                        total_co8_marks=final[7],
                        total_co9_marks=final[8],
                        total_co10_marks=final[9],
                    )
                )

            else:

                new_test = test2_mapping(
                    coursecode=the_course_code,
                    q1a=l[0],
                    q1b=l[1],
                    q1c=l[2],
                    q2a=l[3],
                    q2b=l[4],
                    q2c=l[5],
                    q3a=l[6],
                    q3b=l[7],
                    q3c=l[8],
                    q4a=l[9],
                    q4b=l[10],
                    q4c=l[11],
                    q5a=l[12],
                    q5b=l[13],
                    q5c=l[14],
                    q1am=lm[0],
                    q1bm=lm[1],
                    q1cm=lm[2],
                    q2am=lm[3],
                    q2bm=lm[4],
                    q2cm=lm[5],
                    q3am=lm[6],
                    q3bm=lm[7],
                    q3cm=lm[8],
                    q4am=lm[9],
                    q4bm=lm[10],
                    q4cm=lm[11],
                    q5am=lm[12],
                    q5bm=lm[13],
                    q5cm=lm[14],
                    q1a_bt = 1,
                    q1b_bt = 2,
                    q1c_bt = 0,
                    q2a_bt = 2,
                    q2b_bt = 3,
                    q2c_bt = 0,
                    q3a_bt = 2,
                    q3b_bt = 1,
                    q3c_bt = 0,
                    q4a_bt = 3,
                    q4b_bt = 2,
                    q4c_bt = 0,
                    q5a_bt = 2,
                    q5b_bt = 4,
                    q5c_bt = 0,
                    total_co1_marks=final[0],
                    total_co2_marks=final[1],
                    total_co3_marks=final[2],
                    total_co4_marks=final[3],
                    total_co5_marks=final[4],
                    total_co6_marks=final[5],
                    total_co7_marks=final[6],
                    total_co8_marks=final[7],
                    total_co9_marks=final[8],
                    total_co10_marks=final[9],
                )

                db.session.add(new_test)
            db.session.commit()
            flash(f"The mappings of test 2 were uploaded !", category="success")
            # return redirect(url_for('testmappingco'))
            return render_template("newmain.html")

        elif the_cie_number == 3:
            check = test3_mapping.query.filter_by(coursecode=the_course_code).first()
            if check:
                test3_mapping.query.filter_by(coursecode=the_course_code).update(
                    dict(
                        q1a=l[0],
                        q1b=l[1],
                        q1c=l[2],
                        q2a=l[3],
                        q2b=l[4],
                        q2c=l[5],
                        q3a=l[6],
                        q3b=l[7],
                        q3c=l[8],
                        q4a=l[9],
                        q4b=l[10],
                        q4c=l[11],
                        q5a=l[12],
                        q5b=l[13],
                        q5c=l[14],
                        q1am=lm[0],
                        q1bm=lm[1],
                        q1cm=lm[2],
                        q2am=lm[3],
                        q2bm=lm[4],
                        q2cm=lm[5],
                        q3am=lm[6],
                        q3bm=lm[7],
                        q3cm=lm[8],
                        q4am=lm[9],
                        q4bm=lm[10],
                        q4cm=lm[11],
                        q5am=lm[12],
                        q5bm=lm[13],
                        q5cm=lm[14],
                        q1a_bt = 1,
                        q1b_bt = 2,
                        q1c_bt = 0,
                        q2a_bt = 2,
                        q2b_bt = 3,
                        q2c_bt = 0,
                        q3a_bt = 2,
                        q3b_bt = 1,
                        q3c_bt = 0,
                        q4a_bt = 3,
                        q4b_bt = 2,
                        q4c_bt = 0,
                        q5a_bt = 2,
                        q5b_bt = 4,
                        q5c_bt = 0,
                        total_co1_marks=final[0],
                        total_co2_marks=final[1],
                        total_co3_marks=final[2],
                        total_co4_marks=final[3],
                        total_co5_marks=final[4],
                        total_co6_marks=final[5],
                        total_co7_marks=final[6],
                        total_co8_marks=final[7],
                        total_co9_marks=final[8],
                        total_co10_marks=final[9],
                    )
                )
            else:
                new_test = test3_mapping(
                    coursecode=the_course_code,
                    q1a=l[0],
                    q1b=l[1],
                    q1c=l[2],
                    q2a=l[3],
                    q2b=l[4],
                    q2c=l[5],
                    q3a=l[6],
                    q3b=l[7],
                    q3c=l[8],
                    q4a=l[9],
                    q4b=l[10],
                    q4c=l[11],
                    q5a=l[12],
                    q5b=l[13],
                    q5c=l[14],
                    q1am=lm[0],
                    q1bm=lm[1],
                    q1cm=lm[2],
                    q2am=lm[3],
                    q2bm=lm[4],
                    q2cm=lm[5],
                    q3am=lm[6],
                    q3bm=lm[7],
                    q3cm=lm[8],
                    q4am=lm[9],
                    q4bm=lm[10],
                    q4cm=lm[11],
                    q5am=lm[12],
                    q5bm=lm[13],
                    q5cm=lm[14],
                    q1a_bt = 1,
                    q1b_bt = 2,
                    q1c_bt = 0,
                    q2a_bt = 2,
                    q2b_bt = 3,
                    q2c_bt = 0,
                    q3a_bt = 2,
                    q3b_bt = 1,
                    q3c_bt = 0,
                    q4a_bt = 3,
                    q4b_bt = 2,
                    q4c_bt = 0,
                    q5a_bt = 2,
                    q5b_bt = 4,
                    q5c_bt = 0,
                    total_co1_marks=final[0],
                    total_co2_marks=final[1],
                    total_co3_marks=final[2],
                    total_co4_marks=final[3],
                    total_co5_marks=final[4],
                    total_co6_marks=final[5],
                    total_co7_marks=final[6],
                    total_co8_marks=final[7],
                    total_co9_marks=final[8],
                    total_co10_marks=final[9],
                )

                db.session.add(new_test)
            db.session.commit()
            flash(f"The mappings of test 3 were uploaded !", category="success")
            # return redirect(url_for('testmappingco'))
            return render_template("newmain.html")

    if form.errors != {}:
        for err_msg in form.errors.values():
            flash(f"There was an error : {err_msg}", category="danger")

    return render_template("test_co_mapping.html", form=form)


@app.route("/displayquizmapping", methods=["GET", "POST"])
def disp_quizmapping():
    course_code = session["coursecode"]
    if course_code == "":
        flash("Please enter an appropriate Course Code!", category="danger")
        return render_template("newmain.html")

    q = quiz1_mapping.query.filter_by(coursecode=course_code).first()
    qui2 = quiz2_mapping.query.filter_by(coursecode=course_code).first()
    qui3 = quiz3_mapping.query.filter_by(coursecode=course_code).first()

    if q and qui2 and qui3:
        lco = [
            q.q1,
            q.q2,
            q.q3,
            q.q4,
            q.q5,
            q.q6,
            q.q7,
            q.q8,
            q.q9,
            q.q10,
            q.q11,
            q.q12,
            q.q13,
            q.q14,
            q.q15,
        ]
        lm = [
            q.q1m,
            q.q2m,
            q.q3m,
            q.q4m,
            q.q5m,
            q.q6m,
            q.q7m,
            q.q8m,
            q.q9m,
            q.q10m,
            q.q11m,
            q.q12m,
            q.q13m,
            q.q14m,
            q.q15m,
        ]

        lco2 = [
            qui2.q1,
            qui2.q2,
            qui2.q3,
            qui2.q4,
            qui2.q5,
            qui2.q6,
            qui2.q7,
            qui2.q8,
            qui2.q9,
            qui2.q10,
            qui2.q11,
            qui2.q12,
            qui2.q13,
            qui2.q14,
            qui2.q15,
        ]
        lm2 = [
            qui2.q1m,
            qui2.q2m,
            qui2.q3m,
            qui2.q4m,
            qui2.q5m,
            qui2.q6m,
            qui2.q7m,
            qui2.q8m,
            qui2.q9m,
            qui2.q10m,
            qui2.q11m,
            qui2.q12m,
            qui2.q13m,
            qui2.q14m,
            qui2.q15m,
        ]

        lco3 = [
            qui3.q1,
            qui3.q2,
            qui3.q3,
            qui3.q4,
            qui3.q5,
            qui3.q6,
            qui3.q7,
            qui3.q8,
            qui3.q9,
            qui3.q10,
            qui3.q11,
            qui3.q12,
            qui3.q13,
            qui3.q14,
            qui3.q15,
        ]
        lm3 = [
            qui3.q1m,
            qui3.q2m,
            qui3.q3m,
            qui3.q4m,
            qui3.q5m,
            qui3.q6m,
            qui3.q7m,
            qui3.q8m,
            qui3.q9m,
            qui3.q10m,
            qui3.q11m,
            qui3.q12m,
            qui3.q13m,
            qui3.q14m,
            qui3.q15,
        ]

        return render_template(
            "quizmappingdisplay.html",
            lco=lco,
            lm=lm,
            lco2=lco2,
            lm2=lm2,
            lco3=lco3,
            lm3=lm3,
            sett=[3],
        )

    elif q and qui2:
        lco = [
            q.q1,
            q.q2,
            q.q3,
            q.q4,
            q.q5,
            q.q6,
            q.q7,
            q.q8,
            q.q9,
            q.q10,
            q.q11,
            q.q12,
            q.q13,
            q.q14,
            q.q15,
        ]
        lm = [
            q.q1m,
            q.q2m,
            q.q3m,
            q.q4m,
            q.q5m,
            q.q6m,
            q.q7m,
            q.q8m,
            q.q9m,
            q.q10m,
            q.q11m,
            q.q12m,
            q.q13m,
            q.q14m,
            q.q15m,
        ]

        lco2 = [
            qui2.q1,
            qui2.q2,
            qui2.q3,
            qui2.q4,
            qui2.q5,
            qui2.q6,
            qui2.q7,
            qui2.q8,
            qui2.q9,
            qui2.q10,
            qui2.q11,
            qui2.q12,
            qui2.q13,
            qui2.q14,
            qui2.q15,
        ]
        lm2 = [
            qui2.q1m,
            qui2.q2m,
            qui2.q3m,
            qui2.q4m,
            qui2.q5m,
            qui2.q6m,
            qui2.q7m,
            qui2.q8m,
            qui2.q9m,
            qui2.q10m,
            qui2.q11m,
            qui2.q12m,
            qui2.q13m,
            qui2.q14m,
            qui2.q15m,
        ]

        flash("Quiz 3 Mapping not yet uploaded !", category="danger")
        return render_template(
            "quizmappingdisplay.html", lco=lco, lm=lm, lco2=lco2, lm2=lm2, sett=[2]
        )

    elif q:
        lco = [
            q.q1,
            q.q2,
            q.q3,
            q.q4,
            q.q5,
            q.q6,
            q.q7,
            q.q8,
            q.q9,
            q.q10,
            q.q11,
            q.q12,
            q.q13,
            q.q14,
            q.q15,
        ]
        lm = [
            q.q1m,
            q.q2m,
            q.q3m,
            q.q4m,
            q.q5m,
            q.q6m,
            q.q7m,
            q.q8m,
            q.q9m,
            q.q10m,
            q.q11m,
            q.q12m,
            q.q13m,
            q.q14m,
            q.q15m,
        ]

        flash("Quiz 2 and Quiz 3 Mapping not yet uploaded !", category="danger")
        return render_template("quizmappingdisplay.html", lco=lco, lm=lm, sett=[1])

    else:
        flash(
            f"No quiz mapping has been set yet for the course - {session['coursecode']} !",
            category="danger",
        )
        return render_template("newmain.html")


@app.route("/assignment_num_phases", methods=["GET", "POST"])
def numberphases():
    form = number_phases()

    def ans_marks(num):
        return float(num) if (num) else 0

    current_course = session["coursecode"]
    # current_course='21ME24'
    if current_course == "":
        flash("Please enter an appropriate Course Code!", category="danger")
        return render_template("newmain.html")

    if form.validate_on_submit():
        the_number = form.number.data

        session["coursecode"] = current_course
        session["number_phase"] = the_number

        print(session["coursecode"], session["number_phase"])
        return redirect(url_for("assign_mapping"))

    if form.errors != {}:
        for err_msg in form.errors.values():
            flash(f"There was an error : {err_msg}", category="danger")

    return render_template("assignment_num_phases.html", form=form)


@app.route("/assignmapping", methods=["GET", "POST"])
def assign_mapping():
    l = []

    def ans_co(num):
        return float(num) if (num) else 0

    def ans1(num):
        return int(num) if (num) else 0

    course_code = session["coursecode"]
    if course_code == "":
        flash("Please enter an appropriate Course Code!", category="danger")
        return render_template("newmain.html")

    count = session["number_phase"]
    print(count)
    for i in range(1, count + 1):
        l.append(
            {
                "rubrics1": 0,
                "rubrics2": 0,
                "rubrics3": 0,
                "rubrics4": 0,
                "rubrics5": 0,
                "rubrics6": 0,
                "rubrics1m": 0,
                "rubrics2m": 0,
                "rubrics3m": 0,
                "rubrics4m": 0,
                "rubrics5m": 0,
                "rubrics6m": 0,
            }
        )

    form = all_phases(all=l)

    if form.validate_on_submit():

        co_marks = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        final = form.all.data
        print(final)

        if count == 1:
            phase1 = final[0]
            the_cos = [
                ans1(phase1["rubrics1"]),
                ans1(phase1["rubrics2"]),
                ans1(phase1["rubrics3"]),
                ans1(phase1["rubrics4"]),
                ans1(phase1["rubrics5"]),
                ans1(phase1["rubrics6"]),
            ]
            the_marks = [
                ans1(phase1["rubrics1m"]),
                ans1(phase1["rubrics2m"]),
                ans1(phase1["rubrics3m"]),
                ans1(phase1["rubrics4m"]),
                ans1(phase1["rubrics5m"]),
                ans1(phase1["rubrics6m"]),
            ]
            print(the_cos, the_marks)
            for i in range(6):
                co_marks[int(the_cos[i]) - 1] += the_marks[i]

            check = am.query.filter_by(coursecode=course_code).first()
            if check:
                check1 = am.query.filter_by(coursecode=course_code).update(
                    dict(
                        num_ph=count,
                        p1r1=the_cos[0],
                        p1r2=the_cos[1],
                        p1r3=the_cos[2],
                        p1r4=the_cos[3],
                        p1r5=the_cos[4],
                        p1r6=the_cos[5],
                        p1r1m=the_marks[0],
                        p1r2m=the_marks[1],
                        p1r3m=the_marks[2],
                        p1r4m=the_marks[3],
                        p1r5m=the_marks[4],
                        p1r6m=the_marks[5],
                        p1r1_bt = 0, 
                        p1r2_bt = 0, 
                        p1r3_bt = 0, 
                        p1r4_bt = 0, 
                        p1r5_bt = 0, 
                        p1r6_bt = 0, 
                        total_co1_marks=co_marks[0],
                        total_co2_marks=co_marks[1],
                        total_co3_marks=co_marks[2],
                        total_co4_marks=co_marks[3],
                        total_co5_marks=co_marks[4],
                        total_co6_marks=co_marks[5],
                        total_co7_marks=co_marks[6],
                        total_co8_marks=co_marks[7],
                        total_co9_marks=co_marks[8],
                        total_co10_marks=co_marks[9],
                        max_assignment_marks=sum(co_marks),
                    )
                )
            else:

                new_mapping = am(
                    coursecode=course_code,
                    num_ph=count,
                    p1r1=the_cos[0],
                    p1r2=the_cos[1],
                    p1r3=the_cos[2],
                    p1r4=the_cos[3],
                    p1r5=the_cos[4],
                    p1r6=the_cos[5],
                    p1r1m=the_marks[0],
                    p1r2m=the_marks[1],
                    p1r3m=the_marks[2],
                    p1r4m=the_marks[3],
                    p1r5m=the_marks[4],
                    p1r6m=the_marks[5],
                    p1r1_bt = 0, 
                    p1r2_bt = 0, 
                    p1r3_bt = 0, 
                    p1r4_bt = 0, 
                    p1r5_bt = 0, 
                    p1r6_bt = 0, 
                    total_co1_marks=co_marks[0],
                    total_co2_marks=co_marks[1],
                    total_co3_marks=co_marks[2],
                    total_co4_marks=co_marks[3],
                    total_co5_marks=co_marks[4],
                    total_co6_marks=co_marks[5],
                    total_co7_marks=co_marks[6],
                    total_co8_marks=co_marks[7],
                    total_co9_marks=co_marks[8],
                    total_co10_marks=co_marks[9],
                    max_assignment_marks=sum(co_marks),
                )
                print("assignment mapping added")

                db.session.add(new_mapping)
            db.session.commit()
            session["number_phase"] = 0

            flash(f"The assignment data was added", category="success")
            return redirect(url_for("numberphases"))

        elif count == 2:
            phase1, phase2 = final[0], final[1]
            the_cos = [
                ans1(phase1["rubrics1"]),
                ans1(phase1["rubrics2"]),
                ans1(phase1["rubrics3"]),
                ans1(phase1["rubrics4"]),
                ans1(phase1["rubrics5"]),
                ans1(phase1["rubrics6"]),
                ans1(phase2["rubrics1"]),
                ans1(phase2["rubrics2"]),
                ans1(phase2["rubrics3"]),
                ans1(phase2["rubrics4"]),
                ans1(phase2["rubrics5"]),
                ans1(phase2["rubrics6"]),
            ]
            the_marks = [
                ans1(phase1["rubrics1m"]),
                ans1(phase1["rubrics2m"]),
                ans1(phase1["rubrics3m"]),
                ans1(phase1["rubrics4m"]),
                ans1(phase1["rubrics5m"]),
                ans1(phase1["rubrics6m"]),
                ans1(phase2["rubrics1m"]),
                ans1(phase2["rubrics2m"]),
                ans1(phase2["rubrics3m"]),
                ans1(phase2["rubrics4m"]),
                ans1(phase2["rubrics5m"]),
                ans1(phase2["rubrics6m"]),
            ]
            print(the_cos, the_marks)
            for i in range(12):
                co_marks[int(the_cos[i]) - 1] += the_marks[i]

            check = am.query.filter_by(coursecode=course_code).first()
            if check:
                check1 = am.query.filter_by(coursecode=course_code).update(
                    dict(
                        num_ph=count,
                        p1r1=the_cos[0],
                        p1r2=the_cos[1],
                        p1r3=the_cos[2],
                        p1r4=the_cos[3],
                        p1r5=the_cos[4],
                        p1r6=the_cos[5],
                        p1r1m=the_marks[0],
                        p1r2m=the_marks[1],
                        p1r3m=the_marks[2],
                        p1r4m=the_marks[3],
                        p1r5m=the_marks[4],
                        p1r6m=the_marks[5],
                        p2r1=the_cos[6],
                        p2r2=the_cos[7],
                        p2r3=the_cos[8],
                        p2r4=the_cos[9],
                        p2r5=the_cos[10],
                        p2r6=the_cos[11],
                        p2r1m=the_marks[6],
                        p2r2m=the_marks[7],
                        p2r3m=the_marks[8],
                        p2r4m=the_marks[9],
                        p2r5m=the_marks[10],
                        p2r6m=the_marks[11],
                        p1r1_bt = 0, 
                        p1r2_bt = 0, 
                        p1r3_bt = 0, 
                        p1r4_bt = 0, 
                        p1r5_bt = 0, 
                        p1r6_bt = 0, 
                        p2r1_bt = 0, 
                        p2r2_bt = 0, 
                        p2r3_bt = 0, 
                        p2r4_bt = 0, 
                        p2r5_bt = 0, 
                        p2r6_bt = 0, 
                        total_co1_marks=co_marks[0],
                        total_co2_marks=co_marks[1],
                        total_co3_marks=co_marks[2],
                        total_co4_marks=co_marks[3],
                        total_co5_marks=co_marks[4],
                        total_co6_marks=co_marks[5],
                        total_co7_marks=co_marks[6],
                        total_co8_marks=co_marks[7],
                        total_co9_marks=co_marks[8],
                        total_co10_marks=co_marks[9],
                        max_assignment_marks=sum(co_marks),
                    )
                )
            else:
                new_mapping = am(
                    coursecode=course_code,
                    num_ph=count,
                    p1r1=the_cos[0],
                    p1r2=the_cos[1],
                    p1r3=the_cos[2],
                    p1r4=the_cos[3],
                    p1r5=the_cos[4],
                    p1r6=the_cos[5],
                    p1r1m=the_marks[0],
                    p1r2m=the_marks[1],
                    p1r3m=the_marks[2],
                    p1r4m=the_marks[3],
                    p1r5m=the_marks[4],
                    p1r6m=the_marks[5],
                    p2r1=the_cos[6],
                    p2r2=the_cos[7],
                    p2r3=the_cos[8],
                    p2r4=the_cos[9],
                    p2r5=the_cos[10],
                    p2r6=the_cos[11],
                    p2r1m=the_marks[6],
                    p2r2m=the_marks[7],
                    p2r3m=the_marks[8],
                    p2r4m=the_marks[9],
                    p2r5m=the_marks[10],
                    p2r6m=the_marks[11],
                    p1r1_bt = 0, 
                    p1r2_bt = 0, 
                    p1r3_bt = 0, 
                    p1r4_bt = 0, 
                    p1r5_bt = 0, 
                    p1r6_bt = 0, 
                    p2r1_bt = 0, 
                    p2r2_bt = 0, 
                    p2r3_bt = 0, 
                    p2r4_bt = 0, 
                    p2r5_bt = 0, 
                    p2r6_bt = 0, 
                    total_co1_marks=co_marks[0],
                    total_co2_marks=co_marks[1],
                    total_co3_marks=co_marks[2],
                    total_co4_marks=co_marks[3],
                    total_co5_marks=co_marks[4],
                    total_co6_marks=co_marks[5],
                    total_co7_marks=co_marks[6],
                    total_co8_marks=co_marks[7],
                    total_co9_marks=co_marks[8],
                    total_co10_marks=co_marks[9],
                    max_assignment_marks=sum(co_marks),
                )
                print()

                db.session.add(new_mapping)
            db.session.commit()
            session["number_phase"] = 0

            flash(
                f"Somehow worked..The assignment data was added-2", category="success"
            )
            return redirect(url_for("numberphases"))

        elif count == 3:
            phase1, phase2, phase3 = final[0], final[1], final[2]
            the_cos = [
                ans1(phase1["rubrics1"]),
                ans1(phase1["rubrics2"]),
                ans1(phase1["rubrics3"]),
                ans1(phase1["rubrics4"]),
                ans1(phase1["rubrics5"]),
                ans1(phase1["rubrics6"]),
                ans1(phase2["rubrics1"]),
                ans1(phase2["rubrics2"]),
                ans1(phase2["rubrics3"]),
                ans1(phase2["rubrics4"]),
                ans1(phase2["rubrics5"]),
                ans1(phase2["rubrics6"]),
                ans1(phase3["rubrics1"]),
                ans1(phase3["rubrics2"]),
                ans1(phase3["rubrics3"]),
                ans1(phase3["rubrics4"]),
                ans1(phase3["rubrics5"]),
                ans1(phase3["rubrics6"]),
            ]
            the_marks = [
                ans1(phase1["rubrics1m"]),
                ans1(phase1["rubrics2m"]),
                ans1(phase1["rubrics3m"]),
                ans1(phase1["rubrics4m"]),
                ans1(phase1["rubrics5m"]),
                ans1(phase1["rubrics6m"]),
                ans1(phase2["rubrics1m"]),
                ans1(phase2["rubrics2m"]),
                ans1(phase2["rubrics3m"]),
                ans1(phase2["rubrics4m"]),
                ans1(phase2["rubrics5m"]),
                ans1(phase2["rubrics6m"]),
                ans1(phase3["rubrics1m"]),
                ans1(phase3["rubrics2m"]),
                ans1(phase3["rubrics3m"]),
                ans1(phase3["rubrics4m"]),
                ans1(phase3["rubrics5m"]),
                ans1(phase3["rubrics6m"]),
            ]
            print(the_cos, the_marks)
            for i in range(18):
                co_marks[int(the_cos[i]) - 1] += the_marks[i]

            check = am.query.filter_by(coursecode=course_code).first()
            if check:
                check1 = am.query.filter_by(coursecode=course_code).update(
                    dict(
                        num_ph=count,
                        p1r1=the_cos[0],
                        p1r2=the_cos[1],
                        p1r3=the_cos[2],
                        p1r4=the_cos[3],
                        p1r5=the_cos[4],
                        p1r6=the_cos[5],
                        p1r1m=the_marks[0],
                        p1r2m=the_marks[1],
                        p1r3m=the_marks[2],
                        p1r4m=the_marks[3],
                        p1r5m=the_marks[4],
                        p1r6m=the_marks[5],
                        p2r1=the_cos[6],
                        p2r2=the_cos[7],
                        p2r3=the_cos[8],
                        p2r4=the_cos[9],
                        p2r5=the_cos[10],
                        p2r6=the_cos[11],
                        p2r1m=the_marks[6],
                        p2r2m=the_marks[7],
                        p2r3m=the_marks[8],
                        p2r4m=the_marks[9],
                        p2r5m=the_marks[10],
                        p2r6m=the_marks[11],
                        p3r1=the_cos[12],
                        p3r2=the_cos[13],
                        p3r3=the_cos[14],
                        p3r4=the_cos[15],
                        p3r5=the_cos[16],
                        p3r6=the_cos[17],
                        p3r1m=the_marks[12],
                        p3r2m=the_marks[13],
                        p3r3m=the_marks[14],
                        p3r4m=the_marks[15],
                        p3r5m=the_marks[16],
                        p3r6m=the_marks[17],
                        total_co1_marks=co_marks[0],
                        total_co2_marks=co_marks[1],
                        total_co3_marks=co_marks[2],
                        total_co4_marks=co_marks[3],
                        total_co5_marks=co_marks[4],
                        total_co6_marks=co_marks[5],
                        total_co7_marks=co_marks[6],
                        total_co8_marks=co_marks[7],
                        total_co9_marks=co_marks[8],
                        total_co10_marks=co_marks[9],
                        max_assignment_marks=sum(co_marks),
                    )
                )
            else:

                new_mapping = am(
                    coursecode=course_code,
                    num_ph=count,
                    p1r1=the_cos[0],
                    p1r2=the_cos[1],
                    p1r3=the_cos[2],
                    p1r4=the_cos[3],
                    p1r5=the_cos[4],
                    p1r6=the_cos[5],
                    p1r1m=the_marks[0],
                    p1r2m=the_marks[1],
                    p1r3m=the_marks[2],
                    p1r4m=the_marks[3],
                    p1r5m=the_marks[4],
                    p1r6m=the_marks[5],
                    p2r1=the_cos[6],
                    p2r2=the_cos[7],
                    p2r3=the_cos[8],
                    p2r4=the_cos[9],
                    p2r5=the_cos[10],
                    p2r6=the_cos[11],
                    p2r1m=the_marks[6],
                    p2r2m=the_marks[7],
                    p2r3m=the_marks[8],
                    p2r4m=the_marks[9],
                    p2r5m=the_marks[10],
                    p2r6m=the_marks[11],
                    p3r1=the_cos[12],
                    p3r2=the_cos[13],
                    p3r3=the_cos[14],
                    p3r4=the_cos[15],
                    p3r5=the_cos[16],
                    p3r6=the_cos[17],
                    p3r1m=the_marks[12],
                    p3r2m=the_marks[13],
                    p3r3m=the_marks[14],
                    p3r4m=the_marks[15],
                    p3r5m=the_marks[16],
                    p3r6m=the_marks[17],
                    total_co1_marks=co_marks[0],
                    total_co2_marks=co_marks[1],
                    total_co3_marks=co_marks[2],
                    total_co4_marks=co_marks[3],
                    total_co5_marks=co_marks[4],
                    total_co6_marks=co_marks[5],
                    total_co7_marks=co_marks[6],
                    total_co8_marks=co_marks[7],
                    total_co9_marks=co_marks[8],
                    total_co10_marks=co_marks[9],
                    max_assignment_marks=sum(co_marks),
                )
                print()

                db.session.add(new_mapping)
            db.session.commit()
            session["number_phase"] = 0

            flash(
                f"Somehow worked..The assignment data was added-3", category="success"
            )
            return redirect(url_for("numberphases"))

        elif count == 4:
            phase1, phase2, phase3, phase4 = final[0], final[1], final[2], final[3]
            the_cos = [
                ans1(phase1["rubrics1"]),
                ans1(phase1["rubrics2"]),
                ans1(phase1["rubrics3"]),
                ans1(phase1["rubrics4"]),
                ans1(phase1["rubrics5"]),
                ans1(phase1["rubrics6"]),
                ans1(phase2["rubrics1"]),
                ans1(phase2["rubrics2"]),
                ans1(phase2["rubrics3"]),
                ans1(phase2["rubrics4"]),
                ans1(phase2["rubrics5"]),
                ans1(phase2["rubrics6"]),
                ans1(phase3["rubrics1"]),
                ans1(phase3["rubrics2"]),
                ans1(phase3["rubrics3"]),
                ans1(phase3["rubrics4"]),
                ans1(phase3["rubrics5"]),
                ans1(phase3["rubrics6"]),
                ans1(phase4["rubrics1"]),
                ans1(phase4["rubrics2"]),
                ans1(phase4["rubrics3"]),
                ans1(phase4["rubrics4"]),
                ans1(phase4["rubrics5"]),
                ans1(phase4["rubrics6"]),
            ]
            the_marks = [
                ans1(phase1["rubrics1m"]),
                ans1(phase1["rubrics2m"]),
                ans1(phase1["rubrics3m"]),
                ans1(phase1["rubrics4m"]),
                ans1(phase1["rubrics5m"]),
                ans1(phase1["rubrics6m"]),
                ans1(phase2["rubrics1m"]),
                ans1(phase2["rubrics2m"]),
                ans1(phase2["rubrics3m"]),
                ans1(phase2["rubrics4m"]),
                ans1(phase2["rubrics5m"]),
                ans1(phase2["rubrics6m"]),
                ans1(phase3["rubrics1m"]),
                ans1(phase3["rubrics2m"]),
                ans1(phase3["rubrics3m"]),
                ans1(phase3["rubrics4m"]),
                ans1(phase3["rubrics5m"]),
                ans1(phase3["rubrics6m"]),
                ans1(phase4["rubrics1m"]),
                ans1(phase4["rubrics2m"]),
                ans1(phase4["rubrics3m"]),
                ans1(phase4["rubrics4m"]),
                ans1(phase4["rubrics5m"]),
                ans1(phase4["rubrics6m"]),
            ]
            print(the_cos, the_marks)
            for i in range(24):
                co_marks[int(the_cos[i]) - 1] += the_marks[i]

            check = am.query.filter_by(coursecode=course_code).first()
            if check:
                check1 = am.query.filter_by(coursecode=course_code).update(
                    dict(
                        num_ph=count,
                        p1r1=the_cos[0],
                        p1r2=the_cos[1],
                        p1r3=the_cos[2],
                        p1r4=the_cos[3],
                        p1r5=the_cos[4],
                        p1r6=the_cos[5],
                        p1r1m=the_marks[0],
                        p1r2m=the_marks[1],
                        p1r3m=the_marks[2],
                        p1r4m=the_marks[3],
                        p1r5m=the_marks[4],
                        p1r6m=the_marks[5],
                        p2r1=the_cos[6],
                        p2r2=the_cos[7],
                        p2r3=the_cos[8],
                        p2r4=the_cos[9],
                        p2r5=the_cos[10],
                        p2r6=the_cos[11],
                        p2r1m=the_marks[6],
                        p2r2m=the_marks[7],
                        p2r3m=the_marks[8],
                        p2r4m=the_marks[9],
                        p2r5m=the_marks[10],
                        p2r6m=the_marks[11],
                        p3r1=the_cos[12],
                        p3r2=the_cos[13],
                        p3r3=the_cos[14],
                        p3r4=the_cos[15],
                        p3r5=the_cos[16],
                        p3r6=the_cos[17],
                        p3r1m=the_marks[12],
                        p3r2m=the_marks[13],
                        p3r3m=the_marks[14],
                        p3r4m=the_marks[15],
                        p3r5m=the_marks[16],
                        p3r6m=the_marks[17],
                        p4r1=the_cos[18],
                        p4r2=the_cos[19],
                        p4r3=the_cos[20],
                        p4r4=the_cos[21],
                        p4r5=the_cos[22],
                        p4r6=the_cos[23],
                        p4r1m=the_marks[18],
                        p4r2m=the_marks[19],
                        p4r3m=the_marks[20],
                        p4r4m=the_marks[21],
                        p4r5m=the_marks[22],
                        p4r6m=the_marks[23],
                        total_co1_marks=co_marks[0],
                        total_co2_marks=co_marks[1],
                        total_co3_marks=co_marks[2],
                        total_co4_marks=co_marks[3],
                        total_co5_marks=co_marks[4],
                        total_co6_marks=co_marks[5],
                        total_co7_marks=co_marks[6],
                        total_co8_marks=co_marks[7],
                        total_co9_marks=co_marks[8],
                        total_co10_marks=co_marks[9],
                        max_assignment_marks=sum(co_marks),
                    )
                )
            else:
                new_mapping = am(
                    coursecode=course_code,
                    num_ph=count,
                    p1r1=the_cos[0],
                    p1r2=the_cos[1],
                    p1r3=the_cos[2],
                    p1r4=the_cos[3],
                    p1r5=the_cos[4],
                    p1r6=the_cos[5],
                    p1r1m=the_marks[0],
                    p1r2m=the_marks[1],
                    p1r3m=the_marks[2],
                    p1r4m=the_marks[3],
                    p1r5m=the_marks[4],
                    p1r6m=the_marks[5],
                    p2r1=the_cos[6],
                    p2r2=the_cos[7],
                    p2r3=the_cos[8],
                    p2r4=the_cos[9],
                    p2r5=the_cos[10],
                    p2r6=the_cos[11],
                    p2r1m=the_marks[6],
                    p2r2m=the_marks[7],
                    p2r3m=the_marks[8],
                    p2r4m=the_marks[9],
                    p2r5m=the_marks[10],
                    p2r6m=the_marks[11],
                    p3r1=the_cos[12],
                    p3r2=the_cos[13],
                    p3r3=the_cos[14],
                    p3r4=the_cos[15],
                    p3r5=the_cos[16],
                    p3r6=the_cos[17],
                    p3r1m=the_marks[12],
                    p3r2m=the_marks[13],
                    p3r3m=the_marks[14],
                    p3r4m=the_marks[15],
                    p3r5m=the_marks[16],
                    p3r6m=the_marks[17],
                    p4r1=the_cos[18],
                    p4r2=the_cos[19],
                    p4r3=the_cos[20],
                    p4r4=the_cos[21],
                    p4r5=the_cos[22],
                    p4r6=the_cos[23],
                    p4r1m=the_marks[18],
                    p4r2m=the_marks[19],
                    p4r3m=the_marks[20],
                    p4r4m=the_marks[21],
                    p4r5m=the_marks[22],
                    p4r6m=the_marks[23],
                    total_co1_marks=co_marks[0],
                    total_co2_marks=co_marks[1],
                    total_co3_marks=co_marks[2],
                    total_co4_marks=co_marks[3],
                    total_co5_marks=co_marks[4],
                    total_co6_marks=co_marks[5],
                    total_co7_marks=co_marks[6],
                    total_co8_marks=co_marks[7],
                    total_co9_marks=co_marks[8],
                    total_co10_marks=co_marks[9],
                    max_assignment_marks=sum(co_marks),
                )
                print()

                db.session.add(new_mapping)
            db.session.commit()
            session["number_phase"] = 0

            flash(
                f"Somehow worked..The assignment data was added-4", category="success"
            )
            return redirect(url_for("numberphases"))

        elif count == 5:
            phase1, phase2, phase3, phase4, phase5 = (
                final[0],
                final[1],
                final[2],
                final[3],
                final[4],
            )
            the_cos = [
                ans1(phase1["rubrics1"]),
                ans1(phase1["rubrics2"]),
                ans1(phase1["rubrics3"]),
                ans1(phase1["rubrics4"]),
                ans1(phase1["rubrics5"]),
                ans1(phase1["rubrics6"]),
                ans1(phase2["rubrics1"]),
                ans1(phase2["rubrics2"]),
                ans1(phase2["rubrics3"]),
                ans1(phase2["rubrics4"]),
                ans1(phase2["rubrics5"]),
                ans1(phase2["rubrics6"]),
                ans1(phase3["rubrics1"]),
                ans1(phase3["rubrics2"]),
                ans1(phase3["rubrics3"]),
                ans1(phase3["rubrics4"]),
                ans1(phase3["rubrics5"]),
                ans1(phase3["rubrics6"]),
                ans1(phase4["rubrics1"]),
                ans1(phase4["rubrics2"]),
                ans1(phase4["rubrics3"]),
                ans1(phase4["rubrics4"]),
                ans1(phase4["rubrics5"]),
                ans1(phase4["rubrics6"]),
                ans1(phase5["rubrics1"]),
                ans1(phase5["rubrics2"]),
                ans1(phase5["rubrics3"]),
                ans1(phase5["rubrics4"]),
                ans1(phase5["rubrics5"]),
                ans1(phase5["rubrics6"]),
            ]
            the_marks = [
                ans1(phase1["rubrics1m"]),
                ans1(phase1["rubrics2m"]),
                ans1(phase1["rubrics3m"]),
                ans1(phase1["rubrics4m"]),
                ans1(phase1["rubrics5m"]),
                ans1(phase1["rubrics6m"]),
                ans1(phase2["rubrics1m"]),
                ans1(phase2["rubrics2m"]),
                ans1(phase2["rubrics3m"]),
                ans1(phase2["rubrics4m"]),
                ans1(phase2["rubrics5m"]),
                ans1(phase2["rubrics6m"]),
                ans1(phase3["rubrics1m"]),
                ans1(phase3["rubrics2m"]),
                ans1(phase3["rubrics3m"]),
                ans1(phase3["rubrics4m"]),
                ans1(phase3["rubrics5m"]),
                ans1(phase3["rubrics6m"]),
                ans1(phase4["rubrics1m"]),
                ans1(phase4["rubrics2m"]),
                ans1(phase4["rubrics3m"]),
                ans1(phase4["rubrics4m"]),
                ans1(phase4["rubrics5m"]),
                ans1(phase4["rubrics6m"]),
                ans1(phase5["rubrics1m"]),
                ans1(phase5["rubrics2m"]),
                ans1(phase5["rubrics3m"]),
                ans1(phase5["rubrics4m"]),
                ans1(phase5["rubrics5m"]),
                ans1(phase5["rubrics6m"]),
            ]
            print(the_cos, the_marks)
            for i in range(30):
                co_marks[int(the_cos[i]) - 1] += the_marks[i]

            check = am.query.filter_by(coursecode=course_code).first()
            if check:
                check1 = am.query.filter_by(coursecode=course_code).update(
                    dict(
                        num_ph=count,
                        p1r1=the_cos[0],
                        p1r2=the_cos[1],
                        p1r3=the_cos[2],
                        p1r4=the_cos[3],
                        p1r5=the_cos[4],
                        p1r6=the_cos[5],
                        p1r1m=the_marks[0],
                        p1r2m=the_marks[1],
                        p1r3m=the_marks[2],
                        p1r4m=the_marks[3],
                        p1r5m=the_marks[4],
                        p1r6m=the_marks[5],
                        p2r1=the_cos[6],
                        p2r2=the_cos[7],
                        p2r3=the_cos[8],
                        p2r4=the_cos[9],
                        p2r5=the_cos[10],
                        p2r6=the_cos[11],
                        p2r1m=the_marks[6],
                        p2r2m=the_marks[7],
                        p2r3m=the_marks[8],
                        p2r4m=the_marks[9],
                        p2r5m=the_marks[10],
                        p2r6m=the_marks[11],
                        p3r1=the_cos[12],
                        p3r2=the_cos[13],
                        p3r3=the_cos[14],
                        p3r4=the_cos[15],
                        p3r5=the_cos[16],
                        p3r6=the_cos[17],
                        p3r1m=the_marks[12],
                        p3r2m=the_marks[13],
                        p3r3m=the_marks[14],
                        p3r4m=the_marks[15],
                        p3r5m=the_marks[16],
                        p3r6m=the_marks[17],
                        p4r1=the_cos[18],
                        p4r2=the_cos[19],
                        p4r3=the_cos[20],
                        p4r4=the_cos[21],
                        p4r5=the_cos[22],
                        p4r6=the_cos[23],
                        p4r1m=the_marks[18],
                        p4r2m=the_marks[19],
                        p4r3m=the_marks[20],
                        p4r4m=the_marks[21],
                        p4r5m=the_marks[22],
                        p4r6m=the_marks[23],
                        p5r1=the_cos[24],
                        p5r2=the_cos[25],
                        p5r3=the_cos[26],
                        p5r4=the_cos[27],
                        p5r5=the_cos[28],
                        p5r6=the_cos[29],
                        p5r1m=the_marks[24],
                        p5r2m=the_marks[25],
                        p5r3m=the_marks[26],
                        p5r4m=the_marks[27],
                        p5r5m=the_marks[28],
                        p5r6m=the_marks[29],
                        total_co1_marks=co_marks[0],
                        total_co2_marks=co_marks[1],
                        total_co3_marks=co_marks[2],
                        total_co4_marks=co_marks[3],
                        total_co5_marks=co_marks[4],
                        total_co6_marks=co_marks[5],
                        total_co7_marks=co_marks[6],
                        total_co8_marks=co_marks[7],
                        total_co9_marks=co_marks[8],
                        total_co10_marks=co_marks[9],
                        max_assignment_marks=sum(co_marks),
                    )
                )
            else:

                new_mapping = am(
                    coursecode=course_code,
                    num_ph=count,
                    p1r1=the_cos[0],
                    p1r2=the_cos[1],
                    p1r3=the_cos[2],
                    p1r4=the_cos[3],
                    p1r5=the_cos[4],
                    p1r6=the_cos[5],
                    p1r1m=the_marks[0],
                    p1r2m=the_marks[1],
                    p1r3m=the_marks[2],
                    p1r4m=the_marks[3],
                    p1r5m=the_marks[4],
                    p1r6m=the_marks[5],
                    p2r1=the_cos[6],
                    p2r2=the_cos[7],
                    p2r3=the_cos[8],
                    p2r4=the_cos[9],
                    p2r5=the_cos[10],
                    p2r6=the_cos[11],
                    p2r1m=the_marks[6],
                    p2r2m=the_marks[7],
                    p2r3m=the_marks[8],
                    p2r4m=the_marks[9],
                    p2r5m=the_marks[10],
                    p2r6m=the_marks[11],
                    p3r1=the_cos[12],
                    p3r2=the_cos[13],
                    p3r3=the_cos[14],
                    p3r4=the_cos[15],
                    p3r5=the_cos[16],
                    p3r6=the_cos[17],
                    p3r1m=the_marks[12],
                    p3r2m=the_marks[13],
                    p3r3m=the_marks[14],
                    p3r4m=the_marks[15],
                    p3r5m=the_marks[16],
                    p3r6m=the_marks[17],
                    p4r1=the_cos[18],
                    p4r2=the_cos[19],
                    p4r3=the_cos[20],
                    p4r4=the_cos[21],
                    p4r5=the_cos[22],
                    p4r6=the_cos[23],
                    p4r1m=the_marks[18],
                    p4r2m=the_marks[19],
                    p4r3m=the_marks[20],
                    p4r4m=the_marks[21],
                    p4r5m=the_marks[22],
                    p4r6m=the_marks[23],
                    p5r1=the_cos[24],
                    p5r2=the_cos[25],
                    p5r3=the_cos[26],
                    p5r4=the_cos[27],
                    p5r5=the_cos[28],
                    p5r6=the_cos[29],
                    p5r1m=the_marks[24],
                    p5r2m=the_marks[25],
                    p5r3m=the_marks[26],
                    p5r4m=the_marks[27],
                    p5r5m=the_marks[28],
                    p5r6m=the_marks[29],
                    total_co1_marks=co_marks[0],
                    total_co2_marks=co_marks[1],
                    total_co3_marks=co_marks[2],
                    total_co4_marks=co_marks[3],
                    total_co5_marks=co_marks[4],
                    total_co6_marks=co_marks[5],
                    total_co7_marks=co_marks[6],
                    total_co8_marks=co_marks[7],
                    total_co9_marks=co_marks[8],
                    total_co10_marks=co_marks[9],
                    max_assignment_marks=sum(co_marks),
                )
                print()

                db.session.add(new_mapping)
            db.session.commit()
            session["number_phase"] = 0

            flash(f"Somehow worked..The assignment data was added", category="success")
            return redirect(url_for("numberphases"))

    if form.errors != {}:
        for err_msg in form.errors.values():
            flash(f"There was an error : {err_msg}", category="danger")

    return render_template("assignment.html", form=form)


@app.route("/displaytestmapping", methods=["GET", "POST"])
def disp_testmapping():
    course_code = session["coursecode"]
    if course_code == "":
        flash("Please enter an appropriate Course Code!", category="danger")
        return render_template("newmain.html")

    t1 = test1_mapping.query.filter_by(coursecode=course_code).first()
    t2 = test2_mapping.query.filter_by(coursecode=course_code).first()
    t3 = test3_mapping.query.filter_by(coursecode=course_code).first()
    lques = [
        "q1a",
        "q1b",
        "q1c",
        "q2a",
        "q2b",
        "q2c",
        "q3a",
        "q3b",
        "q3c",
        "q4a",
        "q4b",
        "q4c",
        "q5a",
        "q5b",
        "q5c",
    ]

    if t1 and t2 and t3:

        lques = [
            "q1a",
            "q1b",
            "q1c",
            "q2a",
            "q2b",
            "q2c",
            "q3a",
            "q3b",
            "q3c",
            "q4a",
            "q4b",
            "q4c",
            "q5a",
            "q5b",
            "q5c",
        ]
        l1co = [
            t1.q1a,
            t1.q1b,
            t1.q1c,
            t1.q2a,
            t1.q2b,
            t1.q2c,
            t1.q3a,
            t1.q3b,
            t1.q3c,
            t1.q4a,
            t1.q4b,
            t1.q4c,
            t1.q5a,
            t1.q5b,
            t1.q5c,
        ]
        l2co = [
            t2.q1a,
            t2.q1b,
            t2.q1c,
            t2.q2a,
            t2.q2b,
            t2.q2c,
            t2.q3a,
            t2.q3b,
            t2.q3c,
            t2.q4a,
            t2.q4b,
            t2.q4c,
            t2.q5a,
            t2.q5b,
            t2.q5c,
        ]
        l3co = [
            t3.q1a,
            t3.q1b,
            t3.q1c,
            t3.q2a,
            t3.q2b,
            t3.q2c,
            t3.q3a,
            t3.q3b,
            t3.q3c,
            t3.q4a,
            t3.q4b,
            t3.q4c,
            t3.q5a,
            t3.q5b,
            t3.q5c,
        ]

        l1m = [
            t1.q1am,
            t1.q1bm,
            t1.q1cm,
            t1.q2am,
            t1.q2bm,
            t1.q2cm,
            t1.q3am,
            t1.q3bm,
            t1.q3cm,
            t1.q4am,
            t1.q4bm,
            t1.q4cm,
            t1.q5am,
            t1.q5bm,
            t1.q5cm,
        ]
        l2m = [
            t2.q1am,
            t2.q1bm,
            t2.q1cm,
            t2.q2am,
            t2.q2bm,
            t2.q2cm,
            t2.q3am,
            t2.q3bm,
            t2.q3cm,
            t2.q4am,
            t2.q4bm,
            t2.q4cm,
            t2.q5am,
            t2.q5bm,
            t2.q5cm,
        ]
        l3m = [
            t3.q1am,
            t3.q1bm,
            t3.q1cm,
            t3.q2am,
            t3.q2bm,
            t3.q2cm,
            t3.q3am,
            t3.q3bm,
            t3.q3cm,
            t3.q4am,
            t3.q4bm,
            t3.q4cm,
            t3.q5am,
            t3.q5bm,
            t3.q5cm,
        ]

        return render_template(
            "testmappingdisplay.html",
            l1co=l1co,
            l2co=l2co,
            l3co=l3co,
            l1m=l1m,
            l2m=l2m,
            l3m=l3m,
            sett=[3],
            lques=lques,
        )

    elif t1 and t2:
        l1co = [
            t1.q1a,
            t1.q1b,
            t1.q1c,
            t1.q2a,
            t1.q2b,
            t1.q2c,
            t1.q3a,
            t1.q3b,
            t1.q3c,
            t1.q4a,
            t1.q4b,
            t1.q4c,
            t1.q5a,
            t1.q5b,
            t1.q5c,
        ]
        l2co = [
            t2.q1a,
            t2.q1b,
            t2.q1c,
            t2.q2a,
            t2.q2b,
            t2.q2c,
            t2.q3a,
            t2.q3b,
            t2.q3c,
            t2.q4a,
            t2.q4b,
            t2.q4c,
            t2.q5a,
            t2.q5b,
            t2.q5c,
        ]

        l1m = [
            t1.q1am,
            t1.q1bm,
            t1.q1cm,
            t1.q2am,
            t1.q2bm,
            t1.q2cm,
            t1.q3am,
            t1.q3bm,
            t1.q3cm,
            t1.q4am,
            t1.q4bm,
            t1.q4cm,
            t1.q5am,
            t1.q5bm,
            t1.q5cm,
        ]
        l2m = [
            t2.q1am,
            t2.q1bm,
            t2.q1cm,
            t2.q2am,
            t2.q2bm,
            t2.q2cm,
            t2.q3am,
            t2.q3bm,
            t2.q3cm,
            t2.q4am,
            t2.q4bm,
            t2.q4cm,
            t2.q5am,
            t2.q5bm,
            t2.q5cm,
        ]

        return render_template(
            "testmappingdisplay.html",
            l1co=l1co,
            l2co=l2co,
            l1m=l1m,
            l2m=l2m,
            sett=[2],
            lques=lques,
        )

    elif t1:
        l1co = [
            t1.q1a,
            t1.q1b,
            t1.q1c,
            t1.q2a,
            t1.q2b,
            t1.q2c,
            t1.q3a,
            t1.q3b,
            t1.q3c,
            t1.q4a,
            t1.q4b,
            t1.q4c,
            t1.q5a,
            t1.q5b,
            t1.q5c,
        ]
        l1m = [
            t1.q1am,
            t1.q1bm,
            t1.q1cm,
            t1.q2am,
            t1.q2bm,
            t1.q2cm,
            t1.q3am,
            t1.q3bm,
            t1.q3cm,
            t1.q4am,
            t1.q4bm,
            t1.q4cm,
            t1.q5am,
            t1.q5bm,
            t1.q5cm,
        ]

        return render_template(
            "testmappingdisplay.html", l1co=l1co, l1m=l1m, sett=[1], lques=lques
        )

    else:
        flash(
            f"No test mapping has been set yet for the course - {session['coursecode']} !",
            category="danger",
        )
        return render_template("newmain.html")


@app.route("/displayassignmentmapping", methods=["GET", "POST"])
def disp_assignmentmapping():
    course_code = session["coursecode"]
    if course_code == "":
        flash("Please enter an appropriate Course Code!", category="danger")
        return render_template("newmain.html")

    a = am.query.filter_by(coursecode=session["coursecode"]).first()

    if a:
        numberph = a.num_ph
        if numberph == 5:
            lques1 = [
                "rubrics1",
                "rubrics2",
                "rubrics3",
                "rubrics4",
                "rubrics5",
                "rubrics6",
            ]
            l1co = [a.p1r1, a.p1r2, a.p1r3, a.p1r4, a.p1r5, a.p1r6]
            l1m = [a.p1r1m, a.p1r2m, a.p1r3m, a.p1r4m, a.p1r5m, a.p1r6m]

            lques2 = [
                "rubrics1",
                "rubrics2",
                "rubrics3",
                "rubrics4",
                "rubrics5",
                "rubrics6",
            ]
            l2co = [a.p2r1, a.p2r2, a.p2r3, a.p2r4, a.p2r5, a.p2r6]
            l2m = [a.p2r1m, a.p2r2m, a.p2r3m, a.p2r4m, a.p2r5m, a.p2r6m]

            lques3 = [
                "rubrics1",
                "rubrics2",
                "rubrics3",
                "rubrics4",
                "rubrics5",
                "rubrics6",
            ]
            l3co = [a.p3r1, a.p3r2, a.p3r3, a.p3r4, a.p3r5, a.p3r6]
            l3m = [a.p3r1m, a.p3r2m, a.p3r3m, a.p3r4m, a.p3r5m, a.p3r6m]

            lques4 = [
                "rubrics1",
                "rubrics2",
                "rubrics3",
                "rubrics4",
                "rubrics5",
                "rubrics6",
            ]
            l4co = [a.p4r1, a.p4r2, a.p4r3, a.p4r4, a.p4r5, a.p4r6]
            l4m = [a.p4r1m, a.p4r2m, a.p4r3m, a.p4r4m, a.p4r5m, a.p4r6m]

            lques5 = [
                "rubrics1",
                "rubrics2",
                "rubrics3",
                "rubrics4",
                "rubrics5",
                "rubrics6",
            ]
            l5co = [a.p5r1, a.p5r2, a.p5r3, a.p5r4, a.p5r5, a.p5r6]
            l5m = [a.p5r1m, a.p5r2m, a.p5r3m, a.p5r4m, a.p5r5m, a.p5r6m]

            return render_template(
                "assignmentmappingdisplay.html",
                lques1=lques1,
                l1co=l1co,
                l1m=l1m,
                lques2=lques2,
                l2co=l2co,
                l2m=l2m,
                lques3=lques3,
                l3co=l3co,
                l3m=l3m,
                lques4=lques4,
                l4co=l4co,
                l4m=l4m,
                lques5=lques5,
                l5co=l5co,
                l5m=l5m,
                sett=[5],
            )

        elif numberph == 4:
            lques1 = [
                "rubrics1",
                "rubrics2",
                "rubrics3",
                "rubrics4",
                "rubrics5",
                "rubrics6",
            ]
            l1co = [a.p1r1, a.p1r2, a.p1r3, a.p1r4, a.p1r5, a.p1r6]
            l1m = [a.p1r1m, a.p1r2m, a.p1r3m, a.p1r4m, a.p1r5m, a.p1r6m]

            lques2 = [
                "rubrics1",
                "rubrics2",
                "rubrics3",
                "rubrics4",
                "rubrics5",
                "rubrics6",
            ]
            l2co = [a.p2r1, a.p2r2, a.p2r3, a.p2r4, a.p2r5, a.p2r6]
            l2m = [a.p2r1m, a.p2r2m, a.p2r3m, a.p2r4m, a.p2r5m, a.p2r6m]

            lques3 = [
                "rubrics1",
                "rubrics2",
                "rubrics3",
                "rubrics4",
                "rubrics5",
                "rubrics6",
            ]
            l3co = [a.p3r1, a.p3r2, a.p3r3, a.p3r4, a.p3r5, a.p3r6]
            l3m = [a.p3r1m, a.p3r2m, a.p3r3m, a.p3r4m, a.p3r5m, a.p3r6m]

            lques4 = [
                "rubrics1",
                "rubrics2",
                "rubrics3",
                "rubrics4",
                "rubrics5",
                "rubrics6",
            ]
            l4co = [a.p4r1, a.p4r2, a.p4r3, a.p4r4, a.p4r5, a.p4r6]
            l4m = [a.p4r1m, a.p4r2m, a.p4r3m, a.p4r4m, a.p4r5m, a.p4r6m]

            return render_template(
                "assignmentmappingdisplay.html",
                lques1=lques1,
                l1co=l1co,
                l1m=l1m,
                lques2=lques2,
                l2co=l2co,
                l2m=l2m,
                lques3=lques3,
                l3co=l3co,
                l3m=l3m,
                lques4=lques4,
                l4co=l4co,
                l4m=l4m,
                sett=[4],
            )

        elif numberph == 3:
            lques1 = [
                "rubrics1",
                "rubrics2",
                "rubrics3",
                "rubrics4",
                "rubrics5",
                "rubrics6",
            ]
            l1co = [a.p1r1, a.p1r2, a.p1r3, a.p1r4, a.p1r5, a.p1r6]
            l1m = [a.p1r1m, a.p1r2m, a.p1r3m, a.p1r4m, a.p1r5m, a.p1r6m]

            lques2 = [
                "rubrics1",
                "rubrics2",
                "rubrics3",
                "rubrics4",
                "rubrics5",
                "rubrics6",
            ]
            l2co = [a.p2r1, a.p2r2, a.p2r3, a.p2r4, a.p2r5, a.p2r6]
            l2m = [a.p2r1m, a.p2r2m, a.p2r3m, a.p2r4m, a.p2r5m, a.p2r6m]

            lques3 = [
                "rubrics1",
                "rubrics2",
                "rubrics3",
                "rubrics4",
                "rubrics5",
                "rubrics6",
            ]
            l3co = [a.p3r1, a.p3r2, a.p3r3, a.p3r4, a.p3r5, a.p3r6]
            l3m = [a.p3r1m, a.p3r2m, a.p3r3m, a.p3r4m, a.p3r5m, a.p3r6m]

            return render_template(
                "assignmentmappingdisplay.html",
                lques1=lques1,
                l1co=l1co,
                l1m=l1m,
                lques2=lques2,
                l2co=l2co,
                l2m=l2m,
                lques3=lques3,
                l3co=l3co,
                l3m=l3m,
                sett=[3],
            )

        elif numberph == 2:
            lques1 = [
                "rubrics1",
                "rubrics2",
                "rubrics3",
                "rubrics4",
                "rubrics5",
                "rubrics6",
            ]
            l1co = [a.p1r1, a.p1r2, a.p1r3, a.p1r4, a.p1r5, a.p1r6]
            l1m = [a.p1r1m, a.p1r2m, a.p1r3m, a.p1r4m, a.p1r5m, a.p1r6m]

            lques2 = [
                "rubrics1",
                "rubrics2",
                "rubrics3",
                "rubrics4",
                "rubrics5",
                "rubrics6",
            ]
            l2co = [a.p2r1, a.p2r2, a.p2r3, a.p2r4, a.p2r5, a.p2r6]
            l2m = [a.p2r1m, a.p2r2m, a.p2r3m, a.p2r4m, a.p2r5m, a.p2r6m]

            return render_template(
                "assignmentmappingdisplay.html",
                lques1=lques1,
                l1co=l1co,
                l1m=l1m,
                lques2=lques2,
                l2co=l2co,
                l2m=l2m,
                sett=[2],
            )

        elif numberph == 1:
            lques1 = [
                "rubrics1",
                "rubrics2",
                "rubrics3",
                "rubrics4",
                "rubrics5",
                "rubrics6",
            ]
            l1co = [a.p1r1, a.p1r2, a.p1r3, a.p1r4, a.p1r5, a.p1r6]
            l1m = [a.p1r1m, a.p1r2m, a.p1r3m, a.p1r4m, a.p1r5m, a.p1r6m]

            return render_template(
                "assignmentmappingdisplay.html",
                lques1=lques1,
                l1co=l1co,
                l1m=l1m,
                sett=[1],
            )

    else:
        flash(
            f"No assignment mapping has been set yet for the course - {session['coursecode']}",
            category="danger",
        )
        return render_template("newmain.html")


##################################################################################################
##################################################################################################
# upload of csv files and adding the data to database

# Upload the staff is coursecode mapping
@app.route('/uploadstaffidcoursecodemapping', methods=['GET', 'POST'])
def upload_mapping():
    form = staffid_coursecode()
    
    if form.validate_on_submit():
        filename = secure_filename(form.file.data.filename)
        file_path = app.config["UPLOAD_FOLDER"] + filename
        form.file.data.save(file_path)
        d = {}
        
        with open(file_path, 'r', newline="") as f:
            r = csv.DictReader(f)
            
            for i in r:
                # d[str(i['STAFFID'])] = 
                update_staffid_cc = staffid_cc.query.filter_by(staffid = str(i['STAFFID']), coursecode=i['COURSECODE'], semester=i['SEMESTER']).first()
                if update_staffid_cc:
                    continue
                else:
                    new_mapping = staffid_cc(staffid = str(i['STAFFID']), coursecode=i['COURSECODE'], semester=i['SEMESTER'], usn_list="")
                    db.session.add(new_mapping)
                    db.session.commit()
        
        flash("All staff id coursecode mappings have been uploaded !", category="success")
    
    if form.errors != {}:
        for err_msg in form.errors.values():
            flash(f"There was an error : {err_msg}", category="danger")

    return render_template("staffid_cc_mapping.html", form=form)
    

@app.route("/uploadstudentcsv", methods=["GET", "POST"])
def upload_student():
    form = uploadstudent()

    current_staff = session["staffid"]
    # current_staff = "1234"
    if current_staff == "":
        flash("Please enter an appropriate Staff ID!", category="danger")
        return render_template("newmain.html")

    current_course = session["coursecode"]
    # current_course = "21ME24"
    if current_course == "":
        flash("Please enter an appropriate Course Code!", category="danger")
        return render_template("newmain.html")

    if form.validate_on_submit():
        filename = secure_filename(form.file.data.filename)

        new_filename = str(current_staff) + str(current_course) + ".csv"

        file_path = app.config["UPLOAD_FOLDER"] + filename
        form.file.data.save(file_path)

        findsem = course.query.filter_by(coursecode=current_course).first()
        semes = findsem.semester

        with open(file_path, "r", newline="") as f:
            r = csv.DictReader(f)
            new_str = ""

            for i in r:
                new_str += str(i["USN"]) + ","

                check = student.query.filter_by(usn=i["USN"]).first()
                if check:
                    check1 = student.query.filter_by(usn=i["USN"]).update(
                        dict(
                            department=i["Department"],
                            semester=i["Semester"],
                            name=i["Name"],
                        )
                    )
                else:
                    new_student = student(
                        usn=i["USN"],
                        department=i["Department"],
                        semester=i["Semester"],
                        name=i["Name"],
                    )
                    db.session.add(new_student)
                db.session.commit()

        update_staffid_cc = staffid_cc.query.filter_by(
            staffid=current_staff, coursecode=current_course
        ).update(dict(usn_list=new_str))
        db.session.commit()

        flash(
            "The student data was added and mapped with the staff ID!",
            category="success",
        )

        return redirect(url_for("create_samplecsv"))

    if form.errors != {}:
        for err_msg in form.errors.values():
            flash(f"There was an error : {err_msg}", category="danger")

    return render_template("new_student.html", form=form)


@app.route("/semgradetomarks", methods=["GET", "POST"])
def sem_gradetomarks():
    form = uploadsem()

    course_code = session["coursecode"]
    # access = course.query.filter_by(coursecode=)
    # course_code = '21ME24'
    if course_code == "":
        flash("Please enter an appropriate Course Code!", category="danger")
        return render_template("newmain.html")

    access = course.query.filter_by(coursecode=course_code).first()
    labstat = access.labyorn  
    

    if labstat == "Y":
        max_marks = 300
    elif labstat == "N":
        max_marks = 200

    if form.validate_on_submit():
        
        
        filename = secure_filename(form.file.data.filename)
        given_coursecode = course_code

        file_path = app.config["UPLOAD_FOLDER"] + filename
        form.file.data.save(file_path)  # +filename

        with open(file_path, "r", newline="") as f:
            head = ["USN", "Grade"]
            r = csv.DictReader(f)

            for i in r:
                print(i["USN"], i["Grade"])
                the_grade = str(i["Grade"])
                
                if the_grade in ["F", "NSSR", "NSAR", "X", "NE", "I", "W"]:
                    gp = 0
                else:
                    gp = grade_marks.query.filter_by(scheme=2021, alloted_grade=the_grade).first().gpoint
                
                    # if the_grade == "O":
                    #     #gp = 10
                    #     gp = 10
                    # elif the_grade == "A+":
                    #     gp = 9
                    # elif the_grade == "A":
                    #     gp = 8
                    # elif the_grade == "B+":
                    #     gp = 7
                    # elif the_grade == "B":
                    #     gp = 6
                    # elif the_grade == "C":
                    #     gp = 5
                    # elif the_grade == "P":
                    #     gp = 4
                    
                

                eq_marks = ((gp - 0.75) / 10) * max_marks
                other_one = student_co.query.filter_by(
                    usn=i["USN"], coursecode=course_code
                ).first()
                int_marks = other_one.internal_marks
                sem_marks = eq_marks - int_marks

                check1 = student_co.query.filter_by(
                    usn=i["USN"], coursecode=course_code
                ).update(
                    dict(
                        sem_end_grade=the_grade,
                        equivalent_marks=eq_marks,
                        sem_end_marks=round(sem_marks, 2),
                    )
                )
                db.session.commit()

        flash(
            "The sem end data was updated in the student co table !", category="success"
        )
        return render_template("newmain.html")

    if form.errors != {}:
        for err_msg in form.errors.values():
            flash(f"There was an error : {err_msg}", category="danger")

    return render_template("sem_grade_upload.html", form=form)


@app.route("/uploadassignment", methods=["GET", "POST"])
def upload_assign():
    form = uploadassign()

    def ans1(num):
        return float(num) if num else 0

    def ans2(num):
        return int(num) if num else 0

    the_coursecode = session["coursecode"]
    # the_coursecode = '21ME24'
    if the_coursecode == "":
        flash("Please enter an appropriate Course Code!", category="danger")
        return render_template("newmain.html")

    head = [
        "USN",
        "p1r1",
        "p1r2",
        "p1r3",
        "p1r4",
        "p1r5",
        "p1r6",
        "p2r1",
        "p2r2",
        "p2r3",
        "p2r4",
        "p2r5",
        "p2r6",
        "p3r1",
        "p3r2",
        "p3r3",
        "p3r4",
        "p3r5",
        "p3r6",
        "p4r1",
        "p4r2",
        "p4r3",
        "p4r4",
        "p4r5",
        "p4r6",
        "p5r1",
        "p5r2",
        "p5r3",
        "p5r4",
        "p5r5",
        "p5r6",
    ]

    map_assign = am.query.filter_by(coursecode=the_coursecode).first()

    if form.validate_on_submit():

        filename = secure_filename(form.file.data.filename)

        file_path = app.config["UPLOAD_FOLDER"] + filename
        form.file.data.save(file_path)  # +filename

        m = am.query.filter_by(coursecode=the_coursecode).first()
        print(m.num_ph)

        l_co = [
            m.p1r1,
            m.p1r2,
            m.p1r3,
            m.p1r4,
            m.p1r5,
            m.p1r6,
            m.p2r1,
            m.p2r2,
            m.p2r3,
            m.p2r4,
            m.p2r5,
            m.p2r6,
            m.p3r1,
            m.p3r2,
            m.p3r3,
            m.p3r4,
            m.p3r5,
            m.p3r6,
            m.p4r1,
            m.p4r2,
            m.p4r3,
            m.p4r4,
            m.p4r5,
            m.p4r6,
            m.p5r1,
            m.p5r2,
            m.p5r3,
            m.p5r4,
            m.p5r5,
            m.p5r6,
        ]

        l_m = [
            m.p1r1m,
            m.p1r2m,
            m.p1r3m,
            m.p1r4m,
            m.p1r5m,
            m.p1r6m,
            m.p2r1m,
            m.p2r2m,
            m.p2r3m,
            m.p2r4m,
            m.p2r5m,
            m.p2r6m,
            m.p3r1m,
            m.p3r2m,
            m.p3r3m,
            m.p3r4m,
            m.p3r5m,
            m.p3r6m,
            m.p4r1m,
            m.p4r2m,
            m.p4r3m,
            m.p4r4m,
            m.p4r5m,
            m.p4r6m,
            m.p5r1m,
            m.p5r2m,
            m.p5r3m,
            m.p5r4m,
            m.p5r5m,
            m.p5r6m,
        ]

        with open(file_path, "r", newline="") as f:
            r = csv.DictReader(f)

            for i in r:
                co_scored = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
                new_rec = [
                    ans1(i["p1r1"]),
                    ans1(i["p1r2"]),
                    ans1(i["p1r3"]),
                    ans1(i["p1r4"]),
                    ans1(i["p1r5"]),
                    ans1(i["p1r6"]),
                    ans1(i["p2r1"]),
                    ans1(i["p2r2"]),
                    ans1(i["p2r3"]),
                    ans1(i["p2r4"]),
                    ans1(i["p2r5"]),
                    ans1(i["p2r6"]),
                    ans1(i["p3r1"]),
                    ans1(i["p3r2"]),
                    ans1(i["p3r3"]),
                    ans1(i["p3r4"]),
                    ans1(i["p3r5"]),
                    ans1(i["p3r6"]),
                    ans1(i["p4r1"]),
                    ans1(i["p4r2"]),
                    ans1(i["p4r3"]),
                    ans1(i["p4r4"]),
                    ans1(i["p4r5"]),
                    ans1(i["p4r6"]),
                    ans1(i["p5r1"]),
                    ans1(i["p5r2"]),
                    ans1(i["p5r3"]),
                    ans1(i["p5r4"]),
                    ans1(i["p5r5"]),
                    ans1(i["p5r6"]),
                ]

                for k in range(30):
                    co_scored[int(l_co[k]) - 1] += int(new_rec[k])
                print(co_scored)
                the_cop = [
                    (co_scored[0] / map_assign.total_co1_marks) * 100,
                    (co_scored[1] / map_assign.total_co2_marks) * 100,
                    (co_scored[2] / map_assign.total_co3_marks) * 100,
                    (co_scored[3] / map_assign.total_co4_marks) * 100,
                    (co_scored[4] / map_assign.total_co5_marks) * 100
                    if map_assign.total_co5_marks
                    else 0,
                    (co_scored[5] / map_assign.total_co6_marks) * 100
                    if map_assign.total_co6_marks
                    else 0,
                    (co_scored[6] / map_assign.total_co7_marks) * 100
                    if map_assign.total_co7_marks
                    else 0,
                    (co_scored[7] / map_assign.total_co8_marks) * 100
                    if map_assign.total_co8_marks
                    else 0,
                    (co_scored[8] / map_assign.total_co9_marks) * 100
                    if map_assign.total_co9_marks
                    else 0,
                    (co_scored[9] / map_assign.total_co10_marks) * 100
                    if map_assign.total_co10_marks
                    else 0,
                ]

                check = assignment.query.filter_by(
                    usn=i[head[0]], coursecode=the_coursecode
                ).first()
                if check:
                    check1 = assignment.query.filter_by(
                        usn=i[head[0]], coursecode=the_coursecode
                    ).update(
                        dict(
                            p1r1=new_rec[0],
                            p1r2=new_rec[1],
                            p1r3=new_rec[2],
                            p1r4=new_rec[3],
                            p1r5=new_rec[4],
                            p1r6=new_rec[5],
                            p2r1=new_rec[6],
                            p2r2=new_rec[7],
                            p2r3=new_rec[8],
                            p2r4=new_rec[9],
                            p2r5=new_rec[10],
                            p2r6=new_rec[11],
                            p3r1=new_rec[12],
                            p3r2=new_rec[13],
                            p3r3=new_rec[14],
                            p3r4=new_rec[15],
                            p3r5=new_rec[16],
                            p3r6=new_rec[17],
                            p4r1=new_rec[18],
                            p4r2=new_rec[19],
                            p4r3=new_rec[20],
                            p4r4=new_rec[21],
                            p4r5=new_rec[22],
                            p4r6=new_rec[23],
                            p5r1=new_rec[24],
                            p5r2=new_rec[25],
                            p5r3=new_rec[26],
                            p5r4=new_rec[27],
                            p5r5=new_rec[28],
                            p5r6=new_rec[29],
                            total_assignment_marks=sum(new_rec),
                            co1_marks=co_scored[0],
                            co2_marks=co_scored[1],
                            co3_marks=co_scored[2],
                            co4_marks=co_scored[3],
                            co5_marks=co_scored[4],
                            co6_marks=co_scored[5],
                            co7_marks=co_scored[6],
                            co8_marks=co_scored[7],
                            co9_marks=co_scored[8],
                            co10_marks=co_scored[9],
                            co1p=the_cop[0],
                            co2p=the_cop[1],
                            co3p=the_cop[2],
                            co4p=the_cop[3],
                            co5p=the_cop[4],
                            co6p=the_cop[5],
                            co7p=the_cop[6],
                            co8p=the_cop[7],
                            co9p=the_cop[8],
                            co10p=the_cop[9],
                        )
                    )

                else:

                    to_add = assignment(
                        usn=i[head[0]],
                        coursecode=the_coursecode,
                        p1r1=new_rec[0],
                        p1r2=new_rec[1],
                        p1r3=new_rec[2],
                        p1r4=new_rec[3],
                        p1r5=new_rec[4],
                        p1r6=new_rec[5],
                        p2r1=new_rec[6],
                        p2r2=new_rec[7],
                        p2r3=new_rec[8],
                        p2r4=new_rec[9],
                        p2r5=new_rec[10],
                        p2r6=new_rec[11],
                        p3r1=new_rec[12],
                        p3r2=new_rec[13],
                        p3r3=new_rec[14],
                        p3r4=new_rec[15],
                        p3r5=new_rec[16],
                        p3r6=new_rec[17],
                        p4r1=new_rec[18],
                        p4r2=new_rec[19],
                        p4r3=new_rec[20],
                        p4r4=new_rec[21],
                        p4r5=new_rec[22],
                        p4r6=new_rec[23],
                        p5r1=new_rec[24],
                        p5r2=new_rec[25],
                        p5r3=new_rec[26],
                        p5r4=new_rec[27],
                        p5r5=new_rec[28],
                        p5r6=new_rec[29],
                        total_assignment_marks=sum(new_rec),
                        co1_marks=co_scored[0],
                        co2_marks=co_scored[1],
                        co3_marks=co_scored[2],
                        co4_marks=co_scored[3],
                        co5_marks=co_scored[4],
                        co6_marks=co_scored[5],
                        co7_marks=co_scored[6],
                        co8_marks=co_scored[7],
                        co9_marks=co_scored[8],
                        co10_marks=co_scored[9],
                        co1p=the_cop[0],
                        co2p=the_cop[1],
                        co3p=the_cop[2],
                        co4p=the_cop[3],
                        co5p=the_cop[4],
                        co6p=the_cop[5],
                        co7p=the_cop[6],
                        co8p=the_cop[7],
                        co9p=the_cop[8],
                        co10p=the_cop[9],
                    )

                    db.session.add(to_add)
                db.session.commit()

            flash("The assignment marks were uploaded !", category="success")
            return redirect(url_for("upload_assign"))

    if form.errors != {}:
        for err_msg in form.errors.values():
            flash(f"There was an error : {err_msg}", category="danger")

    return render_template("assignment_upload.html", form=form)


@app.route("/calculatelabco", methods=["GET", "POST"])
def labco_calc():
    form = labfile_upload()

    # course_code = '21ME24'
    course_code = session["coursecode"]
    if course_code == "":
        flash("Please enter an appropriate Course Code!", category="danger")
        return render_template("newmain.html")

    the_course = course.query.filter_by(coursecode=course_code).first()
    lab_status = the_course.labyorn

    if lab_status == "N":
        flash("The current course does not have a lab component !", category="danger")
        return render_template("newmain.html")

    if form.validate_on_submit():
        filename = secure_filename(form.file.data.filename)

        file_path = app.config["UPLOAD_FOLDER"] + filename
        form.file.data.save(file_path)

        with open(file_path, "r", newline="") as f:
            # for i in range(14):
            #     skip_mapping = next(f)

            r = csv.reader(f)

            for row in r:
                # usn = row[1]
                # co1p = row[79]
                # co2p = row[80]
                # co3p = row[81]
                # co4p = row[82]
                # co5p = row[83]
                # co6p = row[84]
                # co7p = row[85]
                # co8p = row[86]
                # co9p = row[87]
                # co10p = row[88]
                if(row["USN"]==""):
                    continue
                usn = row["USN"]
                co1p = row["co1p"]
                co2p = row["co2p"]
                co3p = row["co3p"]
                co4p = row["co4p"]
                co5p = row["co5p"]
                co6p = row["co6p"]
                co7p = row["co7p"]
                co8p = row["co8p"]
                co9p = row["co9p"]
                co10p = row["co10p"]

                check = lab_co.query.filter_by(usn=usn, coursecode=course_code).first()
                if check:
                    check1 = lab_co.query.filter_by(
                        usn=usn, coursecode=course_code
                    ).update(
                        dict(
                            co1p=co1p if co1p else 0,
                            co2p=co2p if co2p else 0,
                            co3p=co3p if co3p else 0,
                            co4p=co4p if co4p else 0,
                            co5p=co5p if co5p else 0,
                            co6p=co6p if co6p else 0,
                            co7p=co7p if co7p else 0,
                            co8p=co8p if co8p else 0,
                            co9p=co9p if co9p else 0,
                            co10p=co10p if co10p else 0,
                        )
                    )
                else:
                    new_student = lab_co(
                        usn=usn,
                        coursecode=course_code,
                        co1p=co1p if co1p else 0,
                        co2p=co2p if co2p else 0,
                        co3p=co3p if co3p else 0,
                        co4p=co4p if co4p else 0,
                        co5p=co5p if co5p else 0,
                        co6p=co6p if co6p else 0,
                        co7p=co7p if co7p else 0,
                        co8p=co8p if co8p else 0,
                        co9p=co9p if co9p else 0,
                        co10p=co10p if co10p else 0,
                    )
                    db.session.add(new_student)
                db.session.commit()

        flash(
            "All the data from the lab csv has been updated to database!",
            category="success",
        )
        return render_template("newmain.html")

    if form.errors != {}:
        for err_msg in form.errors.values():
            flash(f"There was an error : {err_msg}", category="danger")

    return render_template("labcsv_upload.html", form=form)


# --this is for cie , quiz upload
@app.route("/upload", methods=["GET", "POST"])
def upload_csv():
    form = uploadcsv()
    head = [
        "USN",
        "Version",
        "1",
        "2",
        "3",
        "4",
        "5",
        "6",
        "7",
        "8",
        "9",
        "10",
        "11",
        "12",
        "13",
        "14",
        "15",
        "1a",
        "1b",
        "1c",
        "2a",
        "2b",
        "2c",
        "3a",
        "3b",
        "3c",
        "4a",
        "4b",
        "4c",
        "5a",
        "5b",
        "5c",
    ]

    given_coursecode = session["coursecode"]
    # given_coursecode = '21ME24'
    if given_coursecode == "":
        flash("Please enter an appropriate Course Code!", category="danger")
        return render_template("newmain.html")

    if form.validate_on_submit():
        filename = secure_filename(form.file.data.filename)
        the_cie_number = form.cie_number.data

        file_path = app.config["UPLOAD_FOLDER"] + filename
        form.file.data.save(file_path)  # +filename

        with open(file_path, "r", newline="") as f:
            r = csv.DictReader(f)
            final = {}

            if the_cie_number == 1:
                t = test1_mapping.query.filter_by(coursecode=given_coursecode).first()

                # lt and ltm are the values from the test1 database created locally
                lt = [
                    t.q1a,
                    t.q1b,
                    t.q1c,
                    t.q2a,
                    t.q2b,
                    t.q2c,
                    t.q3a,
                    t.q3b,
                    t.q3c,
                    t.q4a,
                    t.q4b,
                    t.q4c,
                    t.q5a,
                    t.q5b,
                    t.q5c,
                ]
                ltm = [
                    t.q1am,
                    t.q1bm,
                    t.q1cm,
                    t.q2am,
                    t.q2bm,
                    t.q2cm,
                    t.q3am,
                    t.q3bm,
                    t.q3cm,
                    t.q4am,
                    t.q4bm,
                    t.q4cm,
                    t.q5am,
                    t.q5bm,
                    t.q5cm,
                ]

                # total_co_test = [t.total_co1_marks, t.total_co2_marks, t.total_co3_marks,
                #                 t.total_co4_marks, t.total_co5_marks, t.total_co6_marks,
                #                 t.total_co7_marks, t.total_co8_marks, t.total_co9_marks, t.total_co10_marks]

                for i in r:

                    def ans2(num):
                        return float(num) if num else sqlalchemy.null()

                    def ans1(num):
                        return float(num) if num else 0

                    m = quiz1_mapping.query.filter_by(
                        coursecode=given_coursecode, version=i["Version"]
                    ).first()
                    mq = [
                        m.q1,
                        m.q2,
                        m.q3,
                        m.q4,
                        m.q5,
                        m.q6,
                        m.q7,
                        m.q8,
                        m.q9,
                        m.q10,
                        m.q11,
                        m.q12,
                        m.q13,
                        m.q14,
                        m.q15,
                    ]
                    mqm = [
                        m.q1m,
                        m.q2m,
                        m.q3m,
                        m.q4m,
                        m.q5m,
                        m.q6m,
                        m.q7m,
                        m.q8m,
                        m.q9m,
                        m.q10m,
                        m.q11m,
                        m.q12m,
                        m.q13m,
                        m.q14m,
                        m.q15m,
                    ]

                    new_quiz = [
                        ans1((i["1"])),
                        ans1((i["2"])),
                        ans1((i["3"])),
                        ans1((i["4"])),
                        ans1((i["5"])),
                        ans1((i["6"])),
                        ans1((i["7"])),
                        ans1((i["8"])),
                        ans1((i["9"])),
                        ans1((i["10"])),
                        ans1((i["11"])),
                        ans1((i["12"])),
                        ans1((i["13"])),
                        ans1((i["14"])),
                        ans1((i["15"])),
                    ]

                    student_co_scores = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

                    for k in range(15):
                        student_co_scores[int(mq[k]) - 1] += new_quiz[k]

                    check = quiz1.query.filter_by(
                        usn=i["USN"], coursecode=given_coursecode
                    ).first()
                    if check:
                        check1 = quiz1.query.filter_by(
                            usn=i["USN"], coursecode=given_coursecode
                        ).update(
                            dict(
                                version=i["Version"],
                                q1=new_quiz[0],
                                q2=new_quiz[1],
                                q3=new_quiz[2],
                                q4=new_quiz[3],
                                q5=new_quiz[4],
                                q6=new_quiz[5],
                                q7=new_quiz[6],
                                q8=new_quiz[7],
                                q9=new_quiz[8],
                                q10=new_quiz[9],
                                q11=new_quiz[10],
                                q12=new_quiz[11],
                                q13=new_quiz[12],
                                q14=new_quiz[13],
                                q15=new_quiz[14],
                                marks_q=sum(new_quiz),
                                co1_marks=student_co_scores[0],
                                co2_marks=student_co_scores[1],
                                co3_marks=student_co_scores[2],
                                co4_marks=student_co_scores[3],
                                co5_marks=student_co_scores[4],
                                co6_marks=student_co_scores[5],
                                co7_marks=student_co_scores[6],
                                co8_marks=student_co_scores[7],
                                co9_marks=student_co_scores[8],
                                co10_marks=student_co_scores[9],
                            )
                        )
                    else:
                        quiz = quiz1(
                            usn=i["USN"],
                            coursecode=given_coursecode,
                            version=i["Version"],
                            q1=new_quiz[0],
                            q2=new_quiz[1],
                            q3=new_quiz[2],
                            q4=new_quiz[3],
                            q5=new_quiz[4],
                            q6=new_quiz[5],
                            q7=new_quiz[6],
                            q8=new_quiz[7],
                            q9=new_quiz[8],
                            q10=new_quiz[9],
                            q11=new_quiz[10],
                            q12=new_quiz[11],
                            q13=new_quiz[12],
                            q14=new_quiz[13],
                            q15=new_quiz[14],
                            marks_q=sum(new_quiz),
                            co1_marks=student_co_scores[0],
                            co2_marks=student_co_scores[1],
                            co3_marks=student_co_scores[2],
                            co4_marks=student_co_scores[3],
                            co5_marks=student_co_scores[4],
                            co6_marks=student_co_scores[5],
                            co7_marks=student_co_scores[6],
                            co8_marks=student_co_scores[7],
                            co9_marks=student_co_scores[8],
                            co10_marks=student_co_scores[9],
                        )
                        db.session.add(quiz)

                    new_test = [
                        ans1(i["1a"]),
                        ans1(i["1b"]),
                        ans1(i["1c"]),
                        ans1(i["2a"]),
                        ans1(i["2b"]),
                        ans1(i["2c"]),
                        ans1(i["3a"]),
                        ans1(i["3b"]),
                        ans1(i["3c"]),
                        ans1(i["4a"]),
                        ans1(i["4b"]),
                        ans1(i["4c"]),
                        ans1(i["5a"]),
                        ans1(i["5b"]),
                        ans1(i["5c"]),
                    ]
                    test_co_scores = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

                    for k in range(15):
                        test_co_scores[int(lt[k]) - 1] += new_test[k]

                    check = test1.query.filter_by(
                        usn=i["USN"], coursecode=given_coursecode
                    ).first()
                    if check:
                        check1 = test1.query.filter_by(
                            usn=i["USN"], coursecode=given_coursecode
                        ).update(
                            dict(
                                q1a=new_test[0],
                                q1b=new_test[1],
                                q1c=new_test[2],
                                q2a=new_test[3],
                                q2b=new_test[4],
                                q2c=new_test[5],
                                q3a=new_test[6],
                                q3b=new_test[7],
                                q3c=new_test[8],
                                q4a=new_test[9],
                                q4b=new_test[10],
                                q4c=new_test[11],
                                q5a=new_test[12],
                                q5b=new_test[13],
                                q5c=new_test[14],
                                marks=sum(new_test),
                                co1_marks=test_co_scores[0],
                                co2_marks=test_co_scores[1],
                                co3_marks=test_co_scores[2],
                                co4_marks=test_co_scores[3],
                                co5_marks=test_co_scores[4],
                                co6_marks=test_co_scores[5],
                                co7_marks=test_co_scores[6],
                                co8_marks=test_co_scores[7],
                                co9_marks=test_co_scores[8],
                                co10_marks=test_co_scores[9],
                            )
                        )
                    else:
                        test = test1(
                            usn=i["USN"],
                            coursecode=given_coursecode,
                            q1a=new_test[0],
                            q1b=new_test[1],
                            q1c=new_test[2],
                            q2a=new_test[3],
                            q2b=new_test[4],
                            q2c=new_test[5],
                            q3a=new_test[6],
                            q3b=new_test[7],
                            q3c=new_test[8],
                            q4a=new_test[9],
                            q4b=new_test[10],
                            q4c=new_test[11],
                            q5a=new_test[12],
                            q5b=new_test[13],
                            q5c=new_test[14],
                            marks=sum(new_test),
                            co1_marks=test_co_scores[0],
                            co2_marks=test_co_scores[1],
                            co3_marks=test_co_scores[2],
                            co4_marks=test_co_scores[3],
                            co5_marks=test_co_scores[4],
                            co6_marks=test_co_scores[5],
                            co7_marks=test_co_scores[6],
                            co8_marks=test_co_scores[7],
                            co9_marks=test_co_scores[8],
                            co10_marks=test_co_scores[9],
                        )

                        db.session.add(test)
                    db.session.commit()
                flash(f"The data from the csv was added for cie-1", category="success")
                return redirect(url_for("upload_csv"))

            elif the_cie_number == 2:
                t = test2_mapping.query.filter_by(coursecode=given_coursecode).first()

                # lt and ltm are the values from the test2 database created locally
                lt = [
                    t.q1a,
                    t.q1b,
                    t.q1c,
                    t.q2a,
                    t.q2b,
                    t.q2c,
                    t.q3a,
                    t.q3b,
                    t.q3c,
                    t.q4a,
                    t.q4b,
                    t.q4c,
                    t.q5a,
                    t.q5b,
                    t.q5c,
                ]
                ltm = [
                    t.q1am,
                    t.q1bm,
                    t.q1cm,
                    t.q2am,
                    t.q2bm,
                    t.q2cm,
                    t.q3am,
                    t.q3bm,
                    t.q3cm,
                    t.q4am,
                    t.q4bm,
                    t.q4cm,
                    t.q5am,
                    t.q5bm,
                    t.q5cm,
                ]

                # total_co_test = [t.total_co1_marks, t.total_co2_marks, t.total_co3_marks,
                #                 t.total_co4_marks, t.total_co5_marks, t.total_co6_marks,
                #                 t.total_co7_marks, t.total_co8_marks, t.total_co9_marks, t.total_co10_marks]

                for i in r:

                    def ans2(num):
                        return float(num) if num else sqlalchemy.null()

                    def ans1(num):
                        return float(num) if num else 0

                    # query.filter_by(coursecode=given_coursecode, version=i['Version'])
                    m = quiz2_mapping.query.filter_by(
                        coursecode=given_coursecode, version=i["Version"]
                    ).first()
                    mq = [
                        m.q1,
                        m.q2,
                        m.q3,
                        m.q4,
                        m.q5,
                        m.q6,
                        m.q7,
                        m.q8,
                        m.q9,
                        m.q10,
                        m.q11,
                        m.q12,
                        m.q13,
                        m.q14,
                        m.q15,
                    ]
                    mqm = [
                        m.q1m,
                        m.q2m,
                        m.q3m,
                        m.q4m,
                        m.q5m,
                        m.q6m,
                        m.q7m,
                        m.q8m,
                        m.q9m,
                        m.q10m,
                        m.q11m,
                        m.q12m,
                        m.q13m,
                        m.q14m,
                        m.q15m,
                    ]

                    new_quiz = [
                        ans1((i["1"])),
                        ans1((i["2"])),
                        ans1((i["3"])),
                        ans1((i["4"])),
                        ans1((i["5"])),
                        ans1((i["6"])),
                        ans1((i["7"])),
                        ans1((i["8"])),
                        ans1((i["9"])),
                        ans1((i["10"])),
                        ans1((i["11"])),
                        ans1((i["12"])),
                        ans1((i["13"])),
                        ans1((i["14"])),
                        ans1((i["15"])),
                    ]

                    student_co_scores = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

                    for k in range(15):
                        student_co_scores[int(mq[k]) - 1] += new_quiz[k]

                    check = quiz2.query.filter_by(
                        usn=i["USN"], coursecode=given_coursecode
                    ).first()
                    if check:
                        check1 = quiz2.query.filter_by(
                            usn=i["USN"], coursecode=given_coursecode
                        ).update(
                            dict(
                                version=i["Version"],
                                q1=new_quiz[0],
                                q2=new_quiz[1],
                                q3=new_quiz[2],
                                q4=new_quiz[3],
                                q5=new_quiz[4],
                                q6=new_quiz[5],
                                q7=new_quiz[6],
                                q8=new_quiz[7],
                                q9=new_quiz[8],
                                q10=new_quiz[9],
                                q11=new_quiz[10],
                                q12=new_quiz[11],
                                q13=new_quiz[12],
                                q14=new_quiz[13],
                                q15=new_quiz[14],
                                marks_q=sum(new_quiz),
                                co1_marks=student_co_scores[0],
                                co2_marks=student_co_scores[1],
                                co3_marks=student_co_scores[2],
                                co4_marks=student_co_scores[3],
                                co5_marks=student_co_scores[4],
                                co6_marks=student_co_scores[5],
                                co7_marks=student_co_scores[6],
                                co8_marks=student_co_scores[7],
                                co9_marks=student_co_scores[8],
                                co10_marks=student_co_scores[9],
                            )
                        )
                    else:

                        quiz = quiz2(
                            usn=i["USN"],
                            coursecode=given_coursecode,
                            version=i["Version"],
                            q1=new_quiz[0],
                            q2=new_quiz[1],
                            q3=new_quiz[2],
                            q4=new_quiz[3],
                            q5=new_quiz[4],
                            q6=new_quiz[5],
                            q7=new_quiz[6],
                            q8=new_quiz[7],
                            q9=new_quiz[8],
                            q10=new_quiz[9],
                            q11=new_quiz[10],
                            q12=new_quiz[11],
                            q13=new_quiz[12],
                            q14=new_quiz[13],
                            q15=new_quiz[14],
                            marks_q=sum(new_quiz),
                            co1_marks=student_co_scores[0],
                            co2_marks=student_co_scores[1],
                            co3_marks=student_co_scores[2],
                            co4_marks=student_co_scores[3],
                            co5_marks=student_co_scores[4],
                            co6_marks=student_co_scores[5],
                            co7_marks=student_co_scores[6],
                            co8_marks=student_co_scores[7],
                            co9_marks=student_co_scores[8],
                            co10_marks=student_co_scores[9],
                        )
                        db.session.add(quiz)

                    new_test = [
                        ans1(i["1a"]),
                        ans1(i["1b"]),
                        ans1(i["1c"]),
                        ans1(i["2a"]),
                        ans1(i["2b"]),
                        ans1(i["2c"]),
                        ans1(i["3a"]),
                        ans1(i["3b"]),
                        ans1(i["3c"]),
                        ans1(i["4a"]),
                        ans1(i["4b"]),
                        ans1(i["4c"]),
                        ans1(i["5a"]),
                        ans1(i["5b"]),
                        ans1(i["5c"]),
                    ]
                    test_co_scores = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

                    for k in range(15):
                        test_co_scores[int(lt[k]) - 1] += new_test[k]

                    check = test2.query.filter_by(
                        usn=i["USN"], coursecode=given_coursecode
                    ).first()
                    if check:
                        check1 = test2.query.filter_by(
                            usn=i["USN"], coursecode=given_coursecode
                        ).update(
                            dict(
                                q1a=new_test[0],
                                q1b=new_test[1],
                                q1c=new_test[2],
                                q2a=new_test[3],
                                q2b=new_test[4],
                                q2c=new_test[5],
                                q3a=new_test[6],
                                q3b=new_test[7],
                                q3c=new_test[8],
                                q4a=new_test[9],
                                q4b=new_test[10],
                                q4c=new_test[11],
                                q5a=new_test[12],
                                q5b=new_test[13],
                                q5c=new_test[14],
                                marks=sum(new_test),
                                co1_marks=test_co_scores[0],
                                co2_marks=test_co_scores[1],
                                co3_marks=test_co_scores[2],
                                co4_marks=test_co_scores[3],
                                co5_marks=test_co_scores[4],
                                co6_marks=test_co_scores[5],
                                co7_marks=test_co_scores[6],
                                co8_marks=test_co_scores[7],
                                co9_marks=test_co_scores[8],
                                co10_marks=test_co_scores[9],
                            )
                        )
                    else:
                        test = test2(
                            usn=i["USN"],
                            coursecode=given_coursecode,
                            q1a=new_test[0],
                            q1b=new_test[1],
                            q1c=new_test[2],
                            q2a=new_test[3],
                            q2b=new_test[4],
                            q2c=new_test[5],
                            q3a=new_test[6],
                            q3b=new_test[7],
                            q3c=new_test[8],
                            q4a=new_test[9],
                            q4b=new_test[10],
                            q4c=new_test[11],
                            q5a=new_test[12],
                            q5b=new_test[13],
                            q5c=new_test[14],
                            marks=sum(new_test),
                            co1_marks=test_co_scores[0],
                            co2_marks=test_co_scores[1],
                            co3_marks=test_co_scores[2],
                            co4_marks=test_co_scores[3],
                            co5_marks=test_co_scores[4],
                            co6_marks=test_co_scores[5],
                            co7_marks=test_co_scores[6],
                            co8_marks=test_co_scores[7],
                            co9_marks=test_co_scores[8],
                            co10_marks=test_co_scores[9],
                        )

                        db.session.add(test)
                    db.session.commit()
                flash(f"SThe data from the csv was added was cie-2", category="success")
                return redirect(url_for("upload_csv"))

            elif the_cie_number == 3:
                t = test3_mapping.query.filter_by(coursecode=given_coursecode).first()

                # lt and ltm are the values from the test1 database created locally
                lt = [
                    t.q1a,
                    t.q1b,
                    t.q1c,
                    t.q2a,
                    t.q2b,
                    t.q2c,
                    t.q3a,
                    t.q3b,
                    t.q3c,
                    t.q4a,
                    t.q4b,
                    t.q4c,
                    t.q5a,
                    t.q5b,
                    t.q5c,
                ]
                ltm = [
                    t.q1am,
                    t.q1bm,
                    t.q1cm,
                    t.q2am,
                    t.q2bm,
                    t.q2cm,
                    t.q3am,
                    t.q3bm,
                    t.q3cm,
                    t.q4am,
                    t.q4bm,
                    t.q4cm,
                    t.q5am,
                    t.q5bm,
                    t.q5cm,
                ]

                # total_co_test = [t.total_co1_marks, t.total_co2_marks, t.total_co3_marks,
                #                 t.total_co4_marks, t.total_co5_marks, t.total_co6_marks,
                #                 t.total_co7_marks, t.total_co8_marks, t.total_co9_marks, t.total_co10_marks]

                for i in r:

                    def ans2(num):
                        return float(num) if num else sqlalchemy.null()

                    def ans1(num):
                        return float(num) if num else 0

                    # query.filter_by(coursecode=given_coursecode, version=i['Version'])
                    m = quiz3_mapping.query.filter_by(
                        coursecode=given_coursecode, version=i["Version"]
                    ).first()
                    mq = [
                        m.q1,
                        m.q2,
                        m.q3,
                        m.q4,
                        m.q5,
                        m.q6,
                        m.q7,
                        m.q8,
                        m.q9,
                        m.q10,
                        m.q11,
                        m.q12,
                        m.q13,
                        m.q14,
                        m.q15,
                    ]
                    mqm = [
                        m.q1m,
                        m.q2m,
                        m.q3m,
                        m.q4m,
                        m.q5m,
                        m.q6m,
                        m.q7m,
                        m.q8m,
                        m.q9m,
                        m.q10m,
                        m.q11m,
                        m.q12m,
                        m.q13m,
                        m.q14m,
                        m.q15m,
                    ]

                    new_quiz = [
                        ans1((i["1"])),
                        ans1((i["2"])),
                        ans1((i["3"])),
                        ans1((i["4"])),
                        ans1((i["5"])),
                        ans1((i["6"])),
                        ans1((i["7"])),
                        ans1((i["8"])),
                        ans1((i["9"])),
                        ans1((i["10"])),
                        ans1((i["11"])),
                        ans1((i["12"])),
                        ans1((i["13"])),
                        ans1((i["14"])),
                        ans1((i["15"])),
                    ]

                    student_co_scores = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

                    for k in range(15):
                        student_co_scores[int(mq[k]) - 1] += new_quiz[k]

                    check = quiz3.query.filter_by(
                        usn=i["USN"], coursecode=given_coursecode
                    ).first()
                    if check:
                        check1 = quiz3.query.filter_by(
                            usn=i["USN"], coursecode=given_coursecode
                        ).update(
                            dict(
                                version=i["Version"],
                                q1=new_quiz[0],
                                q2=new_quiz[1],
                                q3=new_quiz[2],
                                q4=new_quiz[3],
                                q5=new_quiz[4],
                                q6=new_quiz[5],
                                q7=new_quiz[6],
                                q8=new_quiz[7],
                                q9=new_quiz[8],
                                q10=new_quiz[9],
                                q11=new_quiz[10],
                                q12=new_quiz[11],
                                q13=new_quiz[12],
                                q14=new_quiz[13],
                                q15=new_quiz[14],
                                marks_q=sum(new_quiz),
                                co1_marks=student_co_scores[0],
                                co2_marks=student_co_scores[1],
                                co3_marks=student_co_scores[2],
                                co4_marks=student_co_scores[3],
                                co5_marks=student_co_scores[4],
                                co6_marks=student_co_scores[5],
                                co7_marks=student_co_scores[6],
                                co8_marks=student_co_scores[7],
                                co9_marks=student_co_scores[8],
                                co10_marks=student_co_scores[9],
                            )
                        )

                    else:
                        quiz = quiz3(
                            usn=i["USN"],
                            coursecode=given_coursecode,
                            version=i["Version"],
                            q1=new_quiz[0],
                            q2=new_quiz[1],
                            q3=new_quiz[2],
                            q4=new_quiz[3],
                            q5=new_quiz[4],
                            q6=new_quiz[5],
                            q7=new_quiz[6],
                            q8=new_quiz[7],
                            q9=new_quiz[8],
                            q10=new_quiz[9],
                            q11=new_quiz[10],
                            q12=new_quiz[11],
                            q13=new_quiz[12],
                            q14=new_quiz[13],
                            q15=new_quiz[14],
                            marks_q=sum(new_quiz),
                            co1_marks=student_co_scores[0],
                            co2_marks=student_co_scores[1],
                            co3_marks=student_co_scores[2],
                            co4_marks=student_co_scores[3],
                            co5_marks=student_co_scores[4],
                            co6_marks=student_co_scores[5],
                            co7_marks=student_co_scores[6],
                            co8_marks=student_co_scores[7],
                            co9_marks=student_co_scores[8],
                            co10_marks=student_co_scores[9],
                        )
                        db.session.add(quiz)

                    new_test = [
                        ans1(i["1a"]),
                        ans1(i["1b"]),
                        ans1(i["1c"]),
                        ans1(i["2a"]),
                        ans1(i["2b"]),
                        ans1(i["2c"]),
                        ans1(i["3a"]),
                        ans1(i["3b"]),
                        ans1(i["3c"]),
                        ans1(i["4a"]),
                        ans1(i["4b"]),
                        ans1(i["4c"]),
                        ans1(i["5a"]),
                        ans1(i["5b"]),
                        ans1(i["5c"]),
                    ]
                    test_co_scores = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

                    for k in range(15):
                        test_co_scores[int(lt[k]) - 1] += new_test[k]

                    check = test3.query.filter_by(
                        usn=i["USN"], coursecode=given_coursecode
                    ).first()
                    if check:
                        check1 = test3.query.filter_by(
                            usn=i["USN"], coursecode=given_coursecode
                        ).update(
                            dict(
                                q1a=new_test[0],
                                q1b=new_test[1],
                                q1c=new_test[2],
                                q2a=new_test[3],
                                q2b=new_test[4],
                                q2c=new_test[5],
                                q3a=new_test[6],
                                q3b=new_test[7],
                                q3c=new_test[8],
                                q4a=new_test[9],
                                q4b=new_test[10],
                                q4c=new_test[11],
                                q5a=new_test[12],
                                q5b=new_test[13],
                                q5c=new_test[14],
                                marks=sum(new_test),
                                co1_marks=test_co_scores[0],
                                co2_marks=test_co_scores[1],
                                co3_marks=test_co_scores[2],
                                co4_marks=test_co_scores[3],
                                co5_marks=test_co_scores[4],
                                co6_marks=test_co_scores[5],
                                co7_marks=test_co_scores[6],
                                co8_marks=test_co_scores[7],
                                co9_marks=test_co_scores[8],
                                co10_marks=test_co_scores[9],
                            )
                        )
                    else:
                        test = test3(
                            usn=i["USN"],
                            coursecode=given_coursecode,
                            q1a=new_test[0],
                            q1b=new_test[1],
                            q1c=new_test[2],
                            q2a=new_test[3],
                            q2b=new_test[4],
                            q2c=new_test[5],
                            q3a=new_test[6],
                            q3b=new_test[7],
                            q3c=new_test[8],
                            q4a=new_test[9],
                            q4b=new_test[10],
                            q4c=new_test[11],
                            q5a=new_test[12],
                            q5b=new_test[13],
                            q5c=new_test[14],
                            marks=sum(new_test),
                            co1_marks=test_co_scores[0],
                            co2_marks=test_co_scores[1],
                            co3_marks=test_co_scores[2],
                            co4_marks=test_co_scores[3],
                            co5_marks=test_co_scores[4],
                            co6_marks=test_co_scores[5],
                            co7_marks=test_co_scores[6],
                            co8_marks=test_co_scores[7],
                            co9_marks=test_co_scores[8],
                            co10_marks=test_co_scores[9],
                        )

                        db.session.add(test)
                    db.session.commit()
                flash(f"The data from the csv was added for cie-3", category="success")
                return redirect(url_for("upload_csv"))

        return "Success"
    if form.errors != {}:
        for err_msg in form.errors.values():
            flash(f"There was an error : {err_msg}", category="danger")

    return render_template("upload.html", form=form)


########################################################################################
########################################################################################
# Sample CSV


@app.route("/createsamplecsvforentry", methods=["GET", "POST"])
def create_samplecsv():
    current_staff = session["staffid"]
    # current_staff = "1234"
    if current_staff == "":
        flash("Please enter an appropriate Staff ID!", category="danger")
        return render_template("newmain.html")

    current_course = session["coursecode"]
    # current_course = "21ME24"
    if current_course == "":
        flash("Please enter an appropriate Course Code!", category="danger")
        return render_template("newmain.html")

    cie1_filename = (
        str(current_staff) + "-" + str(current_course) + str("-cie1") + ".csv"
    )
    cie2_filename = (
        str(current_staff) + "-" + str(current_course) + str("-cie2") + ".csv"
    )
    cie3_filename = (
        str(current_staff) + "-" + str(current_course) + str("-cie3") + ".csv"
    )
    el_filename = str(current_staff) + "-" + str(current_course) + str("-EL") + ".csv"
    lab_filename = str(current_staff) + "-" + str(current_course) + str("-lab") + ".csv"

    samples_path_cie1 = app.config["SAMPLES_FOLDER"] + cie1_filename
    samples_path_cie2 = app.config["SAMPLES_FOLDER"] + cie2_filename
    samples_path_cie3 = app.config["SAMPLES_FOLDER"] + cie3_filename
    samples_path_el = app.config["SAMPLES_FOLDER"] + el_filename
    samples_path_lab = app.config["SAMPLES_FOLDER"] + lab_filename

    with open(samples_path_cie1, "w", newline="") as f:
        head = [
            "SlNo",
            "Name",
            "USN",
            "Version",
            "1",
            "2",
            "3",
            "4",
            "5",
            "6",
            "7",
            "8",
            "9",
            "10",
            "11",
            "12",
            "13",
            "14",
            "15",
            "1a",
            "1b",
            "1c",
            "2a",
            "2b",
            "2c",
            "3a",
            "3b",
            "3c",
            "4a",
            "4b",
            "4c",
            "5a",
            "5b",
            "5c",
        ]
        w = csv.DictWriter(f, fieldnames=head)
        w.writeheader()
        count = 1
        access = staffid_cc.query.filter_by(
            staffid=current_staff, coursecode=current_course
        ).first()
        students = list(map(str, access.usn_list.split(",")))

        for i in students:
            if i != "":
                the_student = student.query.filter_by(usn=str(i)).first()
                w.writerow({"SlNo": count, "Name": the_student.name, "USN": str(i)})
                count += 1

    with open(samples_path_cie2, "w", newline="") as f:
        head = [
            "SlNo",
            "Name",
            "USN",
            "Version",
            "1",
            "2",
            "3",
            "4",
            "5",
            "6",
            "7",
            "8",
            "9",
            "10",
            "11",
            "12",
            "13",
            "14",
            "15",
            "1a",
            "1b",
            "1c",
            "2a",
            "2b",
            "2c",
            "3a",
            "3b",
            "3c",
            "4a",
            "4b",
            "4c",
            "5a",
            "5b",
            "5c",
        ]
        w = csv.DictWriter(f, fieldnames=head)
        w.writeheader()
        count = 1
        access = staffid_cc.query.filter_by(
            staffid=current_staff, coursecode=current_course
        ).first()
        students = list(map(str, access.usn_list.split(",")))

        for i in students:
            if i != "":
                the_student = student.query.filter_by(usn=str(i)).first()
                w.writerow({"SlNo": count, "Name": the_student.name, "USN": str(i)})
                count += 1

    with open(samples_path_cie3, "w", newline="") as f:
        head = [
            "SlNo",
            "Name",
            "USN",
            "Version",
            "1",
            "2",
            "3",
            "4",
            "5",
            "6",
            "7",
            "8",
            "9",
            "10",
            "11",
            "12",
            "13",
            "14",
            "15",
            "1a",
            "1b",
            "1c",
            "2a",
            "2b",
            "2c",
            "3a",
            "3b",
            "3c",
            "4a",
            "4b",
            "4c",
            "5a",
            "5b",
            "5c",
        ]
        w = csv.DictWriter(f, fieldnames=head)
        w.writeheader()
        count = 1
        access = staffid_cc.query.filter_by(
            staffid=current_staff, coursecode=current_course
        ).first()
        students = list(map(str, access.usn_list.split(",")))

        for i in students:
            if i != "":
                the_student = student.query.filter_by(usn=str(i)).first()
                w.writerow({"SlNo": count, "Name": the_student.name, "USN": str(i)})
                count += 1

    with open(samples_path_el, "w", newline="") as f:
        head = [
            "SlNo",
            "Name",
            "USN",
            "p1r1",
            "p1r2",
            "p1r3",
            "p1r4",
            "p1r5",
            "p1r6",
            "p2r1",
            "p2r2",
            "p2r3",
            "p2r4",
            "p2r5",
            "p2r6",
            "p3r1",
            "p3r2",
            "p3r3",
            "p3r4",
            "p3r5",
            "p3r6",
            "p4r1",
            "p4r2",
            "p4r3",
            "p4r4",
            "p4r5",
            "p4r6",
            "p5r1",
            "p5r2",
            "p5r3",
            "p5r4",
            "p5r5",
            "p5r6",
        ]

        w = csv.DictWriter(f, fieldnames=head)
        w.writeheader()
        count = 1
        access = staffid_cc.query.filter_by(
            staffid=current_staff, coursecode=current_course
        ).first()
        students = list(map(str, access.usn_list.split(",")))

        for i in students:
            if i != "":
                the_student = student.query.filter_by(usn=str(i)).first()
                w.writerow({"SlNo": count, "Name": the_student.name, "USN": str(i)})
                count += 1

    the_course = course.query.filter_by(coursecode=current_course).first()
    lab_status = the_course.labyorn
    if lab_status == "Y":

        with open(samples_path_lab, "w", newline="") as f:
            head = [
                "SlNo",
                "Name",
                "USN",
                "co1p",
                "co2p",
                "co3p",
                "co4p",
                "co5p",
                "co6p",
                "co7p",
                "co8p",
                "co9p",
                "co10p",
            ]
            w = csv.DictWriter(f, fieldnames=head)
            w.writeheader()
            count = 1
            access = staffid_cc.query.filter_by(
                staffid=current_staff, coursecode=current_course
            ).first()
            students = list(map(str, access.usn_list.split(",")))

            for i in students:
                if i != "":
                    the_student = student.query.filter_by(usn=str(i)).first()
                    w.writerow({"SlNo": count, "Name": the_student.name, "USN": str(i)})
                    count += 1

    flash(
        "The student details were added to the student excels, you can download them now.",
        category="success",
    )
    return render_template("newmain.html")


@app.route("/cie1sampledownload", methods=["GET", "POST"])
def download_cie1sample():
    current_staff = session["staffid"]
    # current_staff = "1234"
    if current_staff == "":
        flash("Please enter an appropriate Staff ID!", category="danger")
        return render_template("newmain.html")

    current_course = session["coursecode"]
    # current_course = "21ME24"
    if current_course == "":
        flash("Please enter an appropriate Course Code!", category="danger")
        return render_template("newmain.html")

    url_path = (
        app.config["SAMPLES_FOLDER"]
        + str(current_staff)
        + "-"
        + str(current_course)
        + str("-cie1")
        + ".csv"
    )

    return send_file(url_path, as_attachment=True)


@app.route("/cie2sampledownload", methods=["GET", "POST"])
def download_cie2sample():
    current_staff = session["staffid"]
    # current_staff = "1234"
    if current_staff == "":
        flash("Please enter an appropriate Staff ID!", category="danger")
        return render_template("newmain.html")

    current_course = session["coursecode"]
    # current_course = "21ME24"
    if current_course == "":
        flash("Please enter an appropriate Course Code!", category="danger")
        return render_template("newmain.html")

    url_path = (
        app.config["SAMPLES_FOLDER"]
        + str(current_staff)
        + "-"
        + str(current_course)
        + str("-cie2")
        + ".csv"
    )

    return send_file(url_path, as_attachment=True)


@app.route("/cie3sampledownload", methods=["GET", "POST"])
def download_cie3sample():
    current_staff = session["staffid"]
    # current_staff = "1234"
    if current_staff == "":
        flash("Please enter an appropriate Staff ID!", category="danger")
        return render_template("newmain.html")

    current_course = session["coursecode"]
    # current_course = "21ME24"
    if current_course == "":
        flash("Please enter an appropriate Course Code!", category="danger")
        return render_template("newmain.html")

    url_path = (
        app.config["SAMPLES_FOLDER"]
        + str(current_staff)
        + "-"
        + str(current_course)
        + str("-cie3")
        + ".csv"
    )

    return send_file(url_path, as_attachment=True)


@app.route("/elsampledownload", methods=["GET", "POST"])
def download_elsample():
    current_staff = session["staffid"]
    # current_staff = "1234"
    if current_staff == "":
        flash("Please enter an appropriate Staff ID!", category="danger")
        return render_template("newmain.html")

    current_course = session["coursecode"]
    # current_course = "21ME24"
    if current_course == "":
        flash("Please enter an appropriate Course Code!", category="danger")
        return render_template("newmain.html")

    url_path = (
        app.config["SAMPLES_FOLDER"]
        + str(current_staff)
        + "-"
        + str(current_course)
        + str("-EL")
        + ".csv"
    )

    return send_file(url_path, as_attachment=True)


@app.route("/labsampledownload", methods=["GET", "POST"])
def download_labsample():
    current_staff = session["staffid"]
    # current_staff = "1234"
    if current_staff == "":
        flash("Please enter an appropriate Staff ID!", category="danger")
        return render_template("newmain.html")

    current_course = session["coursecode"]
    # current_course = "21ME24"
    if current_course == "":
        flash("Please enter an appropriate Course Code!", category="danger")
        return render_template("newmain.html")

    the_course = course.query.filter_by(coursecode=current_course).first()
    lab_status = the_course.labyorn

    # change to y
    if lab_status == "Y":
        url_path = (
            app.config["SAMPLES_FOLDER"]
            + str(current_staff)
            + "-"
            + str(current_course)
            + str("-lab")
            + ".csv"
        )
        return send_file(url_path, as_attachment=True)

    else:
        flash("This course does not have a lab component !", category="success")
        return redirect(url_for("labco_calc"))

@app.route("/createsamplepocsvfile", methods=['GET', 'POST'])
def download_posample():    
    
    po_sample_filename = "sample-pomapping.csv"
    samples_path_po = app.config["SAMPLES_FOLDER"] + po_sample_filename
    
    with open(samples_path_po, "w", newline="") as f:
        head = ["Sl.No", "CourseCode", "PO1", "PO2", "PO3", "PO4", "PO5", "PO6", "PO7", 
                                        "PO8", "PO9", "PO10", "PO11", "PO12"]
        w = csv.DictWriter(f, fieldnames=head)
        w.writeheader()
    
    flash("The sample PO file has been created and will now be downloaded")   

    return send_file(samples_path_po, as_attachment=True)

@app.route("/downloadstaffidccmapping", methods=['GET', 'POST'])
def download_staffid_cc_mapping():
    sample_filename = "staffidcc-mapping.csv"
    samples_path_mapping = app.config["SAMPLES_FOLDER"] + sample_filename
    
    with open(samples_path_mapping, "w", newline="") as f:
        head = ["STAFFID", "COURSECODE", "SEMESTER"]
        w = csv.DictWriter(f, fieldnames=head)
        w.writeheader()
    
    return send_file(samples_path_mapping, as_attachment=True)
    

@app.route("/createsamplegradefile", methods=['GET', 'POST'])
def download_gradesample():    
    
    grade_sample_filename = "sample-grademapping.csv"
    samples_path_grade = app.config["SAMPLES_FOLDER"] + grade_sample_filename
    
    with open(samples_path_grade, "w", newline="") as f:
        head = ["MAXMARKS", "MINMARKS", "GRADE", "GPOINT"]
        w = csv.DictWriter(f, fieldnames=head)
        w.writeheader()
    
    flash("The sample grades file has been created and will now be downloaded")   

    return send_file(samples_path_grade, as_attachment=True)
########################################################################################
########################################################################################
# Display database



@app.route("/displayquizscores", methods=["GET", "POST"])
def disp_allmarks():

    current_staff = session["staffid"]
    if current_staff == "":
        flash("Please enter an appropriate Staff ID!", category="danger")
        return render_template("newmain.html")

    current_course = session["coursecode"]
    if current_course == "":
        flash("Please enter an appropriate Course Code!", category="danger")
        return render_template("newmain.html")

    access = staffid_cc.query.filter_by(
        staffid=current_staff, coursecode=current_course
    ).first()
    the_list = list(map(str, access.usn_list.split(",")))

    d = {}
    for i in the_list:
        the_usn = str(i).strip()
        if the_usn != "":
            d[the_usn] = []
            qui1 = quiz1.query.filter_by(
                coursecode=session["coursecode"], usn=the_usn
            ).first()
            if qui1:
                d[the_usn].append(qui1.marks_q)
            else:
                d[the_usn].append("Absent")

            qui2 = quiz2.query.filter_by(
                coursecode=session["coursecode"], usn=the_usn
            ).first()
            if qui2:
                d[the_usn].append(qui2.marks_q)
            else:
                d[the_usn].append("Absent")

            qui3 = quiz3.query.filter_by(
                coursecode=session["coursecode"], usn=the_usn
            ).first()
            if qui3:
                d[the_usn].append(qui3.marks_q)
            else:
                d[the_usn].append("Absent")

            tes1 = test1.query.filter_by(
                coursecode=session["coursecode"], usn=the_usn
            ).first()
            if tes1:
                d[the_usn].append(tes1.marks)
            else:
                d[the_usn].append("Absent")

            tes2 = test2.query.filter_by(
                coursecode=session["coursecode"], usn=the_usn
            ).first()
            if tes2:
                d[the_usn].append(tes2.marks)
            else:
                d[the_usn].append("Absent")

            tes3 = test3.query.filter_by(
                coursecode=session["coursecode"], usn=the_usn
            ).first()
            if tes3:
                d[the_usn].append(tes3.marks)
            else:
                d[the_usn].append("Absent")

            assign = assignment.query.filter_by(
                coursecode=session["coursecode"], usn=the_usn
            ).first()
            if assign:
                d[the_usn].append(assign.total_assignment_marks)
            else:
                d[the_usn].append(0)

            finalint = internal_co.query.filter_by(
                coursecode=session["coursecode"], usn=the_usn
            ).first()
            if finalint:
                d[the_usn].append(finalint.final_cie)
            else:
                d[the_usn].append("Tbc")

    l = list(d.keys())
    print(d)
    return render_template("quizmarksdisplay.html", d=d, l=l)


@app.route("/viewthestudentcoandsubjectco", methods=["GET", "POST"])
def view_dico():
    d = {}

    current_staff = session["staffid"]
    if current_staff == "":
        flash("Please enter an appropriate Staff ID!", category="danger")
        return render_template("newmain.html")

    current_course = session["coursecode"]
    if current_course == "":
        flash("Please enter an appropriate Course Code!", category="danger")
        return render_template("newmain.html")

    access = staffid_cc.query.filter_by(
        staffid=current_staff, coursecode=current_course
    ).first()
    the_list = list(map(str, access.usn_list.split(",")))

    for i in the_list:
        the_usn = str(i).strip()
        if the_usn != "":
            d[the_usn] = []

            new = student_co.query.filter_by(
                usn=the_usn, coursecode=current_course
            ).first()
            if new == "":
                flash(
                    f"The student with USN {the_usn} is not found in the table.",
                    category="danger",
                )
                continue

            d[the_usn] = [
                new.sco1p,
                new.sco2p,
                new.sco3p,
                new.sco4p,
                new.sco5p,
                new.sco6p,
                new.sco7p,
                new.sco8p,
                new.sco9p,
                new.sco10p
                # [new.dico1p, new.dico2p, new.dico3p, new.dico4p, new.dico5p,
                # new.dico6p, new.dico7p, new.dico8p, new.dico9p, new.dico10p]
            ]

    l = list(d.keys())
    return render_template("dico_display.html", l=l, d=d)

@app.route('/displayciequizassignmentattainment', methods=['GET', 'POST'])
def viewciecrsoutcome():
    
    current_course = session["coursecode"]
    if current_course == "":
        flash("Please enter an appropriate Course Code!", category="danger")
        return render_template("newmain.html")
    
    access = student_co.query.filter_by(coursecode=current_course).all()
    
    if access == []:
        flash("No records found for this coursecode!", category="danger")
        return render_template("newmain.html")
    
    else:
        d = {}
        for i in access:
            d[i.usn] = [i.co1p, i.co2p, i.co3p, i.co4p, i.co5p, i.co6p, i.co7p, i.co8p, i.co9p, i.co10p]        
    
    return render_template("disp_crsoutcome.html", d=d)

# This displays the direct attainment
@app.route('/displayinternalcourseoutcome', methods=["GET", "POST"])
def viewinternalcrsoutcome():
    current_course = session["coursecode"]
    if current_course == "":
        flash("Please enter an appropriate Course Code!", category="danger")
        return render_template("newmain.html")
    
    access = student_co.query.filter_by(coursecode=current_course).all()
    
    if access == []:
        flash("No records found for this coursecode!", category="danger")
        return render_template("newmain.html")
    
    else:
        d = {}
        for i in access:
            d[i.usn] = [i.sco1p, i.sco2p, i.sco3p, i.sco4p, i.sco5p, i.sco6p, i.sco7p, i.sco8p, i.sco9p, i.sco10p]        
    
    return render_template("disp_directcrsoutcome.html", d=d)
 

@app.route('/viewdirectindirectattainment', methods=["GET", "POST"])
def viewdirectindirect():
    current_course = session["coursecode"]
    if current_course == "":
        flash("Please enter an appropriate Course Code!", category="danger")
        return render_template("newmain.html")
    
    access = student_co.query.filter_by(coursecode=current_course).all()
    
    if access == []:
        flash("No records found for this coursecode!", category="danger")
        return render_template("newmain.html")
    
    else:
        d = {}
        for i in access:
            d[i.usn] = [i.dico1p, i.dico2p, i.dico3p, i.dico4p, i.dico5p, i.dico6p, i.dico7p, i.dico8p, i.dico9p, i.dico10p]        
    
    return render_template("disp_directindirectattainment.html", d=d)
    
@app.route('/displayfinalpoattainment', methods=["GET", "POST"])
def viewpoattainment():
    access = po_attainment.query.all()
    if access == []:
        flash("No PO attainment has been calculated yet!", category="danger")
        return render_template("newmain.html")
    
    else:
        d = {}
        for i in access:
            d[i.batch] = [i.po1, i.po2, i.po3, i.po4, i.po5, i.po6, i.po7, i.po8, i.po9, i.po10, i.po11, i.po12, i.pso1, i.pso2]
    
    return render_template("disp_poattainment.html", d=d)

@app.route('/displaylevel', methods=['GET', 'POST'])
def viewlevel():
    current_course = session["coursecode"]
    if current_course == "":
        flash("Please enter an appropriate Course Code!", category="danger")
        return render_template("newmain.html")
    
    access = level.query.filter_by(coursecode=current_course).first()
    
    if access:
        flash(f"The level of the course {current_course} is : {access.final_level}", category="success")
        return render_template("newmain.html")
    
    else:
        flash(f"The level has not been calculated yet for : {current_course}", category="danger")
        return render_template("newmain.html")

        
        
#################################################################################
#################################################################################
# Course end Survey and extra


@app.route("/thecoursesendsurvey", methods=["GET", "POST"])
def crsendsurvey():

    l = []
    form = large_crsend()
    course_code = session["coursecode"]

    if course_code == "":
        flash("Please enter an appropriate Course Code!", category="danger")
        return render_template("newmain.html")

    if form.validate_on_submit():
        for i in form.alltogether:
            n = i.exc.data + i.vg.data + i.g.data + i.sat.data + i.poor.data
            break

        lco = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        lcount = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

        for i in form.alltogether:
            qe = i.exc.data
            qvg = i.vg.data
            qg = i.g.data
            qs = i.sat.data
            qp = i.poor.data

            if qe == None or qvg == None or qg == None or qs == None or qp == None:
                break

            q = ((10 * qe) + (8 * qvg) + (6 * qg) + (4 * qs) + (2 * qp)) / n

            lco[int(i.co.data) - 1] += q
            lcount[int(i.co.data) - 1] += 1

        for i in range(10):
            lco[i] = (lco[i] * 10) / lcount[i] if lcount[i] > 0 else 0

        check = courseend_survey.query.filter_by(coursecode=course_code).first()
        if check:
            check1 = courseend_survey.query.filter_by(coursecode=course_code).update(
                dict(
                    co1p=lco[0],
                    co2p=lco[1],
                    co3p=lco[2],
                    co4p=lco[3],
                    co5p=lco[4],
                    co6p=lco[5],
                    co7p=lco[6],
                    co8p=lco[7],
                    co9p=lco[8],
                    co10p=lco[9],
                )
            )

        else:
            new_crsend = courseend_survey(
                coursecode=course_code,
                co1p=lco[0],
                co2p=lco[1],
                co3p=lco[2],
                co4p=lco[3],
                co5p=lco[4],
                co6p=lco[5],
                co7p=lco[6],
                co8p=lco[7],
                co9p=lco[8],
                co10p=lco[9],
            )
            db.session.add(new_crsend)

        db.session.commit()

        flash("The course end survey has been updated !", category="success")
        return redirect(url_for("crsendsurvey"))

    if form.errors != {}:
        for err_msg in form.errors.values():
            flash(f"There was an error : {err_msg}", category="danger")

    return render_template("courseendsurvey.html", form=form)


# have to add the talk, but clarification needed
# @app.route('/extratalkgradingwithco', methods=['GET', 'POST'])
# def talk_grading():
#     l = []
#     form = large_talk()
#     course_code = session['coursecode']

#     if course_code == '':
#         flash('Please enter an appropriate Course Code!', category='danger')
#         return render_template('main.html')

#     if form.validate_on_submit():
#         for i in form.all_q:
#             print()

#################################################################################
#################################################################################
# Major Calculations


@app.route("/calculinternal", methods=["GET", "POST"])
def internal_calc():

    staffid = session["staffid"]
    # staffid = '1234'
    # staffid = '5678'
    if staffid == "":
        flash("Please enter an appropriate Staff ID!", category="danger")
        return render_template("newmain.html")

    course_code = session["coursecode"]
    # course_code = '21EC25'
    # course_code='21ME24'
    if course_code == "":
        flash("Please enter an appropriate Course Code!", category="danger")
        return render_template("newmain.html")

    access = staffid_cc.query.filter_by(staffid=staffid, coursecode=course_code).first()
    students = list(map(str, access.usn_list.split(",")))

    assignm = am.query.filter_by(coursecode=course_code).first()
    q1m = quiz1_mapping.query.filter_by(coursecode=course_code).first()
    q2m = quiz2_mapping.query.filter_by(coursecode=course_code).first()
    q3m = quiz3_mapping.query.filter_by(coursecode=course_code).first()
    t1m = test1_mapping.query.filter_by(coursecode=course_code).first()
    t2m = test2_mapping.query.filter_by(coursecode=course_code).first()
    t3m = test3_mapping.query.filter_by(coursecode=course_code).first()
    
    course_access = course.query.filter_by(coursecode=course_code).first()
    ciep = course_access.internal_cie
    assp = course_access.internal_assign
    qp = course_access.internal_quiz

    print(students)
    for i in students:

        if i != "":
            assign = assignment.query.filter_by(coursecode=course_code, usn=i).first()

            q1 = quiz1.query.filter_by(coursecode=course_code, usn=i).first()

            q2 = quiz2.query.filter_by(coursecode=course_code, usn=i).first()

            q3 = quiz3.query.filter_by(coursecode=course_code, usn=i).first()

            t1 = test1.query.filter_by(coursecode=course_code, usn=i).first()

            t2 = test2.query.filter_by(coursecode=course_code, usn=i).first()

            t3 = test3.query.filter_by(coursecode=course_code, usn=i).first()

            # if quiz 3 is minimum
            if min(q1.marks_q, q2.marks_q) >= q3.marks_q:

                l_q = [q1.marks_q, q2.marks_q]

                q_co1marks = q1.co1_marks + q2.co1_marks
                q_co2marks = q1.co2_marks + q2.co2_marks
                q_co3marks = q1.co3_marks + q2.co3_marks
                q_co4marks = q1.co4_marks + q2.co4_marks
                q_co5marks = q1.co5_marks + q2.co5_marks
                q_co6marks = q1.co6_marks + q2.co6_marks
                q_co7marks = q1.co7_marks + q2.co7_marks
                q_co8marks = q1.co8_marks + q2.co8_marks
                q_co9marks = q1.co9_marks + q2.co9_marks
                q_co10marks = q1.co10_marks + q2.co10_marks

                q_co1_total = q1m.total_co1_marks + q2m.total_co1_marks
                q_co2_total = q1m.total_co2_marks + q2m.total_co2_marks
                q_co3_total = q1m.total_co3_marks + q2m.total_co3_marks
                q_co4_total = q1m.total_co4_marks + q2m.total_co4_marks
                q_co5_total = q1m.total_co5_marks + q2m.total_co5_marks
                q_co6_total = q1m.total_co6_marks + q2m.total_co6_marks
                q_co7_total = q1m.total_co7_marks + q2m.total_co7_marks
                q_co8_total = q1m.total_co8_marks + q2m.total_co8_marks
                q_co9_total = q1m.total_co9_marks + q2m.total_co9_marks
                q_co10_total = q1m.total_co10_marks + q2m.total_co10_marks

            elif min(q1.marks_q, q3.marks_q) >= q2.marks_q:

                l_q = [q1.marks_q, q3.marks_q]
                q_co1marks = q1.co1_marks + q3.co1_marks
                q_co2marks = q1.co2_marks + q3.co2_marks
                q_co3marks = q1.co3_marks + q3.co3_marks
                q_co4marks = q1.co4_marks + q3.co4_marks
                q_co5marks = q1.co5_marks + q3.co5_marks
                q_co6marks = q1.co6_marks + q3.co6_marks
                q_co7marks = q1.co7_marks + q3.co7_marks
                q_co8marks = q1.co8_marks + q3.co8_marks
                q_co9marks = q1.co9_marks + q3.co9_marks
                q_co10marks = q1.co10_marks + q3.co10_marks

                q_co1_total = q1m.total_co1_marks + q3m.total_co1_marks
                q_co2_total = q1m.total_co2_marks + q3m.total_co2_marks
                q_co3_total = q1m.total_co3_marks + q3m.total_co3_marks
                q_co4_total = q1m.total_co4_marks + q3m.total_co4_marks
                q_co5_total = q1m.total_co5_marks + q3m.total_co5_marks
                q_co6_total = q1m.total_co6_marks + q3m.total_co6_marks
                q_co7_total = q1m.total_co7_marks + q3m.total_co7_marks
                q_co8_total = q1m.total_co8_marks + q3m.total_co8_marks
                q_co9_total = q1m.total_co9_marks + q3m.total_co9_marks
                q_co10_total = q1m.total_co10_marks + q3m.total_co10_marks

            elif min(q2.marks_q, q3.marks_q) >= q1.marks_q:

                l_q = [q2.marks_q, q3.marks_q]
                q_co1marks = q2.co1_marks + q3.co1_marks
                q_co2marks = q2.co2_marks + q3.co2_marks
                q_co3marks = q2.co3_marks + q3.co3_marks
                q_co4marks = q2.co4_marks + q3.co4_marks
                q_co5marks = q2.co5_marks + q3.co5_marks
                q_co6marks = q2.co6_marks + q3.co6_marks
                q_co7marks = q2.co7_marks + q3.co7_marks
                q_co8marks = q2.co8_marks + q3.co8_marks
                q_co9marks = q2.co9_marks + q3.co9_marks
                q_co10marks = q2.co10_marks + q3.co10_marks

                q_co1_total = q2m.total_co1_marks + q3m.total_co1_marks
                q_co2_total = q2m.total_co2_marks + q3m.total_co2_marks
                q_co3_total = q2m.total_co3_marks + q3m.total_co3_marks
                q_co4_total = q2m.total_co4_marks + q3m.total_co4_marks
                q_co5_total = q2m.total_co5_marks + q3m.total_co5_marks
                q_co6_total = q2m.total_co6_marks + q3m.total_co6_marks
                q_co7_total = q2m.total_co7_marks + q3m.total_co7_marks
                q_co8_total = q2m.total_co8_marks + q3m.total_co8_marks
                q_co9_total = q2m.total_co9_marks + q3m.total_co9_marks
                q_co10_total = q2m.total_co10_marks + q3m.total_co10_marks

            # now test
            if min(t1.marks, t2.marks) >= t3.marks:

                t_q = [t1.marks, t2.marks]
                t_co1marks = t1.co1_marks + t2.co1_marks
                t_co2marks = t1.co2_marks + t2.co2_marks
                t_co3marks = t1.co3_marks + t2.co3_marks
                t_co4marks = t1.co4_marks + t2.co4_marks
                t_co5marks = t1.co5_marks + t2.co5_marks
                t_co6marks = t1.co6_marks + t2.co6_marks
                t_co7marks = t1.co7_marks + t2.co7_marks
                t_co8marks = t1.co8_marks + t2.co8_marks
                t_co9marks = t1.co9_marks + t2.co9_marks
                t_co10marks = t1.co10_marks + t2.co10_marks

                t_co1_total = t1m.total_co1_marks + t2m.total_co1_marks
                t_co2_total = t1m.total_co2_marks + t2m.total_co2_marks
                t_co3_total = t1m.total_co3_marks + t2m.total_co3_marks
                t_co4_total = t1m.total_co4_marks + t2m.total_co4_marks
                t_co5_total = t1m.total_co5_marks + t2m.total_co5_marks
                t_co6_total = t1m.total_co6_marks + t2m.total_co6_marks
                t_co7_total = t1m.total_co7_marks + t2m.total_co7_marks
                t_co8_total = t1m.total_co8_marks + t2m.total_co8_marks
                t_co9_total = t1m.total_co9_marks + t2m.total_co9_marks
                t_co10_total = t1m.total_co10_marks + t2m.total_co10_marks

            elif min(t1.marks, t3.marks) >= t2.marks:

                t_q = [t1.marks, t3.marks]
                t_co1marks = t1.co1_marks + t3.co1_marks
                t_co2marks = t1.co2_marks + t3.co2_marks
                t_co3marks = t1.co3_marks + t3.co3_marks
                t_co4marks = t1.co4_marks + t3.co4_marks
                t_co5marks = t1.co5_marks + t3.co5_marks
                t_co6marks = t1.co6_marks + t3.co6_marks
                t_co7marks = t1.co7_marks + t3.co7_marks
                t_co8marks = t1.co8_marks + t3.co8_marks
                t_co9marks = t1.co9_marks + t3.co9_marks
                t_co10marks = t1.co10_marks + t3.co10_marks

                t_co1_total = t1m.total_co1_marks + t3m.total_co1_marks
                t_co2_total = t1m.total_co2_marks + t3m.total_co2_marks
                t_co3_total = t1m.total_co3_marks + t3m.total_co3_marks
                t_co4_total = t1m.total_co4_marks + t3m.total_co4_marks
                t_co5_total = t1m.total_co5_marks + t3m.total_co5_marks
                t_co6_total = t1m.total_co6_marks + t3m.total_co6_marks
                t_co7_total = t1m.total_co7_marks + t3m.total_co7_marks
                t_co8_total = t1m.total_co8_marks + t3m.total_co8_marks
                t_co9_total = t1m.total_co9_marks + t3m.total_co9_marks
                t_co10_total = t1m.total_co10_marks + t3m.total_co10_marks

            elif min(t2.marks, t3.marks) >= t1.marks:
                t_q = [t2.marks, t3.marks]
                t_co1marks = t2.co1_marks + t3.co1_marks
                t_co2marks = t2.co2_marks + t3.co2_marks
                t_co3marks = t2.co3_marks + t3.co3_marks
                t_co4marks = t2.co4_marks + t3.co4_marks
                t_co5marks = t2.co5_marks + t3.co5_marks
                t_co6marks = t2.co6_marks + t3.co6_marks
                t_co7marks = t2.co7_marks + t3.co7_marks
                t_co8marks = t2.co8_marks + t3.co8_marks
                t_co9marks = t2.co9_marks + t3.co9_marks
                t_co10marks = t2.co10_marks + t3.co10_marks

                t_co1_total = t2m.total_co1_marks + t3m.total_co1_marks
                t_co2_total = t2m.total_co2_marks + t3m.total_co2_marks
                t_co3_total = t2m.total_co3_marks + t3m.total_co3_marks
                t_co4_total = t2m.total_co4_marks + t3m.total_co4_marks
                t_co5_total = t2m.total_co5_marks + t3m.total_co5_marks
                t_co6_total = t2m.total_co6_marks + t3m.total_co6_marks
                t_co7_total = t2m.total_co7_marks + t3m.total_co7_marks
                t_co8_total = t2m.total_co8_marks + t3m.total_co8_marks
                t_co9_total = t2m.total_co9_marks + t3m.total_co9_marks
                t_co10_total = t2m.total_co10_marks + t3m.total_co10_marks

            co1marks = q_co1marks + t_co1marks
            co2marks = q_co2marks + t_co2marks
            co3marks = q_co3marks + t_co3marks
            co4marks = q_co4marks + t_co4marks
            co5marks = q_co5marks + t_co5marks
            co6marks = q_co6marks + t_co6marks
            co7marks = q_co7marks + t_co7marks
            co8marks = q_co8marks + t_co8marks
            co9marks = q_co9marks + t_co9marks
            co10marks = q_co10marks + t_co10marks

            co1_total = q_co1_total + t_co1_total
            co2_total = q_co2_total + t_co2_total
            co3_total = q_co3_total + t_co3_total
            co4_total = q_co4_total + t_co4_total
            co5_total = q_co5_total + t_co5_total
            co6_total = q_co6_total + t_co6_total
            co7_total = q_co7_total + t_co7_total
            co8_total = q_co8_total + t_co8_total
            co9_total = q_co9_total + t_co9_total
            co10_total = q_co10_total + t_co10_total

            final_quiz, final_test = sum(l_q), (sum(t_q) * 0.4)
            

            final_assign = 40 * (
                assign.total_assignment_marks / assignm.max_assignment_marks
            )
            print(final_quiz, final_test, final_assign, i)

            per1 = (co1marks / co1_total) * 100 if co1_total else 0
            per2 = (co2marks / co2_total) * 100 if co2_total else 0
            per3 = (co3marks / co3_total) * 100 if co3_total else 0
            per4 = (co4marks / co4_total) * 100 if co4_total else 0
            per5 = (co5marks / co5_total) * 100 if co5_total else 0
            per6 = (co6marks / co6_total) * 100 if co6_total else 0
            per7 = (co7marks / co7_total) * 100 if co7_total else 0
            per8 = (co8marks / co8_total) * 100 if co8_total else 0
            per9 = (co9marks / co9_total) * 100 if co9_total else 0
            per10 = (co10marks / co10_total) * 100 if co10_total else 0

            # this is to add to the internal calc table
            check = internal_co.query.filter_by(usn=i, coursecode=course_code).first()
            if check:
                check1 = internal_co.query.filter_by(
                    usn=i, coursecode=course_code
                ).update(
                    dict(
                        quiz1=q1.marks_q,
                        quiz2=q2.marks_q,
                        quiz3=q3.marks_q,
                        test1=t1.marks,
                        test2=t2.marks,
                        test3=t3.marks,
                        co1=co1marks,
                        co2=co2marks,
                        co3=co3marks,
                        co4=co4marks,
                        co5=co5marks,
                        co6=co6marks,
                        co7=co7marks,
                        co8=co8marks,
                        co9=co9marks,
                        co10=co10marks,
                        co1_total_marks=co1_total,
                        co2_total_marks=co2_total,
                        co3_total_marks=co3_total,
                        co4_total_marks=co4_total,
                        co5_total_marks=co5_total,
                        co6_total_marks=co6_total,
                        co7_total_marks=co7_total,
                        co8_total_marks=co8_total,
                        co9_total_marks=co9_total,
                        co10_total_marks=co10_total,
                        co1p=per1,
                        co2p=per2,
                        co3p=per3,
                        co4p=per4,
                        co5p=per5,
                        co6p=per6,
                        co7p=per7,
                        co8p=per8,
                        co9p=per9,
                        co10p=per10,
                        final_cie=sum([final_assign, final_quiz, final_test]),
                    )
                )
            else:

                new_internal_co = internal_co(
                    usn=i,
                    coursecode=course_code,
                    quiz1=q1.marks_q,
                    quiz2=q2.marks_q,
                    quiz3=q3.marks_q,
                    test1=t1.marks,
                    test2=t2.marks,
                    test3=t3.marks,
                    co1=co1marks,
                    co2=co2marks,
                    co3=co3marks,
                    co4=co4marks,
                    co5=co5marks,
                    co6=co6marks,
                    co7=co7marks,
                    co8=co8marks,
                    co9=co9marks,
                    co10=co10marks,
                    co1_total_marks=co1_total,
                    co2_total_marks=co2_total,
                    co3_total_marks=co3_total,
                    co4_total_marks=co4_total,
                    co5_total_marks=co5_total,
                    co6_total_marks=co6_total,
                    co7_total_marks=co7_total,
                    co8_total_marks=co8_total,
                    co9_total_marks=co9_total,
                    co10_total_marks=co10_total,
                    co1p=per1,
                    co2p=per2,
                    co3p=per3,
                    co4p=per4,
                    co5p=per5,
                    co6p=per6,
                    co7p=per7,
                    co8p=per8,
                    co9p=per9,
                    co10p=per10,
                    final_cie=sum([final_assign, final_quiz, final_test]),
                )
                db.session.add(new_internal_co)

            db.session.commit()

            # this is to add to the student_co table
            next_check = student_co.query.filter_by(
                usn=i, coursecode=course_code
            ).first()
            if next_check:
                next_check1 = student_co.query.filter_by(
                    usn=i, coursecode=course_code
                ).update(
                    dict(internal_marks=sum([final_assign, final_quiz, final_test]))
                )
            else:
                newstudentco = student_co(
                    usn=i,
                    coursecode=course_code,
                    internal_marks=sum([final_assign, final_quiz, final_test]),
                )
                db.session.add(newstudentco)
            db.session.commit()

    flash(
        "The student data was uploaded to internal co table and to the student co table",
        category="success",
    )
    return render_template("newmain.html")


@app.route("/directindirectinstudentcocalculation", methods=["GET", "POST"])
def dico_calc():
    staffid = session["staffid"]
    # staffid = '1234'
    # staffid = '5678'
    if staffid == "":
        flash("Please enter an appropriate Staff ID!", category="danger")
        return render_template("newmain.html")

    course_code = session["coursecode"]
    # course_code = '21EC25'
    # course_code='21ME24'
    if course_code == "":
        flash("Please enter an appropriate Course Code!", category="danger")
        return render_template("newmain.html")

    access = staffid_cc.query.filter_by(staffid=staffid, coursecode=course_code).first()
    students = list(map(str, access.usn_list.split(",")))

    the_course = course.query.filter_by(coursecode=course_code).first()
    lab_status = the_course.labyorn
    num_co = the_course.numberco
    dicop = the_course.dicop
    scop = the_course.scop
    qandtp = the_course.internal_cie + the_course.internal_quiz
    assp = the_course.internal_assign
    
    intco = (scop/(scop+1))
    semco = 1 - intco
    
    dco = (dicop/(dicop+1))
    ico = 1 - dco

    for i in students:

        if i != "":
            internal_row = internal_co.query.filter_by(
                coursecode=course_code, usn=i
            ).first()
            assign_row = assignment.query.filter_by(
                coursecode=course_code, usn=i
            ).first()
            semester_access = student_co.query.filter_by(
                coursecode=course_code, usn=i
            ).first()
            crsend_access = courseend_survey.query.filter_by(
                coursecode=course_code
            ).first()
            lab_access = lab_co.query.filter_by(coursecode=course_code, usn=i).first()
            den = 0

            # check the 11th column of table

            if lab_status == "N":
                den = 100
                sem_p = semester_access.sem_end_marks/1
                
                new_co1p = (internal_row.co1p * qandtp + assign_row.co1p * assp) / den
                new_co2p = (internal_row.co2p * qandtp + assign_row.co2p* assp) / den
                new_co3p = (internal_row.co3p * qandtp + assign_row.co3p* assp) / den
                new_co4p = (internal_row.co4p * qandtp + assign_row.co4p* assp) / den
                new_co5p = (internal_row.co5p * qandtp + assign_row.co5p* assp) / den
                new_co6p = (internal_row.co6p * qandtp + assign_row.co6p* assp) / den
                new_co7p = (internal_row.co7p * qandtp + assign_row.co7p* assp) / den
                new_co8p = (internal_row.co8p * qandtp + assign_row.co8p* assp) / den
                new_co9p = (internal_row.co9p * qandtp + assign_row.co9p* assp) / den
                new_co10p = (internal_row.co10p * qandtp + assign_row.co10p* assp) / den
                

            elif lab_status == "Y":
                sem_p = (semester_access.sem_end_marks) / 1.5
                den = 150
                new_co1p = (internal_row.co1p * qandtp + assign_row.co1p * assp + lab_access.co1p * 50) / den
                new_co2p = (internal_row.co2p * qandtp + assign_row.co2p * assp + lab_access.co2p * 50) / den
                new_co3p = (internal_row.co3p * qandtp + assign_row.co3p * assp + lab_access.co3p * 50) / den
                new_co4p = (internal_row.co4p * qandtp + assign_row.co4p * assp + lab_access.co4p * 50) / den
                new_co5p = (internal_row.co5p * qandtp + assign_row.co5p * assp + lab_access.co5p * 50) / den
                new_co6p = (internal_row.co6p * qandtp + assign_row.co6p * assp + lab_access.co6p * 50) / den
                new_co7p = (internal_row.co7p * qandtp + assign_row.co7p * assp + lab_access.co7p * 50) / den
                new_co8p = (internal_row.co8p * qandtp + assign_row.co8p * assp + lab_access.co8p * 50) / den
                new_co9p = (internal_row.co9p * qandtp + assign_row.co9p * assp + lab_access.co9p * 50) / den
                new_co10p = (internal_row.co10p * qandtp + assign_row.co10p * assp + lab_access.co10p* 50) / den

            s_co1p = new_co1p * intco + sem_p * semco
            s_co2p = new_co2p * intco + sem_p * semco
            s_co3p = new_co3p * intco + sem_p * semco
            s_co4p = new_co4p * intco + sem_p * semco
            s_co5p = new_co5p * intco + sem_p * semco
            s_co6p = new_co6p * intco + sem_p * semco
            s_co7p = new_co7p * intco + sem_p * semco
            s_co8p = new_co8p * intco + sem_p * semco
            s_co9p = new_co9p * intco + sem_p* semco
            s_co10p = new_co10p * intco + sem_p * semco
            print(s_co1p)

            di_co1p = s_co1p * dco + crsend_access.co1p * ico
            di_co2p = s_co2p * dco + crsend_access.co2p * ico
            di_co3p = s_co3p * dco + crsend_access.co3p * ico
            di_co4p = s_co4p * dco + crsend_access.co4p * ico
            di_co5p = s_co5p * dco + crsend_access.co5p * ico
            di_co6p = s_co6p * dco + crsend_access.co6p * ico
            di_co7p = s_co7p * dco + crsend_access.co7p * ico
            di_co8p = s_co8p * dco + crsend_access.co8p * ico
            di_co9p = s_co9p * dco + crsend_access.co9p * ico
            di_co10p = s_co10p * dco + crsend_access.co10p * ico
            
             

            new_student_update = student_co.query.filter_by(
                coursecode=course_code, usn=i
            ).update(
                dict(
                    co1p=new_co1p,
                    co2p=new_co2p,
                    co3p=new_co3p,
                    co4p=new_co4p,
                    co5p=new_co5p,
                    co6p=new_co6p,
                    co7p=new_co7p,
                    co8p=new_co8p,
                    co9p=new_co9p,
                    co10p=new_co10p,
                    sco1p=s_co1p,
                    sco2p=s_co2p,
                    sco3p=s_co3p,
                    sco4p=s_co4p,
                    sco5p=s_co5p,
                    sco6p=s_co6p,
                    sco7p=s_co7p,
                    sco8p=s_co8p,
                    sco9p=s_co9p,
                    sco10p=s_co10p,
                    dico1p=di_co1p,
                    dico2p=di_co2p,
                    dico3p=di_co3p,
                    dico4p=di_co4p,
                    dico5p=di_co5p,
                    dico6p=di_co6p,
                    dico7p=di_co7p,
                    dico8p=di_co8p,
                    dico9p=di_co9p,
                    dico10p=di_co10p,
                )
            )
            db.session.commit()

            # Making all the non existant co's = 0
            if num_co == 4:
                avgdico = (di_co1p + di_co2p + di_co3p + di_co4p)/4
                updated = student_co.query.filter_by(
                    coursecode=course_code, usn=i
                ).update(
                    dict(
                        co5p=0,
                        sco5p=0,
                        dico5p=0,
                        co6p=0,
                        sco6p=0,
                        dico6p=0,
                        co7p=0,
                        sco7p=0,
                        dico7p=0,
                        co8p=0,
                        sco8p=0,
                        dico8p=0,
                        co9p=0,
                        sco9p=0,
                        dico9p=0,
                        co10p=0,
                        sco10p=0,
                        dico10p=0,
                        avg_dico = avgdico
                    )
                )

            elif num_co == 5:
                avgdico = (di_co1p + di_co2p + di_co3p + di_co4p + di_co5p)/5
                updated = student_co.query.filter_by(
                    coursecode=course_code, usn=i
                ).update(
                    dict(
                        co6p=0,
                        sco6p=0,
                        dico6p=0,
                        co7p=0,
                        sco7p=0,
                        dico7p=0,
                        co8p=0,
                        sco8p=0,
                        dico8p=0,
                        co9p=0,
                        sco9p=0,
                        dico9p=0,
                        co10p=0,
                        sco10p=0,
                        dico10p=0,
                        avg_dico=avgdico
                    )
                )

            elif num_co == 6:
                avgdico = (di_co1p + di_co2p + di_co3p + di_co4p + di_co5p + di_co6p)/6
                updated = student_co.query.filter_by(
                    coursecode=course_code, usn=i
                ).update(
                    dict(
                        co7p=0,
                        sco7p=0,
                        dico7p=0,
                        co8p=0,
                        sco8p=0,
                        dico8p=0,
                        co9p=0,
                        sco9p=0,
                        dico9p=0,
                        co10p=0,
                        sco10p=0,
                        dico10p=0,
                        avg_dico=avgdico
                    )
                )

            elif num_co == 7:
                avgdico = (di_co1p + di_co2p + di_co3p + di_co4p + di_co5p + di_co6p + di_co7p)/7
                updated = student_co.query.filter_by(
                    coursecode=course_code, usn=i
                ).update(
                    dict(
                        co8p=0,
                        sco8p=0,
                        dico8p=0,
                        co9p=0,
                        sco9p=0,
                        dico9p=0,
                        co10p=0,
                        sco10p=0,
                        dico10p=0,
                        avg_dico=avgdico
                    )
                )

            elif num_co == 8:
                avgdico = (di_co1p + di_co2p + di_co3p + di_co4p + di_co5p + di_co6p + di_co7p + di_co8p)/8
                updated = student_co.query.filter_by(
                    coursecode=course_code, usn=i
                ).update(dict(co9p=0, sco9p=0, dico9p=0, co10p=0, sco10p=0, dico10p=0, avg_dico=avgdico))

            elif num_co == 9:
                avgdico = (di_co1p + di_co2p + di_co3p + di_co4p + di_co5p + di_co6p + di_co7p + di_co8p + di_co9p)/9
                updated = student_co.query.filter_by(
                    coursecode=course_code, usn=i
                ).update(dict(co10p=0, sco10p=0, dico10p=0, avg_dico=avgdico))
            
            elif num_co == 10:
                avgdico = (di_co1p + di_co2p + di_co3p + di_co4p + di_co5p + di_co6p + di_co7p + di_co8p + di_co9p + di_co10p)/10
                updated = student_co.query.filter_by(
                    coursecode=course_code, usn=i
                ).update(dict(avg_dico=avgdico))
                
            db.session.commit()

    flash(
        "The co percentages have been updated in the student co table!",
        category="success",
    )
    return render_template("newmain.html")

@app.route("/subjectcocalculate", methods=["GET", "POST"])
def subjectco_calc():
    # course_code='21ME24'
    course_code = session["coursecode"]
    if course_code == "":
        flash("Please enter an appropriate Course Code!", category="danger")
        return render_template("main.html")

    studentco_access = student_co.query.filter_by(coursecode=course_code).all()
    l = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # for sco's
    di = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # for dicop
    reg = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # for regular cop

    num_student = 0
    for i in studentco_access:
        
        reg[0] += i.co1p
        reg[1] += i.co2p
        reg[2] += i.co3p
        reg[3] += i.co4p
        reg[4] += i.co5p
        reg[5] += i.co6p
        reg[6] += i.co7p
        reg[7] += i.co8p
        reg[8] += i.co9p
        reg[9] += i.co10p

        l[0] += i.sco1p
        l[1] += i.sco2p
        l[2] += i.sco3p
        l[3] += i.sco4p
        l[4] += i.sco5p
        l[5] += i.sco6p
        l[6] += i.sco7p
        l[7] += i.sco8p
        l[8] += i.sco9p
        l[9] += i.sco10p

        di[0] += i.dico1p
        di[1] += i.dico2p
        di[2] += i.dico3p
        di[3] += i.dico4p
        di[4] += i.dico5p
        di[5] += i.dico6p
        di[6] += i.dico7p
        di[7] += i.dico8p
        di[8] += i.dico9p
        di[9] += i.dico10p
        num_student += 1

    for i in range(10):
        l[i] = l[i] / num_student
        di[i] = di[i] / num_student
        reg[i] = reg[i] / num_student

    check = subject_co.query.filter_by(coursecode=course_code).first()
    if check:
        check1 = subject_co.query.filter_by(coursecode=course_code).update(
            dict(
                sco1p=l[0],
                sco2p=l[1],
                sco3p=l[2],
                sco4p=l[3],
                sco5p=l[4],
                sco6p=l[5],
                sco7p=l[6],
                sco8p=l[7],
                sco9p=l[8],
                sco10p=l[9],
                dico1p=di[0],
                dico2p=di[1],
                dico3p=di[2],
                dico4p=di[3],
                dico5p=di[4],
                dico6p=di[5],
                dico7p=di[6],
                dico8p=di[7],
                dico9p=di[8],
                dico10p=di[9],
                co1p=reg[0],
                co2p=reg[1],
                co3p=reg[2],
                co4p=reg[3],
                co5p=reg[4],
                co6p=reg[5],
                co7p=reg[6],
                co8p=reg[7],
                co9p=reg[8],
                co10p=reg[9],
            )
        )
    else:

        new_subjectco = subject_co(
            coursecode=course_code,
            sco1p=l[0],
            sco2p=l[1],
            sco3p=l[2],
            sco4p=l[3],
            sco5p=l[4],
            sco6p=l[5],
            sco7p=l[6],
            sco8p=l[7],
            sco9p=l[8],
            sco10p=l[9],
            dico1p=di[0],
            dico2p=di[1],
            dico3p=di[2],
            dico4p=di[3],
            dico5p=di[4],
            dico6p=di[5],
            dico7p=di[6],
            dico8p=di[7],
            dico9p=di[8],
            dico10p=di[9],
            co1p=reg[0],
            co2p=reg[1],
            co3p=reg[2],
            co4p=reg[3],
            co5p=reg[4],
            co6p=reg[5],
            co7p=reg[6],
            co8p=reg[7],
            co9p=reg[8],
            co10p=reg[9],
        )

        db.session.add(new_subjectco)
    db.session.commit()
    flash("The calculations are done and data is added to Subject CO Table!", category='success')

    return render_template("main.html")

@app.route("/levelcalculation", methods=['GET', 'POST'])
def level_calc():
    staffid = session["staffid"]
    # staffid = '1234'
    # staffid = '5678'
    if staffid == "":
        flash("Please enter an appropriate Staff ID!", category="danger")
        return render_template("newmain.html")

    coursecode = session["coursecode"]
    # course_code = '21EC25'
    # course_code='21ME24'
    if coursecode == "":
        flash("Please enter an appropriate Course Code!", category="danger")
        return render_template("newmain.html")

    studentco_access = student_co.query.filter_by(coursecode=coursecode).all()    
    course_access = course.query.filter_by(coursecode=coursecode).first()
    num_co = course_access.numberco
    level_3 = course_access.level3
    level_2 = course_access.level2
    level_1 = course_access.level1  
    
    final_sum = 0
    final_count = 0
    
    if num_co == 4:
        for i in studentco_access:
            sum = i.co1p + i.co2p + i.co3p + i.co4p 
            avg_co = sum/4
            final_sum += avg_co
            final_count += 1
        
        avgcie = final_sum/final_count
        level_access = level(coursecode=coursecode, avg_cie=avgcie)
        db.session.add(level_access)
        db.session.commit()       
        
        newnum = 0
        count = 0
        for i in studentco_access:
            sum = i.co1p + i.co2p + i.co3p + i.co4p 
            avg_co = sum/4
            count += 1
            if avg_co >= avgcie:
                newnum += 1
        
        # number of people who have got more cie percentage than the avgcie is newnum
        # percentage is newnum/count
        
        ratio = (newnum/count) * 100
        
        if ratio >= level_3:
            lev = 3
        elif ratio >= level_2:
            lev = 2
        elif ratio >= level_1:
            lev = 1
        else:
            lev = 0
        
        level_access = level.query.filter_by(coursecode=coursecode).update(dict(cie_level=lev))
        final_cie_level = float(lev)
        db.session.commit()
        
        see_sum = 0
        count = 0
        for i in studentco_access:
            see_sum += i.sem_end_marks
            count += 1
        see_avg = see_sum/count
        level_access = level.query.filter_by(coursecode=coursecode).update(dict(avg_see=see_avg))
        db.session.commit()
        
        count = 0
        newnum = 0
        for i in studentco_access:
            count += 1
            if i.sem_end_marks >= see_avg:
                newnum += 1
        
        ratio = (newnum/count) * 100
                
        if ratio >= level_3:
            lev = 3
        elif ratio >= level_2:
            lev = 2
        elif ratio >= level_1:
            lev = 1
        else:
            lev = 0
        
        level_access = level.query.filter_by(coursecode=coursecode).update(dict(see_level=lev))
        final_see_level = float(lev)
        db.session.commit()
        
        final_d_level = 0.8 * final_cie_level + 0.2 * final_see_level
        level_access = level.query.filter_by(coursecode=coursecode).update(dict(final_direct_level=final_d_level))
        db.session.commit()
        
        ia = courseend_survey.query.filter_by(coursecode=coursecode).first()
        
        ratio = (ia.co1p + ia.co2p + ia.co3p + ia.co4p)/4
        
        if ratio >= 80:
            lev = 3
        elif ratio >= 60:
            lev = 2
        elif ratio >= 40:
            lev = 1
        else:
            lev = 0
        
        
        final = 0.9*final_d_level + 0.1*lev
        
        level_access = level.query.filter_by(coursecode=coursecode).update(dict(avg_indirect=ratio, indirect_level=lev,
                                                                                final_level=final))
        db.session.commit()
        
    
    elif num_co == 5:
        for i in studentco_access:
            sum = i.co1p + i.co2p + i.co3p + i.co4p + i.co5p
            avg_co = sum/5
            final_sum += avg_co
            final_count += 1
        
        avgcie = final_sum/final_count
        level_access = level(coursecode=coursecode, avg_cie=avgcie)
        db.session.add(level_access)
        db.session.commit()       
        
        newnum = 0
        count = 0
        for i in studentco_access:
            sum = i.co1p + i.co2p + i.co3p + i.co4p + i.co5p
            avg_co = sum/5
            count += 1
            if avg_co >= avgcie:
                newnum += 1
        
        # number of people who have got more cie percentage than the avgcie is newnum
        # percentage is newnum/count
        
        ratio = (newnum/count) * 100
        
        if ratio >= level_3:
            lev = 3
        elif ratio >= level_2:
            lev = 2
        elif ratio >= level_1:
            lev = 1
        else:
            lev = 0
        
        level_access = level.query.filter_by(coursecode=coursecode).update(dict(cie_level=lev))
        final_cie_level = float(lev)
        db.session.commit()
        
        see_sum = 0
        count = 0
        for i in studentco_access:
            see_sum += i.sem_end_marks
            count += 1
        see_avg = see_sum/count
        level_access = level.query.filter_by(coursecode=coursecode).update(dict(avg_see=see_avg))
        db.session.commit()
        
        count = 0
        newnum = 0
        for i in studentco_access:
            count += 1
            if i.sem_end_marks >= see_avg:
                newnum += 1
        
        ratio = (newnum/count) * 100
                
        if ratio >= level_3:
            lev = 3
        elif ratio >= level_2:
            lev = 2
        elif ratio >= level_1:
            lev = 1
        else:
            lev = 0
        
        level_access = level.query.filter_by(coursecode=coursecode).update(dict(see_level=lev))
        final_see_level = float(lev)
        db.session.commit()
        
        final_d_level = 0.8 * final_cie_level + 0.2 * final_see_level
        level_access = level.query.filter_by(coursecode=coursecode).update(dict(final_direct_level=final_d_level))
        db.session.commit()
        
        ia = courseend_survey.query.filter_by(coursecode=coursecode).first()
        
        ratio = (ia.co1p + ia.co2p + ia.co3p + ia.co4p + ia.co5p)/5
        
        if ratio >= 80:
            lev = 3
        elif ratio >= 60:
            lev = 2
        elif ratio >= 40:
            lev = 1
        else:
            lev = 0
        
        
        final = 0.9*final_d_level + 0.1*lev
        
        level_access = level.query.filter_by(coursecode=coursecode).update(dict(avg_indirect=ratio, indirect_level=lev,
                                                                                final_level=final))
        db.session.commit()
            
        
    elif num_co == 6:
        for i in studentco_access:
            sum = i.co1p + i.co2p + i.co3p + i.co4p + i.co5p + i.co6p
            avg_co = sum/6
            final_sum += avg_co
            final_count += 1
        
        avgcie = final_sum/final_count
        level_access = level(coursecode=coursecode, avg_cie=avgcie)
        db.session.add(level_access)
        db.session.commit()       
        
        newnum = 0
        count = 0
        for i in studentco_access:
            sum = i.co1p + i.co2p + i.co3p + i.co4p + i.co5p + i.co6p
            avg_co = sum/6
            count += 1
            if avg_co >= avgcie:
                newnum += 1
        
        # number of people who have got more cie percentage than the avgcie is newnum
        # percentage is newnum/count
        
        ratio = (newnum/count) * 100
        
        if ratio >= level_3:
            lev = 3
        elif ratio >= level_2:
            lev = 2
        elif ratio >= level_1:
            lev = 1
        else:
            lev = 0
        
        level_access = level.query.filter_by(coursecode=coursecode).update(dict(cie_level=lev))
        final_cie_level = float(lev)
        db.session.commit()
        
        see_sum = 0
        count = 0
        for i in studentco_access:
            see_sum += i.sem_end_marks
            count += 1
        see_avg = see_sum/count
        level_access = level.query.filter_by(coursecode=coursecode).update(dict(avg_see=see_avg))
        db.session.commit()
        
        count = 0
        newnum = 0
        for i in studentco_access:
            count += 1
            if i.sem_end_marks >= see_avg:
                newnum += 1
        
        ratio = (newnum/count) * 100
                
        if ratio >= level_3:
            lev = 3
        elif ratio >= level_2:
            lev = 2
        elif ratio >= level_1:
            lev = 1
        else:
            lev = 0
        
        level_access = level.query.filter_by(coursecode=coursecode).update(dict(see_level=lev))
        final_see_level = float(lev)
        db.session.commit()
        
        final_d_level = 0.8 * final_cie_level + 0.2 * final_see_level
        level_access = level.query.filter_by(coursecode=coursecode).update(dict(final_direct_level=final_d_level))
        db.session.commit()
        
        ia = courseend_survey.query.filter_by(coursecode=coursecode).first()
        
        ratio = (ia.co1p + ia.co2p + ia.co3p + ia.co4p + ia.co5p + ia.co6p)/6
        
        if ratio >= 80:
            lev = 3
        elif ratio >= 60:
            lev = 2
        elif ratio >= 40:
            lev = 1
        else:
            lev = 0
        
        
        final = 0.9*final_d_level + 0.1*lev
        
        level_access = level.query.filter_by(coursecode=coursecode).update(dict(avg_indirect=ratio, indirect_level=lev,
                                                                                final_level=final))
        db.session.commit()           
          
    
    elif num_co == 7:
        for i in studentco_access:
            sum = i.co1p + i.co2p + i.co3p + i.co4p + i.co5p + i.co6p + i.co7p
            avg_co = sum/7
            final_sum += avg_co
            final_count += 1
        
        avgcie = final_sum/final_count
        level_access = level(coursecode=coursecode, avg_cie=avgcie)
        db.session.add(level_access)
        db.session.commit()       
        
        newnum = 0
        count = 0
        for i in studentco_access:
            sum = i.co1p + i.co2p + i.co3p + i.co4p + i.co5p + i.co6p + i.co7p
            avg_co = sum/7
            count += 1
            if avg_co >= avgcie:
                newnum += 1
        
        # number of people who have got more cie percentage than the avgcie is newnum
        # percentage is newnum/count
        
        ratio = (newnum/count) * 100
        
        if ratio >= level_3:
            lev = 3
        elif ratio >= level_2:
            lev = 2
        elif ratio >= level_1:
            lev = 1
        else:
            lev = 0
        
        level_access = level.query.filter_by(coursecode=coursecode).update(dict(cie_level=lev))
        final_cie_level = float(lev)
        db.session.commit()
        
        see_sum = 0
        count = 0
        for i in studentco_access:
            see_sum += i.sem_end_marks
            count += 1
        see_avg = see_sum/count
        level_access = level.query.filter_by(coursecode=coursecode).update(dict(avg_see=see_avg))
        db.session.commit()
        
        count = 0
        newnum = 0
        for i in studentco_access:
            count += 1
            if i.sem_end_marks >= see_avg:
                newnum += 1
        
        ratio = (newnum/count) * 100
                
        if ratio >= level_3:
            lev = 3
        elif ratio >= level_2:
            lev = 2
        elif ratio >= level_1:
            lev = 1
        else:
            lev = 0
        
        level_access = level.query.filter_by(coursecode=coursecode).update(dict(see_level=lev))
        final_see_level = float(lev)
        db.session.commit()
        
        final_d_level = 0.8 * final_cie_level + 0.2 * final_see_level
        level_access = level.query.filter_by(coursecode=coursecode).update(dict(final_direct_level=final_d_level))
        db.session.commit()
        
        ia = courseend_survey.query.filter_by(coursecode=coursecode).first()
        
        ratio = (ia.co1p + ia.co2p + ia.co3p + ia.co4p + ia.co5p + ia.co6p + ia.co7p)/7
        
        if ratio >= 80:
            lev = 3
        elif ratio >= 60:
            lev = 2
        elif ratio >= 40:
            lev = 1
        else:
            lev = 0
        
        
        final = 0.9*final_d_level + 0.1*lev
        
        level_access = level.query.filter_by(coursecode=coursecode).update(dict(avg_indirect=ratio, indirect_level=lev,
                                                                                final_level=final))
        db.session.commit()     
    
    
    elif num_co == 8:
        for i in studentco_access:
            sum = i.co1p + i.co2p + i.co3p + i.co4p + i.co5p + i.co6p + i.co7p + i.co8p
            avg_co = sum/8
            final_sum += avg_co
            final_count += 1
        
        avgcie = final_sum/final_count
        level_access = level(coursecode=coursecode, avg_cie=avgcie)
        db.session.add(level_access)
        db.session.commit()       
        
        newnum = 0
        count = 0
        for i in studentco_access:
            sum = i.co1p + i.co2p + i.co3p + i.co4p + i.co5p + i.co6p + i.co7p + i.co8p
            avg_co = sum/8
            count += 1
            if avg_co >= avgcie:
                newnum += 1
        
        # number of people who have got more cie percentage than the avgcie is newnum
        # percentage is newnum/count
        
        ratio = (newnum/count) * 100
        
        if ratio >= level_3:
            lev = 3
        elif ratio >= level_2:
            lev = 2
        elif ratio >= level_1:
            lev = 1
        else:
            lev = 0
        
        level_access = level.query.filter_by(coursecode=coursecode).update(dict(cie_level=lev))
        final_cie_level = float(lev)
        db.session.commit()
        
        see_sum = 0
        count = 0
        for i in studentco_access:
            see_sum += i.sem_end_marks
            count += 1
        see_avg = see_sum/count
        level_access = level.query.filter_by(coursecode=coursecode).update(dict(avg_see=see_avg))
        db.session.commit()
        
        count = 0
        newnum = 0
        for i in studentco_access:
            count += 1
            if i.sem_end_marks >= see_avg:
                newnum += 1
        
        ratio = (newnum/count) * 100
                
        if ratio >= level_3:
            lev = 3
        elif ratio >= level_2:
            lev = 2
        elif ratio >= level_1:
            lev = 1
        else:
            lev = 0
        
        level_access = level.query.filter_by(coursecode=coursecode).update(dict(see_level=lev))
        final_see_level = float(lev)
        db.session.commit()
        
        final_d_level = 0.8 * final_cie_level + 0.2 * final_see_level
        level_access = level.query.filter_by(coursecode=coursecode).update(dict(final_direct_level=final_d_level))
        db.session.commit()
        
        ia = courseend_survey.query.filter_by(coursecode=coursecode).first()
        
        ratio = (ia.co1p + ia.co2p + ia.co3p + ia.co4p + ia.co5p + ia.co6p + ia.co7p + ia.co8p)/8
        
        if ratio >= 80:
            lev = 3
        elif ratio >= 60:
            lev = 2
        elif ratio >= 40:
            lev = 1
        else:
            lev = 0
        
        
        final = 0.9*final_d_level + 0.1*lev
        
        level_access = level.query.filter_by(coursecode=coursecode).update(dict(avg_indirect=ratio, indirect_level=lev,
                                                                                final_level=final))
        db.session.commit()  
    
    
    elif num_co == 9:
        for i in studentco_access:
            sum = i.co1p + i.co2p + i.co3p + i.co4p + i.co5p + i.co6p + i.co7p + i.co8p + i.co9p
            avg_co = sum/9
            final_sum += avg_co
            final_count += 1
        
        avgcie = final_sum/final_count
        level_access = level(coursecode=coursecode, avg_cie=avgcie)
        db.session.add(level_access)
        db.session.commit()       
        
        newnum = 0
        count = 0
        for i in studentco_access:
            sum = i.co1p + i.co2p + i.co3p + i.co4p + i.co5p + i.co6p + i.co7p + i.co8p + i.co9p
            avg_co = sum/9
            count += 1
            if avg_co >= avgcie:
                newnum += 1
        
        # number of people who have got more cie percentage than the avgcie is newnum
        # percentage is newnum/count
        
        ratio = (newnum/count) * 100
        
        if ratio >= level_3:
            lev = 3
        elif ratio >= level_2:
            lev = 2
        elif ratio >= level_1:
            lev = 1
        else:
            lev = 0
        
        level_access = level.query.filter_by(coursecode=coursecode).update(dict(cie_level=lev))
        final_cie_level = float(lev)
        db.session.commit()
        
        see_sum = 0
        count = 0
        for i in studentco_access:
            see_sum += i.sem_end_marks
            count += 1
        see_avg = see_sum/count
        level_access = level.query.filter_by(coursecode=coursecode).update(dict(avg_see=see_avg))
        db.session.commit()
        
        count = 0
        newnum = 0
        for i in studentco_access:
            count += 1
            if i.sem_end_marks >= see_avg:
                newnum += 1
        
        ratio = (newnum/count) * 100
                
        if ratio >= level_3:
            lev = 3
        elif ratio >= level_2:
            lev = 2
        elif ratio >= level_1:
            lev = 1
        else:
            lev = 0
        
        level_access = level.query.filter_by(coursecode=coursecode).update(dict(see_level=lev))
        final_see_level = float(lev)
        db.session.commit()
        
        final_d_level = 0.8 * final_cie_level + 0.2 * final_see_level
        level_access = level.query.filter_by(coursecode=coursecode).update(dict(final_direct_level=final_d_level))
        db.session.commit()
        
        ia = courseend_survey.query.filter_by(coursecode=coursecode).first()
        
        ratio = (ia.co1p + ia.co2p + ia.co3p + ia.co4p + ia.co5p + ia.co6p + ia.co7p + ia.co8p + ia.co9p)/9
        
        if ratio >= 80:
            lev = 3
        elif ratio >= 60:
            lev = 2
        elif ratio >= 40:
            lev = 1
        else:
            lev = 0
        
        
        final = 0.9*final_d_level + 0.1*lev
        
        level_access = level.query.filter_by(coursecode=coursecode).update(dict(avg_indirect=ratio, indirect_level=lev,
                                                                                final_level=final))
        db.session.commit()  
    
    
    elif num_co == 10:
        for i in studentco_access:
            sum = i.co1p + i.co2p + i.co3p + i.co4p + i.co5p + i.co6p + i.co7p + i.co8p + i.co9p +i.co10p
            avg_co = sum/10
            final_sum += avg_co
            final_count += 1
        
        avgcie = final_sum/final_count
        level_access = level(coursecode=coursecode, avg_cie=avgcie)
        db.session.add(level_access)
        db.session.commit()       
        
        newnum = 0
        count = 0
        for i in studentco_access:
            sum = i.co1p + i.co2p + i.co3p + i.co4p + i.co5p + i.co6p + i.co7p + i.co8p + i.co9p + i.co10p
            avg_co = sum/10
            count += 1
            if avg_co >= avgcie:
                newnum += 1
        
        # number of people who have got more cie percentage than the avgcie is newnum
        # percentage is newnum/count
        
        ratio = (newnum/count) * 100
        
        if ratio >= level_3:
            lev = 3
        elif ratio >= level_2:
            lev = 2
        elif ratio >= level_1:
            lev = 1
        else:
            lev = 0
        
        level_access = level.query.filter_by(coursecode=coursecode).update(dict(cie_level=lev))
        final_cie_level = float(lev)
        db.session.commit()
        
        see_sum = 0
        count = 0
        for i in studentco_access:
            see_sum += i.sem_end_marks
            count += 1
        see_avg = see_sum/count
        level_access = level.query.filter_by(coursecode=coursecode).update(dict(avg_see=see_avg))
        db.session.commit()
        
        count = 0
        newnum = 0
        for i in studentco_access:
            count += 1
            if i.sem_end_marks >= see_avg:
                newnum += 1
        
        ratio = (newnum/count) * 100
                
        if ratio >= level_3:
            lev = 3
        elif ratio >= level_2:
            lev = 2
        elif ratio >= level_1:
            lev = 1
        else:
            lev = 0
        
        level_access = level.query.filter_by(coursecode=coursecode).update(dict(see_level=lev))
        final_see_level = float(lev)
        db.session.commit()
        
        final_d_level = 0.8 * final_cie_level + 0.2 * final_see_level
        level_access = level.query.filter_by(coursecode=coursecode).update(dict(final_direct_level=final_d_level))
        db.session.commit()
        
        ia = courseend_survey.query.filter_by(coursecode=coursecode).first()
        
        ratio = (ia.co1p + ia.co2p + ia.co3p + ia.co4p + ia.co5p + ia.co6p + ia.co7p + ia.co8p + ia.co9p + ia.co10p)/10
        
        if ratio >= 80:
            lev = 3
        elif ratio >= 60:
            lev = 2
        elif ratio >= 40:
            lev = 1
        else:
            lev = 0
        
        
        final = 0.9*final_d_level + 0.1*lev
        
        level_access = level.query.filter_by(coursecode=coursecode).update(dict(avg_indirect=ratio, indirect_level=lev,
                                                                                final_level=final))
        db.session.commit()
    
    
    flash("The level has been calculated for this course!", category="success")
    return render_template('newmain.html')
    
@app.route("/threshold_calc", methods=['GET', 'POST'])
def thresh_calc():
    staffid = session["staffid"]
    # staffid = '1234'
    # staffid = '5678'
    if staffid == "":
        flash("Please enter an appropriate Staff ID!", category="danger")
        return render_template("newmain.html")

    coursecode = session["coursecode"]
    # course_code = '21EC25'
    # course_code='21ME24'
    if coursecode == "":
        flash("Please enter an appropriate Course Code!", category="danger")
        return render_template("newmain.html")   
    
    
    access = staffid_cc.query.filter_by(staffid=staffid, coursecode=coursecode).first()
    students = list(map(str, access.usn_list.split(",")))
    course_access = course.query.filter_by(coursecode=coursecode).first()
    pas = course_access.target
    numco = course_access.numberco
    
    for i in students:
        if i != '':
            sa = student_co.query.filter_by(usn=i, coursecode=coursecode).first()
            l = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
            
            if sa.dico1p >= pas:
                l[0] = 'Y'
            else:
                l[0] = 'N'
            if sa.dico2p >= pas:
                l[1] = 'Y'
            else:
                l[1] = 'N'
            if sa.dico3p >= pas:
                l[2] = 'Y'
            else:
                l[2] = 'N'
            if sa.dico4p >= pas:
                l[3] = 'Y'
            else:
                l[3] = 'N'
            
            if numco >= 5:
                if sa.dico5p >= pas:
                    l[4] = 'Y'
                else:
                    l[4] = 'N'
                
                if numco >= 6:
                    if sa.dico6p >= pas:
                        l[5] = 'Y'
                    else:
                        l[5] = 'N'
                        
                    if numco >= 7:
                        if sa.dico7p >= pas:
                            l[6] = 'Y'
                        else:
                            l[6] = 'N'
                        
                        if numco >= 8:
                            if sa.dico8p >= pas:
                                l[7] = 'Y'
                            else:
                                l[7] = 'N'
                                
                            if numco >= 9:
                                if sa.dico9p >= pas:
                                    l[8] = 'Y'
                                else:
                                    l[8] = 'N'
                            
                                if numco == 10:
                                    if sa.dico10p >= pas:
                                        l[9] = 'Y'
                                    else:
                                        l[9] = 'N'               
                                            
            
            thresh_access = threshold.query.filter_by(usn=i, coursecode=coursecode).first()
            print(thresh_access)
            if thresh_access == None:
                print("Inside")
                new_thresh = threshold(usn=i, coursecode=coursecode, 
                                       co1p=l[0], co2p=l[1], co3p=l[2], co4p=l[3], 
                                       co5p=l[4] if len(l)>5 else 0, co6p=l[5] if len(l)>6 else 0, co7p=l[6] if len(l)>7 else 0, 
                                       co8p=l[7] if len(l)>8 else 0, 
                                       co9p=l[8] if len(l)>9 else 0, co10p=l[9] if len(l)>10 else 0)
                db.session.add(new_thresh)
            
            else:
                thresh_update = threshold.query.filter_by(usn=i, coursecode=coursecode).update(dict(
                                        co1p=l[0], co2p=l[1], co3p=l[2], co4p=l[3], 
                                        co5p=l[4] if len(l)>5 else 0, co6p=l[5] if len(l)>6 else 0, co7p=l[6] if len(l)>7 else 0, co8p=l[7], 
                                        co9p=l[8], co10p=l[9]
                ))
            
            db.session.commit()
            
            flash("Threshold has been calculated !", category='success')
            return render_template("newmain.html")


@app.route('/po_firststep', methods=['GET', 'POST'])
def po_calc():
    staffid = session["staffid"]
    # staffid = '1234'
    # staffid = '5678'
    if staffid == "":
        flash("Please enter an appropriate Staff ID!", category="danger")
        return render_template("newmain.html")

    coursecode = session["coursecode"]
    # course_code = '21EC25'
    # course_code='21ME24'
    if coursecode == "":
        flash("Please enter an appropriate Course Code!", category="danger")
        return render_template("newmain.html") 
    
    form = po_form_upload()
    
    if form.validate_on_submit():
        filename = secure_filename(form.file.data.filename)
        file_path = app.config["UPLOAD_FOLDER"] + filename
        form.file.data.save(file_path)  # +filename
        year = form.year.data
        
        numerator = [0] * 14
        denominator = [0] * 14

        with open(file_path, "r", newline="") as f:
            r = csv.DictReader(f)
            for i in r:
                the_coursecode = i['CourseCode']
                po1 = float(i['PO1']) if i['PO1'] else 0
                po2 = float(i['PO2']) if i['PO2'] else 0
                po3 = float(i['PO3']) if i['PO3'] else 0
                po4 = float(i['PO4']) if i['PO4'] else 0
                po5 = float(i['PO5']) if i['PO5'] else 0
                po6 = float(i['PO6']) if i['PO6'] else 0
                po7 = float(i['PO7']) if i['PO7'] else 0
                po8 = float(i['PO8']) if i['PO8'] else 0
                po9 = float(i['PO9']) if i['PO9'] else 0
                po10 = float(i['PO10']) if i['PO10'] else 0
                po11 = float(i['PO11']) if i['PO11'] else 0
                po12 = float(i['PO12'])  if i['PO12'] else 0 
                pso1 = float(i['PSO1']) if i['PSO1'] else 0  
                pso2 = float(i['PSO2']) if i['PSO2'] else 0  
                
                level_access = level.query.filter_by(coursecode=the_coursecode).first()
                
                if level_access:
                    lev = level_access.final_level
                    print((lev), (po1))
                    numerator[0] += lev * po1
                    denominator[0] += po1
                    
                    numerator[1] += lev * po2
                    denominator[1] += po2
                    
                    numerator[2] += lev * po3
                    denominator[2] += po3
                    
                    numerator[3] += lev * po4
                    denominator[3] += po4
                    
                    numerator[4] += lev * po5
                    denominator[4] += po5
                    
                    numerator[5] += lev * po6
                    denominator[5] += po6
                    
                    numerator[6] += lev * po7
                    denominator[6] += po7
                    
                    numerator[7] += lev * po8
                    denominator[7] += po8
                    
                    numerator[8] += lev * po9
                    denominator[8] += po9
                    
                    numerator[9] += lev * po10
                    denominator[9] += po10
                    
                    numerator[10] += lev * po11
                    denominator[10] += po11
                    
                    numerator[11] += lev * po12
                    denominator[11] += po12   
                    
                    numerator[12] += lev * pso1
                    denominator[12] += pso1   
                    
                    numerator[13] += lev * pso2
                    denominator[13] += pso2   
                    
                    print(numerator, denominator)    
                    
                else:
                    flash(f"Level has not yet been calculated for this course- {the_coursecode}", category="danger")
                    return render_template('newmain.html')
                
                po_access = po_mapping.query.filter_by(coursecode=the_coursecode).first()
                if po_access:
                    new_update = po_mapping.query.filter_by(coursecode=the_coursecode).update(dict(
                        po1=po1, po2=po2, po3=po3, po4=po4, po5=po5,
                        po6=po6, po7=po7, po8=po8, po9=po9, po10=po10, po11=po11, po12=po12, 
                        pso1=pso1, pso2=pso2
                    ))
                
                else:
                    new_po = po_mapping(coursecode=the_coursecode, 
                                        po1=po1, po2=po2, po3=po3, po4=po4, po5=po5,
                                        po6=po6, po7=po7, po8=po8, po9=po9, po10=po10, po11=po11, po12=po12, 
                                        pso1=pso1, pso2=pso2)
                    db.session.add(new_po)
                
                db.session.commit()
        # file ended
        
        po_final = [0]*14
        
        for i in range(14):
            po_final[i] = (numerator[i]/denominator[i]) if denominator[i] != 0 else 0
        
        po_attainment_access = po_attainment.query.filter_by(batch=year).first()
        if po_attainment_access:
            new_update = po_attainment.query.filter_by(batch=2021).update(dict(
                po1=po_final[0], po2=po_final[1], po3=po_final[2], po4=po_final[3], po5=po_final[4],
                po6=po_final[5], po7=po_final[6], po8=po_final[7], po9=po_final[8], po10=po_final[9],  
                po11=po_final[10], po12=po_final[11], pso1=po_final[12], pso2=po_final[13]
            ))
        else:
            new_po_attainment = po_attainment(batch=2021, 
                                po1=po_final[0], po2=po_final[1], po3=po_final[2], po4=po_final[3], po5=po_final[4],
                                po6=po_final[5], po7=po_final[6], po8=po_final[7], po9=po_final[8], po10=po_final[9],  
                                po11=po_final[10], po12=po_final[11], pso1=po_final[12], pso2=po_final[13])
            db.session.add(new_po_attainment)
        
        db.session.commit()
        
        
        flash("The PO mapping has been uploaded!", category="success")
        return render_template('newmain.html')
    
    if form.errors != {}:
        for err_msg in form.errors.values():
            flash(f"There was an error : {err_msg}", category="danger")

    return render_template("po_mapping_upload.html", form=form)
    
                
                    
                
        
    

                    
                
                
            
            
    
    
                

    
    
        
    
    
    
