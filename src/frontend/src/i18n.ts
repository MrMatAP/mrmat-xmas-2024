import { createI18n } from 'vue-i18n';

export const i18n = createI18n({
    legacy: false,
    locale: 'en',
    fallbackLocale: 'en',
    messages: {
        en: {
            errorHeader: 'Everything is fine... not',
            errorMessages: {
                unknown: "Something happened but we don't exactly know what it was. Try again later.",
                badResponse: "The backend didn't respond with something I understood. That's likely my bad. Try again later"
            },
            main_challenge_1: 'My analogue engineering challenge for you this year is to bake a ' +
                'cake in the general theme of the season (or some jelly, if you live in a warmer ' +
                'climate). The silicone mould I\'m sending along is good for temperatures between ' +
                '-60C to 230C and it does get along with dishwashers. I\'m afraid I can give you ' +
                'just one of these tree-shaped moulds, so take the opportunity to make some ' +
                'cookies too.',
            main_challenge_2: 'Send me a note and a picture of yourself enjoying the results.',
            feedback_your_message: 'Your note to me',
            feedback_send: 'Send'
        },
        de: {
            errorHeader: 'Alles ist gut... oder eben auch nicht',
            errorMessages: {
                unknown: 'Da ist etwas passiert aber wir wissen nicht so genau was es war. Probiers später nochmal.'
            },
            main_challenge_1: 'Dieses Jahr is meine analoge Engineering-Aufgabe fuer Dich, einen ' +
                'Kuchen zu backen (oder jelly, wenn Du in einer wärmeren Gegend lebst). Die Silikon-Form ' +
                'ist für Temperaturen zwischen -60C und 230C gemacht und kommt auch mit Geschirrspülern klar. ' +
                'Ich kann Dir nur eine Form geben, nimm die Gelegenheit wahr gleich auch noch ein ' +
                'paar Guetzli zu backen.',
            main_challenge_2: 'Schick mir eine Notiz mit einem Foto von Dir und dem Resultat.',
            feedback_your_message: 'Deine Notiz an mich',
            feedback_send: 'Abschicken'
        }
    }
})