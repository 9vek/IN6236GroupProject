<script setup lang="ts">
import Header from './components/Header.vue'
import Footer from './components/Footer.vue'
import { useUserStore } from './store'
import { onMounted } from 'vue'

const userStore = useUserStore()

onMounted(() => {
  userStore.recoverUser()
})

</script>

<template>
  <div class="w-full h-fit scrollbar-none">
    <Header />
    <div class="w-full h-screen bg-stone-50">
      <router-view></router-view>
    </div>
    <Footer />
  </div>
</template>
<style scoped></style>
