import { defineConfig } from '@playwright/test'

const previewURL = 'http://127.0.0.1:4173/dga-kit/'

export default defineConfig({
  testDir: './tests',
  timeout: 45_000,
  expect: { timeout: 8_000 },
  fullyParallel: true,
  workers: 2,
  reporter: [['list'], ['html', { open: 'never' }]],
  use: {
    baseURL: previewURL,
    trace: 'retain-on-failure',
    screenshot: 'only-on-failure',
    viewport: { width: 1440, height: 1000 },
  },
  webServer: {
    command: 'npm run preview',
    url: previewURL,
    reuseExistingServer: false,
    timeout: 30_000,
  },
})
