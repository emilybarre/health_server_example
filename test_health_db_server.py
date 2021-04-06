from health_db_server import init_server

init_server()

def test_add_patient_to_db():
    from health_db_server import add_patient_to_db
    name = "David Ward"
    id = 100
    blood_type = "O+"
    answer = add_patient_to_db(name, id, blood_type)
    answer.delete()
    assert answer.id_no == id
    assert answer.name == name
    assert answer.blood_type == blood_type


def test_add_patient_test_data():
    from health_db_server import add_patient_test_data
    from health_db_server import add_patient_to_db
    name = "David Ward"
    id = 100
    blood_type = "O+"
    added_patient = add_patient_to_db(name, id, blood_type)
    out_data = {"id": 8,
                "test_name": "LDL",
                "test_result": 100}
    answer = add_patient_test_data(out_data)
    answer.delete()
    expected = ("LDL", 100)
    assert answer.test[-1] == expected

# # def test_get_patient_from_db():
# #     from health_db_server import get_patient_from_db
# #     from health_db_server import db
# #     test_patient = {"name": "Erica Emerson",
# #                     "id": 200,
# #                     "blood_type": "O-",
# #                     "test": []}
# #     db.append(test_patient)
# #     answer = get_patient_from_db(200)
# #     assert answer == test_patient
# #
# #
# # def test_get_patient_from_db_missing():
# #     from health_db_server import get_patient_from_db
# #     from health_db_server import db
# #     test_patient = {"name": "Erica Emerson",
# #                     "id": 201,
# #                     "blood_type": "O-",
# #                     "test": []}
# #     db.append(test_patient)
# #     answer = get_patient_from_db(200)
# #     assert answer is False