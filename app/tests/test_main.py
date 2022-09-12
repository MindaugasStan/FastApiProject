from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)

data = {
    "Name": "PC"
}

def test_read_companies():
    response = client.get("/company")
    assert response.status_code == 200


def test_post_company():
    response = client.post("/company", json=data)
    assert response.status_code == 201


def test_get_company_by_id():
    response = client.get("/company/6")
    assert response.status_code == 200
    assert response.json() == {"id": 6, "name": "PC", "employees":[], "levels":[]}


def test_update_company():
    response = client.put("/company/2", json={"Name": "Test"})
    assert response.status_code == 202
    assert response.json() == 'updated'


def test_post_seniorityLevel():
    response = client.post("/seniorityLevel", json={"level": "Junior", "multiplier": 1.2, "time_needed": 5, "company_id":5})
    assert response.status_code == 201


def test_update_seniorityLevel():
    response = client.put("/seniorityLevel/1", json={"level": "Senior", "multiplier": 1.3, "time_needed": 5})
    assert response.status_code == 202
    assert response.json() == 'updated'


def test_post_employee():
    response = client.post("/employee", json={"Name": "Employee", "LastName": "EmployeeLast", "JobStartDate": 20220911, "Experience": 2.5, "HourlyRate": 5, "Company_id": 5})
    assert response.status_code == 201



def test_get_employee_with_fullName():
    response = client.get("/employeeName")
    assert response.status_code == 200


def test_update_employee():
    response = client.put("/employee/1", json={"name": "Employee1", "lastname": "Employee1Last", "jobstartdate": 20220911, "experience": 2.5, "hourlyrate": 5})
    assert response.status_code == 202







