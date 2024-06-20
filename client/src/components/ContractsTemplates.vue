<template>
  <div>
    <div class="flex justify-end button-container">
      <button class="btn btn-accent btn-circle mr-4" @click="openEditor()">
        <span class="text-white text-2xl">+</span>
      </button>
    </div>

    <div class="overflow-x-auto">

      <table class="table">
        <thead>
          <tr>
            <th></th>
            <th>Name</th>
            <th>Active</th>
            <th>Created at</th>
            <th>Elements</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="template in templates" :key="template.id">
            <td>{{ template.id }}</td>
            <td>{{ template.name }}</td>
            <td><input type="checkbox" :checked="template.active" class="checkbox checkbox-success" disabled/></td>
            <td>{{ template.created_at }}</td>
            <td>
              <ul>
                <li v-for="element in template.elements" :key="element.id">
                  <span>{{ element.name }} </span> 
                  <template v-if="element.type === 'input_field'">
                    <span>  (<span class="text-green-500 font-bold">{{ element.type }}</span> - <span class="font-bold">{{ element.input_type }}</span>)</span>
                  </template>
                  <template v-else>
                    <span>  (<span class="text-green-500 font-bold">{{ element.type }}</span>)</span>
                  </template>
                </li>
              </ul>
            </td>
            <td>
              <button class="btn btn-circle ml-2" @click="openEditor(template.id)">
                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" id="edit" width="20" height="20"><path fill="none" d="M0 0h24v24H0V0z"></path><path d="M3 17.46v3.04c0 .28.22.5.5.5h3.04c.13 0 .26-.05.35-.15L17.81 9.94l-3.75-3.75L3.15 17.1c-.1.1-.15.22-.15.36zM20.71 7.04c.39-.39.39-1.02 0-1.41l-2.34-2.34c-.39-.39-1.02-.39-1.41 0l-1.83 1.83 3.75 3.75 1.83-1.83z" fill="#aeaeae" class="color000000 svgShape"></path></svg>
              </button>
              <button class="btn btn-circle ml-2" @click="previewTemplate(template)">
                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64" id="RedEye" width="20" height="20"><path fill="none" stroke="#aeaeae" stroke-miterlimit="10" stroke-width="4" d="M32,18c16,0,29,14,29,14S48,46,32,46,3,32,3,32,16,18,32,18Z" class="colorStroke010101 svgStroke"></path><circle cx="32" cy="32" r="14" fill="none" stroke="#aeaeae" stroke-miterlimit="10" stroke-width="4" class="colorStroke010101 svgStroke"></circle><circle cx="32" cy="32" r="2" fill="none" stroke="#aeaeae" stroke-miterlimit="10" stroke-width="4" class="colorStroke010101 svgStroke"></circle></svg>
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Modal Create and Edit-->
    <dialog id="editor_modal" class="modal">
      <div class="editor-box modal-box w-90 w-11 max-w-10xl">
        <ContractsTemplateEditor :elementId="elementId" @close="closeEditor" />  
      </div>
    </dialog>

    <!-- Modal Preview-->
    <dialog id="preview_modal" class="modal">
      <div class="preview-modal-box modal-box w-11 max-w-10xl">
        <h2 class="preview-modal-title text-lg font-bold mb-4">{{ prevTemplateData.name }} preview</h2>
        <div class="preview-content">
          <div class="mb-5" v-for="element in prevTemplateData.elements" :key="element.id">
            <template v-if="element.type === 'input_field'">
              <div class="preview-field mt-10">
                <label class="form-control w-full max-w-xs">
                  <hr>
                  <div class="label">
                    <span class="label-text-alt">{{ element.name }}</span>
                  </div>
                </label>
              </div>
            </template>
            <template v-else-if="element.type === 'image'">
              <img :src="element.url" width="10%" :alt="element.name" class="max-w-xs preview-image">
            </template>
            <template v-else>
              <p class="text-justify">{{ element.text }}</p>
            </template>
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
import ContractsTemplateEditor from './ContractsTemplateEditor.vue';

export default {
  data() {
    return {
      templates: [],
      prevTemplateData: {
        name: '',
        elements: []
      },
      elementId: null,
    };
  },
  components: {
    ContractsTemplateEditor
  },
  created() {
    this.fetchTemplates();
  },
  methods: {
    fetchTemplates() {
      // Make an API call to retrieve the contracts templates
      fetch(process.env.VUE_APP_API_URL + 'contracts/templates/')
        .then(response => response.json())
        .then(data => {
          this.templates = data;
        })
        .catch(error => {
          console.error('Error fetching templates:', error);
        });
    },
    openEditor (templateId) {
      this.templateId = templateId;
      document.getElementById('editor_modal').showModal();
    },
    closeEditor() {
      this.fetchTemplates();
      this.templateId = null;
      document.getElementById('editor_modal').close();
    },
    previewTemplate(template) {
      this.prevTemplateData = { ...template };
      document.getElementById('preview_modal').showModal();
    },
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

.editor-box {
  border-radius: 8px;
  width: 85%;
  max-width: 850px; 
  overflow: auto;
}
</style>
