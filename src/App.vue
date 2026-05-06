<template>
  <nav class="nav">
    <div class="nav-title-block">
      <span class="nav-title">安政遠足侍マラソン</span>
      <span v-if="currentYearMeta" class="nav-subtitle">{{ currentYearMeta.label }}（{{ currentYearMeta.year }}）</span>
    </div>
    <div class="nav-right">
      <select v-if="years.length > 1" :value="selectedYear" class="year-select" @change="onYearChange">
        <option v-for="y in years" :key="y.year" :value="y.year">{{ y.label }}({{ y.year }})</option>
      </select>
      <a href="https://github.com/monman53/ansei-toashi" target="_blank" rel="noopener" class="github-link" title="GitHub">
        <svg height="20" width="20" viewBox="0 0 16 16" fill="currentColor">
          <path d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27.68 0 1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.013 8.013 0 0016 8c0-4.42-3.58-8-8-8z"/>
        </svg>
      </a>
    </div>
  </nav>
  <main>
    <router-view :year="selectedYear" :yearMeta="currentYearMeta" />
  </main>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'

const years = ref([])
const route = useRoute()
const router = useRouter()

const selectedYear = computed(() => {
  const y = Number(route.params.year)
  return years.value.find(yr => yr.year === y) ? y : (years.value[0]?.year ?? null)
})

const currentYearMeta = computed(() => years.value.find(y => y.year === selectedYear.value) ?? null)

function onYearChange(e) {
  router.push('/' + e.target.value)
}

onMounted(async () => {
  const res = await fetch(import.meta.env.BASE_URL + 'data/index.json')
  years.value = await res.json()
  if (!route.params.year && years.value.length > 0) {
    router.replace('/' + years.value[0].year)
  }
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

.github-link {
  color: rgba(255,255,255,.7);
  display: flex;
  align-items: center;
}
.github-link:visited { color: rgba(255,255,255,.7); }
.github-link:hover { color: white; }

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
