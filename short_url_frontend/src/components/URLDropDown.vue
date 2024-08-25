<script setup lang="ts">
import { ref } from "vue";
import ListDownIcon from "./Icons/ListDownIcon.vue";
import ListUpIcon from "./Icons/ListUpIcon.vue";
import { onClickOutside } from "@vueuse/core";

interface URL {
  id: number;
  orig_url: string;
  shorted_url: string;
}

const el = ref();
const isShow = ref<boolean>(false);

defineProps({
  urls: {
    type: Array<URL>,
    required: true,
  },
});

onClickOutside(el, () => {
  isShow.value = false;
});

function clickUrl(url: string) {
  window.open(url);
}
</script>
<template>
  <div class="relative inline-block" ref="el">
    <button @click="isShow = !isShow">
      <ListUpIcon class="w-6 h-6" v-if="isShow" />
      <ListDownIcon class="w-6 h-6" v-else />
    </button>
    <ul
      v-if="isShow"
      class="absolute top-full right-0 border-2 p-3 bg-white z-10"
    >
      <li
        @click="clickUrl(url.shorted_url)"
        class="hover:bg-gray-300 px-2 py-3 cursor-pointer rounded-md text-nowrap"
        v-for="url in urls"
        :key="url.id"
      >
        {{ url.shorted_url }} => {{ url.orig_url }}
      </li>
    </ul>
  </div>
</template>
