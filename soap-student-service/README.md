# Student Management SOAP API (Python + PostgreSQL)

A production-ready SOAP Web Service built using Python (Spyne) and PostgreSQL, featuring full CRUD operations for student data.

This project demonstrates how to build enterprise-grade SOAP APIs in Python from scratch — with a real database, service contracts (WSDL), schema validation, and structured service logic.

## Features

- SOAP-based API using `Spyne`
- Auto-connects to PostgreSQL running in Docker
- Creates database & tables automatically if missing
- CRUD services for students (Add / Get / Update / Delete)
- XML-based requests & responses using WSDL
- Works with Postman, SOAP UI or Python client
- Clear architecture using MVC + Service Layer

## Project Structure
```bash
student-soap-api/
│
├── app.py                  # Main SOAP server
├── database.py             # PostgreSQL connection & DB creation
├── student_service.py      # SOAP methods (CRUD operations)
├── models.py               # SQLAlchemy ORM for Student table
├── client_test.py          # Example client to test SOAP API
├── requirements.txt
└── README.md               # You are here!

```

## Tech Stack Used
| Component      | Technology                         |
| -------------- | ---------------------------------- |
| Backend API    | Python + Spyne (SOAP)              |
| Database       | PostgreSQL (Docker)                |
| ORM            | SQLAlchemy                         |
| Protocol       | SOAP 1.1/XML                       |
| Server         | WSGI / WsgiApplication             |
| Testing        | Postman / SOAPUI / Python requests |
| Language Style | PEP8 + Clean Architecture          |

## Setup Instructions
### 1. Clone Repository
```bash
git clone https://github.com/Selvam-DG/api-mastery.git
cd api-mastery/soap-student-serivice

```

### 2. Create Virtual Environment and  Install Dependencies
```bash
python -m venv env
source env/bin/activate

pip install -r requirements.txt
```

### 3. Configure Database
- copy `.env.example` to `.env`
```bash
 docker run --name postgres16 -e POSTGRES_PASSWORD=yourpassword \
    -p 5432:5432 -d postgres:16-alpine
```
### 4. 4. Run SOAP Server
```bash
python app.py
```
Your SOAP API is live at:

http://localhost:8000/?wsdl

## How SOAP Works Here

- Client sends SOAP request (XML)
- Spyne parses + validates against WSDL schema
- Business logic runs & interacts with PostgreSQL
- Response returned as SOAP XML

## Sample SOAP Request (Postman / SOAP UI)

POST → http://localhost:8000
```xml
<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:stu="student.soap.api">
   <soapenv:Header/>
   <soapenv:Body>
      <stu:add_student>
         <stu:name>John Doe</stu:name>
         <stu:age>21</stu:age>
         <stu:department>Computer Science</stu:department>
      </stu:add_student>
   </soapenv:Body>
</soapenv:Envelope>
```
## Example SOAP Response
```xml
<senv:Envelope xmlns:senv="http://schemas.xmlsoap.org/soap/envelope/">
  <senv:Body>
    <add_studentResponse xmlns="student.soap.api">
      <add_studentResult>
        Student John Doe added successfully with ID 1
      </add_studentResult>
    </add_studentResponse>
  </senv:Body>
</senv:Envelope>
```
## Example Python SOAP Client
```xml
import requests

xml = """<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:stu="student.soap.api">
   <soapenv:Header/>
   <soapenv:Body>
      <stu:get_student>
         <stu:student_id>1</stu:student_id>
      </stu:get_student>
   </soapenv:Body>
</soapenv:Envelope>"""

response = requests.post("http://localhost:8000", data=xml, headers={"Content-Type": "text/xml"})
print(response.text)
```

## Future Enhancements

- [x] Basic CRUD over SOAP   
- [ ] Token-based Authentication (WS-Security)
- [ ] Deploy to AWS / Render / Azure
- [ ]  pytest + automated test suite


## License

This project is licensed under the MIT License.
You are free to use, modify, and distribute the code with attribution.

## Ideology & Why I Built This

SOAP is still widely used in enterprise, banking, healthcare, aviation, and telecom systems.
Most tutorials online are either outdated or without real database connections.

So I built this project to:
- Understand real SOAP API architecture
- Connect with PostgreSQL using SQLAlchemy ORM
- Create something production-friendly, not just a "Hello World" service
- Help students & engineers learn enterprise-level SOAP workflows

## If you found this useful

Give a ⭐ on GitHub — it motivates me to build more!