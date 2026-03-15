<!-- src/views/HomeView.vue -->
<template>
    <div>
      <h1>poc-frontend</h1>
      <HelloWorld />
      <CallApiButton />
    </div>
  </template>
  
  <script>
  import HelloWorld from '../components/HelloWorld.vue';
  import CallApiButton from '../components/CallApiButton.vue';

  export default {
    components: {
        HelloWorld,
        CallApiButton,
    },
  };
  </script>
  
  <style scoped>
  /* Styles for the home page */
  </style>
  