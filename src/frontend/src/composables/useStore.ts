import {reactive, ref, Ref} from 'vue';
import {mande} from "mande";

export class XMasFeedback {
    year: number = 2024
    hasPicture: boolean = false
    message: string = ""
}

export class XMasPerson {
    id: string = "0"
    name: string = "Stranger"
    language: string = "en"
    greeting: string = "Hello Stranger"
    feedback: XMasFeedback[] = []
}

export class StatusResponse{
    status: number = -1
    msg: string
}

export const appState = reactive({
    version: 'unknown',
    isLoading: true,
    isError: false,
    errorMessageId: 'unknown'
})

export const xmasPerson: Ref<XMasPerson> = ref(new XMasPerson());

export function useStore() {

    const api = mande('/api/xmaspeople')

    const initialise = async (uid?: string) => {
        const localUid = window.localStorage.getItem("mrmat-xmas-2024");
        let queryUid = uid || localUid
        if( ! queryUid ) return
        xmasPerson.value = await api.get<XMasPerson>(queryUid);
        if( xmasPerson.value.id !== "0") {
            window.localStorage.setItem("mrmat-xmas-2024", xmasPerson.value.id);
        }
    }

    const updateFeedback = async (message: string) => {
        let feedback = new XMasFeedback()
        let feedback2024 = identity.value.feedback.filter( (f) => f.year == 2024)
        if(feedback2024.length != 0) feedback = feedback2024[0]
        feedback.message = message
        feedback.hasPicture = hasPicture
        xmasPerson.value = await api.post<XMasPerson>(xmasPerson.value.id, feedback)
    }

    const updatePicture = async (localImage: File) => {
        const formData = new FormData()
        formData.append("file", localImage)
        await fetch(`/api/pictures/${xmasPerson.value.id}`, {
            method: 'POST',
            body: formData})
            .then( (response) => response.json() )
            .then( (response) => {
                console.dir(response)
                xmasPerson.value = response
            })
    }

    return {
            appState,
            identity: xmasPerson,
            initialise,
            updateFeedback,
            updatePicture
    }
}
