import { expect, test } from '@playwright/test'

// Guidance added to dga-kit after the showcase was first built (0.8.0-0.13.0), mostly from DGA's
// Assessment Checklist. Each check names the item it holds the showcase to.
const routes = ['/', '/services', '/services/home-permit', '/apply/home-permit', '/track', '/about', '/privacy', '/accessibility']

for (const locale of ['ar', 'en']) {
  const t = (ar: string, en: string) => locale === 'ar' ? ar : en
  const open = async (page: import('@playwright/test').Page, route: string) => {
    await page.goto(`./${locale === 'en' ? '?lang=en' : ''}#${route}`)
    await expect(page.locator('html')).toHaveAttribute('lang', locale)
    // A route that silently fell through to the 404 page would still carry the shared footer.
    await expect(page.locator('main h1')).toHaveCount(1)
    await expect(page.locator('.not-found'), route).toHaveCount(0)
  }

  test(`${locale}: checklist item 7 - the services section comes directly after the hero`, async ({ page }) => {
    await open(page, '/')
    await expect(page.locator('main section.hero + section.services-section')).toHaveCount(1)
  })

  test(`${locale}: checklist item 8 - service page uses DGA's terms and the service card fields`, async ({ page }) => {
    await open(page, '/services/home-permit')
    for (const heading of [t('الشروط', 'Requirements'), t('المستندات المطلوبة', 'Required Documents'), t('الخطوات', 'Steps'), t('بطاقة تفاصيل الخدمة', 'Service Details Card')])
      await expect(page.getByRole('heading', { level: 2, name: heading, exact: true })).toBeVisible()
    const card = page.locator('.service-summary')
    for (const field of [t('الفئة المستهدفة', 'Target audience'), t('المدة التوضيحية', 'Illustrative timeframe'), t('قنوات تقديم الخدمة', 'Service channels'), t('رسوم التجربة', 'Demo fees')])
      await expect(card.locator('dt', { hasText: field })).toHaveCount(1)
  })

  test(`${locale}: external links, and only external links, carry an external-link icon (Lucide stand-in for items 14/29)`, async ({ page }) => {
    let externals = 0
    for (const route of routes) {
      await open(page, route)
      const links = await page.locator('a[href]').evaluateAll(anchors => anchors.map(a => ({
        href: a.getAttribute('href') || '', marked: !!a.querySelector('.external-mark'),
      })))
      for (const link of links) expect(link.marked, `${route} ${link.href}`).toBe(/^https?:/.test(link.href))
      externals += links.filter(link => /^https?:/.test(link.href)).length
    }
    expect(externals).toBeGreaterThan(0)
  })

  test(`${locale}: the footer link for reporting showcase issues is on every page`, async ({ page }) => {
    for (const route of routes) {
      await open(page, route)
      await expect(page.locator('footer a[href="https://github.com/mohamedsamy911/dga-kit/issues"]'), route).toHaveCount(1)
    }
  })

  test(`${locale}: checklist item 41 - the privacy page is linked before the form collects data`, async ({ page }) => {
    await open(page, '/apply/home-permit')
    const order = await page.locator('form').evaluate(form => {
      const privacy = form.querySelector('a[href="#/privacy"]')
      const firstField = form.querySelector('input, textarea')
      return !!privacy && !!firstField && !!(privacy.compareDocumentPosition(firstField) & Node.DOCUMENT_POSITION_FOLLOWING)
    })
    expect(order).toBe(true)
  })
}
