<template>
<div class="container">
    <h2 class="user-title">Flagged Users</h2>
    <ul class="user-list">
    <li v-for="(user, index) in flaggedUsers" :key="index" class="user-item">
        <div class="user-info">
        <strong>User ID:</strong> {{ user.user_id }}
        </div>
        <div class="user-details">
        <strong>User Name:</strong> {{ user.user_name }} <br>
        <strong>Email:</strong> {{ user.email_id }} <br>
        <strong>Flag Count:</strong> {{ user.flag_count }}
        </div>
        <button @click="fetchFlaggedPosts(user.user_id)">View Flagged Posts</button>
        <ul v-if="user.flaggedPosts && user.flaggedPosts.length" class="flagged-posts">
        <li v-for="(post, idx) in user.flaggedPosts" :key="idx" class="post-item">
            <div class="post-info">
            <strong>Ticket ID:</strong> {{ post.ticket_id }}
            </div>
            <div class="post-details">
            <strong>Title:</strong> {{ post.title }} <br>
            <strong>Description:</strong> {{ post.description }}
            </div>
        </li>
        </ul>
        <button @click="blockAndDisableUser(user.user_id)">Block User & Disable Login</button>
    </li>
    </ul>
</div>
</template>

<script>
import axios from 'axios';

export default {
data() {
    return {
    flaggedUsers: [] // Array to store flagged users received from the backend
    };
},
mounted() {
    this.fetchFlaggedUsers();
},
methods: {
    async fetchFlaggedUsers() {
    try {
        // Fetch flagged users from backend using API endpoint
        const response = await axios.get('/api/get_flagged_users');
        this.flaggedUsers = response.data; // Assuming the response directly contains the flagged users data
    } catch (error) {
        console.error('Error fetching flagged users:', error);
    }
    },
    async fetchFlaggedPosts(userId) {
    try {
        // Fetch flagged posts for the selected user from the backend using API endpoint
        const response = await axios.get(`/api/get_flagged_posts?user_id=${userId}`);
        console.log(response.data); // Check if data is received
        // Update the flagged posts for the selected user
        const userIndex = this.flaggedUsers.findIndex(user => user.user_id === userId);
        if (userIndex !== -1) {
            // Use Object.assign to update the flaggedPosts array
            this.flaggedUsers[userIndex] = Object.assign({}, this.flaggedUsers[userIndex], {
                flaggedPosts: response.data
            });
        }
    } catch (error) {
        console.error('Error fetching flagged posts:', error);
    }
},
async blockAndDisableUser(userId) {
        try {
            const response = await axios.post('/api/ban_user', { user_id: userId });
            console.log(response.data); // Log response from backend
            // Optionally, update the UI to reflect the user has been blocked
            this.disableLogin = true; // Set flag to disable login
            this.$router.push("/dashboard");
        } catch (error) {
            console.error('Error blocking user:', error);
        }
    }
}
};
</script>

<style scoped>
.container {
margin: 33px 63px;
}

.user-title {
font-weight: bold;
font-size: 25px;
}

.user-list {
list-style-type: none;
padding: 0;
}

.user-item {
margin-bottom: 20px;
background-color: #f0f0f0;
padding: 15px;
border-radius: 5px;
}

.user-info {
font-weight: bold;
}

.user-details {
margin-top: 5px;
}

.flagged-posts {
list-style-type: none;
padding: 0;
}

.post-item {
margin-top: 10px;
background-color: #e0e0e0;
padding: 10px;
border-radius: 5px;
}

.post-info {
font-weight: bold;
}

.post-details {
margin-top: 5px;
}
</style>
