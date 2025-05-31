import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import path from 'path'

export default defineConfig({
  plugins: [react()],
  build: {
    outDir: 'dist',
    emptyOutDir: false,
    rollupOptions: {
      input: {
        'content-script': path.resolve(__dirname, 'src/content-script.tsx'),
      },
      output: {
        entryFileNames: 'content-script.js',
        format: 'iife',              // IIFE로 묶기
        inlineDynamicImports: true   // 동적 import를 전부 인라인
      }
    }
  }
})
