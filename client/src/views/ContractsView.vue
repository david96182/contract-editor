<template>
  <div class="contracts">
    <ContractsComponent/>
  </div>
</template>

<script>
// @ is an alias to /src
import ContractsComponent from '@/components/ContractsComponent'

export default {
  name: 'ContractsView',
  components: {
    ContractsComponent
  }
}
</script>
