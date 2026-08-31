import { expect, test } from '@playwright/test'
import AxeBuilder from '@axe-core/playwright'

const pages = ['/', '/services', '/services/home-permit', '/about', '/track', '/apply/home-permit']

for (const locale of ['ar', 'en']) {
  for (const width of [390, 1440]) {
    test(`${locale} ${width}px: accessible routes and no horizontal overflow`, async ({ page }) => {
      await page.setViewportSize({ width, height: 900 })
      await page.goto('./#/')
      if (locale === 'en') await page.getByRole('button', { name: 'Switch to English' }).click()
      for (const route of pages) {
        await page.goto(`./#${route}`)
        await expect(page.locator('html')).toHaveAttribute('lang', locale)
        await expect(page.locator('html')).toHaveAttribute('dir', locale === 'ar' ? 'rtl' : 'ltr')
        await expect(page.locator('main h1')).toHaveCount(1)
        await page.evaluate(() => document.fonts.ready)
        expect(await page.evaluate(() => document.documentElement.scrollWidth <= window.innerWidth + 1), route).toBe(true)
        const result = await new AxeBuilder({ page }).withTags(['wcag2a', 'wcag2aa', 'wcag21a', 'wcag21aa']).analyze()
        expect(result.violations.map(v => ({ id: v.id, impact: v.impact, nodes: v.nodes.map(n => n.target) })), route).toEqual([])
      }
    })
  }

  test(`${locale}: high contrast, font resizing, feedback, and footer tab order`, async ({ page }) => {
    await page.goto('./#/')
    if (locale === 'en') await page.getByRole('button', { name: 'Switch to English' }).click()
    const before = await page.locator('html').evaluate(el => parseFloat(getComputedStyle(el).fontSize))
    await page.getByRole('button', { name: locale === 'ar' ? 'تكبير حجم الخط' : 'Increase text size', exact: true }).click()
    expect(await page.locator('html').evaluate(el => parseFloat(getComputedStyle(el).fontSize))).toBeGreaterThan(before)
    await page.getByRole('button', { name: locale === 'ar' ? 'تباين عالٍ' : 'High contrast', exact: true }).click()
    const result = await new AxeBuilder({ page }).withTags(['wcag2a', 'wcag2aa', 'wcag21a', 'wcag21aa']).analyze()
    expect(result.violations).toEqual([])
    const firstFooterControl = page.locator('footer').locator('button:enabled, a[href], input:enabled').first()
    await expect(firstFooterControl).toHaveJSProperty('tagName', 'BUTTON')
    await page.getByRole('button', { name: locale === 'ar' ? 'نعم' : 'Yes', exact: true }).click()
    await page.getByRole('radio').first().check()
    await page.getByRole('button', { name: locale === 'ar' ? 'تسجيل الملاحظة التجريبية' : 'Record demo feedback' }).click()
    await expect(page.getByRole('status').filter({ hasText: locale === 'ar' ? 'شكرًا' : 'Thank you' })).toBeVisible()
  })
}

test('keyboard skip link, touch targets, mobile navigation and console', async ({ page }) => {
  const errors: string[] = []
  page.on('pageerror', error => errors.push(error.message))
  await page.setViewportSize({ width: 390, height: 844 })
  await page.goto('./#/')
  await page.keyboard.press('Tab')
  await expect(page.getByRole('link', { name: 'تجاوز إلى المحتوى الرئيسي' })).toBeFocused()
  await page.keyboard.press('Enter')
  await expect(page.locator('main')).toBeFocused()
  await page.getByRole('button', { name: 'فتح القائمة' }).click()
  await page.getByRole('navigation', { name: 'التنقل الرئيسي' }).getByRole('link', { name: 'الخدمات', exact: true }).click()
  await expect(page).toHaveURL(/#\/services$/)
  const smallTargets = await page.locator('a[href], button, input, select, textarea').evaluateAll(elements => elements.flatMap(el => {
    const box = el.getBoundingClientRect()
    const style = getComputedStyle(el)
    if (!box.width || !box.height || style.visibility === 'hidden' || (el as HTMLButtonElement).disabled) return []
    if (el instanceof HTMLInputElement && ['checkbox', 'radio'].includes(el.type)) {
      const label = el.closest('label')?.getBoundingClientRect()
      if (label && label.width >= 44 && label.height >= 44) return []
    }
    return box.width < 43.5 || box.height < 43.5 ? [{ text: el.textContent?.trim().slice(0, 60) || el.getAttribute('aria-label'), width: box.width, height: box.height }] : []
  }))
  expect(smallTargets).toEqual([])
  expect(errors).toEqual([])
})

test('English deep link reflows across the DGA breakpoints and large text', async ({ page }) => {
  await page.goto('./?lang=en#/')
  await expect(page.locator('html')).toHaveAttribute('lang', 'en')
  await page.getByRole('button', { name: 'Increase text size', exact: true }).click()
  await page.getByRole('button', { name: 'Increase text size', exact: true }).click()
  for (const width of [320, 600, 960, 1280]) {
    await page.setViewportSize({ width, height: 900 })
    expect(await page.evaluate(() => document.documentElement.scrollWidth <= window.innerWidth + 1), `${width}px at 120%`).toBe(true)
  }
})
