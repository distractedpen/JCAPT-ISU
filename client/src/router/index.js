import { createRouter, createWebHistory } from "vue-router";
import DrillView from "../views/DrillView.vue";
import AdminView from "../views/AdminView.vue";
import LoginView from "../views/LoginView.vue";

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: "/",
      name: "drill",
      component: DrillView,
    },
    {
      path: "/login",
      name: "login",
      component: LoginView,
    },
    {
      path: "/admin",
      name: "admin",
      component: AdminView,
    },
  ],
});

// Authentication added by following tutorial:
// https://www.loginradius.com/blog/engineering/implementing-authentication-on-vuejs-using-jwt/
router.beforeEach((to, from, next) => {
  const publicPages = ["/login", "/"];
  const authRequired = !publicPages.includes(to.path);
  const loggedIn = localStorage.getItem("user");

  if (authRequired && !loggedIn) {
    return next({
      path: "/login",
      query: { returnUrl: to.path },
    });
  }

  next();
});

export default router;
