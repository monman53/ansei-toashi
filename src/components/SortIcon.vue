<template>
  <span class="sort-icon">
    <template v-if="sort === field">
      {{ order === 'asc' ? '↑' : '↓' }}
    </template>
    <template v-else>
      <span class="sort-idle">⇅</span>
    </template>
  </span>
</template>

<script setup>
defineProps({ field: String, sort: String, order: String })
</script>

<style scoped>
.sort-icon { font-size: 10px; margin-left: 2px; }
.sort-idle { opacity: 0.4; }
</style>
