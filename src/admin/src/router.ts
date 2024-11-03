import { createRouter, createWebHistory } from 'vue-router'

const routes = [
    {
        path: '/',
        component: () => import('./layouts/Default.vue'),
        children: [
            {
                path: '/',
                name: 'Landing',
                component: () => import("./pages/Landing.vue")
            },
            {
                path: '/person/:id',
                name: 'PersonEdit',
                component: () => import('./pages/PersonEdit.vue'),
            },
            {
                path: '/person-new',
                name: 'PersonNew',
                component: () => import('./pages/PersonNew.vue'),
            }
        ]
    }
]

const router = createRouter({
    history: createWebHistory(import.meta.env.BASE_URL),
    routes
});

export default router
