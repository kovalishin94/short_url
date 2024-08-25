<script setup lang="ts">
import type { User } from "@/types/user";
import { onMounted, ref, watch } from "vue";
import { useUserStore } from "@/stores/user";
import { useRouter } from "vue-router";
import CheckedIcon from "./Icons/CheckedIcon.vue";
import UncheckedIcon from "./Icons/UncheckedIcon.vue";
import UserCreateModal from "./UserCreateModal.vue";
import UserAddIcon from "./Icons/UserAddIcon.vue";
import DeleteModal from "./DeleteModal.vue";
import TrashIcon from "./Icons/TrashIcon.vue";
import URLDropDown from "./URLDropDown.vue";

const router = useRouter();
const userStore = useUserStore();
const usersList = ref<User[]>([]);
const isShowUserCreateModal = ref<boolean>(false);
const isShowUserDeleteModal = ref<boolean>(false);
const searchQuery = ref<string>("");
const currentUser = ref({
  id: 0,
  username: "",
});

async function getUserList() {
  let url = `${import.meta.env.VITE_API_URL}api/users/`;

  if (searchQuery.value) {
    url += `?search=${searchQuery.value}`;
  }

  try {
    const response = await fetch(url, {
      method: "GET",
      headers: {
        Authorization: `Bearer ${userStore.user.accessToken}`,
      },
    });
    if (response.status === 403) {
      router.push({ name: "forbidden" });
    }
    if (response.status === 401) {
      userStore.refreshToken();
      getUserList();
      return;
    }
    const data = await response.json();
    usersList.value = data;
  } catch (error) {
    console.error(error);
    console.log("Get error");
  }
}

async function deleteUser() {
  try {
    const response = await fetch(
      `${import.meta.env.VITE_API_URL}api/users/${currentUser.value.id}/`,
      {
        method: "DELETE",
        headers: {
          Authorization: `Bearer ${userStore.user.accessToken}`,
        },
      }
    );
    if (response.ok) {
      getUserList();
      isShowUserDeleteModal.value = false;
    }
    if (response.status === 401) {
      userStore.refreshToken();
      deleteUser();
      return;
    }
  } catch (error) {
    console.error(error);
  }
}

async function changeStatus(id: number, data: any) {
  try {
    const response = await fetch(
      `${import.meta.env.VITE_API_URL}api/users/${id}/`,
      {
        method: "PATCH",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${userStore.user.accessToken}`,
        },
        body: JSON.stringify(data),
      }
    );
    if (response.ok) {
      getUserList();
      console.log(await response.json());
      return;
    }
    if (response.status === 401) {
      userStore.refreshToken();
      changeStatus(id, data);
      return;
    }
  } catch (error) {
    console.log(error);
  }
}

function addNewUser(user: User) {
  usersList.value.push(user);
}

function showUserDeleteModal(id: number, username: string) {
  currentUser.value.id = id;
  currentUser.value.username = username;
  isShowUserDeleteModal.value = true;
}

watch(searchQuery, () => {
  getUserList();
});

onMounted(() => {
  getUserList();
});
</script>
<template>
  <div class="p-4">
    <div class="flex my-4 w-full">
      <button @click="isShowUserCreateModal = true" class="m-2 hover:scale-110">
        <UserAddIcon class="w-8 h-8" />
      </button>
      <input
        v-model="searchQuery"
        type="text"
        class="border-2 border-emerald-600 px-4 py-2 rounded-md outline-emerald-700 grow"
        placeholder="Поиск..."
      />
    </div>
    <UserCreateModal
      @close="isShowUserCreateModal = false"
      @new-user="addNewUser"
      :is-show="isShowUserCreateModal"
    />
    <table
      v-if="usersList.length"
      class="min-w-full bg-white border border-emerald-200 rounded-lg"
    >
      <thead>
        <tr class="bg-emerald-200 text-black uppercase text-sm leading-normal">
          <th class="py-3 px-6 text-left">id</th>
          <th class="py-3 px-6 text-left">Логин</th>
          <th class="py-3 px-6 text-left">Имя</th>
          <th class="py-3 px-6 text-left">Фамилия</th>
          <th class="py-3 px-6 text-left">E-mail</th>
          <th class="py-3 px-6 text-left">Активный</th>
          <th class="py-3 px-6 text-left">Админ</th>
          <th class="py-3 px-6 text-left">Список ссылок</th>
          <th class="py-3 px-6 text-left">Удалить</th>
        </tr>
      </thead>
      <tbody class="text-black text-sm">
        <tr
          class="border-b border-emerald-200 hover:bg-emerald-100"
          v-for="user in usersList"
          :key="user.id"
        >
          <td class="py-3 px-6 text-left">{{ user.id }}</td>
          <td class="py-3 px-6 text-left">{{ user.username }}</td>
          <td class="py-3 px-6 text-left">{{ user.first_name }}</td>
          <td class="py-3 px-6 text-left">{{ user.last_name }}</td>
          <td class="py-3 px-6 text-left">{{ user.email }}</td>
          <td class="py-3 px-6 text-left">
            <button
              :disabled="user.id === userStore.user.id"
              :class="[
                user.id === userStore.user.id
                  ? 'cursor-not-allowed'
                  : 'cursor-pointer hover:scale-110',
              ]"
              @click="changeStatus(user.id, { is_active: !user.is_active })"
            >
              <CheckedIcon v-if="user.is_active" />
              <UncheckedIcon v-else />
            </button>
          </td>
          <td class="py-3 px-6 text-left">
            <button
              :disabled="user.id === userStore.user.id"
              :class="[
                user.id === userStore.user.id
                  ? 'cursor-not-allowed'
                  : 'cursor-pointer hover:scale-110',
              ]"
              @click="
                changeStatus(user.id, { is_superuser: !user.is_superuser })
              "
            >
              <CheckedIcon v-if="user.is_superuser" />
              <UncheckedIcon v-else />
            </button>
          </td>
          <td class="py-3 px-6 text-left">
            <URLDropDown v-if="user.urls.length" :urls="user.urls" />
            <p v-else>Нет ссылок созданных этим пользователем</p>
          </td>
          <td class="py-3 px-6 text-left">
            <button
              @click="showUserDeleteModal(user.id, user.username)"
              class="transition-transform hover:scale-110 duration-300"
            >
              <TrashIcon class="w-6 h-6" />
            </button>
          </td>
        </tr>
      </tbody>
    </table>
    <div v-else>Нет записей</div>
  </div>
  <DeleteModal
    :is-show="isShowUserDeleteModal"
    :data="currentUser.username"
    @close="isShowUserDeleteModal = false"
    @delete="deleteUser"
    >Вы действительно хотите удалить пользователя
  </DeleteModal>
</template>
