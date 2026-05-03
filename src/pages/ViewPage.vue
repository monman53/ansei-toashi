<template>
  <div>
    <!-- フィルター / 検索バー -->
    <div class="card filter-bar">
      <div class="search-row">
        <input v-model="q" placeholder="氏名・よみがなで検索..." class="search-input" />
        <button class="btn-secondary reset-btn" @click="resetFilters">クリア</button>
      </div>
      <div class="filter-row">
        <div class="chip-group">
          <button class="chip" :class="{ active: filterGender === '男性' }" @click="toggleFilter('gender', '男性')">男性</button>
          <button class="chip" :class="{ active: filterGender === '女性' }" @click="toggleFilter('gender', '女性')">女性</button>
        </div>
        <div class="chip-group">
          <button class="chip" :class="{ active: filterCourse === '峠コース' }" @click="toggleFilter('course', '峠コース')">峠</button>
          <button class="chip" :class="{ active: filterCourse === '関所・坂本宿コース' }" @click="toggleFilter('course', '関所・坂本宿コース')">関所</button>
        </div>
        <div class="chip-group">
          <button class="chip" :class="{ active: filterCostume === '仮装する' }" @click="toggleFilter('costume', '仮装する')">仮装あり</button>
          <button class="chip" :class="{ active: filterCostume === '仮装しない' }" @click="toggleFilter('costume', '仮装しない')">仮装なし</button>
        </div>
        <button class="chip chip-friend" :class="{ active: filterFriend }" @click="filterFriend = !filterFriend">★ 知り合い</button>
        <select v-model="filterPrefecture" class="pref-select">
          <option value="">都道府県</option>
          <option v-for="p in prefectures" :key="p">{{ p }}</option>
        </select>
      </div>
      <div class="stats-row">
        <span class="stat-text">{{ participants.length }}件表示</span>
        <span class="stat-text friend-count" v-if="friendCount > 0">★ {{ friendCount }}人</span>
        <span class="stat-text loading-inline" v-if="loading || sorting">{{ loading ? '読み込み中...' : 'ソート中...' }}</span>
        <span class="stat-text notice">フリガナはAI生成のため誤りがある場合があります</span>
      </div>
    </div>

    <!-- テーブル -->
    <div class="table-container" :class="{ 'table-loading': loading }">
      <table class="table">
        <thead>
          <tr>
            <th class="col-idx hidden-sm"></th>
            <th class="col-friend"></th>
            <th class="col-no sortable" @click="setSort('no')">
              No <SortIcon field="no" :sort="sort" :order="order" />
            </th>
            <th class="col-gender sortable" @click="setSort('gender')">
              性別 <SortIcon field="gender" :sort="sort" :order="order" />
            </th>
            <th class="col-name sortable" @click="setSort('name_kana')">
              氏名 <SortIcon field="name_kana" :sort="sort" :order="order" />
            </th>
            <th class="col-pref sortable" @click="setSort('prefecture')">
              都道府県 <SortIcon field="prefecture" :sort="sort" :order="order" />
            </th>
            <th class="col-costume hidden-sm">仮装</th>
            <th class="col-times sortable" @click="setSort('times')">
              回数 <SortIcon field="times" :sort="sort" :order="order" />
            </th>
            <th class="col-course hidden-sm sortable" @click="setSort('course')">
              コース <SortIcon field="course" :sort="sort" :order="order" />
            </th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(p, i) in participants" :key="p.no + '-' + p.course" :class="{ 'row-friend': isFriend(p) }">
            <td class="col-idx muted hidden-sm">{{ i + 1 }}</td>
            <td class="col-friend">
              <button
                class="friend-btn"
                :class="{ active: isFriend(p) }"
                @click="toggleFriend(p)"
                :title="isFriend(p) ? '知り合いから外す' : '知り合いに追加'"
              >{{ isFriend(p) ? '★' : '☆' }}</button>
            </td>
            <td class="col-no muted">{{ p.no }}</td>
            <td class="col-gender">
              <span class="badge" :class="p.gender === '男性' ? 'badge-male' : 'badge-female'">
                {{ p.gender === '男性' ? '男' : '女' }}
              </span>
            </td>
            <td class="col-name">
              <ruby class="name">{{ p.name }}<rt>{{ p.name_kana }}</rt></ruby>
            </td>
            <td class="col-pref">{{ p.prefecture }}</td>
            <td class="col-costume hidden-sm">
              <span class="costume-badge" :class="p.costume === '仮装する' ? 'costume-yes' : 'costume-no'">
                {{ p.costume === '仮装する' ? '仮' : '─' }}
              </span>
            </td>
            <td class="col-times">{{ p.times }}</td>
            <td class="col-course hidden-sm">
              <span class="badge" :class="p.course.includes('峠') ? 'badge-toge' : 'badge-sekisho'">
                {{ p.course.includes('峠') ? '峠' : '関所' }}
              </span>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted, nextTick } from 'vue'
import SortIcon from '../components/SortIcon.vue'

const props = defineProps({
  year: Number,
  yearMeta: Object,
})

const allParticipants = ref([])
const loading = ref(true)
const sorting = ref(false)

const q = ref('')
const filterGender = ref('')
const filterPrefecture = ref('')
const filterCourse = ref('')
const filterCostume = ref('')
const filterFriend = ref(false)
const sort = ref('no')
const order = ref('asc')

// localStorage キー（年度ごと）
const friendKey = computed(() => `ansei-toashi-friends-${props.year}`)

// 知り合いセット（no-course の文字列で管理）
const friendSet = ref(new Set())

function friendId(p) {
  return `${p.course}:${p.no}`
}

function isFriend(p) {
  return friendSet.value.has(friendId(p))
}

function toggleFriend(p) {
  const id = friendId(p)
  const next = new Set(friendSet.value)
  if (next.has(id)) {
    next.delete(id)
  } else {
    next.add(id)
  }
  friendSet.value = next
  localStorage.setItem(friendKey.value, JSON.stringify([...next]))
}

function loadFriends() {
  try {
    const raw = localStorage.getItem(friendKey.value)
    friendSet.value = raw ? new Set(JSON.parse(raw)) : new Set()
  } catch {
    friendSet.value = new Set()
  }
}

const courses = ['峠コース', '関所・坂本宿コース']

const prefectures = computed(() =>
  [...new Set(allParticipants.value.map(p => p.prefecture))].sort()
)

const friendCount = computed(() => friendSet.value.size)

const participants = computed(() => {
  let result = allParticipants.value

  if (q.value) {
    result = result.filter(p => p.name.includes(q.value) || p.name_kana.includes(q.value))
  }
  if (filterGender.value)     result = result.filter(p => p.gender === filterGender.value)
  if (filterPrefecture.value) result = result.filter(p => p.prefecture === filterPrefecture.value)
  if (filterCourse.value)     result = result.filter(p => p.course === filterCourse.value)
  if (filterCostume.value)    result = result.filter(p => p.costume === filterCostume.value)
  if (filterFriend.value)     result = result.filter(p => isFriend(p))

  const col = sort.value
  const dir = order.value === 'asc' ? 1 : -1
  return [...result].sort((a, b) => {
    const av = a[col] ?? ''
    const bv = b[col] ?? ''
    return av < bv ? -dir : av > bv ? dir : 0
  })
})

async function setSort(col) {
  sorting.value = true
  await new Promise(r => setTimeout(r, 0))
  if (sort.value === col) {
    order.value = order.value === 'asc' ? 'desc' : 'asc'
  } else {
    sort.value = col
    order.value = 'asc'
  }
  await nextTick()
  sorting.value = false
}

function toggleFilter(type, val) {
  if (type === 'gender')   filterGender.value  = filterGender.value  === val ? '' : val
  if (type === 'course')   filterCourse.value  = filterCourse.value  === val ? '' : val
  if (type === 'costume')  filterCostume.value = filterCostume.value === val ? '' : val
}

function resetFilters() {
  q.value = ''
  filterGender.value = ''
  filterPrefecture.value = ''
  filterCourse.value = ''
  filterCostume.value = ''
  filterFriend.value = false
}

async function loadData(meta) {
  if (!meta) return
  loading.value = true
  allParticipants.value = []
  const base = import.meta.env.BASE_URL
  const res = await fetch(`${base}data/${meta.file}`)
  allParticipants.value = await res.json()
  loadFriends()
  loading.value = false
}

watch(() => props.yearMeta, (meta) => {
  resetFilters()
  loadData(meta)
}, { immediate: true })
</script>

<style scoped>
.filter-bar { margin-bottom: 8px; }

.search-row { display: flex; gap: 8px; margin-bottom: 8px; }
.search-input { flex: 1; }
.reset-btn { flex-shrink: 0; padding: 8px 12px; }

.filter-row {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 6px;
  margin-bottom: 8px;
}

.chip-group {
  display: flex;
  border: 1px solid var(--border);
  border-radius: var(--radius);
  overflow: hidden;
}
.chip-group .chip { border-radius: 0; border: none; border-right: 1px solid var(--border); }
.chip-group .chip:last-child { border-right: none; }

.chip {
  padding: 5px 10px;
  background: white;
  color: var(--muted);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  font-size: 12px;
  white-space: nowrap;
}
.chip.active { background: var(--primary); color: white; border-color: var(--primary); }
.chip-friend { }

.pref-select { width: auto; flex: 1; min-width: 90px; font-size: 12px; padding: 5px 8px; }

.stats-row { display: flex; flex-wrap: wrap; gap: 4px 12px; font-size: 12px; color: var(--muted); }
.friend-count { color: var(--friend-color); font-weight: 500; }
.loading-inline { font-style: italic; }
.notice { width: 100%; }

.table-loading { opacity: 0.4; pointer-events: none; transition: opacity 0.1s; }

.table-container {
  overflow-x: auto;
  overflow-y: auto;
  max-height: calc(100vh - 220px);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  background: white;
}

.table {
  width: 100%;
  border-collapse: separate;
  border-spacing: 0;
  font-size: 13px;
}

.table th {
  background: var(--primary);
  color: white;
  text-align: left;
  padding: 8px 6px;
  white-space: nowrap;
  position: sticky;
  top: 0;
  z-index: 10;
  font-weight: 500;
  font-size: 12px;
}

.table td {
  padding: 7px 6px;
  border-bottom: 1px solid var(--border);
  vertical-align: middle;
}

.table tbody tr:last-child td { border-bottom: none; }
.table tbody tr:hover { background: #F8F8F8; }
.row-friend { background: #FEF6F6; }
.row-friend:hover { background: #FCF0F0; }

.sortable { cursor: pointer; user-select: none; }
.sortable:hover { background: #444; }

.col-idx     { width: 20px; text-align: right; font-size: 10px; padding: 0 2px; }
.col-friend  { width: 40px; padding: 0 4px; text-align: center; }
.col-no      { width: 44px; }
.col-name    { min-width: 100px; }
.col-gender  { width: 36px; text-align: center; }
.col-pref    { min-width: 60px; }
.col-costume { width: 36px; text-align: center; }
.col-times   { width: 44px; text-align: right; }
.col-course  { min-width: 60px; }

.muted { color: var(--muted); }
.name { font-weight: 500; }
ruby.name rt { font-size: 0.65em; font-weight: normal; color: var(--muted); }

.friend-btn {
  background: none;
  padding: 4px 6px;
  font-size: 16px;
  color: #ccc;
  line-height: 1;
  border: none;
  min-width: 32px;
  min-height: 30px;
}
.friend-btn.active { color: var(--friend-color); }
.friend-btn:hover  { color: var(--friend-color); }

.costume-badge {
  display: inline-block;
  font-size: 11px;
  font-weight: bold;
  padding: 1px 4px;
  border-radius: 3px;
}
.costume-yes { background: #EAEAF4; color: #333; }
.costume-no  { color: #aaa; }

@media (max-width: 600px) {
  .hidden-sm { display: none; }
  .filter-row select { min-width: 90px; }
  .table-container { max-height: calc(100vh - 240px); }
}
</style>
