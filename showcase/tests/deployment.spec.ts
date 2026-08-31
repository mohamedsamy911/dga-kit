import { expect, test } from '@playwright/test'

// Keep this expectation independent of vite.config.ts: a root-base build still
// works in Vite preview, but its /assets URLs break on a GitHub project site.
const projectPath = '/dga-kit/'

test('production assets stay inside the GitHub Pages project path', async ({ page, request }) => {
  const resourceURLs: string[] = []
  const failures: string[] = []
  page.on('request', resource => { resourceURLs.push(resource.url()) })
  page.on('response', response => {
    if (response.status() >= 400) failures.push(`${response.status()} ${response.url()}`)
  })
  page.on('pageerror', error => failures.push(error.message))
  await page.goto('./')
  await expect(page.locator('main h1')).toBeVisible()
  await page.evaluate(() => document.fonts.ready)
  expect(new URL(page.url()).pathname).toBe(projectPath)

  const assets = await page.locator('script[src], link[rel="stylesheet"], link[rel="icon"]').evaluateAll(elements => elements.map(element => ({
    kind: element.tagName === 'SCRIPT' ? 'script' : element.getAttribute('rel'),
    url: (element as HTMLScriptElement).src || (element as HTMLLinkElement).href,
  })))
  expect(assets.some(asset => asset.kind === 'script')).toBe(true)
  expect(assets.some(asset => asset.kind === 'stylesheet')).toBe(true)
  expect(assets.some(asset => asset.kind === 'icon')).toBe(true)
  for (const asset of assets) {
    expect(new URL(asset.url).origin, asset.url).toBe(new URL(page.url()).origin)
    expect(new URL(asset.url).pathname, asset.url).toMatch(/^\/dga-kit\//)
    const response = await request.get(asset.url)
    expect(response.ok(), asset.url).toBe(true)
    expect(response.headers()['content-type'], asset.url).not.toContain('text/html')
  }
  expect(resourceURLs.some(url => /\.woff2?(?:\?|$)/.test(url))).toBe(true)
  for (const url of resourceURLs.filter(url => /^https?:/.test(url))) {
    expect(new URL(url).origin, url).toBe(new URL(page.url()).origin)
    expect(new URL(url).pathname, url).toMatch(/^\/dga-kit\//)
  }
  expect(failures).toEqual([])
})

for (const locale of ['ar', 'en']) {
  test(`${locale}: a shared hash deep link survives production reload`, async ({ page }) => {
    await page.goto(`./?lang=${locale}#/services/home-permit`)
    const heading = page.locator('main h1')
    await expect(heading).toBeVisible()
    const title = await heading.innerText()
    await page.reload()
    await expect(heading).toHaveText(title)
    await expect(page.locator('html')).toHaveAttribute('lang', locale)
    await expect(page.locator('html')).toHaveAttribute('dir', locale === 'ar' ? 'rtl' : 'ltr')
    await expect(page.locator('.not-found')).toHaveCount(0)
    expect(new URL(page.url()).pathname).toBe(projectPath)
    expect(new URL(page.url()).hash).toBe('#/services/home-permit')
    await page.getByRole('link', { name: locale === 'ar' ? 'ابدأ الخدمة التجريبية' : 'Start demo service' }).click()
    await expect(page).toHaveURL(new RegExp(`${projectPath}\\?lang=${locale}#/apply/home-permit$`))
    await expect(page.locator('main')).toBeFocused()
  })
}
