<template>
    <component :is="appropriateComponent"></component>
</template>
  

<script>
import { mapGetters } from "vuex";
import DashboardStudentComponent from './DashboardStudentComponent.vue';
import DashboardAdminComponent from './DashboardAdminComponent.vue';
import DashboardSupportStaffMemberComponent from './DashboardSupportStaffMemberComponent.vue';
import DashboardManagerComponent from './DashboardManager.vue';
import DashboardModeratorComponent from "./DashboardModeratorComponent.vue";

export default {
  name: 'dash_board',
  components: {
    DashboardStudent: DashboardStudentComponent,
    DashboardAdmin: DashboardAdminComponent,
    DashboardSupport: DashboardSupportStaffMemberComponent,
    DashboardManager: DashboardManagerComponent,
    DashboardModerator: DashboardModeratorComponent
  },
  computed: {
    ...mapGetters(["role"]),
    appropriateComponent() {
    switch(this.$store.state.role){
        case 1:
            return "DashboardStudent"
        case 2: 
            return "DashboardSupport"
        case 3: 
            return "DashboardAdmin"
        case 4:
            return "DashboardManager"
        case 5:
            return "DashboardModerator"
    }
    return null
    }
  },
};
</script>./DashboardSupportStaffMember.vue