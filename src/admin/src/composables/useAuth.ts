import { ref, reactive } from 'vue'
import {
    PublicClientApplication,
    type AccountInfo,
    type RedirectRequest,
} from '@azure/msal-browser'

export const msalConfig = {
    auth: {
        tenantId: import.meta.env.VITE_TENANT_ID,
        clientId: import.meta.env.VITE_CLIENT_ID,
        authority: import.meta.env.VITE_AUTHORITY,
        redirectUri: import.meta.env.VITE_REDIRECT_URI,
        postLogoutUrl: window.location.origin
    },
    cache: {
        cacheLocation: 'sessionStorage',
        storeAuthStateInCookie: false
    }
}
export const graphScopes: RedirectRequest = {
    scopes: ['user.read', 'openid', 'profile'],
}
export const state = reactive({
    isAuthenticated: false,
    user: null as AccountInfo | null
})
export const msal = new PublicClientApplication(msalConfig)

export function useAuth() {
    const isAuthenticated = ref(false)

    const login = async () => {
        try {
            if(! msal) {
                throw new Error('MSAL not initialised')
            }
            await msal.loginRedirect(graphScopes)
            isAuthenticated.value = true

            const loginResponse = await msal.loginRedirect(graphScopes)
            isAuthenticated.value = true
            console.log('Login success:', loginResponse)
        } catch(error) {
            console.error('Login error:', error)
        }
    }

    const logout = () => {
        if(! msal) {
            throw new Error('MSAL not initialised')
        }
        msal.logoutRedirect()
        isAuthenticated.value = false
        console.log('Logged out')
    }
    const handleRedirect = async () => {
        try {
            await msal.handleRedirectPromise()
            state.isAuthenticated = msal.getAllAccounts().length > 0
            state.user = msal.getAllAccounts()[0]
            msal.setActiveAccount(state.user)
        } catch(error) {
            console.error('Redirect error:', error)
        }
    }

    return { isAuthenticated, login, logout, handleRedirect, state, msal: msal }
}