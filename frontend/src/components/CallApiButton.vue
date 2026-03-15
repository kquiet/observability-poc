<!-- src/components/FetchDataButton.vue -->
<template>
    <div>
      <button @click="handleClick">/backend/beats/</button>
      <input
        type="text"
        v-model="inputValue"
        @input="validateNumericInput"
        placeholder="Enter a number"
      />
      <div v-if="data">
        <h2>Response Data:</h2>
        <pre>{{ data }}</pre>
      </div>
    </div>
  </template>
  
  <script>
  import apiService from '../services/apiService.js';
  import { clickCounter } from '../metrics'
  import { tracer } from '../traces';
  
  export default {
    data() {
      return {
        inputValue: '123', // Store the numeric input value here
        data: null, // Store the API response or error message
      };
    },
    methods: {
      validateNumericInput() {
        // Allow only numeric characters in the input
        this.inputValue = this.inputValue.replace(/[^0-9]/g, '');
      },
      handleClick() {
        // Use startActiveSpan to automatically manage the span's lifecycle and add attributes
        tracer.startActiveSpan('click_counter_increment', span => {
          // Set attributes on the span for additional context
          span.setAttributes({
            component: 'CallApiButton',
            button_type: 'call_api',
            user_id: this.inputValue,
            environment: 'prod'
          });

          // Add 1 to the click counter and include labels for context
          clickCounter.add(1, {
            button_type: 'call_api', // Label to specify the type of button clicked
            user_id: this.inputValue, // Example label with a user ID or other context
            environment: 'prod'
          });

          span.end();
        });

        this.callApi();
      },
      async callApi() {
        try {
          const response = await apiService.callApi(this.inputValue);
          this.data = response.data;
        } catch (error) {
          if (error.response) {
            // HTTP error with status code
            this.data = `Error ${error.response.status}: ${error.response.statusText}`;
          } else {
            // Non-HTTP error (e.g., network error)
            this.data = `Error: ${error.message}`;
          }
        }
      },
    },
  };
  </script>
  
  <style scoped>
  /* Add any component-specific styles here */
  </style>
  