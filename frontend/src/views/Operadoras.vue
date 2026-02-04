<template>
  <div class="page">
    <div class="header">
      <div>
        <h2>Operadoras</h2>
        <p class="subtitle">Busca e exploração das operadoras com base nos CSVs processados.</p>
      </div>
    </div>

    <div class="card">
      <div class="searchRow">
        <div class="searchWrap">
          <span class="material-icons searchIcon">search</span>
          <input
            v-model="q"
            placeholder="Filtrar por Razão Social ou CNPJ"
            class="searchInput"
            @keydown.enter="load(1)"
          />
        </div>

        <button @click="load(1)" :disabled="loading">
          <span class="material-icons" style="font-size:18px;">search</span>
          Buscar
        </button>
      </div>

      <UfChart :items="ufs" />

      <table class="table" style="margin-top: 12px;">
        <thead>
          <tr>
            <th style="width: 180px;">CNPJ</th>
            <th>Razão Social</th>
            <th style="width: 80px;">UF</th>
            <th style="width: 220px;">Modalidade</th>
          </tr>
        </thead>

        <tbody>
          <tr v-if="loading">
            <td colspan="4" class="muted">Carregando...</td>
          </tr>

          <tr v-else-if="items.length === 0">
            <td colspan="4" class="muted">Nenhum resultado.</td>
          </tr>

          <tr v-else v-for="op in items" :key="op.cnpj">
            <td>
              <router-link :to="`/operadoras/${op.cnpj}`">
                {{ formatCnpj(op.cnpj) }}
              </router-link>
            </td>
            <td>{{ op.razao_social }}</td>
            <td><span class="badge">{{ op.uf || "-" }}</span></td>
            <td class="muted">{{ op.modalidade || "-" }}</td>
          </tr>
        </tbody>
      </table>

      <div class="pagination">
        <button :disabled="page===1 || loading" @click="load(page-1)">Anterior</button>

        <div class="muted">
          Página <b>{{ page }}</b>
          <span v-if="total"> — Total: {{ total }}</span>
        </div>

        <button :disabled="(page*pageSize)>=total || loading" @click="load(page+1)">Próxima</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { api } from "../api";
import UfChart from "../components/UfChart.vue";

const q = ref("");
const items = ref([]);
const total = ref(0);
const page = ref(1);
const pageSize = ref(20);
const loading = ref(false);
const ufs = ref([]);

function formatCnpj(cnpj) {
  const d = String(cnpj || "").replace(/\D/g, "").padStart(14, "0");
  return `${d.slice(0,2)}.${d.slice(2,5)}.${d.slice(5,8)}/${d.slice(8,12)}-${d.slice(12,14)}`;
}

async function load(p = 1) {
  loading.value = true;
  try {
    page.value = p;
    const data = await api.operadoras(q.value, page.value, pageSize.value);
    items.value = data.items || [];
    total.value = data.total || 0;
  } finally {
    loading.value = false;
  }
}

onMounted(async () => {
  await load(1);
  ufs.value = await api.estatisticas();
});
</script>

<style scoped>
.page {
  padding: 24px;
}

.header {
  max-width: 1000px;
  margin: 0 auto 14px auto;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

h2 { margin: 0; }

.subtitle {
  margin: 6px 0 0 0;
  color: var(--muted);
  font-size: 14px;
}

.card {
  max-width: 1000px;
  margin: 0 auto;
  background: var(--card);
  padding: 18px;
  border-radius: 14px;
  border: 1px solid var(--border);
  box-shadow: 0 10px 26px rgba(0,0,0,0.06);
}

.searchRow {
  display: grid;
  grid-template-columns: 1fr auto;
  gap: 10px;
  align-items: center;
}

.searchWrap {
  position: relative;
}

.searchIcon {
  position: absolute;
  left: 10px;
  top: 10px;
  font-size: 18px;
  color: var(--muted);
}

.searchInput {
  padding-left: 36px;
}

.pagination {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 14px;
}

.muted { color: var(--muted); }
</style>
