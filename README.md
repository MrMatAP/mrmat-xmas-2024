# MrMat :: XMas 2024

Xmas Card 2024

## Notes

### Admin Site

For the first time in years, I actually have a semi-decent admin site. It requires authentication, does authenticate me but I still can't figure out how to run this without a Storage SAS token or CosmosDB key and use my personal credentials instead.

Run it locally for now and update `src/admin/.env.local` with the following local environment variables:

| Variable              | Description                                           |
|-----------------------|-------------------------------------------------------|
| VITE_CLIENT_ID        | The public client_id for the SPA app                  |
| VITE_AUTHORITY        | The authority URL, including the tenant_id            |
| VITE_REDIRECT_URI     | The redirect URI for the SPA                          |
| VITE_COSMOS_ENDPOINT  | Cosmos Endpoint                                       |
| VITE_COSMOS_KEY       | Secret Cosmos Key (needs rotating every now and then) |
| VITE_COSMOS_DATABASE  | The database to connect to                            |
| VITE_COSMOS_CONTAINER | The container to connect to                           |
| VITE_BLOB_SAS_URL     | The SAS URL of the storage account                    |
| VITE_BLOB_CONTAINER   | Name of the blob container of the storage account     |
