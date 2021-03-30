from flask import Flask, request, jsonify
import logging
from pymodem import connect
from patient_class import patient

logging.basicConfig(filename="server.log", level=logging.INFO)

app = Flask(__name__)

db = list()


def init_server():
    print("Connecting to MongoDB...")
    connect("mongodb+srv://ebarre2021:<password>@bme547.rectr.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
    print("MongoDB connected.")


def add_patient_to_db(name, id, blood_type):
    new_patient = Patient(name = name,
                          id_no = id,
                          blood_type = blood_type)

    new_patient.save()
    #print(db)
    logging.info("Added new patient_id {} to database.".format(id_no))
    return True


@app.route("/new_patient", methods=["POST"])
def post_new_patient():
    # get input data from requests
    in_data = request.get_json()

    # validate input & process patient
    answer, server_status = process_new_patient(in_data)

    # Return/display results
    return answer, server_status


def validate_blood_type(in_data):
    blood_types = ["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"]
    if in_data["blood_type"] not in blood_types:
        return "{} is not a valid blood type".format(in_data["blood_type"])
    return True


def validate_new_patient_info(in_dict):
    expected_keys = ("name", "id", "blood_type")
    expected_types = (str, int, str)
    for key, ty in zip(expected_keys, expected_types):
        if key not in in_dict.keys():
            return "{} key not found".format(key), 400
        if type(in_dict[key]) != ty:
            return "{} key has the wrong value type".format(key), 400
    return True, 200


def process_new_patient(in_data):
    validate_input, server_status = validate_new_patient_info(in_data)
    if validate_input is not True:
        return validate_input, server_status
    valid_blood_type = validate_blood_type(in_data)
    if valid_blood_type is not True:
        return valid_blood_type, 400

    # define new patient dictionary
    add_patient_to_db(in_data["name"],
                      in_data["id"],
                      in_data["blood_type"])
    return "Patient successfully added", 200


@app.route("/get_image", methods=["GET"])
def get_image_route():
    return jsonify(db), 200


@app.route("/add_test", methods=["POST"])
def post_add_test():
    in_data = request.get_json()
    result, server_status = process_add_test(in_data)
    return result, server_status


def process_add_test(in_data):
    validate_input, server_status = validate_add_test_info(in_data)
    if validate_input is not True:
        return validate_input, server_status
    valid_patient_id = validate_patient_id(in_data["id"])
    if valid_patient_id is not True:
        return "Patient id {} does not exist".format(in_data["id"]), 400
    add_patient_test_data(in_data)
    return "Test data successfully added", 200


def validate_add_test_info(in_dict):
    expected_keys = ("id", "test_name", "test_result")
    expected_types = (int, str, int)
    for key, ty in zip(expected_keys, expected_types):
        if key not in in_dict.keys():
            return "{} key not found".format(key), 400
        if type(in_dict[key]) != ty:
            return "{} key has the wrong value type".format(key), 400
    return True, 200


def validate_patient_id(patient_id):
    for patient in db:
        if patient["id"] == patient_id:
            return True
    return False


def add_patient_test_data(in_data):
    for patient in db:
        if patient["id"] == in_data["id"]:
            break
    patient["test"].append((in_data["test_name"], in_data["test_result"]))


@app.route("/get_results/<patient_id>", methods=["GET"])
def get_results(patient_id):
    validation_info, server_status = \
        validate_variable_url_patient_id(patient_id)
    if server_status != 200:
        return validation_info, server_status
    patient_info = get_patient_from_db(validation_info)
    return jsonify(patient_info), 200


def validate_variable_url_patient_id(patient_id):
    try:
        id_int = int(patient_id)
    except ValueError:
        return "{} is not a valid patient id".format(patient_id), 400
    valid_patient_id = validate_patient_id(id_int)
    if valid_patient_id is False:
        return "Patient id {} does not exist in database".format(id_int), 400
    return id_int, 200


def get_patient_from_db(patient_id):
    for patient in db:
        if patient["id"] == patient_id:
            return patient
    return False



if __name__ == '__main__':
    init_server()
    app.run()