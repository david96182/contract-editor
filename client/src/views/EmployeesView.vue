<template>
  <div class="employees">
    <EmployeesComponent/>
  </div>
</template>

<script>
// @ is an alias to /src
import EmployeesComponent from '@/components/EmployeesComponent.vue'

export default {
  name: 'EmployeesView',
  components: {
    EmployeesComponent
  }
}
</script>
