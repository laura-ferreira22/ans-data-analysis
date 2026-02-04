<template>
  <div class="card">
    <div class="cardHeader">
      <h3>Top UFs por despesa</h3>
      <span class="badge">Top 10</span>
    </div>

    <div v-if="!items || items.length === 0" class="muted">Sem dados.</div>

    <div v-else class="rows">
      <div v-for="row in items" :key="row.uf" class="row">
        <div class="uf">{{ row.uf }}</div>

        <div class="barTrack">
          <div class="barFill" :style="barStyle(row.total_despesas)"></div>
        </div>

        <div class="meta">
          <div><b>{{ money(row.total_despesas) }}</b></div>
          <small class="muted">Média/op: {{ money(row.media_por_operadora) }}</small>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
const props = defineProps({
  items: { type: Array, default: () => [] }
});

function maxVal() {
  if (!props.items.length) return 1;
  const m = Math.max(...props.items.map(i => Number(i.total_despesas || 0)));
  return m || 1;
}

function barStyle(v) {
  const pct = (Number(v || 0) / maxVal()) * 100;
  return {
    width: `${pct}%`
  };
}

function money(v) {
  return Number(v || 0).toLocaleString("pt-BR", {
    style: "currency",
    currency: "BRL"
  });
}
</script>

<style scoped>
.card {
  background: var(--card);
  border: 1px solid var(--border);
  border-radius: 14px;
  padding: 14px;
  box-shadow: 0 8px 22px rgba(0,0,0,0.05);
  margin: 12px 0;
}

.cardHeader {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 10px;
  margin-bottom: 12px;
}

h3 {
  margin: 0;
  font-size: 16px;
}

.rows { display: flex; flex-direction: column; gap: 10px; }

.row {
  display: grid;
  grid-template-columns: 44px 1fr 220px;
  gap: 12px;
  align-items: center;
}

.uf {
  font-weight: 700;
  color: var(--primary);
}

.barTrack {
  background: #eef2ff;
  border-radius: 999px;
  height: 10px;
  overflow: hidden;
  border: 1px solid rgba(79, 70, 229, 0.18);
}

.barFill {
  height: 10px;
  border-radius: 999px;
  background: linear-gradient(90deg, #6366f1, #4f46e5);
}

.meta {
  text-align: right;
}

.muted { color: var(--muted); }
</style>
