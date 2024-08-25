<script setup lang="ts">
defineProps({
  id: {
    type: String,
    required: true,
  },
  type: {
    type: String,
    required: true,
  },
  errors: {
    type: Array,
    default: [],
  },
  modelValue: String,
});

const emit = defineEmits(["update:modelValue"]);

function handlerInput(event: Event) {
  emit("update:modelValue", (event.target as HTMLInputElement).value);
}
</script>

<template>
  <div class="relative mb-6">
    <input
      @input="handlerInput"
      :id="id"
      :type="type"
      :value="modelValue"
      placeholder=" "
      class="block w-full px-2.5 pb-2.5 pt-4 text-sm text-gray-900 bg-transparent border border-gray-300 rounded-lg appearance-none focus:outline-none focus:ring-0 focus:border-emerald-600 peer"
    />
    <label
      :for="id"
      class="absolute text-sm text-gray-500 duration-300 transform -translate-y-4 scale-75 top-3 z-10 origin-[0] bg-white px-2 peer-placeholder-shown:scale-100 peer-placeholder-shown:translate-y-0 peer-focus:scale-75 peer-focus:-translate-y-5 left-1"
      ><slot></slot
    ></label>
    <div class="flex flex-col" v-if="errors.length">
      <p class="text-sm text-red-800" v-for="error in errors">{{ error }}</p>
    </div>
  </div>
</template>
