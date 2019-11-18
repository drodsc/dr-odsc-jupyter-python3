# -----------------------------------------------------------
# Import Libraries
# -----------------------------------------------------------

import json
import importlib
import os
from traceback import format_exc

import pandas as pd
from werkzeug.exceptions import InternalServerError
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import Imputer

from flask import Flask, request, render_template
from wtforms import Form, IntegerField, SelectField, validators
import requests
from io import StringIO

# -----------------------------------------------------------
# Forms
# -----------------------------------------------------------

races = [('Caucasian', 'Caucasian'), ('AfricanAmerican', 'AfricanAmerican'), ('Hispanic', 'Hispanic'),
         ('Other', 'Other'), ('Asian', 'Asian')]

genders = [('Female', 'Female'), ('Male', 'Male')]

ages = [('[50-60)', '[50-60)'), ('[20-30)', '[20-30)'), ('[80-90)', '[80-90)'), ('[70-80)', '[70-80)'),
        ('[60-70)', '[60-70)'), ('[30-40)', '[30-40)'), ('[40-50)', '[40-50)'), ('[10-20)', '[10-20)'),
        ('[90-100)', '[90-100)'), ('[0-10)', '[0-10)')]

weights = [('[50-75)', '[50-75)'), ('[75-100)', '[75-100)'), ('[100-125)', '[100-125)'), ('[150-175)', '[150-175)'),
           ('[0-25)', '[0-25)'), ('[125-150)', '[125-150)'), ('[25-50)', '[25-50)')]

admission_types = [('Elective', 'Elective'), ('Urgent', 'Urgent'), ('Not Available', 'Not Available'),
                   ('Emergency', 'Emergency'), ('Newborn', 'Newborn')]

discharge_dispositions = [('Discharged to home', 'Discharged to home'), (
'Discharged/transferred to home with home health service', 'Discharged/transferred to home with home health service'),
                          ('Expired', 'Expired'), ('Discharged/transferred to a long term care hospital.',
                                                   'Discharged/transferred to a long term care hospital.'),
                          ('Discharged/transferred to SNF', 'Discharged/transferred to SNF'), (
                          'Discharged/transferred to another  type of inpatient care institution',
                          'Discharged/transferred to another  type of inpatient care institution'),
                          ('Not Mapped', 'Not Mapped'), ('Discharged/transferred to another short term hospital',
                                                         'Discharged/transferred to another short term hospital'),
                          ('Left AMA', 'Left AMA'), (
                          'Discharged/transferred to another rehab fac including rehab units of a hospital.',
                          'Discharged/transferred to another rehab fac including rehab units of a hospital.'),
                          ('Hospice / medical facility', 'Hospice / medical facility'),
                          ('Hospice / home', 'Hospice / home'), (
                          'Discharged/transferred/referred to a psychiatric hospital of a psychiatric distinct part unit of a hospital',
                          'Discharged/transferred/referred to a psychiatric hospital of a psychiatric distinct part unit of a hospital'),
                          ('Discharged/transferred to ICF', 'Discharged/transferred to ICF'), (
                          'Discharged/transferred to home under care of Home IV provider',
                          'Discharged/transferred to home under care of Home IV provider'),
                          ('Admitted as an inpatient to this hospital', 'Admitted as an inpatient to this hospital'), (
                          'Discharged/transferred/referred another institution for outpatient services',
                          'Discharged/transferred/referred another institution for outpatient services'), (
                          'Discharged/transferred to a federal health care facility.',
                          'Discharged/transferred to a federal health care facility.'), (
                          'Discharged/transferred within this institution to Medicare approved swing bed',
                          'Discharged/transferred within this institution to Medicare approved swing bed'), (
                          'Discharged/transferred/referred to this institution for outpatient services',
                          'Discharged/transferred/referred to this institution for outpatient services'), (
                          'Discharged/transferred to a nursing facility certified under Medicaid but not certified under Medicare',
                          'Discharged/transferred to a nursing facility certified under Medicaid but not certified under Medicare')]

admission_sources = [('Physician Referral', 'Physician Referral'),
                     ('Transfer from another health care facility', 'Transfer from another health care facility'),
                     ('Emergency Room', 'Emergency Room'), ('Transfer from a Skilled Nursing Facility (SNF)',
                                                            'Transfer from a Skilled Nursing Facility (SNF)'),
                     ('Transfer from a hospital', 'Transfer from a hospital'), ('Not Mapped', 'Not Mapped'),
                     ('Clinic Referral', 'Clinic Referral'), ('HMO Referral', 'HMO Referral'),
                     ('Not Available', 'Not Available'), ('Court/Law Enforcement', 'Court/Law Enforcement')]

times_in_hospitals = [(1, 1), (2, 2), (7, 7), (4, 4), (5, 5), (6, 6), (3, 3), (14, 14), (10, 10), (8, 8), (11, 11),
                      (12, 12), (9, 9), (13, 13)]

payer_codes = [('CP', 'CP'), ('UN', 'UN'), ('MC', 'MC'), ('?', '?'), ('HM', 'HM'), ('SP', 'SP'), ('CM', 'CM'),
               ('BC', 'BC'), ('MD', 'MD'), ('WC', 'WC'), ('OG', 'OG'), ('PO', 'PO'), ('DM', 'DM'), ('SI', 'SI'),
               ('OT', 'OT'), ('CH', 'CH')]

medical_specialties = [('Surgery-Neuro', 'Surgery-Neuro'), ('Family/GeneralPractice', 'Family/GeneralPractice'),
                       ('Psychiatry', 'Psychiatry'), ('Cardiology', 'Cardiology'),
                       ('InternalMedicine', 'InternalMedicine'),
                       ('Surgery-Cardiovascular/Thoracic', 'Surgery-Cardiovascular/Thoracic'),
                       ('Nephrology', 'Nephrology'), ('Emergency/Trauma', 'Emergency/Trauma'),
                       ('Gastroenterology', 'Gastroenterology'), ('Orthopedics', 'Orthopedics'),
                       ('Cardiology-Pediatric', 'Cardiology-Pediatric'),
                       ('PhysicalMedicineandRehabilitation', 'PhysicalMedicineandRehabilitation'),
                       ('Gynecology', 'Gynecology'), ('Pulmonology', 'Pulmonology'),
                       ('Surgery-General', 'Surgery-General'), ('Pediatrics', 'Pediatrics'),
                       ('Orthopedics-Reconstructive', 'Orthopedics-Reconstructive'),
                       ('Surgery-Pediatric', 'Surgery-Pediatric'), ('Otolaryngology', 'Otolaryngology'),
                       ('Pediatrics-CriticalCare', 'Pediatrics-CriticalCare'),
                       ('Hematology/Oncology', 'Hematology/Oncology'),
                       ('ObstetricsandGynecology', 'ObstetricsandGynecology'),
                       ('Pediatrics-Endocrinology', 'Pediatrics-Endocrinology'),
                       ('Surgery-Vascular', 'Surgery-Vascular'), ('Urology', 'Urology'), ('Neurology', 'Neurology'),
                       ('Radiologist', 'Radiologist'), ('Osteopath', 'Osteopath'),
                       ('Surgery-Cardiovascular', 'Surgery-Cardiovascular'), ('Psychology', 'Psychology'),
                       ('Oncology', 'Oncology'), ('Endocrinology', 'Endocrinology'),
                       ('OutreachServices', 'OutreachServices'), ('Podiatry', 'Podiatry'),
                       ('Ophthalmology', 'Ophthalmology'), ('Hospitalist', 'Hospitalist'), ('Radiology', 'Radiology'),
                       ('Obsterics&Gynecology-GynecologicOnco', 'Obsterics&Gynecology-GynecologicOnco'),
                       ('Surgery-Thoracic', 'Surgery-Thoracic'), ('Surgeon', 'Surgeon'), ('Pathology', 'Pathology'),
                       ('Surgery-Plastic', 'Surgery-Plastic'), ('InfectiousDiseases', 'InfectiousDiseases'),
                       ('Anesthesiology-Pediatric', 'Anesthesiology-Pediatric'),
                       ('Pediatrics-Pulmonology', 'Pediatrics-Pulmonology'),
                       ('Pediatrics-Hematology-Oncology', 'Pediatrics-Hematology-Oncology'),
                       ('Hematology', 'Hematology'), ('Surgery-Colon&Rectal', 'Surgery-Colon&Rectal'),
                       ('Surgery-PlasticwithinHeadandNeck', 'Surgery-PlasticwithinHeadandNeck'),
                       ('Pediatrics-EmergencyMedicine', 'Pediatrics-EmergencyMedicine'), ('Obstetrics', 'Obstetrics')]

num_lab_procedures = [(35, 35), (8, 8), (12, 12), (33, 33), (31, 31), (29, 29), (46, 46), (49, 49), (54, 54), (47, 47),
                      (45, 45), (60, 60), (43, 43), (38, 38), (50, 50), (66, 66), (59, 59), (17, 17), (1, 1), (74, 74),
                      (10, 10), (19, 19), (39, 39), (61, 61), (13, 13), (68, 68), (64, 64), (18, 18), (57, 57),
                      (78, 78), (48, 48), (51, 51), (71, 71), (70, 70), (27, 27), (32, 32), (58, 58), (44, 44),
                      (37, 37), (42, 42), (53, 53), (52, 52), (11, 11), (14, 14), (41, 41), (26, 26), (75, 75),
                      (40, 40), (34, 34), (79, 79), (2, 2), (23, 23), (56, 56), (36, 36), (65, 65), (28, 28), (55, 55),
                      (80, 80), (72, 72), (84, 84), (69, 69), (67, 67), (77, 77), (21, 21), (25, 25), (24, 24),
                      (30, 30), (9, 9), (63, 63), (101, 101), (22, 22), (5, 5), (16, 16), (62, 62), (15, 15), (89, 89),
                      (4, 4), (3, 3), (87, 87), (20, 20), (91, 91), (73, 73), (83, 83), (81, 81), (6, 6), (76, 76),
                      (86, 86), (85, 85), (90, 90), (7, 7), (120, 120), (94, 94), (108, 108), (98, 98), (82, 82),
                      (104, 104), (95, 95), (92, 92), (103, 103), (96, 96), (114, 114), (106, 106), (97, 97),
                      (109, 109), (93, 93), (113, 113), (107, 107), (88, 88)]

num_procedures = [(4, 4), (5, 5), (0, 0), (1, 1), (2, 2), (3, 3), (6, 6)]


# Class for patient form
class PatientForm(Form):
    race = SelectField('races', choices=races, default=races[1], coerce=str)
    gender = SelectField('genders', choices=genders, default=genders[1], coerce=str)
    age = SelectField('ages', choices=ages, default=ages[1], coerce=str)
    weight = SelectField('weights', choices=weights, default=weights[1], coerce=str)
    admission_type = SelectField('admission_types', choices=admission_types, default=admission_types[1], coerce=str)
    discharge_disposition = SelectField('discharge_dispositions', choices=discharge_dispositions,
                                        default=discharge_dispositions[1], coerce=str)
    admission_source = SelectField('admission_sources', choices=admission_sources, default=admission_sources[1],
                                   coerce=str)
    times_in_hospital = SelectField('times_in_hospitals', choices=times_in_hospitals, default=times_in_hospitals[1],
                                    coerce=int)
    payer_code = SelectField('payer_codes', choices=payer_codes, default=payer_codes[1], coerce=str)
    medical_specialty = SelectField('medical_specialties', choices=medical_specialties, default=medical_specialties[1],
                                    coerce=str)
    num_lab_procedure = SelectField('num_lab_procedures', choices=num_lab_procedures, default=num_lab_procedures[1],
                                    coerce=int)
    num_procedure = SelectField('num_procedures', choices=num_procedures, default=num_procedures[1], coerce=int)


sample_input = """race,gender,age,weight,admission_type_id,discharge_disposition_id,admission_source_id,time_in_hospital,payer_code,medical_specialty,num_lab_procedures,num_procedures,num_medications,number_outpatient,number_emergency,number_inpatient,diag_1,diag_2,diag_3,number_diagnoses,max_glu_serum,A1Cresult,metformin,repaglinide,nateglinide,chlorpropamide,glimepiride,acetohexamide,glipizide,glyburide,tolbutamide,pioglitazone,rosiglitazone,acarbose,miglitol,troglitazone,tolazamide,examide,citoglipton,insulin,glyburide.metformin,glipizide.metformin,glimepiride.pioglitazone,metformin.rosiglitazone,metformin.pioglitazone,change,diabetesMed,diag_1_desc,diag_2_desc,diag_3_desc

{},{},{},{},{},{},{},{},{},{},{},{},14,0,0,0,428,427,401,4,None,>7,No,Steady,No,No,No,No,No,No,No,No,Steady,No,No,No,No,No,No,Steady,No,No,No,No,No,Ch,Yes,None,None,None"""


app = Flask(__name__, template_folder= 'frontend/templates', static_folder= 'frontend/static')


@app.errorhandler(InternalServerError)
def internal_server_error_handler(error):
    response = {
        'message': InternalServerError.description,
        'exception': repr(error),
        'traceback': format_exc(),
    }
    return json.dumps(response), 500


def get_url_prefix():
    return os.environ.get('URL_PREFIX', '')


def get_custom_model_instance():
    module_name = os.environ.get('MODULE_NAME')
    class_name = os.environ.get('CLASS_NAME')
    custom_model_module = importlib.import_module(module_name)
    CustomModelClass = getattr(custom_model_module, class_name)
    return CustomModelClass()


custom_model = get_custom_model_instance()
url_prefix = get_url_prefix()


# -----------------------------------------------------------
# Route Function
# -----------------------------------------------------------

@app.route('/frontend', methods=['GET', 'POST'])
def predict_patient_prob():
    """Renders a template with a form that asks for patient data.
       Uses that data to predict."""

    form = PatientForm(request.form)
    if request.method == 'POST' and form.validate():
        try:
            to_send = sample_input.format(form.race.data,
                                          form.gender.data,
                                          form.age.data,
                                          form.weight.data,
                                          form.admission_type.data,
                                          form.discharge_disposition.data,
                                          form.admission_source.data,
                                          form.times_in_hospital.data,
                                          form.payer_code.data,
                                          form.medical_specialty.data,
                                          form.num_lab_procedure.data,
                                          form.num_procedure.data)

            data = StringIO(to_send)
            X = pd.read_csv(data)
            predictions = custom_model.predict(X)
            return render_template('apis/PredictPatientReadmissionScore.html', form = form,
                                pred = predictions)




        except ValueError:
            return render_template('apis//PredictPatientReadmissionScore.html', form=form)

        return render_template('apis//PredictPatientReadmissionScore.html', form=form,
                               pred=predictions_response)
    else:
        return render_template('apis//PredictPatientReadmissionScore.html', form=form)


@app.route('{}/predict/'.format(url_prefix), methods=['POST'])
def predict():
    payload = request.form
    X = pd.read_csv(request.files['X'])
    positive_class_label = payload.get('positiveClassLabel')
    negative_class_label = payload.get('negativeClassLabel')
    predictions = custom_model.predict(
        X,
        positive_class_label=positive_class_label,
        negative_class_label=negative_class_label,
    )
    return json.dumps({'predictions': [pred for pred in predictions]})


@app.route('{}/'.format(url_prefix))
def ping():
    """This route is used to ensure that server has started"""
    return 'Server is up!\n'
