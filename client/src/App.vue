<template>
  <div class="minimal-container">
    <div class="minimal-header">safedit</div>
    <div id="editor" class="minimal-editor"></div>
  </div>
</template>

<script setup lang="ts">
import { onMounted } from 'vue';
import { setupMonacoEditor } from './monaco';

onMounted(() => {
  setupMonacoEditor();
});
</script>

<style>
@import url('https://fonts.googleapis.com/css2?family=Mozilla+Text:wght@200..700&display=swap');
</style>

<style scoped>
*,
:global(body) {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

.minimal-container {
  min-height: 100vh;
  background: #181a1b;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: flex-start;
}
.minimal-header {
  font-size: 1.3rem;
  letter-spacing: 0.1em;
  margin: 3.5rem 0 3rem 0;
  color: #e0e0e0;
  opacity: 0.8;
  font-family: 'Mozilla Text', serif;
}
.minimal-editor {
  width: 92vw;
  max-width: 820px;
  height: 72vh;
  border-radius: 7px;
  border: 1px solid #23272e;
  background: #1e1e1e;
  box-shadow: 0 2px 16px #0006;
  overflow: hidden;
}
</style>
