<template>
  <div class="page">
    <div class="card">
      <router-link to="/" class="back">← Voltar</router-link>

      <h2>Detalhes da Operadora</h2>

      <div v-if="loading" class="muted">Carregando...</div>

      <div v-else-if="error" class="error">
        {{ error }}
      </div>

      <div v-else>
        <div class="infoCard">
          <div class="infoRow">
            <span class="label">CNPJ</span>
            <span class="value">{{ formatCnpj(op.cnpj) }}</span>
          </div>

          <div class="infoRow">
            <span class="label">Razão Social</span>
            <span class="value">{{ op.razao_social }}</span>
          </div>

          <div class="infoRow">
            <span class="label">UF</span>
            <span class="value"><span class="badge">{{ op.uf || "-" }}</span></span>
          </div>

          <div class="infoRow">
            <span class="label">Modalidade</span>
            <span class="value muted">{{ op.modalidade || "-" }}</span>
          </div>
        </div>

        <h3>Despesas por trimestre</h3>

        <table class="table">
          <thead>
            <tr>
              <th style="width: 100px;">Ano</th>
              <th style="width: 120px;">Trimestre</th>
              <th>Valor</th>
            </tr>
          </thead>
          <tbody>
            <tr v-if="despesas.length === 0">
              <td colspan="3" class="muted">Sem dados de despesas.</td>
            </tr>

            <tr v-else v-for="d in despesas" :key="d.ano + '-' + d.trimestre">
              <td>{{ d.ano }}</td>
              <td><span class="badge">{{ d.trimestre }}</span></td>
              <td><b>{{ money(d.valor_despesas) }}</b></td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { useRoute } from "vue-router";
import { api } from "../api";

const route = useRoute();
const cnpj = route.params.cnpj;

const op = ref(null);
const despesas = ref([]);
const loading = ref(false);
const error = ref("");

function formatCnpj(cnpj) {
  const d = String(cnpj || "").replace(/\D/g, "").padStart(14, "0");
  return `${d.slice(0,2)}.${d.slice(2,5)}.${d.slice(5,8)}/${d.slice(8,12)}-${d.slice(12,14)}`;
}

function money(v) {
  return Number(v || 0).toLocaleString("pt-BR", {
    style: "currency",
    currency: "BRL"
  });
}

onMounted(async () => {
  loading.value = true;
  try {
    op.value = await api.operadora(cnpj);
    despesas.value = await api.despesas(cnpj);
  } catch (e) {
    error.value = "Não foi possível carregar os dados dessa operadora.";
  } finally {
    loading.value = false;
  }
});
</script>

<style scoped>
.page {
  padding: 24px;
}

.card {
  max-width: 900px;
  margin: 0 auto;
  background: var(--card);
  padding: 18px;
  border-radius: 14px;
  border: 1px solid var(--border);
  box-shadow: 0 10px 26px rgba(0,0,0,0.06);
}

.back {
  display: inline-block;
  margin-bottom: 12px;
}

h2 { margin: 0 0 12px 0; }

.infoCard {
  border: 1px solid var(--border);
  border-radius: 12px;
  padding: 12px;
  background: #fbfbff;
  margin-bottom: 14px;
}

.infoRow {
  display: grid;
  grid-template-columns: 140px 1fr;
  gap: 12px;
  padding: 8px 0;
  border-top: 1px solid var(--border);
}

.infoRow:first-child { border-top: 0; }

.label {
  color: var(--muted);
  font-size: 13px;
}

.value {
  font-weight: 600;
}

.muted { color: var(--muted); }

.error {
  color: #b00020;
  font-weight: 600;
}
</style>
