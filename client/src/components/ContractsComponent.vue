<template>
  <div>
    <div class="flex justify-end button-container">
      <button class="btn btn-accent btn-circle mr-4" @click="openCreator()">
        <span class="text-white text-2xl">+</span>
      </button>
    </div>

    <div class="overflow-x-auto">

      <table class="table">
        <thead>
          <tr>
            <th></th>
            <th>Template</th>
            <th>Employee</th>
            <th>Signed at</th>
            <th>Data</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="contract in contracts" :key="contract.id">
            <td>{{ contract.id }}</td>
            <td>{{ contract.templateName }}</td>
            <td>{{ contract.employeeName }}</td>
            <td>{{ formatDate(contract.signed_date) }}</td>
            <td>
              <ul>
                 <li v-for="(value, key) in contract.contract_data" :key="key">
                  <template v-if="findElementByKey(key)">
                    <span>{{ findElementByKey(key).name }} (<span class="text-green-500 font-bold">{{ findElementByKey(key).type }}</span> - <span class="font-bold">{{ findElementByKey(key).input_type }}</span>)</span>
                  </template>
                  : {{ value }}
                </li>
              </ul>
            </td>
            <td>
              <button class="btn btn-circle ml-2" @click="previewContract(contract.id)">
                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64" id="RedEye" width="20" height="20"><path fill="none" stroke="#aeaeae" stroke-miterlimit="10" stroke-width="4" d="M32,18c16,0,29,14,29,14S48,46,32,46,3,32,3,32,16,18,32,18Z" class="colorStroke010101 svgStroke"></path><circle cx="32" cy="32" r="14" fill="none" stroke="#aeaeae" stroke-miterlimit="10" stroke-width="4" class="colorStroke010101 svgStroke"></circle><circle cx="32" cy="32" r="2" fill="none" stroke="#aeaeae" stroke-miterlimit="10" stroke-width="4" class="colorStroke010101 svgStroke"></circle></svg>
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Modal Create-->
    <dialog id="create_modal" class="modal">
      <div class="create-modal-box modal-box w-11 max-w-10xl">
        <h2 class="preview-modal-title text-lg font-bold mb-4">Sign Contract </h2>
        <form @submit.prevent="createContract" class="flex flex-col items-center">
          <div class="form-control mb-4">
            <label class="form-control w-full max-w-xs">
              <div class="label">
                <span class="label-text">Employee</span>
              </div>
              <select class="select select-bordered" v-model="selectedEmployee" required>
                <option disabled selected>Pick one</option>
                <option v-for="employee in employees" :value="employee.id">{{ employee.name }}</option>
              </select>
            </label>
          </div>

          <div class="form-control mb-4">
            <label class="form-control w-full max-w-xs">
              <div class="label">
                <span class="label-text">Template</span>
              </div>
              <select class="select select-bordered" v-model="selectedTemplate" required>
                <option disabled selected>Pick one</option>
                <option v-for="template in templates" :value="template">{{ template.name }}</option>
              </select>
            </label>
          </div>

          <div v-if="selectedTemplate.name">
            <div class="contract-content">
              <div class="mb-5" v-for="element in selectedTemplate.elements" :key="element.id">
                <template v-if="element.type === 'input_field'">
                  <div class="preview-field mt-10">
                    <label class="form-control w-full max-w-xs">
                      <p v-if="element.input_type === 'signature'">
                        <Vue3Signature sigOption="" :w="'300px'" :h="'80px'"
                                         class="example"></Vue3Signature>
                      </p>
                      <p v-else>
                        <textarea class="textarea input_field" :id="element.id" required></textarea>
                      </p>
                      <hr>
                      <div class="label">
                        <span class="label-text-alt">{{ element.name }}</span>
                      </div>
                    </label>
                  </div>
                </template>
                <contract v-else-if="element.type === 'image'">
                  <img :src="element.url" width="10%" :alt="element.name" class="max-w-xs preview-image">
                </contract>
                <contract v-else>
                  <p class="text-justify">{{ element.text }}</p>
                </contract>
              </div>
            </div>
          </div>
          

          <div class="flex justify-end">
            <button class="btn btn-accent mr-2" type="submit">Sign</button>
            <button class="btn btn-ghost" @click="closeCreate">Cancel</button>
          </div>
        </form>
      </div>
    </dialog>

    <!-- Modal Preview-->
    <dialog id="preview_modal" class="modal">
      <div class="preview-modal-box modal-box w-11 max-w-10xl">
        <h2 class="preview-modal-title text-lg font-bold mb-4">{{ prevtemplateData.name }}: {{ prevtemplateData.employee }} </h2>
        <div class="preview-content">
          <div class="mb-5" v-for="element in prevtemplateData.elements" :key="element.id">
            <contract v-if="element.type === 'input_field'">
              <div class="preview-field mt-10">
                <label class="form-control w-full max-w-xs">
                  <p v-if="element.input_type === 'signature'">
                    <img :src="element.data" width="25%" :alt="element.name" class="max-w-xs preview-image">
                  </p>
                  <p v-else>
                    <b>{{ element.data }}</b>
                  </p>
                  <hr>
                  <div class="label">
                    <span class="label-text-alt">{{ element.name }}</span>
                  </div>
                </label>
              </div>
            </contract>
            <contract v-else-if="element.type === 'image'">
              <img :src="element.url" width="10%" :alt="element.name" class="max-w-xs preview-image">
            </contract>
            <contract v-else>
              <p class="text-justify">{{ element.text }}</p>
            </contract>
          </div>
        </div>
      </div>
      <form method="dialog" class="modal-backdrop">
        <button>close</button>
      </form>
    </dialog>

  </div>
</template>

<script>
export default {
  data() {
    return {
      contracts: [],
      elements: [],
      templates: [],
      employees: [],
      prevtemplateData: {
        name: '',
        elements: [],
        employee: ''
      },
      selectedEmployee: null,
      selectedTemplate: {
        id: '',
        name: '',
        elements: [],
      },
    };
  },
  created() {
    this.fetchElements();
    this.fetchTemplates();
    this.fetchEmployees();
    this.fetchcontracts();
  },
  methods: {
    fetchcontracts() {
      fetch(process.env.VUE_APP_API_URL + 'contracts/')
        .then(response => response.json())
        .then(data => {
          this.contracts = data;

          this.contracts.forEach(contract => {
            this.getTemplateName(contract.template_id)
              .then(name => {
                contract.templateName = name;
              })
              .catch(error => {
                console.error('Error fetching template information:', error);
              });

            this.getEmployeeName(contract.employee_id)
              .then(name => {
                contract.employeeName = name;
              })
              .catch(error => {
                console.error('Error fetching employee information:', error);
              });
          });
        })
        .catch(error => {
          console.error('Error fetching contracts:', error);
        });
    },
    fetchElements() {
      fetch(process.env.VUE_APP_API_URL + 'contracts/templates/elements')
        .then(response => response.json())
        .then(data => {
          this.elements = data;
        })
        .catch(error => {
          console.error('Error fetching templates:', error);
        });
    },
    fetchTemplates() {
      fetch(process.env.VUE_APP_API_URL + 'contracts/templates/')
        .then(response => response.json())
        .then(data => {
          const activeTemplates = data.filter(template => template.active);
          this.templates = activeTemplates;
        })
        .catch(error => {
          console.error('Error fetching templates:', error);
        });
    },
    fetchEmployees() {
      fetch(process.env.VUE_APP_API_URL + 'employees/')
        .then(response => response.json())
        .then(data => {
          this.employees = data;
        })
        .catch(error => {
          console.error('Error fetching employees:', error);
        });
    },
    getTemplateById(template_id) {
      return fetch(process.env.VUE_APP_API_URL + `contracts/templates/${template_id}`)
        .then(response => response.json())
        .then(data => {
          return data;
        })
        .catch(error => {
          console.error('Error fetching template information:', error);
        });
    },
    getTemplateName(template_id) {
      return fetch(process.env.VUE_APP_API_URL + `contracts/templates/${template_id}`)
        .then(response => response.json())
        .then(data => {
          return data.name;
        })
        .catch(error => {
          console.error('Error fetching template information:', error);
        });
    },
    getEmployeeName(employee_id) {
      return fetch(process.env.VUE_APP_API_URL + `employees/${employee_id}`)
        .then(response => response.json())
        .then(data => {
          return data.name;
        })
        .catch(error => {
          console.error('Error fetching template information:', error);
        });
    },
    formatDate(dateString) {
      return new Date(dateString).toLocaleDateString();
    },
    openCreator () {
      document.getElementById('create_modal').showModal();
    },
    closeCreate() {
      this.selectedEmployee = null;
      this.selectedEmployee = {
        id: '',
        name: '',
        elements: [],
      };
      this.prevtemplateData = {
        name: '',
        elements: [],
        employee: ''
      };
      this.fetchcontracts();
      document.getElementById('create_modal').close();
    },
    previewContract(contract_id) {
      const contract = this.contracts.find(c => c.id === contract_id);

      if (contract) {
        this.prevtemplateData.name = null;
        this.prevtemplateData.elements = [];
        this.getEmployeeName(contract.employee_id)
          .then( employee => {
            this.prevtemplateData.employee = employee   
          });

        this.getTemplateById(contract.template_id)
          .then(template => {
            this.prevtemplateData.name = template.name;
            template.elements.forEach(element => {
              const contractData = contract.contract_data[element.id];
              const updatedElement = { ...element, data: contractData };
              this.prevtemplateData.elements.push(updatedElement);
            });
          })
          .catch(error => {
            console.error('Error fetching template:', error);
          });
      } else {
        console.error('Contract not found');
      }
      
      document.getElementById('preview_modal').showModal();
    },
    findElementByKey(key) {
      return this.elements.find(element => element.id == key);
    },
    createContract() {
      const inputFields = document.getElementsByClassName('input_field');
      
      let contract_data = {}
      this.selectedTemplate.elements.forEach((element) => {
        if (element.type === 'input_field') {
          if (element.input_type === 'signature') {
            contract_data[element.id] = 'https://i.imgur.com/AvYlBf5.png'; 
          } else {
            const inputField = document.getElementById(element.id); // Get the text input field by its ID
            if (inputField) {
              contract_data[element.id] = inputField.value; // Retrieve the value from the input field and assign it to contract_data[element.id]
          }
        }
        }
      });

      const employee_id = this.selectedEmployee;
      const template_id = this.selectedTemplate.id;

      fetch(process.env.VUE_APP_API_URL + 'contracts/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          employee_id: employee_id,
          template_id: template_id,
          contract_data: contract_data
        }),
      })
        .then(response => response.json())
        .then(data => {
          this.contracts.push(data);
          this.closeCreate();
        })
        .catch(error => {
          console.error('Error creating contract:', error);
        });
    }
  },
};
</script>

<style scoped lang="scss">
table {
  width: 75%;
  border-collapse: collapse;
  margin-top: 20px;
  margin: 0 auto;
}
.table th,
.table td {
  padding: 8px;
  text-align: left;
}
.button-container {
  width: 90%;
}
#preview-modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5); /* Semi-transparent background */
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000; /* Ensure modal is on top of other content */
}
.preview-modal-box {
  background-color: #fff; /* White background */
  border: 1px solid #ccc; /* Light gray border */
  padding: 20px;
  border-radius: 8px;
  width: 90%;
  max-width: 800px; /* Limit maximum width */
  overflow: auto; /* Enable scrolling if content exceeds dimensions */
  font-family: Arial, sans-serif; /* Set font family to Arial */
  font-size: 11px; /* Set font size to 11px */
  line-height: 1.5; /* Set line height for readability */
}

.preview-modal-title {
  font-size: 18px; /* Larger font size for title */
  font-weight: bold;
  margin-bottom: 10px;
}

.preview-content {
  margin-top: 10px;
}

.preview-field {
  margin-bottom: 15px;
}

.preview-label {
  display: inline-block;
  width: 120px; /* Adjust width as needed */
  font-weight: bold;
}

.preview-input {
  width: calc(100% - 130px); /* Adjust width accounting for label width */
  padding: 5px;
  font-size: inherit; /* Inherit font size */
  border: 1px solid #ccc;
  border-radius: 4px;
  box-sizing: border-box;
}

.preview-image {
  max-width: 100%;
  height: auto;
  display: block;
  margin-top: 10px;
}

.preview-modal-backdrop {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: transparent; /* Transparent background for backdrop */
  display: flex;
  justify-content: center;
  align-items: center;
}

.preview-modal-backdrop button {
  padding: 10px 20px;
  background-color: #007bff; /* Blue background */
  color: #fff; /* White text */
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 14px; /* Larger font size for button */
}

.preview-modal-backdrop button:hover {
  background-color: #0056b3; /* Darker blue on hover */
}

#create_modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5); /* Semi-transparent background */
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.contract-content {
  background-color: #fff; /* White background */
  border: 1px solid #ccc; /* Light gray border */
  padding: 20px;
  border-radius: 8px;
  width: 100%;
  max-width: 1200px; /* Limit maximum width */
  overflow: auto; 
  font-family: Arial, sans-serif; 
  font-size: 11px; 
  line-height: 1.5;
  margin-bottom: 10px;
}

.create-modal-box {
  padding: 20px;
  border-radius: 8px;
  width: 90%;
  max-width: 800px; /* Limit maximum width */
  overflow: auto; /* Enable scrolling if content exceeds dimensions */
  font-family: Arial, sans-serif; /* Set font family to Arial */
  font-size: 11px; /* Set font size to 11px */
  line-height: 1.5; /* Set line height for readability */
}

.contract-content hr {
  border: none;
  border-top: 1px solid #ccc; /* Gray horizontal line */
  margin: 10px 0; /* Space above and below the line */
}

.contract-content label {
  display: block;
  margin-bottom: 5px;
}

.contract-content p {
  margin-bottom: 10px;
}

.contract-content b {
  font-weight: bold;
}

.contract-content .preview-field {
  margin-bottom: 15px;
}

.contract-content .preview-image {
  max-width: 100%;
  height: auto;
  display: block;
  margin-top: 10px;
}

.contract-content .label-text-alt {
  font-weight: bold;
}

.contract-content .text-justify {
  text-align: justify;
}


</style>
