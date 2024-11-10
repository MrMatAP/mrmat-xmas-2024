import {reactive, ref, Ref, readonly} from 'vue';
import {mande} from "mande";

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

    const api = mande('/api/people')

    const getUser = async (uid?: string) => {
        const localUid = window.localStorage.getItem("mrmat-xmas-2024");
        let queryUid = uid || localUid
        if( ! queryUid ) return
        xmasPerson.value = await api.get<XMas2024Person>(queryUid);
        if(xmasPerson.value.id !== "0")
            window.localStorage.setItem("mrmat-xmas-2024", xmasPerson.value.id);
        if(xmasPerson.value.hasPicture)
            xmasPicture.value = `/api/pictures/${xmasPerson.value.id}?t=${Date.now()}`
    }

    const updateUser = async () => {
        xmasPerson.value = await api.post<XMas2024Person>(
            xmasPerson.value.id,
            new XMas2024Feedback(xmasPerson.value.message))
    }

    const updatePicture = async (localImage: File) => {
        const formData = new FormData()
        formData.append("file", localImage)
        await fetch(`/api/pictures/${xmasPerson.value.id}`, {
            method: 'POST',
            body: formData})
            .then( (response) => response.json() )
            .then( (response) => {
                xmasPerson.value = response as XMas2024Person;
                xmasPicture.value = `/api/pictures/${xmasPerson.value.id}?t=${Date.now()}`
            })
    }

    return {
            appState,
            person: xmasPerson,
            pictureUrl: readonly<string>(xmasPicture),
            getUser,
            updateUser,
            updatePicture
    }
}
