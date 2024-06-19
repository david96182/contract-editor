<template>
  <div>
    <div class="flex justify-end button-container">
      <button class="btn btn-accent btn-circle mr-4" onclick="form_modal.showModal()">
        <span class="text-white text-2xl">+</span>
      </button>
    </div>

    <div class="overflow-x-auto">

      <table class="table">
        <thead>
          <tr>
            <th></th>
            <th>Name</th>
            <th>Email</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="employee in employees" :key="employee.id">
            <td>{{ employee.id }}</td>
            <td>{{ employee.name }}</td>
            <td>{{ employee.email }}</td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Modal -->
    <dialog id="form_modal" class="modal">
      <div class="modal-box">
        <h2 class="text-lg font-bold mb-4">Add Employee</h2>
        <form @submit.prevent="createEmployee" class="flex flex-col items-center">
          <div class="form-control mb-4">
            <label for="name" class="label">Name:</label>
            <input class="input input-bordered focus:ring-accent w-full max-w-xs" type="text" id="name" v-model="newEmployee.name" required>
          </div>
          <div class="form-control mb-4">
            <label for="email" class="label">Email:</label>
            <input class="input input-bordered focus:ring-accent w-full max-w-xs" type="email" id="email" v-model="newEmployee.email" required>
          </div>
          <div class="flex justify-end">
            <button class="btn btn-accent mr-2" type="submit">Save</button>
            <button class="btn btn-ghost" @click="closeModal">Cancel</button>
          </div>
        </form>
      </div>
    </dialog>

  </div>

</template>

<script>
export default {
  data() {
    return {
      employees: [],
      newEmployee: {
        name: '',
        email: '',
      },
    };
  },
  created() {
    this.fetchEmployees();
  },
  methods: {
    fetchEmployees() {
      // Make an API call to retrieve the employees
      fetch(process.env.VUE_APP_API_URL + 'employees/')
        .then(response => response.json())
        .then(data => {
          this.employees = data;
        })
        .catch(error => {
          console.error('Error fetching employees:', error);
        });
    },
    createEmployee() {
      // Make an API call to create a new employee
      fetch(process.env.VUE_APP_API_URL + 'employees/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          company_id: 1, 
          name: this.newEmployee.name,
          email: this.newEmployee.email,
        }),
      })
        .then(response => response.json())
        .then(data => {
          // Handle the created employee
          this.employees.push(data);
          this.closeModal();
        })
        .catch(error => {
          console.error('Error creating employee:', error);
        });
    },
    closeModal() {
      // Clear form data and close the modal
      this.newEmployee.name = '';
      this.newEmployee.email = '';
      document.getElementById('form_modal').close();
    },
  },
};
</script>

<style scoped lang="scss">
table {
  width: 70%;
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

</style>
