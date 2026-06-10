<template>
  <div class="loading loading-active" v-show="loadingStore.isLoading">
    <div class="load-box">
      <div class="loading-spinner"></div>
      <span>比卡丘正在带着数据走向你~~</span>
    </div>
  </div>
</template>

<script setup lang="ts">
import useLoadingStore from "@/store/modules/loading.ts";
const loadingStore = useLoadingStore()

</script>

<style scoped lang="scss">

.loading {
  width: 100%;
  height: 100%;
  position: fixed;
  background: var(--el-bg-color);
  top: 0;
  left: 0;
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 999;

  .load-box{
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;

    .loading-spinner {
      width: 60px;
      height: 60px;
      border: 4px solid #e0e0e0;
      border-top-color: #409EFF;
      border-radius: 50%;
      animation: spin 0.8s linear infinite;
    }

    @keyframes spin {
      to { transform: rotate(360deg); }
    }

    span{
      margin-top: 1rem;
      font-size: 1rem;
      font-weight: bold;
    }
  }
}
</style>
