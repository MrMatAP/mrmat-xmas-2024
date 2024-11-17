import {defineConfig} from 'vite'
import {fileURLToPath, URL} from "node:url";
import vue from '@vitejs/plugin-vue'
import {quasar, transformAssetUrls} from '@quasar/vite-plugin'

// https://vite.dev/config/
export default defineConfig({
    resolve: {
        alias: {
            "@": fileURLToPath(new URL("./src", import.meta.url))
        },
        extensions: ['.ts', '.tsx', '.js', '.vue']
    },
    plugins: [
        vue({
            template: {transformAssetUrls}
        }),
        quasar({
            sassVariables: '@/quasar-variables.sass'
        })
    ],

})
