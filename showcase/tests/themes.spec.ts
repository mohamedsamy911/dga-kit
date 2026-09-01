import { expect, test } from '@playwright/test'
import AxeBuilder from '@axe-core/playwright'

const routes = ['/', '/services', '/services/home-permit', '/about', '/track', '/apply/home-permit']

for (const locale of ['ar', 'en']) {
  for (const width of [390, 1440]) {
    test(`${locale} ${width}px: dark theme covers the main routes`, async ({ page }) => {
      await page.setViewportSize({ width, height: 900 })
      await page.goto(`./?lang=${locale}#/`)
      const html = page.locator('html')
      const body = page.locator('body')
      const toggle = page.getByRole('button', { name: locale === 'ar' ? 'الوضع الداكن' : 'Dark mode' })
      const lightBackground = await body.evaluate(element => getComputedStyle(element).backgroundColor)

      await expect(toggle).toHaveAttribute('aria-pressed', 'false')
      await toggle.click()
      await expect(toggle).toHaveAttribute('aria-pressed', 'true')
      await expect(html).toHaveAttribute('data-theme', 'dark')
      expect(await html.evaluate(element => getComputedStyle(element).colorScheme)).toContain('dark')
      expect(await body.evaluate(element => getComputedStyle(element).backgroundColor)).not.toBe(lightBackground)

      for (const route of routes) {
        await page.evaluate(nextRoute => { window.location.hash = nextRoute }, route)
        await expect(page).toHaveURL(new RegExp(`#${route.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')}$`))
        await expect(html).toHaveAttribute('data-theme', 'dark')
        await expect(page.locator('main h1')).toHaveCount(1)
        await page.evaluate(() => document.fonts.ready)
        expect(await page.evaluate(() => document.documentElement.scrollWidth <= window.innerWidth + 1), route).toBe(true)
        const result = await new AxeBuilder({ page }).withTags(['wcag2a', 'wcag2aa', 'wcag21a', 'wcag21aa']).analyze()
        expect(result.violations.map(violation => ({ id: violation.id, impact: violation.impact, nodes: violation.nodes.map(node => node.target) })), route).toEqual([])
      }
    })
  }
}

test('dark selection survives high contrast and remains session-local', async ({ page }) => {
  await page.goto('./?lang=en#/')
  const html = page.locator('html')
  const body = page.locator('body')
  const theme = page.getByRole('button', { name: 'Dark mode' })
  const contrast = page.getByRole('button', { name: 'High contrast' })

  await theme.click()
  const darkBackground = await body.evaluate(element => getComputedStyle(element).backgroundColor)
  await contrast.click()
  await expect(html).toHaveAttribute('data-theme', 'dark')
  await expect(html).toHaveAttribute('data-contrast', 'high')
  const highContrastBackground = await body.evaluate(element => getComputedStyle(element).backgroundColor)
  expect(highContrastBackground).not.toBe(darkBackground)

  await theme.click()
  await expect(html).toHaveAttribute('data-theme', 'light')
  expect(await body.evaluate(element => getComputedStyle(element).backgroundColor)).toBe(highContrastBackground)
  await theme.click()
  await expect(html).toHaveAttribute('data-theme', 'dark')
  expect(await body.evaluate(element => getComputedStyle(element).backgroundColor)).toBe(highContrastBackground)

  await contrast.click()
  await expect(html).toHaveAttribute('data-contrast', 'standard')
  expect(await body.evaluate(element => getComputedStyle(element).backgroundColor)).toBe(darkBackground)
  await page.reload()
  await expect(html).toHaveAttribute('data-theme', 'light')
  await expect(theme).toHaveAttribute('aria-pressed', 'false')
})
