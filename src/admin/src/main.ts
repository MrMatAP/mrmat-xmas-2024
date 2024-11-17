import { createApp } from 'vue'
import router from "./router";
import { createPinia } from "pinia";
import { Quasar, Loading } from 'quasar'
import quasarLang from 'quasar/lang/en-GB'
import '@quasar/extras/material-icons/material-icons.css'
import 'quasar/src/css/index.sass'
import App from './App.vue'

const app = createApp(App)
app
    .use(Quasar, {
        plugins: { Loading },
        lang: quasarLang
    })
    .use(createPinia())
    .use(router)
    .mount('#app')
