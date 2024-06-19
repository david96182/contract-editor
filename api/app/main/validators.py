from ..models import ContractElement

def validate_contract_elements(elements):
    if len(elements) != len(set(elements)):
        return {'error': 'Duplicate elements are not allowed'}

    existing_elements = ContractElement.query.filter(ContractElement.id.in_(elements)).all()
    existing_element_ids = {element.id for element in existing_elements}

    if len(existing_element_ids) != len(elements):
        missing_element_ids = [element_id for element_id in elements if element_id not in existing_element_ids]
        return {'error': f"Invalid element IDs(doesn`t exist): {', '.join(map(str, missing_element_ids))}"} 

    if len(elements) < 3:
        return {'error': 'A contract template must have at least three elements'}

    paragraph_count = 0
    signature_count = 0

    for element in existing_elements:
        if not element.is_optional:
            if element.element_type == 'paragraph':
                paragraph_count += 1
            elif element.element_type == 'input_field' and element.input_type == 'signature':
                signature_count += 1

    if paragraph_count < 2:
        return {'error': 'A contract template must have at least two paragraphs non optionals'}
    if signature_count < 1:
        return {'error': 'A contract template must have at least one input field of type "signature" non optional'}

    return None
