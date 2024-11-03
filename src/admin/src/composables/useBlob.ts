import { ref, reactive } from 'vue';
import { BlobServiceClient, ContainerClient } from '@azure/storage-blob';

export const blob = reactive({
    containerClient: null as ContainerClient | null
})

export function useBlob() {
    const client = ref(
        new BlobServiceClient(import.meta.env.VITE_BLOB_SAS_URL))

    const login = async () => {
        try {
            blob.containerClient = client.value.getContainerClient(import.meta.env.VITE_BLOB_CONTAINER);
        } catch(error) {
            console.error('Blob error: ', error)
            throw error
        }
    }

    return { blobLogin: login, blob: blob }
}