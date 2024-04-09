<script setup lang="ts">
import { onMounted} from 'vue'
import { useUserStore } from '../store';
const userStore = useUserStore()

onMounted(() => {
    userStore.me()
})

</script>

<template>
    <div class="h-full w-full py-2">
        <div class="mx-auto rounded-sm shadow-sm bg-white container max-w-6xl h-full">
            <div class="text-3xl font-bold m-2 p-2">Profile Page</div>
            <div v-if="userStore.loggedIn">
                <div class="text-3xl font-bold m-2 p-2">Hi, {{ userStore.username }}</div>
                <div class="text-3xl font-bold m-2 p-2">{{ userStore.profile }}</div>
                <div @click="userStore.removeUser()"
                    class="w-fit text-xl border border-stone-400 p-2 m-2 cursor-pointer">Logout</div>
            </div>
        </div>
    </div>
</template>

<style scoped></style>