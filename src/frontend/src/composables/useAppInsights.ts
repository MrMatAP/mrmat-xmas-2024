import {ref} from 'vue';
import {ApplicationInsights} from '@microsoft/applicationinsights-web';

const appInsights = ref(new ApplicationInsights(
    {
        config: {
            connectionString: 'InstrumentationKey=d619e9b8-669b-44e1-9f59-fb3a825ae1f7;IngestionEndpoint=https://northeurope-2.in.applicationinsights.azure.com/;LiveEndpoint=https://northeurope.livediagnostics.monitor.azure.com/;ApplicationId=19b01af9-1e87-456f-8f13-4782bd2114db'
        }
    }))

export function useAppInsights() {

    return {
        appInsights
    }
}
