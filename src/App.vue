<template>
  <nav class="nav">
    <div class="nav-title-block">
      <span class="nav-title">安政遠足侍マラソン</span>
      <span v-if="currentYearMeta" class="nav-subtitle">{{ currentYearMeta.label }}（{{ currentYearMeta.year }}）</span>
    </div>
    <div class="nav-right">
      <select v-if="years.length > 1" v-model="selectedYear" class="year-select" @change="onYearChange">
        <option v-for="y in years" :key="y.year" :value="y.year">{{ y.label }}({{ y.year }})</option>
      </select>
    </div>
  </nav>
  <main>
    <router-view :year="selectedYear" :yearMeta="currentYearMeta" />
  </main>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'

const years = ref([])
const selectedYear = ref(null)

const currentYearMeta = computed(() => years.value.find(y => y.year === selectedYear.value) ?? null)

function onYearChange() {
  localStorage.setItem('ansei-toashi-selected-year', String(selectedYear.value))
}

onMounted(async () => {
  const res = await fetch('./data/index.json')
  years.value = await res.json()
  const saved = Number(localStorage.getItem('ansei-toashi-selected-year'))
  const found = years.value.find(y => y.year === saved)
  selectedYear.value = found ? found.year : years.value[0]?.year ?? null
})
</script>

<style>
* { box-sizing: border-box; margin: 0; padding: 0; }

:root {
  --primary: #2A2A2A;
  --bg: #F4F4F4;
  --card: #FFFFFF;
  --border: #DEDEDE;
  --text: #1A1A1A;
  --muted: #888888;
  --friend-color: #B03030;
  --radius: 6px;
  --shadow: 0 1px 3px rgba(0,0,0,.08);
}

body {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Hiragino Sans', sans-serif;
  background: var(--bg);
  color: var(--text);
  font-size: 14px;
  overflow-x: hidden;
}

.nav {
  background: var(--primary);
  color: white;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 16px;
  height: 48px;
  position: sticky;
  top: 0;
  z-index: 100;
  box-shadow: 0 1px 4px rgba(0,0,0,.2);
}

.nav-title-block {
  display: flex;
  flex-direction: column;
  justify-content: center;
  overflow: hidden;
}

.nav-title {
  font-weight: bold;
  font-size: 15px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  line-height: 1.2;
}

.nav-subtitle {
  font-size: 11px;
  color: rgba(255,255,255,.65);
  white-space: nowrap;
  line-height: 1.2;
}

.nav-right { display: flex; align-items: center; gap: 8px; }

.year-select {
  background: rgba(255,255,255,.15);
  color: white;
  border: 1px solid rgba(255,255,255,.3);
  border-radius: 4px;
  padding: 4px 8px;
  font-size: 13px;
  width: auto;
}
.year-select option { background: var(--primary); }

.year-label { font-size: 13px; color: rgba(255,255,255,.8); }

main { padding: 10px; max-width: 900px; margin: 0 auto; }

button {
  cursor: pointer;
  border: none;
  border-radius: var(--radius);
  padding: 6px 14px;
  font-size: 13px;
  font-family: inherit;
  transition: opacity .15s;
}
button:active { opacity: 0.75; }

input, select, textarea {
  font-family: inherit;
  font-size: 14px;
  border: 1px solid var(--border);
  border-radius: var(--radius);
  padding: 8px 10px;
  background: white;
  color: var(--text);
  outline: none;
  width: 100%;
}
input:focus, select:focus, textarea:focus { border-color: #888; }

.btn-primary { background: var(--primary); color: white; }
.btn-primary:hover { background: #444; }
.btn-secondary { background: var(--border); color: var(--text); }

.card { background: var(--card); border-radius: var(--radius); padding: 10px; box-shadow: var(--shadow); }
.badge { display: inline-block; font-size: 11px; font-weight: bold; padding: 1px 5px; border-radius: 3px; }
.badge-male { background: #E8EEF4; color: #336; }
.badge-female { background: #F4E8EE; color: #633; }
.badge-toge { background: #E8F0E8; color: #363; }
.badge-sekisho { background: #F0EEE8; color: #553; }

.modal-overlay {
  position: fixed; inset: 0;
  background: rgba(0,0,0,.4);
  display: flex; align-items: center; justify-content: center;
  z-index: 200;
}
.modal {
  background: white; border-radius: var(--radius);
  padding: 20px; width: 90%; max-width: 400px;
  box-shadow: 0 4px 20px rgba(0,0,0,.2);
}
.modal-title { font-weight: bold; font-size: 16px; margin-bottom: 12px; }
.modal-actions { display: flex; gap: 8px; justify-content: flex-end; margin-top: 12px; }
.form-group { margin-bottom: 12px; }
.form-label { display: block; font-size: 12px; color: var(--muted); margin-bottom: 4px; }
</style>
