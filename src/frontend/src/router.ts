import { createRouter, createWebHistory } from 'vue-router'

const routes = [
    {
        path: '/',
        component: () => import('./layouts/Default.vue'),
        children: [
            {
                path: '/:uid',
                name: 'Landing',
                component: () => import("./pages/Landing.vue")
            },
            {
                path: '/',
                name: 'Main',
                component: () => import("./pages/Main.vue")
            },
            {
                path: '/stranger',
                name: 'Stranger',
                component: () => import("./pages/Stranger.vue")
            }
        ]
    }
]

const router = createRouter({
    history: createWebHistory(import.meta.env.BASE_URL),
    routes
});

export default router
