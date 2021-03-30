import requests

patient = {"name": "Keith",
            "id": 8,
            "blood_type": "A+"}

r = requests.post("http://127.0.0.1:5000/new_patient", json=patient)
print(r.status_code)
print(r.text)

new_test = {"id": 8,
            "test_name": "HDL",
            "test_result": 60}
r = requests.post("http://127.0.0.1:5000/add_test", json=new_test)
print(r.status_code)
print(r.text)

r = requests.get("http://127.0.0.1:5000/get_results/8")
print(r.status_code)
print(r.text)