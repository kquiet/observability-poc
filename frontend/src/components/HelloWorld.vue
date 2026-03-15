<template>
  <div class="card">
    <button type="button" @click="handleClick">hello world count is {{ count }}</button>
  </div>
</template>

<script>
  import { clickCounter } from '../metrics'
  
  export default {
    data() {
      return {
        count: 0, // Store the API response or error message
      };
    },
    methods: {
      handleClick() {
        // Add 1 to the click counter and include labels for context
        clickCounter.add(1, {
          button_type: 'hello_world', // Label to specify the type of button clicked
          user_id: '863',
          environment: 'prod'
        });
        this.count++;
      },
    },
  };
  </script>

<style scoped>
.read-the-docs {
  color: #888;
}
</style>
