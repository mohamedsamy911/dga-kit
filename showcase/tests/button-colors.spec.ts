import { expect, test, type Locator, type Page } from '@playwright/test'

// Exercise the browser's resolved cascade, including transparent backgrounds and
// ancestor opacity. Disabled contrast is our usability target, not a WCAG rule.
async function colors(button: Locator) {
  return button.evaluate(element => {
    const rgba = (value: string) => {
      const parts = value.match(/[\d.]+/g)!.map(Number)
      return [parts[0], parts[1], parts[2], parts[3] ?? 1]
    }
    const mix = (front: number[], back: number[]) => [
      ...front.slice(0, 3).map((channel, index) => channel * front[3] + back[index] * (1 - front[3])), 1,
    ]
    const luminance = (color: number[]) => color.slice(0, 3).map(channel => {
      const s = channel / 255
      return s <= .04045 ? s / 12.92 : ((s + .055) / 1.055) ** 2.4
    }).reduce((sum, channel, index) => sum + channel * [.2126, .7152, .0722][index], 0)
    const ratio = (a: number[], b: number[]) => {
      const x = luminance(a), y = luminance(b)
      return (Math.max(x, y) + .05) / (Math.min(x, y) + .05)
    }
    const ancestors: Element[] = []
    for (let parent = element.parentElement; parent; parent = parent.parentElement) ancestors.unshift(parent)
    let canvas = [255, 255, 255, 1]
    for (const ancestor of ancestors) canvas = mix(rgba(getComputedStyle(ancestor).backgroundColor), canvas)
    const style = getComputedStyle(element)
    const background = mix(rgba(style.backgroundColor), canvas)
    const opacity = [element, ...ancestors].reduce((value, node) => value * Number(getComputedStyle(node).opacity), 1)
    return {
      color: style.color, background: style.backgroundColor, opacity,
      textRatio: ratio(mix(rgba(style.color), background), background),
      boundaryRatio: ratio(mix(rgba(style.borderTopColor), canvas), canvas),
      focusRatio: ratio(mix(rgba(style.outlineColor), canvas), canvas),
      focusWidth: parseFloat(style.outlineWidth), focusStyle: style.outlineStyle,
      focusVisible: element.matches(':focus-visible'),
    }
  })
}

async function expectDisabledStable(page: Page, button: Locator) {
  await expect(button).toBeDisabled()
  await page.mouse.move(0, 0)
  const resting = await colors(button)
  // Explicitly protect the screenshot defect: inherited pale fill + pale glyph.
  expect(resting.opacity).toBe(1)
  expect(resting.textRatio).toBeGreaterThanOrEqual(3)
  await button.hover()
  const hovered = await colors(button)
  expect(hovered.background).toBe(resting.background)
  expect(hovered.color).toBe(resting.color)
}

for (const locale of ['ar', 'en']) {
  for (const mode of ['standard', 'dark', 'high'] as const) {
    test(`${locale}: footer button colors in ${mode} mode`, async ({ page }, testInfo) => {
      const t = (ar: string, en: string) => locale === 'ar' ? ar : en
      await page.goto(`./?lang=${locale}#/`)
      const footer = page.getByRole('contentinfo')
      const contrast = footer.getByRole('button', { name: t('تباين عالٍ', 'High contrast') })
      const theme = footer.getByRole('button', { name: new RegExp(t('الوضع الداكن', 'Dark mode')) })
      const increase = footer.getByRole('button', { name: t('تكبير حجم الخط', 'Increase text size') })
      const decrease = footer.getByRole('button', { name: t('تصغير حجم الخط', 'Decrease text size') })
      const reset = footer.getByRole('button', { name: t('إعادة حجم الخط إلى 100 بالمئة', 'Reset text size to 100 percent') })
      if (mode === 'dark') await theme.click()
      if (mode === 'high') await contrast.click()
      await expectDisabledStable(page, decrease)
      const measurements: object[] = []
      for (const button of [increase, reset, contrast, theme]) {
        await page.mouse.move(0, 0)
        const resting = await colors(button)
        expect(resting.textRatio).toBeGreaterThanOrEqual(4.5)
        // A visible outline is a project choice, beyond the text/icon requirement.
        expect(resting.boundaryRatio).toBeGreaterThanOrEqual(3)
        await button.hover()
        const hovered = await colors(button)
        expect(hovered.textRatio).toBeGreaterThanOrEqual(4.5)
        await page.mouse.down()
        const pressed = await colors(button)
        expect(pressed.textRatio).toBeGreaterThanOrEqual(4.5)
        await page.mouse.move(0, 0)
        await page.mouse.up()
        await button.focus()
        await page.keyboard.press('Tab')
        await page.keyboard.press('Shift+Tab')
        await expect(button).toBeFocused()
        const focused = await colors(button)
        expect(focused.focusVisible).toBe(true)
        expect(focused.focusWidth).toBeGreaterThanOrEqual(2)
        expect(focused.focusStyle).not.toBe('none')
        expect(focused.focusRatio).toBeGreaterThanOrEqual(3)
        measurements.push({ label: await button.getAttribute('aria-label') ?? await button.innerText(), resting, hovered, pressed, focused })
      }
      await increase.click()
      await expect(decrease).toBeEnabled()
      await increase.click()
      await expectDisabledStable(page, increase)
      await reset.click()
      await expectDisabledStable(page, decrease)
      // The same cascade defect also affected the disabled primary feedback CTA.
      await page.getByRole('button', { name: t('نعم', 'Yes'), exact: true }).click()
      const submit = page.getByRole('button', { name: t('تسجيل الملاحظة التجريبية', 'Record demo feedback') })
      await expectDisabledStable(page, submit)
      expect((await colors(submit)).textRatio).toBeGreaterThanOrEqual(4.5)
      await testInfo.attach('resolved-button-colors', { body: JSON.stringify(measurements, null, 2), contentType: 'application/json' })
    })
  }
}
