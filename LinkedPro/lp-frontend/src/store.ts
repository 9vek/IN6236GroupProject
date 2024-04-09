import { createPinia, defineStore } from 'pinia'
import axios from 'axios'
const store = createPinia()
export default store

type UserStore = {
    loggedIn: boolean,
    username: string,
    profile: string,
    registerUser: (user: { username: string, password: string }) => Promise<string>,
    validateUser: (user: { username: string, password: string }) => Promise<string>,
    recoverUser: () => void,
    removeUser: () => void,
    me: () => void
}

export const useUserStore = defineStore('user', (): UserStore => ({
    loggedIn: false,
    username: '',
    profile: '',
    async registerUser(user) {
        try {
            const resp = await axios.post('/api/signup', user)
            return ''
        }
        catch (error) {
            return 'fail to register.'
        }
    },
    async validateUser(user) {
        try {
            const resp = await axios.post('/api/login', user)
            this.loggedIn = true
            this.username = resp.data.username
            localStorage.setItem("token", resp.data.token)
            console.log(resp.data.token)
            console.log(localStorage.getItem("token"))
            axios.defaults.headers.common.Authorization = `Bearer ${resp.data.token}`
            return ''
        }
        catch (error) {
            return 'Fail to sign in, wrong email or password!'
        }
    },
    async recoverUser() {
        const token = localStorage.getItem('token')
        console.log(token);
        if (!token) {
            return
        }
        if (token && !this.loggedIn) {
            axios.defaults.headers.common.Authorization = `Bearer ${token}`
            console.log(axios.defaults.headers.common.Authorization)
            const resp = await axios.get(`/users/me`)
            this.loggedIn = true
            this.username = resp.data.username
            this.me()
        }
    },
    removeUser() {
        delete axios.defaults.headers.common["Authorization"]
        localStorage.removeItem('token')
        this.loggedIn = false
        this.username = ''
    },
   async me() {
        try {
            const resp = await axios.get('/api/me')
            this.username = resp.data.username
            this.profile = resp.data.profile
        }
        catch (error) {
            
        }

    }
}))