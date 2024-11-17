import { ref, reactive } from 'vue'
import { CosmosClient, Container } from '@azure/cosmos';

export const cosmos = reactive({
    container: null as Container | null
})

export function useCosmos() {
    const endpoint = import.meta.env.VITE_COSMOS_ENDPOINT
    const key = import.meta.env.VITE_COSMOS_KEY
    const client = ref(new CosmosClient({ endpoint, key }))

    const login = async () => {
        try {
            const { database } = await client.value.databases.createIfNotExists({
                id: import.meta.env.VITE_COSMOS_DATABASE
            })
            const { container} = await database.containers.createIfNotExists({
                id: import.meta.env.VITE_COSMOS_CONTAINER
            })
            cosmos.container = container
        } catch(error) {
            console.error('Cosmos error: ', error)
        }
    }

    return { cosmosLogin: login, cosmos: cosmos }
}