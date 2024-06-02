<template>
    <div class="feedback-button" @click="toggleFeedbackForm">
        <img src="https://cdn-icons-png.freepik.com/512/10014/10014906.png" alt="Feedback" className="feedback-icon">
    </div>
    <div v-if="showFeedbackForm" class="feedback-form">
        <h6>Submit feedback!</h6>
      <textarea v-model="feedbackText" placeholder="Enter your feedback"></textarea>
      <button @click="submitFeedback">Submit</button>
    </div>
  </template>
  
  <script>
  import axios from "axios";
  export default {
    name: 'FeedbackButton',
    data() {
      return {
        showFeedbackForm: false,
        feedbackText: ''
      };
    },
    methods: {
      toggleFeedbackForm() {
        this.showFeedbackForm = !this.showFeedbackForm;
      },
      async submitFeedback() {
        var payload = {'feedback': this.feedbackText}
        await axios.post("/api/submitFeedback",payload).then((res) => {
                console.log(res);
                if (res.status == 200) {
                    alert("Feedback submitted Successfully");
                }
            }).catch((err) => {
                console.log(err);
            });    
        // Optionally, you can clear the feedback text and hide the form after submission
        this.feedbackText = '';
        this.showFeedbackForm = false;
      }
    }
  };
  </script>
  
  
  <style scoped>
  .feedback-button {
    position: fixed;
    bottom: 20px;
    right: 25px;
    cursor: pointer;
    z-index: 9999;
  }
  
  .feedback-icon {
    width: 60px;
    height: 60px;
  }
  
  .feedback-form {
    position: fixed;
    bottom: 80px;
    right: 30px;
    background-color: #fff;
    border: 1px solid #ccc;
    padding: 20px;
    box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
    z-index: 9998;
  }
  
  .feedback-form textarea {
    width: 100%;
    height: 100px;
    margin-bottom: 10px;
  }
  
  .feedback-form button {
    background-color: #007bff;
    color: #fff;
    border: none;
    padding: 8px 16px;
    cursor: pointer;
  }
  
  .feedback-form button:hover {
    background-color: #0056b3;
  }
  </style>