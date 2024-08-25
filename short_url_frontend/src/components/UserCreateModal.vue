<script setup lang="ts">
import { ref } from "vue";
import FloatingInput from "./UI/FloatingInput.vue";
import CheckedIcon from "./Icons/CheckedIcon.vue";
import UncheckedIcon from "./Icons/UncheckedIcon.vue";
import { useUserStore } from "@/stores/user";
import type { User } from "@/types/user";

const userStore = useUserStore();
const username = ref<string>("");
const password = ref<string>("");
const first_name = ref<string>("");
const last_name = ref<string>("");
const email = ref<string>("");
const is_active = ref<boolean>(false);
const is_superuser = ref<boolean>(false);
const validationErrors = ref({});

defineProps({
  isShow: {
    type: Boolean,
    default: false,
  },
});

const emit = defineEmits(["close", "newUser"]);

async function createUser() {
  try {
    const response = await fetch(`${import.meta.env.VITE_API_URL}api/users/`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${userStore.user.accessToken}`,
      },
      body: JSON.stringify({
        username: username.value,
        password: password.value,
        first_name: first_name.value,
        last_name: last_name.value,
        email: email.value,
        is_active: is_active.value,
        is_superuser: is_superuser.value,
      }),
    });
    if (response.ok) {
      const data = (await response.json()) as User;
      emit("newUser", data);
      emit("close");
    }
    if (response.status === 401) {
      userStore.refreshToken();
      createUser();
      return;
    }
    if (response.status === 400) {
      validationErrors.value = await response.json();
    }
  } catch (error) {}
}

function closeModal() {
  emit("close");
  username.value = "";
  password.value = "";
  first_name.value = "";
  last_name.value = "";
  email.value = "";
  is_active.value = false;
  is_superuser.value = false;
}
</script>

<template>
  <div
    @click="closeModal"
    :class="[isShow ? 'visible' : 'invisible']"
    class="fixed top-0 bottom-0 left-0 right-0 flex justify-center bg-black bg-opacity-50"
  >
    <div
      @click.stop
      :class="[
        isShow ? 'visible translate-y-0' : 'invisible -translate-y-full',
      ]"
      class="bg-white w-fit h-fit mt-10 transition-all duration-300 rounded-md shadow-2xl p-8"
    >
      <div class="text-black font-bold mb-8 text-2xl">
        Создание нового пользователя
      </div>
      <div>
        <FloatingInput id="username" v-model="username" type="text"
          >Логин</FloatingInput
        >
        <FloatingInput id="password" v-model="password" type="password"
          >Пароль</FloatingInput
        >
        <FloatingInput id="first_name" v-model="first_name" type="text"
          >Имя</FloatingInput
        >
        <FloatingInput id="last_name" v-model="last_name" type="text"
          >Фамилия</FloatingInput
        >
        <FloatingInput id="email" v-model="email" type="email"
          >E-mail</FloatingInput
        >
        <div class="flex items-center mb-4 gap-x-3">
          <button @click="is_active = !is_active" class="hover:scale-110">
            <CheckedIcon class="w-4 h-4" v-if="is_active" />
            <UncheckedIcon class="w-4 h-4" v-else />
          </button>
          <p>Активный</p>
        </div>
        <div class="flex items-center mb-4 gap-x-3">
          <button @click="is_superuser = !is_superuser" class="hover:scale-110">
            <CheckedIcon class="w-4 h-4" v-if="is_superuser" />
            <UncheckedIcon class="w-4 h-4" v-else />
          </button>
          <p>Админ</p>
        </div>
      </div>
      <div class="flex flex-row-reverse gap-x-3 mt-10">
        <button
          @click="closeModal"
          class="rounded-md bg-gray-600 px-12 py-1.5 text-sm font-semibold leading-6 text-white shadow-sm hover:bg-gray-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-gray-600"
        >
          Отмена
        </button>
        <button
          @click="createUser"
          class="rounded-md bg-emerald-600 px-12 py-1.5 text-sm font-semibold leading-6 text-white shadow-sm hover:bg-emerald-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-emerald-600"
        >
          Создать
        </button>
      </div>
    </div>
  </div>
</template>
