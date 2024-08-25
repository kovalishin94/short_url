import { createRouter, createWebHistory } from "vue-router";
import { useUserStore } from "@/stores/user";
import HomeView from "@/views/HomeView.vue";
import NotFoundView from "@/views/NotFoundView.vue";
import AuthView from "@/views/AuthView.vue";
import URLListView from "@/views/URLListView.vue";
import URLCreateView from "@/views/URLCreateView.vue";
import UserListView from "@/views/UserListView.vue";
import ForbiddenView from "@/views/ForbiddenView.vue";

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: "/",
      name: "home",
      component: HomeView,
      meta: {
        requiresAuth: true,
      },
    },
    {
      path: "/urls",
      name: "urls",
      component: URLListView,
      meta: {
        requiresAuth: true,
      },
    },
    {
      path: "/urls/create",
      name: "urls-create",
      component: URLCreateView,
      meta: {
        requiresAuth: true,
      },
    },
    {
      path: "/users",
      name: "users",
      component: UserListView,
      meta: {
        requiresAuth: true,
      },
    },
    {
      path: "/auth",
      name: "auth",
      component: AuthView,
    },
    {
      path: "/:pathMatch(.*)*",
      name: "notfound",
      component: NotFoundView,
    },
    {
      path: "/:pathMatch(.*)*",
      name: "forbidden",
      component: ForbiddenView,
    },
  ],
});

router.beforeEach((to, from, next) => {
  const userStore = useUserStore();
  if (
    to.matched.some((record) => record.meta.requiresAuth) &&
    !userStore.user.isAuthenticated
  ) {
    next({ name: "auth" });
  } else if (to.name === "auth" && userStore.user.isAuthenticated) {
    next({ name: "urls" });
  } else {
    next();
  }

  if (userStore.user.isAuthenticated) {
    userStore.getMe();
  }
});

export default router;
