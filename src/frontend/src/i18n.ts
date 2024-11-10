import { createI18n } from 'vue-i18n';

export const i18n = createI18n({
    legacy: false,
    locale: 'en',
    fallbackLocale: 'en',
    messages: {
        en: {
            errorHeader: 'Everything is fine... not',
            errorMessages: {
                unknown: "Something happened but we don't exactly know what it was. Try again later."
            }
        },
        de: {
            errorHeader: 'Alles ist gut... oder eben auch nicht',
            errorMessages: {
                unknown: 'Da ist etwas passiert aber wir wissen nicht so genau was es war. Probiers später nochmal.'
            }
        }
    }
})