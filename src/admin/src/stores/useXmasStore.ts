import { defineStore } from "pinia";
import { useCosmos } from "../composables/useCosmos.ts"
import { v4 as uuidv4 } from "uuid";

const { cosmos } = useCosmos();

export class XMasFeedback {
    year: number
    hasPicture: boolean
    message: string

    constructor(
        year: number = 2024,
        hasPicture: boolean = false,
        message: string = "",
    ) {
        this.year = year;
        this.hasPicture = hasPicture
        this.message = message;
    }
}

export class XMasPerson {
    type: string = "XMasPerson"
    id: string
    name: string
    language: string
    greeting: string
    eligibleForCurrentYear: boolean
    feedback: XMasFeedback[]

    constructor(
        id: string = uuidv4(),
        name: string = "Unknown Person",
        language: string = "en",
        greeting: string = "Merry Christmas",
        eligibleForCurrentYear: boolean = false,
        feedback: XMasFeedback[] = []
    ) {
        this.id = id;
        this.name = name;
        this.language = language;
        this.greeting = greeting;
        this.eligibleForCurrentYear = eligibleForCurrentYear;
        this.feedback = feedback;
    }
}

export const useXmasStore = defineStore("xmas", {
    state: () => ({
        people: new Map<string, XMasPerson>(),
    }),
    actions: {
        async list(): Promise<Map<string, XMasPerson>> {
            if(cosmos.container === null) throw new Error("Cosmos not initialised");
            try {
                const { resources } = await cosmos.container.items.query("SELECT * FROM c WHERE c.type = 'XMasPerson'").fetchAll();
                const update = new Set<XMasPerson>(resources)
                this.$patch( (state) => {
                    update.forEach( (p: XMasPerson) => state.people.set(p.id, p))
                })
                return this.people
            } catch(error: any) {
                console.error('Store error: ', error)
                throw error
            }
        },

        async get(id: string): Promise<XMasPerson> {
            try {
                return this.people.get(id) as XMasPerson
            } catch(error: any) {
                console.error('Store error: ', error)
                throw error
            }
        },

        async create(create: XMasPerson): Promise<XMasPerson> {
            if(cosmos.container === null) throw new Error("Cosmos not initialised");
            try {
                await cosmos.container.items.create(create)
                this.$patch( (state) => {
                    state.people.set(create.id, create)
                })
                return create
            } catch(error: any) {
                console.error('Store error: ', error)
                throw error
            }
        },

        async modify(update: XMasPerson): Promise<XMasPerson> {
            if(cosmos.container === null) throw new Error("Cosmos not initialised");
            try {
                await cosmos.container.items.upsert(update)
                this.$patch( (state) => {
                    state.people.set(update.id, update)
                })
                return update
            } catch(error: any) {
                console.error('Store error: ', error)
                throw error
            }
        },

        async remove(id: string) {
            if(cosmos.container === null) throw new Error("Cosmos not initialised");
            try {
                await cosmos.container.item(id, id).delete()
                this.$patch( (state) => state.people.delete(id))
            } catch(error: any) {
                console.error('Store error: ', error)
                throw error
            }
        }
    }
}) 

