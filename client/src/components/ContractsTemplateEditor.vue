<template>
  <h2 class="text-lg font-bold mb-4">{{ isCreateView ? 'Create Template' : 'Edit Template' }}</h2>
  <form @submit.prevent="" class="flex flex-col items-center">
    <div class="form-control mb-4">
      <label for="name" class="label">Name:</label>
      <input class="input input-bordered focus:ring-accent w-full max-w-xs" type="text" id="name" v-model="newTemplate.name" required>
    </div>
    
    <div class="form-control">
      <label class="cursor-pointer label">
        <p class="label-text">Active </p>
        <input type="checkbox" checked="checked" class="checkbox checkbox-accent" v-model="newTemplate.active" />
      </label>
    </div>

    <div class="form-control mt-5 ">
      <span >Elements: </span>
      <div class="mb-2" v-for="element in newTemplate.elements" :value="element">
            
        <div v-if="element.type === 'paragraph'" class="card w-96 bg-neutral text-neutral-content">
          <div class="card-body items-center text-center">
            <h2 class="card-title">{{ element.name }}</h2>
            <p>{{ element.text }}</p>
            <div class="card-actions justify-end">
              <p v-if="element.is_optional">This element is optional.</p>
              <p v-else>This element is mandatory.</p>
            </div>
          </div>
        </div>

        <div v-else-if="element.type === 'image'" class="card w-96 bg-neutral text-neutral-content">
          <div class="card-body items-center text-center">
            <h2 class="card-title">{{ element.name }}</h2>
            <img :src="element.url" alt="Preview Image" />
            <div class="card-actions justify-end">
              <p v-if="element.is_optional">This element is optional.</p>
              <p v-else>This element is mandatory.</p>
            </div>
          </div>
        </div>

        <div v-else-if="element.type === 'input_field'" class="card w-96 bg-neutral text-neutral-content">
          <div class="card-body items-center text-center">
            <h2 class="card-title">{{ element.name }}</h2>
            <label>{{ element.label }}</label>
            <input :type="element.input_type" />
            <div class="card-actions justify-end">
              <p v-if="element.is_optional">This element is optional.</p>
              <p v-else>This element is mandatory.</p>
            </div>
          </div>
        </div>

      </div> 
      <button class="btn btn-accent btn-circle mr-4" style="margin: 0 auto;" @click="openAddElementModal">
        <span class="text-white text-2xl">+</span>
      </button>
    </div>

    <div class="flex justify-end mt-5">
      <button class="btn btn-accent mr-2" type="submit" @click="createTemplate">Save</button>
      <button class="btn btn-ghost" @click="closeModal">Cancel</button>
    </div>
  </form>
  
  <!-- Add Element Modal-->
  <dialog id="add_modal" class="modal">
    <div class="modal-box">
      <h2 class="text-lg font-bold mb-4">Select Element</h2>
      <form @submit.prevent="addElement" class="flex flex-col items-center">
        <div class="form-control mb-4">
          <label class="form-control w-full max-w-xs">
            <div class="label">
              <span class="label-text">Type</span>
            </div>
            <select class="select select-bordered" v-model="selectedType">
              <option disabled selected>Pick one</option>
              <option v-for="element in elementTypes" :value="element">{{ element }}</option>
            </select>
          </label>
        </div>
        <div class="form-control mb-4">
          <label class="label">Elements</label>
          <select class="select select-bordered" v-model="selectedElement">
            <option disabled selected>Select an element</option>
            <option v-for="element in filteredElements" :value="element">{{ element.name }}</option>
          </select>
        </div>
        <div v-if="selectedElement" class="form-control mb-4">
          <label class="label">Preview:</label>
          <div class="preview">
            
            <div v-if="selectedElement.type === 'paragraph'" class="card  w-96 bg-neutral text-neutral-content">
              <div class="card-body items-center text-center">
                <h2 class="card-title">{{ selectedElement.name }}</h2>
                <p>{{ selectedElement.text }}</p>
                <div class="card-actions justify-end">
                  <p v-if="selectedElement.is_optional">This element is optional.</p>
                  <p v-else>This element is mandatory.</p>
                </div>
              </div>
            </div>

            <div v-else-if="selectedElement.type === 'image'" class="card w-96 bg-neutral text-neutral-content">
              <div class="card-body items-center text-center">
                <h2 class="card-title">{{ selectedElement.name }}</h2>
                <img :src="selectedElement.url" alt="Preview Image" />
                <div class="card-actions justify-end">
                  <p v-if="selectedElement.is_optional">This element is optional.</p>
                  <p v-else>This element is mandatory.</p>
                </div>
              </div>
            </div>

            <div v-else-if="selectedElement.type === 'input_field'" class="card w-96 bg-neutral text-neutral-content">
              <div class="card-body items-center text-center">
                <h2 class="card-title">{{ selectedElement.name }}</h2>
                <label>{{ selectedElement.label }}</label>
                <input :type="selectedElement.input_type" />
                <div class="card-actions justify-end">
                  <p v-if="selectedElement.is_optional">This element is optional.</p>
                  <p v-else>This element is mandatory.</p>
                </div>
              </div>
            </div>

          </div>
        </div>
        <div class="form-control mb-4">
        </div>
        <div class="flex justify-end">
          <button class="btn btn-accent mr-2" type="submit">Add</button>
          <button class="btn btn-ghost" @click="closeAdd">Cancel</button>
        </div>
      </form>
    </div>
  </dialog>
</template>

<script>
export default {
  props: {
    elementId: {
      type: String,
      default: null
    },
  },
  data() {
    return {
      templates: [],
      newTemplate: {
        name: '',
        active: false,
        elements: []
      },
      elementTypes: ['paragraph', 'image', 'input_field'],
      selectedType: null,
      selectedElement: null,
      elements: []
    };
  },
  created() {
    this.fetchElements();
    if (this.elementId) {
    }
  },
  computed: {
    isCreateView() {
      return !this.elementId;
    },
    filteredElements() {
      if (this.selectedType) {
        return this.elements.filter(element => element.type === this.selectedType);
      }
      return [];
    }
  },
  methods: {
    createTemplate() {
      fetch(process.env.VUE_APP_API_URL + 'contracts/templates/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          name: this.newTemplate.name, 
          active: this.newTemplate.active,
          elements: this.newTemplate.elements.map(element => element.id)
        }),
      })
        .then(response => response.json())
        .then(data => {
          this.closeModal();
        })
        .catch(error => {
          console.error('Error creating template:', error);
        });
    },
    updateTemplate() {

    },
    fetchTemplate() {
      fetch(process.env.VUE_APP_API_URL + `contracts/templates/${this.elementId}`)
        .then(response => response.json())
        .then(data => {
          this.newTemplate = data.name;
          this.newTemplate = data.active;
          this.newTemplate = data.elements;
        })
        .catch(error => {
          console.error('Error fetching the template:', error);
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
    closeModal() {
      this.$emit('close');
    },
    openAddElementModal() {
      document.getElementById('add_modal').showModal();
    },
    closeAdd() {
      this.selectedType = null;
      this.selectedElement = null;
      document.getElementById('add_modal').close();
    },
    addElement() {
      if (this.selectedElement) {
        this.newTemplate.elements.push(this.selectedElement);
      }
      this.selectedType = null;
      this.selectedElement = null;
      document.getElementById('add_modal').close();
    }
  },
};
</script>

<style scoped lang="scss">

</style>

