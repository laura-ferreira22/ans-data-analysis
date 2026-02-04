const BASE = "http://localhost:8000"

export const api = {
  operadoras: (q, page=1, pageSize=20) =>
    fetch(`${BASE}/api/operadoras?q=${q || ''}&page=${page}&page_size=${pageSize}`).then(r => r.json()),

  operadora: (cnpj) =>
    fetch(`${BASE}/api/operadoras/${cnpj}`).then(r => r.json()),

  despesas: (cnpj) =>
    fetch(`${BASE}/api/operadoras/${cnpj}/despesas`).then(r => r.json()),

  estatisticas: () =>
    fetch(`${BASE}/api/estatisticas`).then(r => r.json())
}
