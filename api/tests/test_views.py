import pytest
from app import create_app, db
from app.models import Company, Employee, ContractTemplate, ContractElement, Contract, Paragraph, Image, InputField

@pytest.fixture(scope='module')
def app():
    """Create a Flask app context for testing."""
    app = create_app('testing')
    app.config['TESTING'] = True
    with app.app_context():
        yield app

@pytest.fixture(scope='module')
def client(app):
    """Create a test client for the Flask app."""
    return app.test_client()

@pytest.fixture(scope='module')
def setup_database(app):
    """Fixture to set up the database for testing."""
    with app.app_context():
        db.create_all()
        yield db
        db.session.remove()
        db.drop_all()

def test_list_companies(client, setup_database):
    """Test the companies/ endpoint."""
    # Create test data
    company1 = Company(name='Company 1', address='123 Main St')
    company2 = Company(name='Company 2', address='456 Elm St')
    db.session.add(company1)
    db.session.add(company2)
    db.session.commit()

    # Test GET request
    response = client.get('api/companies/')
    assert response.status_code == 200
    companies = response.json
    assert len(companies) == 2

def test_list_employees(client, setup_database):
    """Test the employees/ endpoint for listing employees."""
    # Create test data
    company = Company(name='Test Company', address='123 Main St')
    db.session.add(company)
    db.session.commit()

    employee1 = Employee(company_id=company.id, name='John Doe', email='john.doe@example.com')
    employee2 = Employee(company_id=company.id, name='Jane Doe', email='jane.doe@example.com')
    db.session.add(employee1)
    db.session.add(employee2)
    db.session.commit()

    # Test GET request
    response = client.get('api/employees/')
    assert response.status_code == 200
    employees = response.json
    assert len(employees) == 2

def test_get_employee(client, setup_database):
    """Test the employees/<id> endpoint for retrieving a single employee."""
    # Create test data
    company = Company(name='The Test Company', address='123 Main St')
    db.session.add(company)
    db.session.commit()

    employee = Employee(company_id=1, name='John Doer', email='johndoe@xample.com')
    db.session.add(employee)
    db.session.commit()

    # Test GET request
    response = client.get(f'api/employees/{employee.id}')
    assert response.status_code == 200
    assert response.json['name'] == 'John Doer'

def test_create_employee(client, setup_database):
    """Test the employees/ POST endpoint for creating employees."""
    # Create test data
    company = Company(name='Test Company 33', address='123 Main St')
    db.session.add(company)
    db.session.commit()

    # Test POST request with valid data
    new_employee_data = {
        'company_id': company.id,
        'name': 'Jane Doe',
        'email': 'jane.doe@email.com'
    }
    response = client.post('api/employees/', json=new_employee_data)
    assert response.status_code == 201
    assert response.json['name'] == 'Jane Doe'
    assert response.json['email'] == 'jane.doe@email.com'

    # Test POST request with missing fields
    invalid_employee_data = {
        'name': 'John Doe'
    }
    response = client.post('api/employees/', json=invalid_employee_data)
    assert response.status_code == 400

    # Test POST request with invalid email format
    invalid_email_employee_data = {
        'company_id': company.id,
        'name': 'John Doe',
        'email': 'invalid_email_format'
    }
    response = client.post('api/employees/', json=invalid_email_employee_data)
    assert response.status_code == 400

    # Test POST request with existing email
    existing_employee_data = {
        'company_id': company.id,
        'name': 'Existing Employee',
        'email': 'jane.doe@email.com'
    }
    response = client.post('api/employees/', json=existing_employee_data)
    assert response.status_code == 409

    # Test POST request with invalid JSON payload
    invalid_json_payload = 'not a json'
    response = client.post('api/employees/', data=invalid_json_payload)
    assert response.status_code == 400

def test_list_contract_templates(client, setup_database):
    """Test GET request to list all contract templates."""
    # Create test data
    paragraph_element1 = Paragraph(name='Paragraph Element 1', is_optional=False, text='Sample text')
    paragraph_element2 = Paragraph(name='Paragraph Element 2', is_optional=False, text='Sample text')
    image_element = Image(name='Image Element', url='https://example.com/image.jpg')
    input_field_element = InputField(name='Input Field Element', label='Name', is_optional=False, input_type='signature')
    db.session.add(paragraph_element1)
    db.session.add(paragraph_element2)
    db.session.add(image_element)
    db.session.add(input_field_element)
    db.session.commit()

    template1 = ContractTemplate(name='Template 1', active=True, elements=[paragraph_element1.id, paragraph_element2.id, input_field_element.id, image_element.id])
    template2 = ContractTemplate(name='Template 2', active=False, elements=[paragraph_element2.id, input_field_element.id, paragraph_element1.id])
    db.session.add(template1)
    db.session.add(template2)
    db.session.commit()

    # Make GET request
    response = client.get('api/contracts/templates/')
    
    # Assert response
    assert response.status_code == 200
    data = response.json
    assert len(data) == 2
    assert data[0]['name'] == 'Template 1'
    assert data[0]['active'] == True
    assert len(data[0]['elements']) == 4
    assert data[1]['name'] == 'Template 2'
    assert data[1]['active'] == False
    assert len(data[1]['elements']) == 3

def test_get_contract_template(client, setup_database):
    """Test GET request to retrieve a single contract template."""
    # Create test data
    paragraph_element = Paragraph(name='Paragraph Element', text='Sample text')
    db.session.add(paragraph_element)
    db.session.commit()

    template = ContractTemplate(name='Template get1', active=True, elements=[paragraph_element.id])
    db.session.add(template)
    db.session.commit()

    # Make GET request
    response = client.get(f'api/contracts/templates/{template.id}')
    
    # Assert response
    assert response.status_code == 200
    data = response.json
    assert data['name'] == 'Template get1'
    assert data['active'] == True
    assert len(data['elements']) == 1
    assert data['elements'][0]['name'] == 'Paragraph Element'

def test_create_contract_template(client, setup_database):
    """Test POST request to create a new contract template."""
    paragraph_element1 = Paragraph(name='Paragraph Element ext1', is_optional=False, text='Sample text')
    paragraph_element2 = Paragraph(name='Paragraph Element ext2', is_optional=False, text='Sample text')
    input_field_element = InputField(name='Input Field Element ext', label='Name', is_optional=False, input_type='signature')
    db.session.add(paragraph_element1)
    db.session.add(paragraph_element2)
    db.session.add(input_field_element)
    db.session.commit()
    # Test data
    data = {
        'name': 'New Template',
        'active': False,
        'elements': [paragraph_element1.id, paragraph_element2.id, input_field_element.id]
    }

    # Make POST request
    response = client.post('api/contracts/templates/', json=data)
    
    # Assert response
    print(response.text)
    assert response.status_code == 201
    assert response.json['name'] == 'New Template'
    assert response.json['active'] == False
    assert len(response.json['elements']) == 3

    # Check database for created template
    created_template = ContractTemplate.query.filter_by(name='New Template').first()
    assert created_template is not None
    assert created_template.active == False
    assert created_template.elements == [paragraph_element1.id, paragraph_element2.id, input_field_element.id]
