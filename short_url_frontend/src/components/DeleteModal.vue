<script setup lang="ts">
defineProps({
  isShow: {
    type: Boolean,
    default: false,
  },
  data: {
    type: String,
  },
});

defineEmits(["close", "delete"]);
</script>
<template>
  <div
    @click="$emit('close')"
    :class="[isShow ? 'visible' : 'invisible']"
    class="fixed top-0 bottom-0 left-0 right-0 flex justify-center bg-black bg-opacity-50"
  >
    <div
      @click.stop
      :class="[isShow ? 'visible translate-y-0' : 'invisible -translate-y-32']"
      class="bg-white w-fit h-fit mt-10 transition-all duration-300 rounded-md shadow-2xl p-4"
    >
      <div class="text-red-700 font-bold" v-if="data">
        <slot></slot>
        <strong class="text-black italic font-medium">{{ data }}</strong>
        ?
      </div>
      <div class="flex flex-row-reverse gap-x-3 mt-6">
        <button
          @click="$emit('close')"
          class="rounded-md bg-gray-600 px-12 py-1.5 text-sm font-semibold leading-6 text-white shadow-sm hover:bg-gray-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-gray-600"
        >
          Отмена
        </button>
        <button
          @click="$emit('delete')"
          class="rounded-md bg-red-600 px-12 py-1.5 text-sm font-semibold leading-6 text-white shadow-sm hover:bg-red-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-red-600"
        >
          Удалить
        </button>
      </div>
    </div>
  </div>
</template>
