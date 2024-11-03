import { reactive } from 'vue';
import { BlobServiceClient, ContainerClient } from '@azure/storage-blob';

export const blob = reactive({
    containerClient: null as ContainerClient | null
})

export function useBlob() {

    const login = async () => {
        try {

            //
            // A failed attempt to re-use browser credentials for authentication to blob storage
            // const browserCreds = new InteractiveBrowserCredential({
            //     redirectUri: msalConfig.auth.redirectUri,
            //     tenantId: msalConfig.auth.tenantId,
            //     clientId: msalConfig.auth.clientId
            // })
            // await browserCreds.authenticate(['user.read', 'openid', 'profile'])
            // const serviceClient = new BlobServiceClient(
            //     'https://stomrmatinfra.blob.core.windows.net/',
            //     browserCreds
            // )
            // blob.containerClient = serviceClient.getContainerClient(import.meta.env.VITE_BLOB_CONTAINER)
            // console.log(await browserCreds.getToken(['user.read', 'openid', 'profile']))

            // Using a SAS token works, but it's ugly because we need to maintain it
            const client = new BlobServiceClient(import.meta.env.VITE_BLOB_SAS_URL)
            blob.containerClient = client.getContainerClient(import.meta.env.VITE_BLOB_CONTAINER);
        } catch(error) {
            console.error('Blob error: ', error)
            throw error
        }
    }

    return { blobLogin: login, blob: blob }
}