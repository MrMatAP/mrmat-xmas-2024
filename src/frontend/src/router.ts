import { createRouter, createWebHistory } from 'vue-router'

const routes = [
    {
        path: '/',
        component: () => import('./layouts/Default.vue'),
        children: [
            {
                path: '/',
                name: 'Identified',
                component: () => import("./pages/Identified.vue")
            },
            {
                path: '/stranger',
                name: 'Stranger',
                component: () => import("./pages/Stranger.vue")
            },
            {
                path: '/:uid',
                name: 'Landing',
                component: () => import("./pages/Landing.vue")
            },
        ]
    }
]

const router = createRouter({
    history: createWebHistory(import.meta.env.BASE_URL),
    routes
});

export default router
