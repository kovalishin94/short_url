import { defineStore } from "pinia";
import { useRouter } from "vue-router";

type User = {
  isAuthenticated: boolean;
  id: number | null;
  username: string | null;
  is_superuser: boolean;
  accessToken: string | null;
  refreshToken: string | null;
};

export const useUserStore = defineStore("user", {
  state: () => ({
    router: useRouter(),
    user: {
      isAuthenticated: false,
      id: null,
      username: null,
      is_superuser: false,
      accessToken: null,
      refreshToken: null,
    } as User,
  }),
  actions: {
    initUser() {
      if (localStorage.getItem("user.accessToken")) {
        this.user.isAuthenticated = true;
        this.user.id = Number(localStorage.getItem("user.id"));
        this.user.username = localStorage.getItem("user.username");
        this.user.is_superuser =
          localStorage.getItem("user.is_superuser") === "true";
        this.user.accessToken = localStorage.getItem("user.accessToken");
        this.user.refreshToken = localStorage.getItem("user.refreshToken");
      }
    },
    removeUserData() {
      this.user.isAuthenticated = false;
      this.user.id = null;
      this.user.username = null;
      this.user.is_superuser = false;
      this.user.accessToken = null;
      this.user.refreshToken = null;

      localStorage.removeItem("user.id");
      localStorage.removeItem("user.username");
      localStorage.removeItem("user.is_superuser");
      localStorage.removeItem("user.accessToken");
      localStorage.removeItem("user.refreshToken");

      this.router.push({ name: "auth" });
    },
    async refreshToken() {
      try {
        const response = await fetch(
          `${import.meta.env.VITE_API_URL}api/token/refresh/`,
          {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
            },
            body: JSON.stringify({
              refresh: this.user.refreshToken,
            }),
          }
        );
        if (!response.ok) {
          throw new Error("Неверный токен");
        }
        const data = await response.json();
        this.user.accessToken = data.access;
        localStorage.setItem("user.accessToken", data.access);
        this.router.go(0);
      } catch (error) {
        console.error(error);
        this.removeUserData();
      }
    },
    async getMe() {
      try {
        const response = await fetch(`${import.meta.env.VITE_API_URL}api/me/`, {
          method: "GET",
          headers: {
            Authorization: `Bearer ${this.user.accessToken}`,
          },
        });
        if (!response.ok) {
          throw new Error("Нет возможности получить данные");
        }
        const data = await response.json();

        localStorage.setItem("user.id", data.id);
        localStorage.setItem("user.username", data.username);
        localStorage.setItem("user.is_superuser", data.is_superuser.toString());

        this.user.id = data.id;
        this.user.username = data.username;
        this.user.is_superuser = data.is_superuser;
      } catch (error) {
        this.refreshToken();
      }
    },
    setTokens(access: string, refresh: string) {
      localStorage.setItem("user.accessToken", access);
      localStorage.setItem("user.refreshToken", refresh);
      this.user.accessToken = access;
      this.user.refreshToken = refresh;

      this.getMe();
    },
  },
});
