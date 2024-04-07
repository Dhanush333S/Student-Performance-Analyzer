
from email.policy import default
from enum import unique
from sqlalchemy import null
from Teacher import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from Teacher import login_manager
from wtforms.validators import ValidationError

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

#################################################################################
#User login and logout to webiste tables
#added
class User(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key = True)
    username = db.Column(db.String(length = 30), nullable = False, unique = True)
    password_hash = db.Column(db.String(length = 300), nullable = True)
    role=db.Column(db.String(length=30),nullable=False,default="staff")
    email=db.Column(db.String(length=300),nullable=False)
    # def __init__(self, username, password):
    #     self.username = username
    #     self.password = password
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)    

    def __repr__(self):
        return "A user with username : %s" % (self.username)
#################################################################################
# assignment (EL) and Assignment CO mapping
#all added
class assignment(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)    
    usn = db.Column(db.String(length=15), nullable=False)
    coursecode = db.Column(db.String(length=30), nullable=False)

    p1r1 = db.Column(db.Float(), default=0)
    p1r2 = db.Column(db.Float(), default=0)
    p1r3 = db.Column(db.Float(), default=0)
    p1r4 = db.Column(db.Float(), default=0)
    p1r5 = db.Column(db.Float(), default=0)
    p1r6 = db.Column(db.Float(), default=0)
    
    p2r1 = db.Column(db.Float(), default=0)
    p2r2 = db.Column(db.Float(), default=0)
    p2r3 = db.Column(db.Float(), default=0)
    p2r4 = db.Column(db.Float(), default=0)
    p2r5 = db.Column(db.Float(), default=0)
    p2r6 = db.Column(db.Float(), default=0)

    p3r1 = db.Column(db.Float(), default=0)
    p3r2 = db.Column(db.Float(), default=0)
    p3r3 = db.Column(db.Float(), default=0)
    p3r4 = db.Column(db.Float(), default=0)
    p3r5 = db.Column(db.Float(), default=0)
    p3r6 = db.Column(db.Float(), default=0)

    p4r1 = db.Column(db.Float(), default=0)
    p4r2 = db.Column(db.Float(), default=0)
    p4r3 = db.Column(db.Float(), default=0)
    p4r4 = db.Column(db.Float(), default=0)
    p4r5 = db.Column(db.Float(), default=0)
    p4r6 = db.Column(db.Float(), default=0)

    p5r1 = db.Column(db.Float(), default=0)
    p5r2 = db.Column(db.Float(), default=0)
    p5r3 = db.Column(db.Float(), default=0)
    p5r4 = db.Column(db.Float(), default=0)
    p5r5 = db.Column(db.Float(), default=0)
    p5r6 = db.Column(db.Float(), default=0)

    total_assignment_marks = db.Column(db.Float())    

    co1_marks = db.Column(db.Float(), default=0)
    co2_marks = db.Column(db.Float(), default=0)
    co3_marks = db.Column(db.Float(), default=0)
    co4_marks = db.Column(db.Float(), default=0)
    co5_marks = db.Column(db.Float(), default=0)
    co6_marks = db.Column(db.Float(), default=0)
    co7_marks = db.Column(db.Float(), default=0)
    co8_marks = db.Column(db.Float(), default=0)
    co9_marks = db.Column(db.Float(), default=0)
    co10_marks = db.Column(db.Float(), default=0)

    co1p = db.Column(db.Float(), default=0.0)  
    co2p = db.Column(db.Float(), default=0.0)  
    co3p = db.Column(db.Float(), default=0.0)  
    co4p = db.Column(db.Float(), default=0.0)  
    co5p = db.Column(db.Float(), default=0.0)  
    co6p = db.Column(db.Float(), default=0.0)  
    co7p = db.Column(db.Float(), default=0.0)  
    co8p = db.Column(db.Float(), default=0.0)  
    co9p = db.Column(db.Float(), default=0.0)  
    co10p = db.Column(db.Float(), default=0.0)    

    def __repr__(self):
        return "The assignment CO table"


class assignment_mapping(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)       
    coursecode = db.Column(db.String(length=30), nullable=False) 
    num_ph = db.Column(db.Integer(), nullable=False)   

    p1r1 = db.Column(db.Integer(), default=0)    
    p1r2 = db.Column(db.Integer(), default=0)
    p1r3 = db.Column(db.Integer(), default=0)
    p1r4 = db.Column(db.Integer(), default=0)
    p1r5 = db.Column(db.Integer(), default=0)
    p1r6 = db.Column(db.Integer(), default=0)
    p1r1m = db.Column(db.Float(), default=0)
    p1r2m = db.Column(db.Float(), default=0)
    p1r3m = db.Column(db.Float(), default=0)
    p1r4m = db.Column(db.Float(), default=0)
    p1r5m = db.Column(db.Float(), default=0)
    p1r6m = db.Column(db.Float(), default=0) 
    p1r1_bt = db.Column(db.Integer(), default=0) 
    p1r2_bt = db.Column(db.Integer(), default=0) 
    p1r3_bt = db.Column(db.Integer(), default=0) 
    p1r4_bt = db.Column(db.Integer(), default=0) 
    p1r5_bt = db.Column(db.Integer(), default=0) 
    p1r6_bt = db.Column(db.Integer(), default=0) 
    

    p2r1 = db.Column(db.Integer(), default=0)
    p2r2 = db.Column(db.Integer(), default=0)
    p2r3 = db.Column(db.Integer(), default=0)
    p2r4 = db.Column(db.Integer(), default=0)
    p2r5 = db.Column(db.Integer(), default=0)
    p2r6 = db.Column(db.Integer(), default=0)
    p2r1m = db.Column(db.Float(), default=0)
    p2r2m = db.Column(db.Float(), default=0)
    p2r3m = db.Column(db.Float(), default=0)
    p2r4m = db.Column(db.Float(), default=0)
    p2r5m = db.Column(db.Float(), default=0)
    p2r6m = db.Column(db.Float(), default=0)
    p2r1_bt = db.Column(db.Integer(), default=0) 
    p2r2_bt = db.Column(db.Integer(), default=0) 
    p2r3_bt = db.Column(db.Integer(), default=0) 
    p2r4_bt = db.Column(db.Integer(), default=0) 
    p2r5_bt = db.Column(db.Integer(), default=0) 
    p2r6_bt = db.Column(db.Integer(), default=0) 

    p3r1 = db.Column(db.Integer(), default=0)
    p3r2 = db.Column(db.Integer(), default=0)
    p3r3 = db.Column(db.Integer(), default=0)
    p3r4 = db.Column(db.Integer(), default=0)
    p3r5 = db.Column(db.Integer(), default=0)
    p3r6 = db.Column(db.Integer(), default=0) 
    p3r1m = db.Column(db.Float(), default=0)
    p3r2m = db.Column(db.Float(), default=0)
    p3r3m = db.Column(db.Float(), default=0)
    p3r4m = db.Column(db.Float(), default=0)
    p3r5m = db.Column(db.Float(), default=0)
    p3r6m = db.Column(db.Float(), default=0)
    p3r1_bt = db.Column(db.Integer(), default=0) 
    p3r2_bt = db.Column(db.Integer(), default=0) 
    p3r3_bt = db.Column(db.Integer(), default=0) 
    p3r4_bt = db.Column(db.Integer(), default=0) 
    p3r5_bt = db.Column(db.Integer(), default=0) 
    p3r6_bt = db.Column(db.Integer(), default=0) 
    
    p4r1 = db.Column(db.Integer(), default=0)
    p4r2 = db.Column(db.Integer(), default=0)
    p4r3 = db.Column(db.Integer(), default=0)
    p4r4 = db.Column(db.Integer(), default=0)
    p4r5 = db.Column(db.Integer(), default=0)
    p4r6 = db.Column(db.Integer(), default=0)
    p4r1m = db.Column(db.Float(), default=0)
    p4r2m = db.Column(db.Float(), default=0)
    p4r3m = db.Column(db.Float(), default=0)
    p4r4m = db.Column(db.Float(), default=0)
    p4r5m = db.Column(db.Float(), default=0)
    p4r6m = db.Column(db.Float(), default=0)
    p4r1_bt = db.Column(db.Integer(), default=0) 
    p4r2_bt = db.Column(db.Integer(), default=0) 
    p4r3_bt = db.Column(db.Integer(), default=0) 
    p4r4_bt = db.Column(db.Integer(), default=0) 
    p4r5_bt = db.Column(db.Integer(), default=0) 
    p4r6_bt = db.Column(db.Integer(), default=0) 
    
    p5r1 = db.Column(db.Integer(), default=0)
    p5r2 = db.Column(db.Integer(), default=0)
    p5r3 = db.Column(db.Integer(), default=0)
    p5r4 = db.Column(db.Integer(), default=0)
    p5r5 = db.Column(db.Integer(), default=0)
    p5r6 = db.Column(db.Integer(), default=0)
    p5r1m = db.Column(db.Float(), default=0)
    p5r2m = db.Column(db.Float(), default=0)
    p5r3m = db.Column(db.Float(), default=0)
    p5r4m = db.Column(db.Float(), default=0)
    p5r5m = db.Column(db.Float(), default=0)
    p5r6m = db.Column(db.Float(), default=0)
    p5r1_bt = db.Column(db.Integer(), default=0) 
    p5r2_bt = db.Column(db.Integer(), default=0) 
    p5r3_bt = db.Column(db.Integer(), default=0) 
    p5r4_bt = db.Column(db.Integer(), default=0) 
    p5r5_bt = db.Column(db.Integer(), default=0) 
    p5r6_bt = db.Column(db.Integer(), default=0) 
    
    max_assignment_marks = db.Column(db.Float(), default=0)

    total_co1_marks = db.Column(db.Float(), default = null)
    total_co2_marks = db.Column(db.Float(), default = null)
    total_co3_marks = db.Column(db.Float(), default = null)
    total_co4_marks = db.Column(db.Float(), default = null)
    total_co5_marks = db.Column(db.Float(), default = null)
    total_co6_marks = db.Column(db.Float(), default = null)
    total_co7_marks = db.Column(db.Float(), default = null)
    total_co8_marks = db.Column(db.Float(), default = null)
    total_co9_marks = db.Column(db.Float(), default = null)
    total_co10_marks = db.Column(db.Float(), default = null)

    def __repr__(self):
        return "Assignment(EL) mapping table"

#################################################################################
#Internal Quiz co mapping and marks tables
#all added
class quiz1_mapping(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)       
    coursecode = db.Column(db.String(length=30), nullable=False)

    version = db.Column(db.String(length=10), default=null)

    q1 = db.Column(db.Integer(), default=null)
    q2 = db.Column(db.Integer(), default=null)
    q3 = db.Column(db.Integer(), default=null)
    q4 = db.Column(db.Integer(), default=null)
    q5 = db.Column(db.Integer(), default=null)
    q6 = db.Column(db.Integer(), default=null)
    q7 = db.Column(db.Integer(), default=null)
    q8 = db.Column(db.Integer(), default=null)
    q9 = db.Column(db.Integer(), default=null)
    q10 = db.Column(db.Integer(), default=null)
    q11 = db.Column(db.Integer(), default=null)
    q12 = db.Column(db.Integer(), default=null)
    q13 = db.Column(db.Integer(), default=null)
    q14 = db.Column(db.Integer(), default=null)
    q15 = db.Column(db.Integer(), default=null)
    
    q1_bt = db.Column(db.Integer(), default=null)
    q2_bt = db.Column(db.Integer(), default=null)
    q3_bt = db.Column(db.Integer(), default=null)
    q4_bt = db.Column(db.Integer(), default=null)
    q5_bt = db.Column(db.Integer(), default=null)
    q6_bt = db.Column(db.Integer(), default=null)
    q7_bt = db.Column(db.Integer(), default=null)
    q8_bt = db.Column(db.Integer(), default=null)
    q9_bt = db.Column(db.Integer(), default=null)
    q10_bt = db.Column(db.Integer(), default=null)
    q11_bt = db.Column(db.Integer(), default=null)
    q12_bt = db.Column(db.Integer(), default=null)
    q13_bt = db.Column(db.Integer(), default=null)
    q14_bt = db.Column(db.Integer(), default=null)
    q15_bt = db.Column(db.Integer(), default=null)

    q1m = db.Column(db.Float(), default=null)
    q2m = db.Column(db.Float(), default=null)
    q3m = db.Column(db.Float(), default=null)
    q4m = db.Column(db.Float(), default=null)
    q5m = db.Column(db.Float(), default=null)
    q6m = db.Column(db.Float(), default=null)
    q7m = db.Column(db.Float(), default=null)
    q8m = db.Column(db.Float(), default=null)
    q9m = db.Column(db.Float(), default=null)
    q10m = db.Column(db.Float(), default=null)
    q11m = db.Column(db.Float(), default=null)
    q12m = db.Column(db.Float(), default=null)
    q13m = db.Column(db.Float(), default=null)
    q14m = db.Column(db.Float(), default=null)
    q15m = db.Column(db.Float(), default=null)

    total_co1_marks = db.Column(db.Float(), default = null)
    total_co2_marks = db.Column(db.Float(), default = null)
    total_co3_marks = db.Column(db.Float(), default = null)
    total_co4_marks = db.Column(db.Float(), default = null)
    total_co5_marks = db.Column(db.Float(), default = null)
    total_co6_marks = db.Column(db.Float(), default = null)
    total_co7_marks = db.Column(db.Float(), default = null)
    total_co8_marks = db.Column(db.Float(), default = null)
    total_co9_marks = db.Column(db.Float(), default = null)
    total_co10_marks = db.Column(db.Float(), default = null)

class quiz2_mapping(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)       
    coursecode = db.Column(db.String(length=30), nullable=False)

    version = db.Column(db.String(length=10), default=null)

    q1 = db.Column(db.Integer(), default=null)
    q2 = db.Column(db.Integer(), default=null)
    q3 = db.Column(db.Integer(), default=null)
    q4 = db.Column(db.Integer(), default=null)
    q5 = db.Column(db.Integer(), default=null)
    q6 = db.Column(db.Integer(), default=null)
    q7 = db.Column(db.Integer(), default=null)
    q8 = db.Column(db.Integer(), default=null)
    q9 = db.Column(db.Integer(), default=null)
    q10 = db.Column(db.Integer(), default=null)
    q11 = db.Column(db.Integer(), default=null)
    q12 = db.Column(db.Integer(), default=null)
    q13 = db.Column(db.Integer(), default=null)
    q14 = db.Column(db.Integer(), default=null)
    q15 = db.Column(db.Integer(), default=null)
    
    q1_bt = db.Column(db.Integer(), default=null)
    q2_bt = db.Column(db.Integer(), default=null)
    q3_bt = db.Column(db.Integer(), default=null)
    q4_bt = db.Column(db.Integer(), default=null)
    q5_bt = db.Column(db.Integer(), default=null)
    q6_bt = db.Column(db.Integer(), default=null)
    q7_bt = db.Column(db.Integer(), default=null)
    q8_bt = db.Column(db.Integer(), default=null)
    q9_bt = db.Column(db.Integer(), default=null)
    q10_bt = db.Column(db.Integer(), default=null)
    q11_bt = db.Column(db.Integer(), default=null)
    q12_bt = db.Column(db.Integer(), default=null)
    q13_bt = db.Column(db.Integer(), default=null)
    q14_bt = db.Column(db.Integer(), default=null)
    q15_bt = db.Column(db.Integer(), default=null)

    q1m = db.Column(db.Float(), default=null)
    q2m = db.Column(db.Float(), default=null)
    q3m = db.Column(db.Float(), default=null)
    q4m = db.Column(db.Float(), default=null)
    q5m = db.Column(db.Float(), default=null)
    q6m = db.Column(db.Float(), default=null)
    q7m = db.Column(db.Float(), default=null)
    q8m = db.Column(db.Float(), default=null)
    q9m = db.Column(db.Float(), default=null)
    q10m = db.Column(db.Float(), default=null)
    q11m = db.Column(db.Float(), default=null)
    q12m = db.Column(db.Float(), default=null)
    q13m = db.Column(db.Float(), default=null)
    q14m = db.Column(db.Float(), default=null)
    q15m = db.Column(db.Float(), default=null)

    total_co1_marks = db.Column(db.Float(), default = null)
    total_co2_marks = db.Column(db.Float(), default = null)
    total_co3_marks = db.Column(db.Float(), default = null)
    total_co4_marks = db.Column(db.Float(), default = null)
    total_co5_marks = db.Column(db.Float(), default = null)
    total_co6_marks = db.Column(db.Float(), default = null)
    total_co7_marks = db.Column(db.Float(), default = null)
    total_co8_marks = db.Column(db.Float(), default = null)
    total_co9_marks = db.Column(db.Float(), default = null)
    total_co10_marks = db.Column(db.Float(), default = null)  

    def __repr__(self):
        return "CO Mapping for Quiz 2"

class quiz3_mapping(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)       
    coursecode = db.Column(db.String(length=30), nullable=False)

    version = db.Column(db.String(length=10), default=null)

    q1 = db.Column(db.Integer(), default=null)
    q2 = db.Column(db.Integer(), default=null)
    q3 = db.Column(db.Integer(), default=null)
    q4 = db.Column(db.Integer(), default=null)
    q5 = db.Column(db.Integer(), default=null)
    q6 = db.Column(db.Integer(), default=null)
    q7 = db.Column(db.Integer(), default=null)
    q8 = db.Column(db.Integer(), default=null)
    q9 = db.Column(db.Integer(), default=null)
    q10 = db.Column(db.Integer(), default=null)
    q11 = db.Column(db.Integer(), default=null)
    q12 = db.Column(db.Integer(), default=null)
    q13 = db.Column(db.Integer(), default=null)
    q14 = db.Column(db.Integer(), default=null)
    q15 = db.Column(db.Integer(), default=null)
    
    q1_bt = db.Column(db.Integer(), default=null)
    q2_bt = db.Column(db.Integer(), default=null)
    q3_bt = db.Column(db.Integer(), default=null)
    q4_bt = db.Column(db.Integer(), default=null)
    q5_bt = db.Column(db.Integer(), default=null)
    q6_bt = db.Column(db.Integer(), default=null)
    q7_bt = db.Column(db.Integer(), default=null)
    q8_bt = db.Column(db.Integer(), default=null)
    q9_bt = db.Column(db.Integer(), default=null)
    q10_bt = db.Column(db.Integer(), default=null)
    q11_bt = db.Column(db.Integer(), default=null)
    q12_bt = db.Column(db.Integer(), default=null)
    q13_bt = db.Column(db.Integer(), default=null)
    q14_bt = db.Column(db.Integer(), default=null)
    q15_bt = db.Column(db.Integer(), default=null)

    q1m = db.Column(db.Float(), default=null)
    q2m = db.Column(db.Float(), default=null)
    q3m = db.Column(db.Float(), default=null)
    q4m = db.Column(db.Float(), default=null)
    q5m = db.Column(db.Float(), default=null)
    q6m = db.Column(db.Float(), default=null)
    q7m = db.Column(db.Float(), default=null)
    q8m = db.Column(db.Float(), default=null)
    q9m = db.Column(db.Float(), default=null)
    q10m = db.Column(db.Float(), default=null)
    q11m = db.Column(db.Float(), default=null)
    q12m = db.Column(db.Float(), default=null)
    q13m = db.Column(db.Float(), default=null)
    q14m = db.Column(db.Float(), default=null)
    q15m = db.Column(db.Float(), default=null)

    total_co1_marks = db.Column(db.Float(), default = null)
    total_co2_marks = db.Column(db.Float(), default = null)
    total_co3_marks = db.Column(db.Float(), default = null)
    total_co4_marks = db.Column(db.Float(), default = null)
    total_co5_marks = db.Column(db.Float(), default = null)
    total_co6_marks = db.Column(db.Float(), default = null)
    total_co7_marks = db.Column(db.Float(), default = null)
    total_co8_marks = db.Column(db.Float(), default = null)
    total_co9_marks = db.Column(db.Float(), default = null)
    total_co10_marks = db.Column(db.Float(), default = null)

    def __repr__(self):
        return "CO Mapping for Quiz 3"

class quiz1(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)    
    usn = db.Column(db.String(length=15), nullable=False)
    coursecode = db.Column(db.String(length=30), nullable=False)

    version = db.Column(db.String(length=3), default=null)

    q1 = db.Column(db.Float(), default=null)
    q2 = db.Column(db.Float(), default=null)
    q3 = db.Column(db.Float(), default=null)
    q4 = db.Column(db.Float(), default=null)
    q5 = db.Column(db.Float(), default=null)
    q6 = db.Column(db.Float(), default=null)
    q7 = db.Column(db.Float(), default=null)
    q8 = db.Column(db.Float(), default=null)
    q9 = db.Column(db.Float(), default=null)
    q10 = db.Column(db.Float(), default=null)
    q11 = db.Column(db.Float(), default=null)
    q12 = db.Column(db.Float(), default=null)
    q13 = db.Column(db.Float(), default=null)
    q14 = db.Column(db.Float(), default=null)
    q15 = db.Column(db.Float(), default=null)    

    marks_q = db.Column(db.Float(), default=null)

    co1_marks = db.Column(db.Float(), default=null)
    co2_marks = db.Column(db.Float(), default=null)
    co3_marks = db.Column(db.Float(), default=null)
    co4_marks = db.Column(db.Float(), default=null)
    co5_marks = db.Column(db.Float(), default=null)
    co6_marks = db.Column(db.Float(), default=null)
    co7_marks = db.Column(db.Float(), default=null)
    co8_marks = db.Column(db.Float(), default=null)
    co9_marks = db.Column(db.Float(), default=null)
    co10_marks = db.Column(db.Float(), default=null)

    def __repr__(self):
        return "The Quiz 1 marks obtained by students"

class quiz2(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)    
    usn = db.Column(db.String(length=15), nullable=False)
    coursecode = db.Column(db.String(length=30), nullable=False)

    version = db.Column(db.String(length=3), default=null)

    q1 = db.Column(db.Float(), default=null)
    q2 = db.Column(db.Float(), default=null)
    q3 = db.Column(db.Float(), default=null)
    q4 = db.Column(db.Float(), default=null)
    q5 = db.Column(db.Float(), default=null)
    q6 = db.Column(db.Float(), default=null)
    q7 = db.Column(db.Float(), default=null)
    q8 = db.Column(db.Float(), default=null)
    q9 = db.Column(db.Float(), default=null)
    q10 = db.Column(db.Float(), default=null)
    q11 = db.Column(db.Float(), default=null)
    q12 = db.Column(db.Float(), default=null)
    q13 = db.Column(db.Float(), default=null)
    q14 = db.Column(db.Float(), default=null)
    q15 = db.Column(db.Float(), default=null)

    marks_q = db.Column(db.Float(), default=null)

    co1_marks = db.Column(db.Float(), default=null)
    co2_marks = db.Column(db.Float(), default=null)
    co3_marks = db.Column(db.Float(), default=null)
    co4_marks = db.Column(db.Float(), default=null)
    co5_marks = db.Column(db.Float(), default=null)
    co6_marks = db.Column(db.Float(), default=null)
    co7_marks = db.Column(db.Float(), default=null)
    co8_marks = db.Column(db.Float(), default=null)
    co9_marks = db.Column(db.Float(), default=null)
    co10_marks = db.Column(db.Float(), default=null)

    def __repr__(self):
        return "The Quiz 2 marks obtained by students"

class quiz3(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)    
    usn = db.Column(db.String(length=15), nullable=False)
    coursecode = db.Column(db.String(length=30), nullable=False)

    version = db.Column(db.String(length=3), default=null)

    q1 = db.Column(db.Float(), default=null)
    q2 = db.Column(db.Float(), default=null)
    q3 = db.Column(db.Float(), default=null)
    q4 = db.Column(db.Float(), default=null)
    q5 = db.Column(db.Float(), default=null)
    q6 = db.Column(db.Float(), default=null)
    q7 = db.Column(db.Float(), default=null)
    q8 = db.Column(db.Float(), default=null)
    q9 = db.Column(db.Float(), default=null)
    q10 = db.Column(db.Float(), default=null)
    q11 = db.Column(db.Float(), default=null)
    q12 = db.Column(db.Float(), default=null)
    q13 = db.Column(db.Float(), default=null)
    q14 = db.Column(db.Float(), default=null)
    q15 = db.Column(db.Float(), default=null)

    marks_q = db.Column(db.Float(), default=null)

    co1_marks = db.Column(db.Float(), default=null)
    co2_marks = db.Column(db.Float(), default=null)
    co3_marks = db.Column(db.Float(), default=null)
    co4_marks = db.Column(db.Float(), default=null)
    co5_marks = db.Column(db.Float(), default=null)
    co6_marks = db.Column(db.Float(), default=null)
    co7_marks = db.Column(db.Float(), default=null)
    co8_marks = db.Column(db.Float(), default=null)
    co9_marks = db.Column(db.Float(), default=null)
    co10_marks = db.Column(db.Float(), default=null)

    def __repr__(self):
        return "The Quiz 3 marks obtained by students"

#################################################################################


#################################################################################
#CIE co mapping and marks tables
#all added
class test1_mapping(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)        
    coursecode = db.Column(db.String(length=30), nullable=False)

    q1a = db.Column(db.Integer(), default=null)
    q1b = db.Column(db.Integer(), default=null)
    q1c = db.Column(db.Integer(), default=null)

    q2a = db.Column(db.Integer(), default=null)
    q2b = db.Column(db.Integer(), default=null)
    q2c = db.Column(db.Integer(), default=null)

    q3a = db.Column(db.Integer(), default=null)
    q3b = db.Column(db.Integer(), default=null)
    q3c = db.Column(db.Integer(), default=null)

    q4a = db.Column(db.Integer(), default=null)
    q4b = db.Column(db.Integer(), default=null)
    q4c = db.Column(db.Integer(), default=null)

    q5a = db.Column(db.Integer(), default=null)
    q5b = db.Column(db.Integer(), default=null)
    q5c = db.Column(db.Integer(), default=null)
    
    q1a_bt = db.Column(db.Integer(), default=null)
    q1b_bt = db.Column(db.Integer(), default=null)
    q1c_bt = db.Column(db.Integer(), default=null)

    q2a_bt = db.Column(db.Integer(), default=null)
    q2b_bt = db.Column(db.Integer(), default=null)
    q2c_bt = db.Column(db.Integer(), default=null)

    q3a_bt = db.Column(db.Integer(), default=null)
    q3b_bt = db.Column(db.Integer(), default=null)
    q3c_bt = db.Column(db.Integer(), default=null)

    q4a_bt = db.Column(db.Integer(), default=null)
    q4b_bt = db.Column(db.Integer(), default=null)
    q4c_bt = db.Column(db.Integer(), default=null)

    q5a_bt = db.Column(db.Integer(), default=null)
    q5b_bt = db.Column(db.Integer(), default=null)
    q5c_bt = db.Column(db.Integer(), default=null)

    q1am = db.Column(db.Float(), default = null)
    q1bm = db.Column(db.Float(), default = null)
    q1cm = db.Column(db.Float(), default = null)

    q2am = db.Column(db.Float(), default = null)
    q2bm = db.Column(db.Float(), default = null)
    q2cm = db.Column(db.Float(), default = null)

    q3am = db.Column(db.Float(), default = null)
    q3bm = db.Column(db.Float(), default = null)
    q3cm = db.Column(db.Float(), default = null)

    q4am = db.Column(db.Float(), default = null)
    q4bm = db.Column(db.Float(), default = null)
    q4cm = db.Column(db.Float(), default = null)

    q5am = db.Column(db.Float(), default = null)
    q5bm = db.Column(db.Float(), default = null)
    q5cm = db.Column(db.Float(), default = null)

    total_co1_marks = db.Column(db.Float(), default = null)
    total_co2_marks = db.Column(db.Float(), default = null)
    total_co3_marks = db.Column(db.Float(), default = null)
    total_co4_marks = db.Column(db.Float(), default = null)
    total_co5_marks = db.Column(db.Float(), default = null)
    total_co6_marks = db.Column(db.Float(), default = null)
    total_co7_marks = db.Column(db.Float(), default = null)
    total_co8_marks = db.Column(db.Float(), default = null)
    total_co9_marks = db.Column(db.Float(), default = null)
    total_co10_marks = db.Column(db.Float(), default = null)

    def __repr__(self):
        return "CIE 1 mapping table with CO's"

class test2_mapping(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)        
    coursecode = db.Column(db.String(length=30), nullable=False)

    q1a = db.Column(db.Integer(), default=null)
    q1b = db.Column(db.Integer(), default=null)
    q1c = db.Column(db.Integer(), default=null)

    q2a = db.Column(db.Integer(), default=null)
    q2b = db.Column(db.Integer(), default=null)
    q2c = db.Column(db.Integer(), default=null)

    q3a = db.Column(db.Integer(), default=null)
    q3b = db.Column(db.Integer(), default=null)
    q3c = db.Column(db.Integer(), default=null)

    q4a = db.Column(db.Integer(), default=null)
    q4b = db.Column(db.Integer(), default=null)
    q4c = db.Column(db.Integer(), default=null)

    q5a = db.Column(db.Integer(), default=null)
    q5b = db.Column(db.Integer(), default=null)
    q5c = db.Column(db.Integer(), default=null)
    
    q1a_bt = db.Column(db.Integer(), default=null)
    q1b_bt = db.Column(db.Integer(), default=null)
    q1c_bt = db.Column(db.Integer(), default=null)

    q2a_bt = db.Column(db.Integer(), default=null)
    q2b_bt = db.Column(db.Integer(), default=null)
    q2c_bt = db.Column(db.Integer(), default=null)

    q3a_bt = db.Column(db.Integer(), default=null)
    q3b_bt = db.Column(db.Integer(), default=null)
    q3c_bt = db.Column(db.Integer(), default=null)

    q4a_bt = db.Column(db.Integer(), default=null)
    q4b_bt = db.Column(db.Integer(), default=null)
    q4c_bt = db.Column(db.Integer(), default=null)

    q5a_bt = db.Column(db.Integer(), default=null)
    q5b_bt = db.Column(db.Integer(), default=null)
    q5c_bt = db.Column(db.Integer(), default=null)

    q1am = db.Column(db.Float(), default = null)
    q1bm = db.Column(db.Float(), default = null)
    q1cm = db.Column(db.Float(), default = null)

    q2am = db.Column(db.Float(), default = null)
    q2bm = db.Column(db.Float(), default = null)
    q2cm = db.Column(db.Float(), default = null)

    q3am = db.Column(db.Float(), default = null)
    q3bm = db.Column(db.Float(), default = null)
    q3cm = db.Column(db.Float(), default = null)

    q4am = db.Column(db.Float(), default = null)
    q4bm = db.Column(db.Float(), default = null)
    q4cm = db.Column(db.Float(), default = null)

    q5am = db.Column(db.Float(), default = null)
    q5bm = db.Column(db.Float(), default = null)
    q5cm = db.Column(db.Float(), default = null)

    total_co1_marks = db.Column(db.Float(), default = null)
    total_co2_marks = db.Column(db.Float(), default = null)
    total_co3_marks = db.Column(db.Float(), default = null)
    total_co4_marks = db.Column(db.Float(), default = null)
    total_co5_marks = db.Column(db.Float(), default = null)
    total_co6_marks = db.Column(db.Float(), default = null)
    total_co7_marks = db.Column(db.Float(), default = null)
    total_co8_marks = db.Column(db.Float(), default = null)
    total_co9_marks = db.Column(db.Float(), default = null)
    total_co10_marks = db.Column(db.Float(), default = null)

    def __repr__(self):
        return "CIE 2 mapping table with CO's"

class test3_mapping(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)        
    coursecode = db.Column(db.String(length=30), nullable=False)

    q1a = db.Column(db.Integer(), default=null)
    q1b = db.Column(db.Integer(), default=null)
    q1c = db.Column(db.Integer(), default=null)

    q2a = db.Column(db.Integer(), default=null)
    q2b = db.Column(db.Integer(), default=null)
    q2c = db.Column(db.Integer(), default=null)

    q3a = db.Column(db.Integer(), default=null)
    q3b = db.Column(db.Integer(), default=null)
    q3c = db.Column(db.Integer(), default=null)

    q4a = db.Column(db.Integer(), default=null)
    q4b = db.Column(db.Integer(), default=null)
    q4c = db.Column(db.Integer(), default=null)

    q5a = db.Column(db.Integer(), default=null)
    q5b = db.Column(db.Integer(), default=null)
    q5c = db.Column(db.Integer(), default=null)
    
    q1a_bt = db.Column(db.Integer(), default=null)
    q1b_bt = db.Column(db.Integer(), default=null)
    q1c_bt = db.Column(db.Integer(), default=null)

    q2a_bt = db.Column(db.Integer(), default=null)
    q2b_bt = db.Column(db.Integer(), default=null)
    q2c_bt = db.Column(db.Integer(), default=null)

    q3a_bt = db.Column(db.Integer(), default=null)
    q3b_bt = db.Column(db.Integer(), default=null)
    q3c_bt = db.Column(db.Integer(), default=null)

    q4a_bt = db.Column(db.Integer(), default=null)
    q4b_bt = db.Column(db.Integer(), default=null)
    q4c_bt = db.Column(db.Integer(), default=null)

    q5a_bt = db.Column(db.Integer(), default=null)
    q5b_bt = db.Column(db.Integer(), default=null)
    q5c_bt = db.Column(db.Integer(), default=null)

    q1am = db.Column(db.Float(), default = null)
    q1bm = db.Column(db.Float(), default = null)
    q1cm = db.Column(db.Float(), default = null)

    q2am = db.Column(db.Float(), default = null)
    q2bm = db.Column(db.Float(), default = null)
    q2cm = db.Column(db.Float(), default = null)

    q3am = db.Column(db.Float(), default = null)
    q3bm = db.Column(db.Float(), default = null)
    q3cm = db.Column(db.Float(), default = null)

    q4am = db.Column(db.Float(), default = null)
    q4bm = db.Column(db.Float(), default = null)
    q4cm = db.Column(db.Float(), default = null)

    q5am = db.Column(db.Float(), default = null)
    q5bm = db.Column(db.Float(), default = null)
    q5cm = db.Column(db.Float(), default = null)

    total_co1_marks = db.Column(db.Float(), default = null)
    total_co2_marks = db.Column(db.Float(), default = null)
    total_co3_marks = db.Column(db.Float(), default = null)
    total_co4_marks = db.Column(db.Float(), default = null)
    total_co5_marks = db.Column(db.Float(), default = null)
    total_co6_marks = db.Column(db.Float(), default = null)
    total_co7_marks = db.Column(db.Float(), default = null)
    total_co8_marks = db.Column(db.Float(), default = null)
    total_co9_marks = db.Column(db.Float(), default = null)
    total_co10_marks = db.Column(db.Float(), default = null)

    def __repr__(self):
        return "CIE 3 mapping table with CO's"

class test1(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)    
    usn = db.Column(db.String(length=15), nullable=False)
    coursecode = db.Column(db.String(length=30), nullable=False)

    q1a = db.Column(db.Float(), default=null)
    q1b = db.Column(db.Float(), default=null)
    q1c = db.Column(db.Float(), default=null)

    q2a = db.Column(db.Float(), default=null)
    q2b = db.Column(db.Float(), default=null)
    q2c = db.Column(db.Float(), default=null)

    q3a = db.Column(db.Float(), default=null)
    q3b = db.Column(db.Float(), default=null)
    q3c = db.Column(db.Float(), default=null)

    q4a = db.Column(db.Float(), default=null)
    q4b = db.Column(db.Float(), default=null)
    q4c = db.Column(db.Float(), default=null)

    q5a = db.Column(db.Float(), default=null)
    q5b = db.Column(db.Float(), default=null)
    q5c = db.Column(db.Float(), default=null)

    marks = db.Column(db.Float(), default=null)

    co1_marks = db.Column(db.Float(), default=null)
    co2_marks = db.Column(db.Float(), default=null)
    co3_marks = db.Column(db.Float(), default=null)
    co4_marks = db.Column(db.Float(), default=null)
    co5_marks = db.Column(db.Float(), default=null)
    co6_marks = db.Column(db.Float(), default=null)
    co7_marks = db.Column(db.Float(), default=null)
    co8_marks = db.Column(db.Float(), default=null)
    co9_marks = db.Column(db.Float(), default=null)
    co10_marks = db.Column(db.Float(), default=null)


    def __repr__(self):
        return "Marks obtained by students for the CIE 1 for a particular course"

class test2(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)    
    usn = db.Column(db.String(length=15), nullable=False)
    coursecode = db.Column(db.String(length=30), nullable=False)

    q1a = db.Column(db.Float(), default=null)
    q1b = db.Column(db.Float(), default=null)
    q1c = db.Column(db.Float(), default=null)

    q2a = db.Column(db.Float(), default=null)
    q2b = db.Column(db.Float(), default=null)
    q2c = db.Column(db.Float(), default=null)

    q3a = db.Column(db.Float(), default=null)
    q3b = db.Column(db.Float(), default=null)
    q3c = db.Column(db.Float(), default=null)

    q4a = db.Column(db.Float(), default=null)
    q4b = db.Column(db.Float(), default=null)
    q4c = db.Column(db.Float(), default=null)

    q5a = db.Column(db.Float(), default=null)
    q5b = db.Column(db.Float(), default=null)
    q5c = db.Column(db.Float(), default=null)

    marks = db.Column(db.Float(), default=null)

    co1_marks = db.Column(db.Float(), default=null)
    co2_marks = db.Column(db.Float(), default=null)
    co3_marks = db.Column(db.Float(), default=null)
    co4_marks = db.Column(db.Float(), default=null)
    co5_marks = db.Column(db.Float(), default=null)
    co6_marks = db.Column(db.Float(), default=null)
    co7_marks = db.Column(db.Float(), default=null)
    co8_marks = db.Column(db.Float(), default=null)
    co9_marks = db.Column(db.Float(), default=null)
    co10_marks = db.Column(db.Float(), default=null)

    def __repr__(self):
        return "Marks obtained by students for the CIE 2 for a particular course"

class test3(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)    
    usn = db.Column(db.String(length=15), nullable=False)
    coursecode = db.Column(db.String(length=30), nullable=False)

    q1a = db.Column(db.Float(), default=null)
    q1b = db.Column(db.Float(), default=null)
    q1c = db.Column(db.Float(), default=null)

    q2a = db.Column(db.Float(), default=null)
    q2b = db.Column(db.Float(), default=null)
    q2c = db.Column(db.Float(), default=null)

    q3a = db.Column(db.Float(), default=null)
    q3b = db.Column(db.Float(), default=null)
    q3c = db.Column(db.Float(), default=null)

    q4a = db.Column(db.Float(), default=null)
    q4b = db.Column(db.Float(), default=null)
    q4c = db.Column(db.Float(), default=null)

    q5a = db.Column(db.Float(), default=null)
    q5b = db.Column(db.Float(), default=null)
    q5c = db.Column(db.Float(), default=null)

    marks = db.Column(db.Float(), default=null)

    co1_marks = db.Column(db.Float(), default=null)
    co2_marks = db.Column(db.Float(), default=null)
    co3_marks = db.Column(db.Float(), default=null)
    co4_marks = db.Column(db.Float(), default=null)
    co5_marks = db.Column(db.Float(), default=null)
    co6_marks = db.Column(db.Float(), default=null)
    co7_marks = db.Column(db.Float(), default=null)
    co8_marks = db.Column(db.Float(), default=null)
    co9_marks = db.Column(db.Float(), default=null)
    co10_marks = db.Column(db.Float(), default=null)

    def __repr__(self):
        return "Marks obtained by students for the CIE 3 for a particular course"

#################################################################################

#added
class lab_co(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)    
    usn = db.Column(db.String(length=15), nullable=False)
    coursecode = db.Column(db.String(length=30), nullable=False)

    co1p = db.Column(db.Float(), default=0.0)
    co2p = db.Column(db.Float(), default=0.0)
    co3p = db.Column(db.Float(), default=0.0)
    co4p = db.Column(db.Float(), default=0.0)
    co5p = db.Column(db.Float(), default=0.0)
    co6p = db.Column(db.Float(), default=0.0)
    co7p = db.Column(db.Float(), default=0.0)
    co8p = db.Column(db.Float(), default=0.0)
    co9p = db.Column(db.Float(), default=0.0)
    co10p = db.Column(db.Float(), default=0.0)

    def __repr__(self):
        return "Marks obtained in various COs for lab component"
    

#################################################################################

class final_internal_co(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)    
    usn = db.Column(db.String(length=15), nullable=False)
    coursecode = db.Column(db.String(length=30), nullable=False)

    co1 = db.Column(db.Integer(), default=null)
    co2 = db.Column(db.Integer(), default=null)
    co3 = db.Column(db.Integer(), default=null)
    co4 = db.Column(db.Integer(), default=null)
    co5 = db.Column(db.Integer(), default=null)
    co6 = db.Column(db.Integer(), default=null)
    co7 = db.Column(db.Integer(), default=null)
    co8 = db.Column(db.Integer(), default=null)
    co9 = db.Column(db.Integer(), default=null)
    co10 = db.Column(db.Integer(), default=null)

    co1_m_obtained = db.Column(db.Float(), default=null)
    co2_m_obtained = db.Column(db.Float(), default=null)
    co3_m_obtained = db.Column(db.Float(), default=null)
    co4_m_obtained = db.Column(db.Float(), default=null)
    co5_m_obtained = db.Column(db.Float(), default=null)
    co6_m_obtained = db.Column(db.Float(), default=null)
    co7_m_obtained = db.Column(db.Float(), default=null)
    co8_m_obtained = db.Column(db.Float(), default=null)
    co9_m_obtained = db.Column(db.Float(), default=null)
    co10_m_obtained = db.Column(db.Float(), default=null)

    co1p = db.Column(db.Float(), default=null)
    co2p = db.Column(db.Float(), default=null)
    co3p = db.Column(db.Float(), default=null)
    co4p = db.Column(db.Float(), default=null)
    co5p = db.Column(db.Float(), default=null)
    co6p = db.Column(db.Float(), default=null)
    co7p = db.Column(db.Float(), default=null)
    co8p = db.Column(db.Float(), default=null)
    co9p = db.Column(db.Float(), default=null)
    co10p = db.Column(db.Float(), default=null)

    quiz1_total = db.Column(db.Float(), default=0.0)
    test1_total = db.Column(db.Float(), default=0.0)
    quiz2_total = db.Column(db.Float(), default=0.0)
    test2_total = db.Column(db.Float(), default=0.0)
    quiz3_total = db.Column(db.Float(), default=0.0)
    test3_total = db.Column(db.Float(), default=0.0)

    cie = db.Column(db.Float(), nullable=False)

    def __repr__(self):
        return "Gives final CIE marks of every student"

#################################################################################

class subject_co(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)      
    coursecode = db.Column(db.String(length=30), nullable=False)

    co1p = db.Column(db.Float())
    co2p = db.Column(db.Float())
    co3p = db.Column(db.Float())
    co4p = db.Column(db.Float())
    co5p = db.Column(db.Float())
    co6p = db.Column(db.Float())
    co7p = db.Column(db.Float())
    co8p = db.Column(db.Float())
    co9p = db.Column(db.Float())
    co10p = db.Column(db.Float())
    

    sco1p = db.Column(db.Float())
    sco2p = db.Column(db.Float())
    sco3p = db.Column(db.Float())
    sco4p = db.Column(db.Float())
    sco5p = db.Column(db.Float())
    sco6p = db.Column(db.Float())
    sco7p = db.Column(db.Float())
    sco8p = db.Column(db.Float())
    sco9p = db.Column(db.Float())
    sco10p = db.Column(db.Float())

    dico1p = db.Column(db.Float())
    dico2p = db.Column(db.Float())
    dico3p = db.Column(db.Float())
    dico4p = db.Column(db.Float())
    dico5p = db.Column(db.Float())
    dico6p = db.Column(db.Float())
    dico7p = db.Column(db.Float())
    dico8p = db.Column(db.Float())
    dico9p = db.Column(db.Float())
    dico10p = db.Column(db.Float())

    def __repr__(self):
        return "Subject CO Table"


class student_co(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)    
    usn = db.Column(db.String(length=15), nullable=False)
    coursecode = db.Column(db.String(length=30), nullable=False)

    co1p = db.Column(db.Float())
    co2p = db.Column(db.Float())
    co3p = db.Column(db.Float())
    co4p = db.Column(db.Float())
    co5p = db.Column(db.Float())
    co6p = db.Column(db.Float())
    co7p = db.Column(db.Float())
    co8p = db.Column(db.Float())
    co9p = db.Column(db.Float())
    co10p = db.Column(db.Float())

    internal_marks = db.Column(db.Float())
    internal_grade = db.Column(db.String(length=10))
    sem_end_grade = db.Column(db.String(length=10))
    equivalent_marks = db.Column(db.Float())
    sem_end_marks = db.Column(db.Float())

    sco1p = db.Column(db.Float())
    sco2p = db.Column(db.Float())
    sco3p = db.Column(db.Float())
    sco4p = db.Column(db.Float())
    sco5p = db.Column(db.Float())
    sco6p = db.Column(db.Float())
    sco7p = db.Column(db.Float())
    sco8p = db.Column(db.Float())
    sco9p = db.Column(db.Float())
    sco10p = db.Column(db.Float())

    dico1p = db.Column(db.Float())
    dico2p = db.Column(db.Float())
    dico3p = db.Column(db.Float())
    dico4p = db.Column(db.Float())
    dico5p = db.Column(db.Float())
    dico6p = db.Column(db.Float())
    dico7p = db.Column(db.Float())
    dico8p = db.Column(db.Float())
    dico9p = db.Column(db.Float())
    dico10p = db.Column(db.Float())

    avg_dico = db.Column(db.Float())

    def __repr__(self):
        return "Student CO Table"

class subject(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)    
    coursecode = db.Column(db.String(length=10), nullable=False)
    coursename = db.Column(db.String(length=50), nullable=False)
    courseabb = db.Column(db.String(length=20))
    department_id = db.Column(db.Integer())
    number_of_co = db.Column(db.Integer(), nullable=False)

    def __repr__(self):
        return "The table that stores all the courses and their necessary details"

class student(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    usn = db.Column(db.String(length=12), nullable=False)
    department = db.Column(db.String(length=10), nullable=False)
    semester = db.Column(db.Integer())
    name = db.Column(db.String(length=100), nullable=False)
    

    def __repr__(self):
        return "The table that stores all necessary details of the students."


class program_output(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)      
    coursecode = db.Column(db.String(length=30), nullable=False)

    po1 = db.Column(db.Float(), default=0.0)
    po2 = db.Column(db.Float(), default=0.0)
    po3 = db.Column(db.Float(), default=0.0)
    po4 = db.Column(db.Float(), default=0.0)
    po5 = db.Column(db.Float(), default=0.0)
    po6 = db.Column(db.Float(), default=0.0)
    po7 = db.Column(db.Float(), default=0.0)
    po8 = db.Column(db.Float(), default=0.0)
    po9 = db.Column(db.Float(), default=0.0)
    po10 = db.Column(db.Float(), default=0.0)
    po11 = db.Column(db.Float(), default=0.0)
    po12 = db.Column(db.Float(), default=0.0)
    po13 = db.Column(db.Float(), default=0.0)
    po14 = db.Column(db.Float(), default=0.0)
    po15 = db.Column(db.Float(), default=0.0)

    def __repr__(self):
        return "This table does POS"


class course(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)

    coursename = db.Column(db.String(length=50), nullable=False)
    coursecode = db.Column(db.String(length=20), nullable=False, unique=True)
    courseabb = db.Column(db.String(length=20))
    labyorn = db.Column(db.String(length=1), nullable=False, default="Y")
    numberco = db.Column(db.Integer(), nullable=False)
    semester = db.Column(db.Integer(), nullable=False)
    dicop = db.Column(db.Float(), nullable=False)
    scop = db.Column(db.Float(), nullable=False)
    internal_cie = db.Column(db.Float(), nullable=False)
    internal_assign = db.Column(db.Float(), nullable=False)
    internal_quiz = db.Column(db.Float(), nullable=False)
    level1 = db.Column(db.Float(), nullable=False)
    level2 = db.Column(db.Float(), nullable=False)
    level3 = db.Column(db.Float(), nullable=False)
    target = db.Column(db.Float(), nullable=False)   
    

    def __repr__(self):
        return "The table with Course names and number of co's per course"

class co_info(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    coursecode = db.Column(db.String(length=30), nullable=False)
    co_number = db.Column(db.Integer(), nullable=False)
    co_details = db.Column(db.String(length=800), nullable=False)   

class grade_marks(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    
    scheme = db.Column(db.Integer())
    max_marks = db.Column(db.Float(), nullable=False)
    min_marks = db.Column(db.Float(), nullable=False)
    alloted_grade = db.Column(db.String(length=2), nullable=False)
    gpoint = db.Column(db.Integer())
    
    def __repr__(self):
        return "Table for grade allotment"
    
    


class internal_co(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    usn = db.Column(db.String(length=12), nullable=False)
    coursecode = db.Column(db.String(length=30), nullable=False)

    quiz1 = db.Column(db.Float(), default=0)
    quiz2 = db.Column(db.Float(), default=0)
    quiz3 = db.Column(db.Float(), default=0)

    test1 = db.Column(db.Float(), default=0)
    test2 = db.Column(db.Float(), default=0)
    test3 = db.Column(db.Float(), default=0)

    co1 = db.Column(db.Float())
    co2 = db.Column(db.Float())
    co3 = db.Column(db.Float())
    co4 = db.Column(db.Float())
    co5 = db.Column(db.Float())
    co6 = db.Column(db.Float())
    co7 = db.Column(db.Float())
    co8 = db.Column(db.Float())
    co9 = db.Column(db.Float())
    co10 = db.Column(db.Float())

    co1_total_marks = db.Column(db.Float())
    co2_total_marks = db.Column(db.Float())
    co3_total_marks = db.Column(db.Float())
    co4_total_marks = db.Column(db.Float())
    co5_total_marks = db.Column(db.Float())
    co6_total_marks = db.Column(db.Float())
    co7_total_marks = db.Column(db.Float())
    co8_total_marks = db.Column(db.Float())
    co9_total_marks = db.Column(db.Float())
    co10_total_marks = db.Column(db.Float())

    co1p = db.Column(db.Float())
    co2p = db.Column(db.Float())
    co3p = db.Column(db.Float())
    co4p = db.Column(db.Float())
    co5p = db.Column(db.Float())
    co6p = db.Column(db.Float())
    co7p = db.Column(db.Float())
    co8p = db.Column(db.Float())
    co9p = db.Column(db.Float())
    co10p = db.Column(db.Float())
    
    final_cie = db.Column(db.Float())

    def __repr__(self):
        return "The final Internal CIE table"


class staffid_cc(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    staffid = db.Column(db.Integer(), nullable=False)
    coursecode = db.Column(db.String(length=20), nullable=False)
    usn_list = db.Column(db.String(length=2000), nullable=False)
    semester = db.Column(db.Integer(), nullable=False)

    def __repr__(self):
        return "Staff ID mapped with student USN"


class courseend_survey(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    coursecode = db.Column(db.String(length=20), nullable=False)
    co1p = db.Column(db.Float(), default=0.0)
    co2p = db.Column(db.Float(), default=0.0)
    co3p = db.Column(db.Float(), default=0.0)
    co4p = db.Column(db.Float(), default=0.0)
    co5p = db.Column(db.Float(), default=0.0)
    co6p = db.Column(db.Float(), default=0.0)
    co7p = db.Column(db.Float(), default=0.0)
    co8p = db.Column(db.Float(), default=0.0)
    co9p = db.Column(db.Float(), default=0.0)
    co10p = db.Column(db.Float(), default=0.0)

    def __repr__(self):
        return "The table that contains course end survey percentages."


class talk(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    coursecode = db.Column(db.String(length=20), nullable=False)
    usn = db.Column(db.String(length=15), nullable=False)
    co1p = db.Column(db.Float(), default=0.0)
    co2p = db.Column(db.Float(), default=0.0)
    co3p = db.Column(db.Float(), default=0.0)
    co4p = db.Column(db.Float(), default=0.0)
    co5p = db.Column(db.Float(), default=0.0)
    co6p = db.Column(db.Float(), default=0.0)
    co7p = db.Column(db.Float(), default=0.0)
    co8p = db.Column(db.Float(), default=0.0)
    co9p = db.Column(db.Float(), default=0.0)
    co10p = db.Column(db.Float(), default=0.0)

    def __repr__(self):
        return "The table that contains extra activities like talks co percentages."

# level access is used to store the average of avg_dico of all students, and calculate the level
class level(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    coursecode = db.Column(db.String(length=20), nullable=False)    
    
    avg_cie = db.Column(db.Float())
    cie_level = db.Column(db.Integer())
    avg_see = db.Column(db.Float())
    see_level = db.Column(db.Float())
    final_direct_level = db.Column(db.Float())
    
    avg_indirect = db.Column(db.Float())
    indirect_level = db.Column(db.Integer())
    
    final_level = db.Column(db.Float())
    
    
class threshold(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    usn = db.Column(db.String(length=15), nullable=False)
    coursecode = db.Column(db.String(length=30), nullable=False)
    
    co1p = db.Column(db.String(length=1))
    co2p = db.Column(db.String(length=1))
    co3p = db.Column(db.String(length=1))
    co4p = db.Column(db.String(length=1))
    co5p = db.Column(db.String(length=1))
    co6p = db.Column(db.String(length=1))
    co7p = db.Column(db.String(length=1))
    co8p = db.Column(db.String(length=1))
    co9p = db.Column(db.String(length=1))
    co10p = db.Column(db.String(length=1))
    

class po_mapping(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    coursecode = db.Column(db.String(length=20), nullable=False)  
    po1 = db.Column(db.Float())
    po2 = db.Column(db.Float())
    po3 = db.Column(db.Float())
    po4 = db.Column(db.Float())
    po5 = db.Column(db.Float())
    po6 = db.Column(db.Float())
    po7 = db.Column(db.Float())
    po8 = db.Column(db.Float())
    po9 = db.Column(db.Float())
    po10 = db.Column(db.Float())
    po11 = db.Column(db.Float())
    po12 = db.Column(db.Float())
    pso1 = db.Column(db.Float())
    pso2 = db.Column(db.Float())

class po_attainment(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    batch = db.Column(db.Integer())
    po1 = db.Column(db.Float())
    po2 = db.Column(db.Float())
    po3 = db.Column(db.Float())
    po4 = db.Column(db.Float())
    po5 = db.Column(db.Float())
    po6 = db.Column(db.Float())
    po7 = db.Column(db.Float())
    po8 = db.Column(db.Float())
    po9 = db.Column(db.Float())
    po10 = db.Column(db.Float())
    po11 = db.Column(db.Float())
    po12 = db.Column(db.Float())
    pso1 = db.Column(db.Float())
    pso2 = db.Column(db.Float())
    
    
    
    


