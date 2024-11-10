import {reactive, ref, Ref, readonly} from 'vue';

export class XMas2024Person {
    id: string = "0"
    name: string = "Stranger"
    language: string = "en"
    greeting: string = "Hello Stranger"
    hasPicture: boolean = false;
    message: string = ""
}

export class XMas2024Feedback {
    message: string

    constructor(message: string) {
        this.message = message
    }
}

export const appState = reactive({
    version: 'unknown',
    isLoading: true,
    isError: false,
    errorMessageId: 'unknown'
})

export const xmasPerson: Ref<XMas2024Person> = ref(new XMas2024Person());
export const xmasPicture: Ref<string> = ref('/tap-to-update.png')

export function useStore() {

    const getUser = async (uid?: string) => {
        const localUid = window.localStorage.getItem("mrmat-xmas-2024");
        let queryUid = uid || localUid
        if( ! queryUid ) return
        let response = await fetch(`/api/people/${queryUid}`)
        if(response.status !== 200) {
            xmasPerson.value = new XMas2024Person()
            return
        }
        xmasPerson.value = await response.json();
        window.localStorage.setItem("mrmat-xmas-2024", xmasPerson.value.id);
        if(xmasPerson.value.hasPicture)
            xmasPicture.value = `/api/pictures/${xmasPerson.value.id}?t=${Date.now()}`
    }

    const updateUser = async () => {
        let response = await fetch(`/api/people/${xmasPerson.value.id}`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(new XMas2024Feedback(xmasPerson.value.message))})
        if(response.status !== 200) {
            appState.isError = true;
            appState.errorMessageId = 'badResponse'
            return
        }
        xmasPerson.value = await response.json() as XMas2024Person;
    }

    const updatePicture = async (localImage: File) => {
        const formData = new FormData()
        formData.append("file", localImage)
        let response = await fetch(`/api/pictures/${xmasPerson.value.id}`, {
            method: 'POST',
            body: formData})
        if(response.status !== 200) {
            appState.isError = true;
            appState.errorMessageId = 'badResponse'
            return
        }
        xmasPerson.value = await response.json() as XMas2024Person;
        xmasPicture.value = `/api/pictures/${xmasPerson.value.id}?t=${Date.now()}`
    }

    return {
            appState,
            person: xmasPerson,
            pictureUrl: readonly(xmasPicture),
            getUser,
            updateUser,
            updatePicture
    }
}
