# Student Management SOAP API

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-336791.svg)](https://www.postgresql.org/)
[![SOAP](https://img.shields.io/badge/Protocol-SOAP%201.1-green.svg)](https://www.w3.org/TR/soap/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

A production-ready SOAP Web Service implementing enterprise-grade student management with full CRUD operations. Built with Python (Spyne) and PostgreSQL, this project demonstrates modern SOAP API development with real database integration, WSDL contracts, and XML schema validation.

---

## Table of Contents

- [Overview](#overview)
- [Why SOAP?](#why-soap)
- [Features](#features)
- [Architecture](#architecture)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Running the Service](#running-the-service)
- [API Documentation](#api-documentation)
- [Testing](#testing)
- [Deployment](#deployment)
- [Roadmap](#roadmap)
- [Contributing](#contributing)
- [License](#license)

---

## Overview

This project provides a fully functional SOAP web service for managing student records with PostgreSQL persistence. Unlike simple "Hello World" SOAP examples, this implementation includes:

- **Real database integration** with automatic schema creation
- **Production-ready architecture** following MVC + Service Layer pattern
- **Complete CRUD operations** with proper error handling
- **WSDL contract** for client code generation
- **Docker support** for easy database setup
- **Comprehensive testing** examples

### SOAP Communication Flow

```
┌──────────┐                ┌──────────────┐                ┌──────────────┐
│  Client  │   XML/SOAP     │  Spyne API   │   SQL Queries  │  PostgreSQL  │
│ (Postman)│───────────────▶│   Server     │───────────────▶│   Database   │
│          │◀───────────────│  (Python)    │◀───────────────│              │
└──────────┘   XML Response └──────────────┘   Query Results└──────────────┘
```

---

## Why SOAP?

While REST and GraphQL dominate modern API development, **SOAP remains critical** in:

### Enterprise Sectors:
- **Banking & Finance**: Transaction processing, payment gateways
- **Healthcare**: HL7 integration, patient record systems
- **Aviation**: Booking systems, flight information
- **Telecommunications**: Billing, provisioning services
- **Government**: Tax systems, regulatory compliance

### Key Advantages:
- **Strict contracts (WSDL)**: Prevents breaking changes
- **Built-in security**: WS-Security standards
- **ACID transactions**: Critical for financial operations
- **Language independence**: Java, .NET, Python interoperability
- **Enterprise support**: Mature tooling and standards

---

## Features

### Core Functionality
- **Create Student**: Add new student records with validation
- **Get Student**: Retrieve student by ID with detailed information
- **Update Student**: Modify existing student data
- **Delete Student**: Remove student records
- **List Students**: Fetch all students with pagination support

### Technical Features
- **Auto-initialization**: Database and tables created automatically
- **Schema Validation**: XML validation against WSDL
- **Docker Ready**: PostgreSQL containerization support
- **ORM Integration**: SQLAlchemy for database operations
- **Clean Architecture**: Separation of concerns (MVC + Service Layer)
- **WSDL Generation**: Auto-generated service description
- **Client Examples**: Python and cURL test implementations

---

## Architecture

### Design Pattern: MVC + Service Layer

```
┌─────────────────────────────────────────────────────────┐
│                     Client Layer                        │
│            (Postman, SOAP UI, Python Client)            │
└────────────────────┬────────────────────────────────────┘
                     │ SOAP/XML
                     ▼
┌─────────────────────────────────────────────────────────┐
│                  Controller Layer                       │
│                   (app.py - Spyne)                      │
│        ┌──────────────────────────────────┐             │
│        │  SOAP Endpoint Handler           │             │
│        │  - Request Parsing               │             │
│        │  - Response Serialization        │             │
│        └──────────────┬───────────────────┘             │
└───────────────────────┼─────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────┐
│                   Service Layer                         │
│              (student_service.py)                       │
│        ┌──────────────────────────────────┐             │
│        │  Business Logic                  │             │
│        │  - Validation Rules              │             │
│        │  - Data Transformation           │             │
│        │  - Error Handling                │             │
│        └──────────────┬───────────────────┘             │
└───────────────────────┼─────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────┐
│                     Model Layer                         │
│                    (models.py)                          │
│        ┌──────────────────────────────────┐             │
│        │  Student ORM Model               │             │
│        │  - Schema Definition             │             │
│        │  - Relationships                 │             │
│        └──────────────┬───────────────────┘             │
└───────────────────────┼─────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────┐
│                  Database Layer                         │
│                  (database.py)                          │
│        ┌──────────────────────────────────┐             │
│        │  PostgreSQL Connection Pool      │             │
│        │  - Session Management            │             │
│        │  - Connection Pooling            │             │
│        └──────────────┬───────────────────┘             │
└───────────────────────┼─────────────────────────────────┘
                        │
                        ▼
                 ┌──────────────┐
                 │  PostgreSQL  │
                 │   Database   │
                 └──────────────┘
```

---

## Tech Stack

| Component | Technology | Purpose |
|-----------|-----------|---------|
| **Framework** | Spyne 2.14+ | SOAP service implementation |
| **Database** | PostgreSQL 16 | Data persistence |
| **ORM** | SQLAlchemy 2.0+ | Database abstraction layer |
| **Server** | WSGI | Production-grade HTTP server |
| **Protocol** | SOAP 1.1/1.2 | XML-based messaging |
| **Container** | Docker | Database containerization |
| **Testing** | Requests, Zeep | API testing and validation |
| **Code Style** | PEP 8 | Python code standards |

---

## Project Structure

```
soap-student-service/
│
├── app.py                  # SOAP server initialization & routing
├── database.py             # PostgreSQL connection & setup
├── student_service.py      # SOAP service methods (CRUD)
├── models.py               # SQLAlchemy ORM models
├── client_test.py          # Python client examples
│
├── requirements.txt        # Python dependencies
├── .env.example            # Environment variables template
├── docker-compose.yml      # Docker setup (optional)
│
├── README.md               # Project documentation
└── LICENSE                 # MIT License
```

### File Descriptions

- **app.py**: Main entry point, configures Spyne application and WSGI server
- **database.py**: Database connection pooling, session management, auto-initialization
- **student_service.py**: SOAP operations implementation with business logic
- **models.py**: Student entity definition using SQLAlchemy ORM
- **client_test.py**: Sample SOAP client for testing API endpoints

---

## Prerequisites

Ensure you have the following installed:

- **Python**: 3.8 or higher ([Download](https://www.python.org/downloads/))
- **PostgreSQL**: 16+ ([Download](https://www.postgresql.org/download/)) or Docker
- **pip**: Python package manager (comes with Python)
- **Git**: Version control ([Download](https://git-scm.com/))

### Optional Tools:
- **Docker Desktop**: For containerized PostgreSQL ([Download](https://www.docker.com/products/docker-desktop))
- **Postman**: For API testing ([Download](https://www.postman.com/downloads/))
- **SOAP UI**: Advanced SOAP testing ([Download](https://www.soapui.org/downloads/soapui/))

---

##  Installation

### Step 1: Clone Repository

```bash
git clone https://github.com/Selvam-DG/api-mastery.git
cd api-mastery/soap-student-service
```

### Step 2: Create Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Linux/Mac:
source venv/bin/activate

# On Windows:
venv\Scripts\activate
```

### Step 3: Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### Dependencies Installed:
```
spyne==2.14.0           # SOAP framework
SQLAlchemy==2.0.25      # ORM
psycopg2-binary==2.9.9  # PostgreSQL adapter
python-dotenv==1.0.0    # Environment variables
lxml==5.1.0             # XML processing
requests==2.31.0        # HTTP client for testing
```

---

## Configuration

### Step 1: Create Environment File

```bash
cp .env.example .env
```

### Step 2: Configure Database Connection

Edit `.env` file with your database credentials:

```bash
# PostgreSQL Configuration
DB_HOST=localhost
DB_PORT=5432
DB_NAME=student_db
DB_USER=postgres
DB_PASSWORD=yourpassword

# Server Configuration
SOAP_HOST=0.0.0.0
SOAP_PORT=8000
```

### Step 3: Setup PostgreSQL

#### Option A: Using Docker (Recommended)

```bash
# Run PostgreSQL container
docker run --name postgres-soap \
  -e POSTGRES_PASSWORD=yourpassword \
  -e POSTGRES_DB=student_db \
  -p 5432:5432 \
  -d postgres:16-alpine

# Verify container is running
docker ps
```

#### Option B: Local PostgreSQL Installation

```bash
# Create database
psql -U postgres -c "CREATE DATABASE student_db;"

# Verify connection
psql -U postgres -d student_db -c "\dt"
```

---

## Running the Service

### Start the SOAP Server

```bash
python app.py
```

You should see:

```
INFO:spyne.server.wsgi:Application started on 0.0.0.0:8000
INFO:spyne.server.wsgi:WSDL available at: http://localhost:8000/?wsdl
```

### Verify Service is Running

Open your browser and navigate to:
```
http://localhost:8000/?wsdl
```

You should see the WSDL (Web Services Description Language) document describing the service contract.

---

## API Documentation

### Available SOAP Operations

| Operation | Description | Input | Output |
|-----------|-------------|-------|--------|
| `add_student` | Create new student | name, age, department | Success message with ID |
| `get_student` | Retrieve student by ID | student_id | Student object |
| `update_student` | Update student details | student_id, name, age, department | Success message |
| `delete_student` | Remove student | student_id | Success message |
| `get_all_students` | List all students | None | Array of students |

---

### 1. Add Student

**Request:**
```xml
<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" 
                  xmlns:stu="student.soap.api">
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

**Response:**
```xml
<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/">
   <soapenv:Body>
      <ns0:add_studentResponse xmlns:ns0="student.soap.api">
         <ns0:add_studentResult>
            Student John Doe added successfully with ID 1
         </ns0:add_studentResult>
      </ns0:add_studentResponse>
   </soapenv:Body>
</soapenv:Envelope>
```

---

### 2. Get Student

**Request:**
```xml
<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" 
                  xmlns:stu="student.soap.api">
   <soapenv:Header/>
   <soapenv:Body>
      <stu:get_student>
         <stu:student_id>1</stu:student_id>
      </stu:get_student>
   </soapenv:Body>
</soapenv:Envelope>
```

**Response:**
```xml
<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/">
   <soapenv:Body>
      <ns0:get_studentResponse xmlns:ns0="student.soap.api">
         <ns0:get_studentResult>
            <ns0:id>1</ns0:id>
            <ns0:name>John Doe</ns0:name>
            <ns0:age>21</ns0:age>
            <ns0:department>Computer Science</ns0:department>
         </ns0:get_studentResult>
      </ns0:get_studentResponse>
   </soapenv:Body>
</soapenv:Envelope>
```

---

### 3. Update Student

**Request:**
```xml
<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" 
                  xmlns:stu="student.soap.api">
   <soapenv:Header/>
   <soapenv:Body>
      <stu:update_student>
         <stu:student_id>1</stu:student_id>
         <stu:name>John Smith</stu:name>
         <stu:age>22</stu:age>
         <stu:department>Data Science</stu:department>
      </stu:update_student>
   </soapenv:Body>
</soapenv:Envelope>
```

**Response:**
```xml
<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/">
   <soapenv:Body>
      <ns0:update_studentResponse xmlns:ns0="student.soap.api">
         <ns0:update_studentResult>
            Student with ID 1 updated successfully
         </ns0:update_studentResult>
      </ns0:update_studentResponse>
   </soapenv:Body>
</soapenv:Envelope>
```

---

### 4. Delete Student

**Request:**
```xml
<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" 
                  xmlns:stu="student.soap.api">
   <soapenv:Header/>
   <soapenv:Body>
      <stu:delete_student>
         <stu:student_id>1</stu:student_id>
      </stu:delete_student>
   </soapenv:Body>
</soapenv:Envelope>
```

**Response:**
```xml
<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/">
   <soapenv:Body>
      <ns0:delete_studentResponse xmlns:ns0="student.soap.api">
         <ns0:delete_studentResult>
            Student with ID 1 deleted successfully
         </ns0:delete_studentResult>
      </ns0:delete_studentResponse>
   </soapenv:Body>
</soapenv:Envelope>
```

---

### 5. Get All Students

**Request:**
```xml
<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" 
                  xmlns:stu="student.soap.api">
   <soapenv:Header/>
   <soapenv:Body>
      <stu:get_all_students/>
   </soapenv:Body>
</soapenv:Envelope>
```

**Response:**
```xml
<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/">
   <soapenv:Body>
      <ns0:get_all_studentsResponse xmlns:ns0="student.soap.api">
         <ns0:get_all_studentsResult>
            <ns0:Student>
               <ns0:id>1</ns0:id>
               <ns0:name>John Doe</ns0:name>
               <ns0:age>21</ns0:age>
               <ns0:department>Computer Science</ns0:department>
            </ns0:Student>
            <ns0:Student>
               <ns0:id>2</ns0:id>
               <ns0:name>Jane Smith</ns0:name>
               <ns0:age>20</ns0:age>
               <ns0:department>Mathematics</ns0:department>
            </ns0:Student>
         </ns0:get_all_studentsResult>
      </ns0:get_all_studentsResponse>
   </soapenv:Body>
</soapenv:Envelope>
```

---

## Testing

### Method 1: Using Python Client

```bash
python client_test.py
```

**Python Client Example:**
```python
import requests

# SOAP Endpoint
url = "http://localhost:8000"

# Add Student Request
xml_request = """
<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" 
                  xmlns:stu="student.soap.api">
   <soapenv:Header/>
   <soapenv:Body>
      <stu:add_student>
         <stu:name>Alice Johnson</stu:name>
         <stu:age>22</stu:age>
         <stu:department>Engineering</stu:department>
      </stu:add_student>
   </soapenv:Body>
</soapenv:Envelope>
"""

# Send request
headers = {"Content-Type": "text/xml; charset=utf-8"}
response = requests.post(url, data=xml_request, headers=headers)

# Print response
print("Status Code:", response.status_code)
print("Response:\n", response.text)
```

---

### Method 2: Using cURL

```bash
curl -X POST http://localhost:8000 \
  -H "Content-Type: text/xml" \
  -d '<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:stu="student.soap.api">
   <soapenv:Header/>
   <soapenv:Body>
      <stu:get_all_students/>
   </soapenv:Body>
</soapenv:Envelope>'
```

---

### Method 3: Using Postman

1. **Create New Request**
   - Method: `POST`
   - URL: `http://localhost:8000`

2. **Set Headers**
   - `Content-Type`: `text/xml`

3. **Set Body**
   - Select `raw` and paste SOAP XML request

4. **Send Request**
   - Click Send button
   - View XML response in the body section

---

### Method 4: Using SOAP UI

1. **Create New SOAP Project**
   - WSDL URL: `http://localhost:8000/?wsdl`

2. **Generate Test Cases**
   - SOAP UI will auto-generate request templates

3. **Execute Requests**
   - Fill in parameters and click the play button

---

## Deployment

### Docker Deployment

**1. Create Dockerfile:**

copy from [`Dockerfile`](Dockerfile)

**2. Create docker-compose.yml:**

copy from [`Dockerfile`](docker-compose.yml)

**3. Deploy:**

```bash
docker-compose up -d
```

---

### Cloud Deployment Options

#### AWS Elastic Beanstalk
```bash
eb init -p python-3.11 soap-student-api
eb create production-env
eb deploy
```

#### Heroku
```bash
heroku create soap-student-api
git push heroku main
```

#### Azure App Service
```bash
az webapp up --name soap-student-api --runtime "PYTHON:3.11"
```

---

## Roadmap

### Completed
- [x] Basic CRUD operations
- [x] PostgreSQL integration
- [x] Auto database initialization
- [x] WSDL contract generation
- [x] Python client examples
- [x] Docker support

### In Progress 
- [ ] WS-Security authentication
- [ ] Input validation middleware
- [ ] Logging and monitoring
- [ ] API rate limiting

### Planned 
- [ ] Unit test suite with pytest
- [ ] Integration tests
- [ ] CI/CD pipeline (GitHub Actions)
- [ ] Swagger documentation
- [ ] Performance benchmarking
- [ ] Kubernetes deployment manifests
- [ ] GraphQL comparison example

---

## Contributing

Contributions are welcome! Please follow these guidelines:

### How to Contribute

1. **Fork the repository**
2. **Create feature branch**: `git checkout -b feature/amazing-feature`
3. **Commit changes**: `git commit -m 'Add amazing feature'`
4. **Push to branch**: `git push origin feature/amazing-feature`
5. **Open Pull Request**

### Code Standards
- Follow PEP 8 style guide
- Add docstrings to all functions
- Include type hints where applicable
- Write tests for new features
- Update documentation

---

## License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

MIT License


## Learning Resources

### SOAP & Web Services
- [W3C SOAP Specification](https://www.w3.org/TR/soap/)
- [WSDL Tutorial](https://www.w3schools.com/xml/xml_wsdl.asp)
- [Spyne Documentation](https://spyne.io/)

### Python & Databases
- [SQLAlchemy ORM Tutorial](https://docs.sqlalchemy.org/en/20/tutorial/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [Python Best Practices](https://docs.python-guide.org/)

---

## Why I Built This

> **SOAP is still widely used in enterprise, banking, healthcare, aviation, and telecom systems.**  
> Most tutorials online are either outdated or without real database connections.

### My Goals:
- Understand real-world SOAP API architecture  
- Build production-ready services, not just "Hello World" examples  
- Connect with PostgreSQL using modern ORM practices  
- Help students & engineers learn enterprise-level SOAP workflows  
- Create a reference project for SOAP development in Python

---

## Acknowledgments

- **Spyne Framework**: For excellent SOAP support in Python
- **SQLAlchemy Team**: For the best Python ORM
- **PostgreSQL Community**: For robust database technology
- **Python Community**: For comprehensive libraries and support

---

## Contact & Support

- **GitHub**: [@Selvam-DG](https://github.com/Selvam-DG)
- **Issues**: [Report bugs or request features](https://github.com/Selvam-DG/api-mastery/issues)
- **Discussions**: [Join community discussions](https://github.com/Selvam-DG/api-mastery/discussions)

---

<div align="center">

### ⭐ If you found this useful, give it a star on GitHub!

**It motivates me to build more production-ready projects.**

Made with ❤️ for developers learning SOAP APIs

[⬆ Back to Top](#-student-management-soap-api)

</div>