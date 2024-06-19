import pytest
from datetime import datetime
from app import db, create_app
from app.models  import Company, Employee, ContractTemplate, Paragraph, Image, InputField, Contract

@pytest.fixture(scope='module')
def app():
    """Create a Flask app context for testing."""
    app = create_app('testing')  
    app.config['TESTING'] = True
    with app.app_context():
        yield app

@pytest.fixture(scope='module')
def setup_database(app):
    """Fixture to set up the database for testing."""
    with app.app_context():
        db.create_all()
        yield db  
        db.session.remove()
        db.drop_all()

def test_company_model(setup_database):
    company = Company(name='Test Company', address='123 Main St')
    setup_database.session.add(company)
    setup_database.session.commit()

    company_dict = company.to_dict()
    assert company_dict["company_id"] == company.id
    assert company_dict["name"] == company.name
    assert company_dict["address"] == company.address
    
    assert company.id is not None
    assert company.name == 'Test Company'
    assert company.address == '123 Main St'

def test_employee_model(setup_database):
    company = Company(name='Test Company', address='123 Main St')
    setup_database.session.add(company)
    setup_database.session.commit()

    employee = Employee(company_id=company.id, name='John Doe', email='john.doe@example.com')
    setup_database.session.add(employee)
    setup_database.session.commit()

    assert employee.id is not None
    assert employee.name == 'John Doe'
    assert employee.email == 'john.doe@example.com'
    assert employee.to_dict() == {'id': employee.id, 'company_id': company.id, 'name': 'John Doe', 'email': 'john.doe@example.com'}
    
def test_contract_template_model(setup_database):
    template = ContractTemplate(name='Standard Template', elements=[1, 2, 3])
    setup_database.session.add(template)
    setup_database.session.commit()

    assert template.id is not None
    assert template.name == 'Standard Template'
    assert template.active is False
    assert isinstance(template.created_at, datetime)

def test_contract_element_models(setup_database):
    paragraph = Paragraph(name='Intro', text='This is the introduction.')
    setup_database.session.add(paragraph)
    setup_database.session.commit()

    assert paragraph.id is not None
    assert paragraph.text == 'This is the introduction.'
    assert paragraph.to_dict() == {
        'id': paragraph.id,
        'type': 'paragraph',
        'name': 'Intro',
        'text': 'This is the introduction.',
        'is_optional': True
    }

    image = Image(name='Company Logo', url='https://example.com/logo.png')
    setup_database.session.add(image)
    setup_database.session.commit()

    assert image.id is not None
    assert image.url == 'https://example.com/logo.png'
    assert image.to_dict() == {
        'id': image.id,
        'type': 'image',
        'name': 'Company Logo',
        'url': 'https://example.com/logo.png',
        'is_optional': True
    }

    input_field = InputField(name='Feedback', label='Feedback Text', input_type='text')
    setup_database.session.add(input_field)
    setup_database.session.commit()

    assert input_field.id is not None
    assert input_field.label == 'Feedback Text'
    assert input_field.to_dict() == {
        'id': input_field.id,
        'type': 'input_field',
        'name': 'Feedback',
        'label': 'Feedback Text',
        'input_type': 'text',
        'is_optional': True
    }

def test_contract_model(setup_database):
    company = Company(name='Test Company', address='123 Main St')
    setup_database.session.add(company)
    setup_database.session.commit()

    employee = Employee(company_id=company.id, name='John Doe', email='johndoe@example.com')
    setup_database.session.add(employee)
    setup_database.session.commit()

    template = ContractTemplate(name='Basic Template', elements=[1, 2, 3])
    setup_database.session.add(template)
    setup_database.session.commit()

    contract_data = {'field1': 'value1', 'field2': 'value2'}
    contract = Contract(employee_id=employee.id, template_id=template.id, contract_data=contract_data, signed_date=datetime.now().date())
    setup_database.session.add(contract)
    setup_database.session.commit()

    assert contract.id is not None
    assert contract.contract_data == contract_data
    assert contract.signed_date == datetime.now().date()
    assert contract.to_dict() == {
        'id': contract.id,
        'employee_id': 2,
        'template_id': 2,
        'contract_data': {'field1': 'value1', 'field2': 'value2'},
        'signed_date': contract.signed_date
    }

