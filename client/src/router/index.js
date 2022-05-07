import { createRouter, createWebHistory } from "vue-router";
import DrillView from "../views/DrillView.vue";
import AdminView from "../views/AdminView.vue";

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: "/",
      name: "drill",
      component: DrillView,
    },
    {
      path: "/admin",
      name: "admin",
      component: AdminView,
    },
  ],
});

export default router;
