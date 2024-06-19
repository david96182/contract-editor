<template>
  <div class="templates">
    <ContractsTemplates/>
  </div>
</template>

<script>
// @ is an alias to /src
import ContractsTemplates from '@/components/ContractsTemplates.vue'

export default {
  name: 'TemplatesView',
  components: {
    ContractsTemplates
  }
}
</script>

