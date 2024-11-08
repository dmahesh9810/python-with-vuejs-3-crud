<template>
  <div id="app">
    <h1>Vue.js CRUD Application</h1>
    <CrudApp />
  </div>
</template>

<script>
import CrudApp from './components/CrudApp.vue';

export default {
  name: 'App',
  components: {
    CrudApp
  }
};
</script>

<style>
/* Add styling if needed */
</style>
