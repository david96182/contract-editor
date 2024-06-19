from flask import jsonify, request
from datetime import datetime
import re
from . import main
from ..models import Company, Employee, ContractTemplate, ContractElement, Contract, Paragraph, Image, InputField 
from .. import db
from .validators import validate_contract_elements

ELEMENT_TYPES = ['paragraph', 'image', 'input_field']

@main.route('/ping', methods=['GET'])
def index():
    return 'pong!'

@main.route('/companies/', methods=['GET'])
def list_companies():
    companies = Company.query.all()
    companies_list = [company.to_dict() for company in companies]
    return jsonify(companies_list)

@main.route('/employees/', methods=['GET'])
def list_employees():
    employees = Employee.query.all()
    employees_list = [employee.to_dict() for employee in employees]
    return jsonify(employees_list)

@main.route('/employees/<int:id>', methods=['GET'])
def get_employee(id):
    employee = Employee.query.get(id)
    if employee:
        return jsonify(employee.to_dict())
    else:
        return jsonify({'error': 'Employee not found'}), 404

@main.route('/employees/', methods=['POST'])
def create_employee():
    try:
        data = request.json
    except Exception as e:
        return jsonify({"error": "Invalid JSON payload"}), 400

    if not all(key in data for key in ['company_id', 'name', 'email']):
        return jsonify({"error": "Missing one or more required fields"}), 400

    company_id = data.get('company_id')
    name = data.get('name')
    email = data.get('email')

    company = Company.query.get(company_id)
    if not company:
        return jsonify({"error": "Company not found"}), 404

    email_regex = r"[^@]+@[^@]+\.[^@]+"
    if not re.match(email_regex, email):
        return jsonify({"error": "Email is not valid"}), 400

    existing_employee = Employee.query.filter_by(email=email).first()
    if existing_employee:
        return jsonify({"error": "An employee with this email already exists"}), 409

    employee = Employee(company_id=company_id, name=name, email=email)
    db.session.add(employee)
    db.session.commit()

    return jsonify(employee.to_dict()), 201

@main.route('/contracts/templates/', methods=['GET'])
def list_contract_templates():
    templates = ContractTemplate.query.all()
    templates_list = [template.to_dict() for template in templates]
    return jsonify(templates_list)

@main.route('/contracts/templates/<int:id>', methods=['GET'])
def get_contract_template(id):
    template = ContractTemplate.query.get(id)
    if template:
        return jsonify(template.to_dict())
    else:
        return jsonify({'error': 'Contract template not found'}), 404

@main.route('/contracts/templates/', methods=['POST'])
def create_contract_template():
    try:
        data = request.json
    except Exception as e:
        return jsonify({"error": "Invalid JSON payload"}), 400

    name = data.get('name')
    if not name:
        return jsonify({'error': ' Name is required to create contract templates'}), 400
    existing_template = ContractTemplate.query.filter_by(name=name).first()
    if existing_template:
        return jsonify({"error": "A contract template with this name already exists"}), 409

    active = data.get('active', False)
    elements = data.get('elements', [])

    validation_error = validate_contract_elements(elements)
    if validation_error:
        return jsonify(validation_error), 400

    template = ContractTemplate(name=name, active=active, elements=elements)
    db.session.add(template)
    db.session.commit()

    return jsonify(template.to_dict()), 201

@main.route('/contracts/templates/<int:id>', methods=['PUT'])
def update_contract_template(id):
    template = ContractTemplate.query.get(id)
    if template:
        try:
            data = request.json
        except Exception as e:
            return jsonify({"error": "Invalid JSON payload"}), 400

        name = data.get('name', template.name)
        template.active = data.get('active', template.active)
        elements = data.get('elements', template.elements)
    
        validation_error = validate_contract_elements(elements)
        if validation_error:
            return jsonify(validation_error), 400

        template.name = name
        template.elements = elements
        db.session.commit()

        return jsonify(template.to_dict())
    else:
        return jsonify({'error': 'Contract template not found'}), 404

@main.route('/contracts/templates/elements/', methods=['GET'])
def list_template_elements():
    elements = ContractElement.query.all()
    elements_list = [element.to_dict() for element in elements]
    return jsonify(elements_list)

@main.route('/contracts/templates/elements/<int:id>', methods=['GET'])
def get_template_element(id):
    element = ContractElement.query.get(id)
    if element:
        return jsonify(element.to_dict())
    else:
        return jsonify({'error': 'Contract element not found'}), 404

@main.route('/contracts/templates/elements/types', methods=['GET'])
def list_supported_element_types():
    return jsonify(ELEMENT_TYPES)

@main.route('/contracts/templates/elements/type/<string:name>', methods=['GET'])
def list_elements_by_type(name):
    if name not in ELEMENT_TYPES:
        return jsonify({'error': 'Invalid element type'}), 404

    elements = ContractElement.query.filter_by(element_type=name).all()
    elements_list = [element.to_dict() for element in elements]
    return jsonify(elements_list)

@main.route('/contracts/templates/elements', methods=['POST'])
def create_template_element():
    try:
        data = request.json
    except Exception as e:
        return jsonify({"error": "Invalid JSON payload"}), 400

    element_type = data.get('element_type')
    name = data.get('name')
    is_optional = data.get('is_optional', True)

    if element_type not in ELEMENT_TYPES:
        return jsonify({'error': 'Invalid element type'}), 400
    if not name:
        return jsonify({'error': ' Name is required to create elements'}), 400
    existing_element = ContractElement.query.filter_by(name=name).first()
    if existing_element:
        return jsonify({"error": "An element with this name already exists"}), 409

    if element_type == 'paragraph':
        text = data.get('text')
        if not text:
            return jsonify({'error': 'Text is required for a paragraph element'}), 400
        new_element = Paragraph(name=name, is_optional=is_optional, text=text)

    elif element_type == 'image':
        url = data.get('url')
        if not url:
            return jsonify({'error': 'URL is required for an image element'}), 400
        new_element = Image(name=name, is_optional=is_optional, url=url)

    elif element_type == 'input_field':
        input_types = ['phone', 'signature', 'email', 'address', 'name']
        label = data.get('label')
        input_type = data.get('input_type')

        if not label:
            return jsonify({'error': 'Label is required for an input field element'}), 400
        if not input_type:
            return jsonify({'error': 'Input type is required for an input field element'}), 400
        elif input_type not in input_types:
            return jsonify({'error': f'Input type is not supported, supported input types: {input_types}'}), 400 

        new_element = InputField(name=name, is_optional=is_optional, label=label, input_type=input_type)

    db.session.add(new_element)
    db.session.commit()

    return jsonify(new_element.to_dict()), 201

@main.route('/contracts/templates/elements/<int:id>', methods=['PUT'])
def update_specific_element(id):
    element = ContractElement.query.get(id)
    if element:
        try:
            data = request.json
        except Exception as e:
            return jsonify({"error": "Invalid JSON payload"}), 400

        element.name = data.get('name', element.name)
        element.is_optional = data.get('is_optional', element.is_optional)

        if isinstance(element, Paragraph):
            element.text = data.get('text', element.text)
        elif isinstance(element, Image):
            element.url = data.get('url', element.url)
        elif isinstance(element, InputField):
            input_types = ['phone', 'signature', 'email', 'address', 'name']

            element.label = data.get('label', element.label)
            input_type = data.get('input_type', element.input_type)
            if input_type not in input_types:
                return jsonify({'error': f'Input type is not supported, supported input types: {input_types}'}), 400
            element.input_type = input_type

        db.session.commit()
        return jsonify(element.to_dict())
    else:
        return jsonify({'error': 'Contract element not found'}), 404

@main.route('/contracts/', methods=['GET'])
def list_contracts():
    contracts = Contract.query.all()
    contracts_list = [contract.to_dict() for contract in contracts]
    return jsonify(contracts_list)

@main.route('/contracts/', methods=['POST'])
def create_contract():
    try:
        data = request.json
    except Exception as e:
        return jsonify({"error": "Invalid JSON payload"}), 400

    employee_id = data.get('employee_id')
    template_id = data.get('template_id')
    contract_data = data.get('contract_data')
    signed_date = datetime.utcnow().date()

    if not contract_data or not isinstance(contract_data, dict):
        return jsonify({"error": "Contract data must be a JSON object"}), 400

    employee = Employee.query.get(employee_id)
    if not employee:
        return jsonify({'error': 'Employee not found'}), 404

    template = ContractTemplate.query.get(template_id)
    if not template:
        return jsonify({'error': 'Contract template not found'}), 404

    template_elements = ContractElement.query.filter(ContractElement.id.in_(template.elements)).all()
    template_input_fields = [element for element in template_elements if isinstance(element, InputField)]

    if len(contract_data.keys()) != len(template_input_fields):
        return jsonify({'error': 'Not enough contract data for input fields'}), 400

    for input_field in template_input_fields:
        field_id = str(input_field.id)
        if field_id not in contract_data or not contract_data.get(field_id):
            return jsonify({'error': f'Missing contract data for input field: {input_field.name}'}), 400

    contract = Contract(employee_id=employee_id, template_id=template_id, contract_data=contract_data, signed_date=signed_date)
    db.session.add(contract)
    db.session.commit()

    return jsonify(contract.to_dict()), 201

@main.route('/contracts/<int:id>', methods=['GET'])
def get_contract(id):
    contract = Contract.query.get(id)
    if contract:
        return jsonify(contract.to_dict())
    else:
        return jsonify({'error': 'Contract not found'}), 404

