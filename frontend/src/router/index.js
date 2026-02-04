import { createRouter, createWebHistory } from 'vue-router'
import Operadoras from '../views/Operadoras.vue'
import OperadoraDetalhe from '../views/OperadoraDetalhe.vue'

export default createRouter({
  history: createWebHistory(),
  routes: [
    { path: '/', component: Operadoras },
    { path: '/operadoras/:cnpj', component: OperadoraDetalhe, props: true }
  ]
})
