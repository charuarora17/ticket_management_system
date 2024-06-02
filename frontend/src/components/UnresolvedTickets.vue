<template>
    <div class="container">
      <h2 class="ticket-title">Unresolved Tickets</h2>
      <ul class="notification-list">
        <li v-for="(notification, index) in notifications" :key="index" class="notification-item">
          <div class="ticket-info">
            <strong>Ticket ID:</strong> {{ notification.ticket_id }}
          </div>
          <div class="creation-date">
            <strong>Creation Date:</strong> {{ notification.creation_date }}
          </div>
          <RouterLink :to="{ name: 'response', params: { ticketId: notification.ticket_id } }" class="resolve-button">
            <strong>Resolve</strong>
          </RouterLink>
        </li>
      </ul>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  
  export default {
    data() {
      return {
        notifications: [] // Array to store notifications received from the backend
      };
    },
    mounted() {
      this.fetchUnresolvedTickets();
    },
    methods: {
      async fetchUnresolvedTickets() {
        try {
          // Fetch unresolved tickets from backend
          const response = await axios.get('/api/notifications/unresolved_tickets');
          this.notifications = response.data.notifications.map(notification => {
            // Parse the notification message to extract ticket ID and creation date
            const matches = notification.match(/Ticket ID (\d+) created on (.+) is still unresolved\./);
            if (matches && matches.length === 3) {
              return {
                ticket_id: matches[1],
                creation_date: matches[2]
              };
            }
            return null;
          }).filter(notification => notification !== null);
        } catch (error) {
          console.error('Error fetching unresolved tickets:', error);
        }
      }
    }
  };
  </script>
  
  <style scoped>
  .container {
    margin: 33px 63px;
  }
  
  .ticket-title {
    font-weight: bold;
    font-size: 25px;
  }
  
  .notification-list {
    list-style-type: none;
    padding: 0;
  }
  
  .notification-item {
    margin-bottom: 20px;
    background-color: #f0f0f0;
    padding: 15px;
    border-radius: 5px;
  }
  
  .ticket-info {
    font-weight: bold;
  }
  
  .creation-date {
    margin-top: 5px;
  }
  
  .resolve-button {
    display: inline-block;
    padding: 8px 12px;
    background-color: #007bff;
    color: #fff;
    text-decoration: none;
    border-radius: 5px;
    cursor: pointer;
  }
  
  .resolve-button:hover {
    background-color: #0056b3;
  }
  </style>
  