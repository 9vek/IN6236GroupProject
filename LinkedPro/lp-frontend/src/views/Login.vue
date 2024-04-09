<script setup lang="ts">
import { ref } from 'vue';
import { useUserStore } from '../store';
import { useRouter } from 'vue-router';

const userStore = useUserStore()
const router = useRouter()

let username = ref('')
let password = ref('')

const login = async () => {
    if (
        username.value.length != 0 && 
        password.value.length != 0) 
    {
        await userStore.validateUser({
            username: username.value, 
            password: password.value
        })
        router.push('/me')
    }
}
</script>

<template>
    <!-- <Header /> -->
    <div class="h-full grid grid-cols-1 place-items-center p-1">
        <div class="bg-white p-8 container rounded-lg shadow-md max-w-lg">
            <h2 class="text-3xl mb-6 font-bold">Login</h2>
            <div class="flex flex-col">
                <div class="mb-4">
                    <div class="block text-gray-500 font-bold">Username</div>
                    <input type="text" id="username" v-model="username"
                        class="mt-1 p-2 border-2 border-gray-300 rounded-md w-full">
                </div>
                <div class="mb-4">
                    <div class="block text-gray-500 font-bold">Password</div>
                    <input type="password" v-model="password"
                        class="mt-1 p-2 border-2 border-gray-300 rounded-md w-full">
                </div>
                <div @click="login()" class="bg-sky-900 hover:bg-sky-600 p-3 font-bold text-pink-50 rounded-md w-full text-center">Submit</div>
                <router-link to="/signup" class="mt-1 pt-1 text-sky-600 text-sm flex justify-center">Have an account? Login</router-link>
            </div>
            <!-- <p v-if="error" class="text-red-500 mt-4">{{ error }}</p> -->
        </div>
    </div>                                                                                                          
</template>

<style scoped></style>
