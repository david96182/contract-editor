# API

This is the backend API of the application, created with Flask and Postgres. It provides endpoints for creating, retrieving, updating, and sign contracts and contracts templates.

## Environment Variables

To run this project, you will need to add the following environment variables to your `.env` file:

```
SECRET_KEY=<Your-Secret-Key>
DEV_DATABASE_URL=postgresql://username:password@localhost/dbname
TEST_DATABASE_URL=postgresql://username:password@localhost/dbname
DATABASE_URL=postgresql://username:password@localhost/dbname
```

In the project folder there is a .env.example that has the exact structure. You could rename the file to .env(removing the .example) and set your specific settings.

## Project Setup

You must have Python installed on your machine. You can download it and follow the instructions on the

Before running the project, you need to install the dependencies. You can do this by running:

```
pip install -r requirements.txt
```

To start the server, you can run:

```
python manage.py run
```

## API Endpoints

The API has the following endpoints, all prefixed with `/api`:

#### 1. `GET /ping`

- **Description:** A simple endpoint to check if the server is running.
- **Functionality:** Returns a string "pong!" indicating that the server is active.

#### 2. `GET /companies/`

- **Description:** Lists all companies stored in the database.
- **Functionality:** Retrieves all companies from the database and returns their details in JSON format.

#### 3. `GET /employees/`

- **Description:** Lists all employees stored in the database.
- **Functionality:** Retrieves all employees from the database and returns their details in JSON format.

#### 4. `GET /employees/<int:id>`

- **Description:** Retrieves details of a specific employee.
- **Functionality:** Takes an employee ID as a parameter, retrieves the corresponding employee from the database, and returns their details in JSON format.

#### 5. `POST /employees`

- **Description:** Creates a new employee record.
- **Functionality:** Accepts JSON payload with `company_id`, `name`, and `email` fields. Validates the payload, checks if the company exists, validates email format, and ensures no duplicate emails. If all checks pass, creates a new employee record and returns its details in JSON format.

#### 6. `GET /contracts/templates/`

- **Description:** Lists all contract templates.
- **Functionality:** Retrieves all contract templates from the database and returns their details in JSON format.

#### 7. `GET /contracts/templates/<int:id>`

- **Description:** Retrieves details of a specific contract template.
- **Functionality:** Takes a template ID as a parameter, retrieves the corresponding contract template from the database, and returns its details in JSON format.

#### 8. `POST /contracts/templates/`

- **Description:** Creates a new contract template.
- **Functionality:** Accepts JSON payload with `name`, `active` (optional), and `elements` fields. Validates the payload, checks for existing templates with the same name, validates elements using a custom validator, and creates a new contract template if validation passes. Returns the created template details in JSON format.

#### 9. `PUT /contracts/templates/<int:id>`

- **Description:** Updates details of a specific contract template.
- **Functionality:** Takes a template ID as a parameter, retrieves the corresponding contract template from the database, updates its `name`, `active`, and `elements` fields based on the JSON payload. Validates the elements using a custom validator and updates the template in the database. Returns the updated template details in JSON format.

#### 10. `GET /contracts/templates/elements/`

- **Description:** Lists all contract elements.
- **Functionality:** Retrieves all contract elements from the database and returns their details in JSON format.

#### 11. `GET /contracts/templates/elements/<int:id>`

- **Description:** Retrieves details of a specific contract element.
- **Functionality:** Takes an element ID as a parameter, retrieves the corresponding contract element from the database, and returns its details in JSON format.

#### 12. `GET /contracts/templates/elements/types`

- **Description:** Lists supported element types for contract elements.
- **Functionality:** Returns a JSON list of supported element types (`paragraph`, `image`, `input_field`).

#### 13. `GET /contracts/templates/elements/type/<string:name>`

- **Description:** Lists contract elements of a specific type.
- **Functionality:** Takes an element type (`paragraph`, `image`, `input_field`) as a parameter, retrieves all contract elements of that type from the database, and returns their details in JSON format.

#### 14. `POST /contracts/templates/elements`

- **Description:** Creates a new contract element.
- **Functionality:** Accepts JSON payload with `element_type`, `name`, `is_optional` (optional), and additional fields based on the `element_type`. Validates the payload, checks for existing elements with the same name, creates a new contract element of the specified type, and returns its details in JSON format.

#### 15. `PUT /contracts/templates/elements/<int:id>`

- **Description:** Updates details of a specific contract element.
- **Functionality:** Takes an element ID as a parameter, retrieves the corresponding contract element from the database, updates its details based on the JSON payload, and returns the updated element details in JSON format.

#### 16. `GET /contracts/`

- **Description:** Lists all contracts.
- **Functionality:** Retrieves all contracts from the database and returns their details in JSON format.

#### 17. `POST /contracts/`

- **Description:** Creates a new contract.
- **Functionality:** Accepts JSON payload with `employee_id`, `template_id`, `contract_data`, and automatically sets the `signed_date` to the current date. Validates the payload, checks if the employee and template exist, validates the contract data against template input fields, creates a new contract record, and returns its details in JSON format.

#### 18. `GET /contracts/<int:id>`

- **Description:** Retrieves details of a specific contract.
- **Functionality:** Takes a contract ID as a parameter, retrieves the corresponding contract from the database, and returns its details in JSON format.

## Models

**Company**

Represents a company entity with attributes:

- `id`: Unique identifier for the company.
- `name`: Name of the company.
- `address`: Address of the company.

**Employee**

Represents an employee associated with a company. Attributes include:

- `id`: Unique identifier for the employee.
- `company_id`: Foreign key referencing the company the employee belongs to.
- `name`: Name of the employee.
- `email`: Email address of the employee.

**ContractTemplate**

Represents a template for contracts with attributes:

- `id`: Unique identifier for the contract template.
- `name`: Name of the contract template.
- `active`: Boolean indicating whether the template is active.
- `created_at`: Timestamp indicating when the template was created.
- `elements`: Array of integers representing IDs of associated contract elements.

**ContractElement**

Base class for different types of contract elements, with attributes:

- `id`: Unique identifier for the contract element.
- `name`: Name of the contract element.
- `is_optional`: Boolean indicating whether the element is optional.
- `element_type`: Type of the contract element (`paragraph`, `image`, `input_field`).

**Paragraph**

Subclass of `ContractElement` representing a paragraph element, with attributes:

- `id`: Unique identifier for the paragraph element.
- `text`: Text content of the paragraph.

**Image**

Subclass of `ContractElement` representing an image element, with attributes:

- `id`: Unique identifier for the image element.
- `url`: URL of the image.

**InputField**

Subclass of `ContractElement` representing an input field element, with attributes:

- `id`: Unique identifier for the input field element.
- `label`: Label for the input field.
- `input_type`: Type of input for the field (text, signature, address, phone, email).

**Contract**

Represents a contract instance with attributes:

- `id`: Unique identifier for the contract.
- `employee_id`: Foreign key referencing the employee associated with the contract.
- `template_id`: Foreign key referencing the contract template used for the contract.
- `contract_data`: JSON data representing the contract details.
- `signed_date`: Date when the contract was signed.


## Testing

To run the tests, you can use the `pytest --cov` command.
