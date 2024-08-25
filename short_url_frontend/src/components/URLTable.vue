<script setup lang="ts">
import { useUserStore } from "@/stores/user";
import { onMounted, ref, watch } from "vue";
import CopyToClipboardIcon from "@/components/Icons/CopyToClipboardIcon.vue";
import TrashIcon from "./Icons/TrashIcon.vue";
import DeleteModal from "./DeleteModal.vue";
import type { URL } from "@/types/url";

const userStore = useUserStore();
const urlList = ref<URL[]>([]);
const isShowUrlDeleteModal = ref<boolean>(false);
const searchQuery = ref<string>("");
const currentURL = ref<URL>({
  id: 0,
  orig_url: "",
  shorted_url: "",
  click_stat: 0,
  created_at: "",
  user: { id: 0, username: "", last_name: "", first_name: "" },
});
function copyToClipboard(text: string) {
  navigator.clipboard.writeText(text);
}

function showDeleteModal(url: URL) {
  currentURL.value = url;
  isShowUrlDeleteModal.value = true;
}

async function getURLList() {
  let url = `${import.meta.env.VITE_API_URL}api/urls/`;

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

    const data = await response.json();
    urlList.value = data;
  } catch (error) {
    console.error(error);
  }
}

async function deleteURL() {
  try {
    const response = await fetch(
      `${import.meta.env.VITE_API_URL}api/urls/${currentURL.value.id}/`,
      {
        method: "DELETE",
        headers: {
          Authorization: `Bearer ${userStore.user.accessToken}`,
        },
      }
    );
    getURLList();
  } catch (error) {
    console.error(error);
  }
  isShowUrlDeleteModal.value = false;
}

function clickUrl(url: string) {
  window.open(url);
}

onMounted(async () => {
  getURLList();
});

watch(searchQuery, () => {
  getURLList();
});
</script>

<template>
  <div class="p-4">
    <div class="flex my-4 w-full">
      <input
        v-model="searchQuery"
        type="text"
        class="border-2 border-emerald-600 px-4 py-2 rounded-md outline-emerald-700 grow"
        placeholder="Поиск..."
      />
    </div>
    <table
      v-if="urlList.length"
      class="min-w-full bg-white border border-emerald-200 rounded-lg"
    >
      <thead>
        <tr class="bg-emerald-200 text-black uppercase text-sm leading-normal">
          <th class="py-3 px-6 text-left">#</th>
          <th class="py-3 px-6 text-left">Ссылка</th>
          <th class="py-3 px-6 text-left">Короткая ссылка</th>
          <th class="py-3 px-6 text-left" v-if="userStore.user.is_superuser">
            Пользователь
          </th>
          <th class="py-3 px-6 text-left">Дата создания</th>
          <th class="py-3 px-6 text-left" v-if="userStore.user.is_superuser">
            Количество кликов
          </th>
          <th class="py-3 px-6 text-left">Удалить</th>
        </tr>
      </thead>
      <tbody class="text-black text-sm">
        <tr
          v-for="(url, index) in urlList"
          :key="url.id"
          class="border-b border-emerald-200 hover:bg-emerald-100"
          @click="clickUrl(url.orig_url)"
        >
          <td class="py-3 px-6 text-left">{{ index + 1 }}</td>
          <td class="py-3 px-6 text-left">{{ url.orig_url }}</td>
          <td class="py-3 px-6 text-left">
            {{ url.shorted_url }}
            <button
              @click.stop="copyToClipboard(url.shorted_url)"
              class="py-2 px-4 hover:scale-110"
            >
              <CopyToClipboardIcon />
            </button>
          </td>
          <td class="py-3 px-6 text-left" v-if="userStore.user.is_superuser">
            {{ url.user.username }}
          </td>
          <td class="py-3 px-6 text-left">{{ url.created_at }}</td>
          <td class="py-3 px-6 text-left" v-if="userStore.user.is_superuser">
            {{ url.click_stat }}
          </td>
          <td class="py-3 px-6 text-left">
            <button
              @click.stop="showDeleteModal(url)"
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
    :is-show="isShowUrlDeleteModal"
    :data="currentURL.shorted_url"
    @close="isShowUrlDeleteModal = false"
    @delete="deleteURL"
    >Вы действительно хотите удалить короткую ссылку
  </DeleteModal>
</template>
