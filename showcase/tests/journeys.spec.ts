import { expect, test } from '@playwright/test'
import AxeBuilder from '@axe-core/playwright'

for (const locale of ['ar', 'en']) {
  const t = (ar: string, en: string) => locale === 'ar' ? ar : en
  test(`${locale}: filter, validate, review, edit and create a local demo request`, async ({ page }) => {
    const externalRequests: string[] = []
    page.on('request', request => {
      if (/^https?:/.test(request.url()) && new URL(request.url()).hostname !== '127.0.0.1') externalRequests.push(request.url())
    })
    await page.goto('./#/services')
    if (locale === 'en') await page.getByRole('button', { name: 'Switch to English' }).click()
    await expect(page.locator('.service-card')).toHaveCount(6)
    await page.getByRole('button', { name: t('الأعمال', 'Business'), exact: true }).click()
    await expect(page.locator('.service-card')).toHaveCount(1)
    await page.getByRole('searchbox', { name: t('البحث في الخدمات', 'Search services') }).fill('zzzz-no-service')
    await expect(page.locator('.service-card')).toHaveCount(0)
    await page.getByRole('button', { name: t('إعادة تعيين التصفية', 'Reset Filter') }).click()
    await expect(page.locator('.service-card')).toHaveCount(6)
    await page.getByRole('link', { name: t('تصريح تحسين المنزل', 'Home improvement permit'), exact: true }).click()
    await expect(page.getByRole('banner')).toHaveCount(1)
    await page.getByRole('link', { name: t('ابدأ الخدمة التجريبية', 'Start demo service') }).click()
    await expect(page.getByRole('banner')).toHaveCount(1)
    await page.getByRole('button', { name: t('مراجعة الطلب', 'Review request'), exact: true }).click()
    await expect(page.locator('.error-summary')).toBeFocused()
    await expect(page.locator('[aria-invalid="true"]')).toHaveCount(3)
    const invalidScan = await new AxeBuilder({ page }).withTags(['wcag2a', 'wcag2aa', 'wcag21a', 'wcag21aa']).analyze()
    expect(invalidScan.violations).toEqual([])
    await page.locator('.error-summary').getByRole('link').nth(1).click()
    await expect(page.getByLabel(t('بريد إلكتروني تجريبي', 'Demo email'))).toBeFocused()
    await page.getByLabel(t('اسم تجريبي', 'Demo name')).fill(t('مستفيد تجريبي', 'Demo Visitor'))
    await page.getByLabel(t('بريد إلكتروني تجريبي', 'Demo email')).fill('demo@example.com')
    await page.getByLabel(t('وصف الطلب', 'Request description')).fill(t('هذا طلب خيالي لاختبار تحسين المنزل فقط.', 'A fictional home improvement request used only to test the showcase.'))
    await page.getByRole('button', { name: t('مراجعة الطلب', 'Review request'), exact: true }).click()
    await expect(page.getByRole('heading', { name: t('كل شيء واضح؟', 'Does everything look right?') })).toBeFocused()
    await page.getByRole('button', { name: t('تعديل البيانات', 'Edit details') }).click()
    await expect(page.getByLabel(t('بريد إلكتروني تجريبي', 'Demo email'))).toHaveValue('demo@example.com')
    await page.getByRole('button', { name: t('مراجعة الطلب', 'Review request'), exact: true }).click()
    await page.getByRole('button', { name: t('تأكيد الطلب التجريبي', 'Confirm demo request') }).click()
    await expect(page.getByRole('heading', { name: t('تم إنشاء طلبك التجريبي', 'Your demo request is ready') })).toBeVisible()
    const reference = (await page.locator('.reference-box strong').innerText()).trim()
    expect(reference).toMatch(/^WASL-2026-\d+$/)
    await page.getByRole('link', { name: t('متابعة الطلب التجريبي', 'Track demo request'), exact: true }).click()
    await expect(page.getByLabel(t('الرقم المرجعي للطلب', 'Request reference'), { exact: true })).toHaveValue(reference)
    await expect(page.getByText(reference, { exact: true })).toBeVisible()
    await expect(page.getByRole('banner')).toHaveCount(1)
    expect(externalRequests).toEqual([])
  })

  test(`${locale}: tracking empty, unknown, simulated error and successful retry`, async ({ page }) => {
    await page.goto('./#/track')
    if (locale === 'en') await page.getByRole('button', { name: 'Switch to English' }).click()
    const input = page.getByLabel(t('الرقم المرجعي للطلب', 'Request reference'), { exact: true })
    await page.getByRole('button', { name: t('متابعة الطلب', 'Track request'), exact: true }).click()
    await expect(input).toBeFocused()
    await expect(input).toHaveAttribute('aria-invalid', 'true')
    await input.fill('WASL-2026-9999')
    await page.getByRole('button', { name: t('متابعة الطلب', 'Track request'), exact: true }).click()
    await expect(page.getByRole('heading', { name: t('لم نعثر على هذا الطلب', 'We couldn’t find that request') })).toBeFocused()
    await page.getByText(t('استكشاف حالات الواجهة', 'Explore interface states'), { exact: true }).click()
    await page.getByRole('button', { name: t('محاكاة خطأ اتصال', 'Simulate a connection error') }).click()
    await expect(page.getByRole('heading', { name: t('تعذّر تحميل حالة الطلب', 'The request status couldn’t load') })).toBeFocused()
    await page.getByRole('button', { name: t('إعادة المحاولة بالطلب النموذجي', 'Retry with sample request') }).click()
    await expect(page.locator('.request-result-card .request-reference')).toHaveText('WASL-2026-1042')
    await expect(page.getByRole('heading', { name: t('تم استلام الطلب', 'Request received') })).toBeVisible()
  })
}

test('language switch preserves unfinished input and translates errors', async ({ page }) => {
  await page.goto('./#/apply/home-permit')
  await page.getByLabel('اسم تجريبي').fill('مستفيد تجريبي')
  await page.getByRole('button', { name: 'مراجعة الطلب', exact: true }).click()
  await page.getByRole('button', { name: 'Switch to English' }).click()
  await expect(page.getByLabel('Demo name')).toHaveValue('مستفيد تجريبي')
  await expect(page.locator('.error-summary')).toContainText('This field is required.')
  await expect(page.locator('html')).toHaveAttribute('dir', 'ltr')
})

test('every home-page hash route resolves without accumulating duplicate layout', async ({ page }) => {
  const errors: string[] = []
  page.on('console', message => { if (message.type() === 'error') errors.push(message.text()) })
  await page.goto('./?lang=en#/')
  const links = await page.locator('a[href^="#/"]').evaluateAll(elements => [...new Set(elements.map(el => el.getAttribute('href')!))])
  expect(links.length).toBeGreaterThan(8)
  for (const href of links) {
    await page.goto(`./?lang=en${href}`)
    await expect(page.locator('main h1')).toHaveCount(1)
    await expect(page.locator('.not-found')).toHaveCount(0)
    await expect(page.getByRole('banner')).toHaveCount(1)
    await expect(page.getByRole('contentinfo')).toHaveCount(1)
  }
  expect(errors).toEqual([])
})
