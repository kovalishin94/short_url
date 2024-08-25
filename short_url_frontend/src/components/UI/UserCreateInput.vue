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
  modelValue: String,
});

const emit = defineEmits(["update:modelValue"]);

function handlerInput(event: Event) {
  emit("update:modelValue", (event.target as HTMLInputElement).value);
}
</script>

<template>
  <div class="mb-6">
    <label
      :for="id"
      class="block mb-2 text-sm font-medium text-gray-900 dark:text-white"
      ><slot></slot>
    </label>
    <input
      @input="handlerInput"
      :type="type"
      :id="id"
      :value="modelValue"
      class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-emerald-500 focus:border-emerald-500 block w-full p-2.5"
    />
  </div>
</template>
