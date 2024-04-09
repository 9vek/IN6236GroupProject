<script setup lang="ts">
import { useRouter } from 'vue-router';

const router = useRouter()

</script>

<template>
    <div class="bg-sky-900 h-16 w-full flex">
        <div @click="router.push('/')" class="flex-shrink-0 h-full ml-4 w-fit grid grid-cols-1 place-items-center font-bold text-white text-2xl cursor-pointer">LinkedPro</div>
        <div class="flex flex-row justify-end w-full h-full">
            <div @click="router.push('/login')" class="h-full mr-4 w-fit grid grid-cols-1 place-items-center font-bold text-white text-xl cursor-pointer">Login</div>
        </div>
    </div>
</template>

<style scoped></style>