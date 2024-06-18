from datetime import datetime
from sqlalchemy import UniqueConstraint
from . import db

class Company(db.Model):
    __tablename__ = 'companies'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(200), nullable=False)
    
    def to_dict(self):
        return {
            'company_id': self.id,
            'name': self.name,
            'address': self.address
        }

class Employee(db.Model):
    __tablename__ = 'employees'
    
    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey('companies.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)

    __table_args__ = (UniqueConstraint('email', name='_employee_email_uc'),)
    
    def to_dict(self):
        return {
            'id': self.id,
            'company_id': self.company_id,
            'name': self.name,
            'email': self.email
        }

class ContractTemplate(db.Model):
    __tablename__ = 'contract_templates'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    active = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    
    elements = db.Column(db.ARRAY(db.Integer), nullable=False)

    __table_args__ = (UniqueConstraint('name', name='_contract_template_name_uc'),)
    
    def to_dict(self):
        element_mapping = {element.id: element.to_dict() for element in ContractElement.query.filter(ContractElement.id.in_(self.elements)).all()}
        element_dicts = [element_mapping[element_id] for element_id in self.elements]

        return {
            'id': self.id,
            'name': self.name,
            'active': self.active,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'elements': element_dicts
        }

class ContractElement(db.Model):
    __tablename__ = 'contract_elements'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    is_optional = db.Column(db.Boolean, default=True)
    element_type = db.Column(db.String(20), nullable=False)  # 'paragraph', 'image', 'input_field'

    __table_args__ = (UniqueConstraint('name', name='_contract_element_name_uc'),)
    
    __mapper_args__ = {
        'polymorphic_on': element_type,
        'polymorphic_identity': 'contract_element'
    }

    def to_dict(self):
        raise NotImplementedError("to_dict method should be implemented in subclasses")

class Paragraph(ContractElement):
    __tablename__ = 'paragraphs'
    
    id = db.Column(db.Integer, db.ForeignKey('contract_elements.id'), primary_key=True)
    text = db.Column(db.Text, nullable=False)
    
    __mapper_args__ = {
        'polymorphic_identity': 'paragraph'
    }
    
    def to_dict(self):
        return {
            'id': self.id,
            'type': self.element_type,
            'name': self.name,
            'text': self.text,
            'is_optional': self.is_optional
        }

class Image(ContractElement):
    __tablename__ = 'images'
    
    id = db.Column(db.Integer, db.ForeignKey('contract_elements.id'), primary_key=True)
    url = db.Column(db.String(200), nullable=False)
    
    __mapper_args__ = {
        'polymorphic_identity': 'image'
    }
    
    def to_dict(self):
        return {
            'id': self.id,
            'type': self.element_type,
            'name': self.name,
            'url': self.url,
            'is_optional': self.is_optional
        }

class InputField(ContractElement):
    __tablename__ = 'input_fields'
    
    id = db.Column(db.Integer, db.ForeignKey('contract_elements.id'), primary_key=True)
    label = db.Column(db.String(100), nullable=False)
    input_type = db.Column(db.String(100), nullable=False)
    
    __mapper_args__ = {
        'polymorphic_identity': 'input_field'
    }
    
    def to_dict(self):
        return {
            'id': self.id,
            'type': self.element_type,
            'name': self.name,
            'label': self.label,
            'input_type': self.input_type,
            'is_optional': self.is_optional
        }

class Contract(db.Model):
    __tablename__ = 'contracts'
    
    id = db.Column(db.Integer, primary_key=True)
    employer_id = db.Column(db.Integer, db.ForeignKey('employees.id'), nullable=False)
    template_id = db.Column(db.Integer, db.ForeignKey('contract_templates.id'), nullable=False)
    contract_data = db.Column(db.JSON, nullable=False) 
    signed_date = db.Column(db.Date, nullable=False)
    
    def to_dict(self):
        return {
            'id': self.id,
            'employer_id': self.employer_id,
            'template_id': self.template_id,
            'contract_data': self.contract_data,
            'signed_date': self.signed_date
        }

