import { useState } from 'react';
import { Accessibility, ArrowUpRight, Check, Contrast, Globe2, Info, Menu, Minus, Moon, Plus, Sun, X } from 'lucide-react';
import { PAGE_UPDATED, PLATFORM_UPDATED } from '../data';
import { useI18n } from '../i18n';
import { Brand } from './ui';

export function Header({ route, onLanguage }: { route: string; onLanguage: () => void }) {
  const { locale, t } = useI18n();
  const [menuOpen, setMenuOpen] = useState(false);
  const links = [
    { href: '#/', label: t('الرئيسية', 'Home'), active: route === '/' },
    { href: '#/services', label: t('الخدمات', 'Services'), active: route.startsWith('/services') || route.startsWith('/apply') },
    { href: '#/track', label: t('متابعة طلب', 'Track a request'), active: route === '/track' },
    { href: '#/about', label: t('عن التجربة', 'About the showcase'), active: route === '/about' },
  ];
  return <header className="site-header">
    <a className="skip-link" href="#main-content" onClick={event => { event.preventDefault(); document.getElementById('main-content')?.focus(); document.getElementById('main-content')?.scrollIntoView(); }}>{t('تجاوز إلى المحتوى الرئيسي', 'Skip to main content')}</a>
    <div className="demo-banner"><div className="container demo-banner-inner"><span><Info size={15} aria-hidden="true" />{t('منصة خيالية لعرض قدرات إضافة dga-kit — ليست خدمة حكومية', 'A fictional showcase of the dga-kit plugin — not a government service')}</span><a href="#/about">{t('تعرّف على التجربة', 'Explore the showcase')}<ArrowUpRight size={14} aria-hidden="true" /></a></div></div>
    <div className="container header-main">
      <a className="brand-link" href="#/" aria-label={t('وصل — الرئيسية', 'WASL — Home')} onClick={() => setMenuOpen(false)}><Brand /></a>
      <nav className={`main-nav ${menuOpen ? 'is-open' : ''}`} id="main-navigation" aria-label={t('التنقل الرئيسي', 'Main navigation')}>
        {links.map(link => <a key={link.href} href={link.href} onClick={() => setMenuOpen(false)} aria-current={link.active ? 'page' : undefined}>{link.label}</a>)}
      </nav>
      <div className="header-actions"><button type="button" className="language-button" onClick={onLanguage} lang={locale === 'ar' ? 'en' : 'ar'} aria-label={locale === 'ar' ? 'Switch to English' : 'التبديل إلى العربية'}><Globe2 size={19} aria-hidden="true" />{locale === 'ar' ? 'English' : 'العربية'}</button><button type="button" className="menu-button icon-button" aria-controls="main-navigation" aria-expanded={menuOpen} aria-label={menuOpen ? t('إغلاق القائمة', 'Close menu') : t('فتح القائمة', 'Open menu')} onClick={() => setMenuOpen(value => !value)}>{menuOpen ? <X aria-hidden="true" /> : <Menu aria-hidden="true" />}</button></div>
    </div>
  </header>;
}

export function Feedback() {
  const { t } = useI18n();
  const [answer, setAnswer] = useState<'yes' | 'no' | null>(null);
  const [reason, setReason] = useState('');
  const [done, setDone] = useState(false);
  const positive = [t('المعلومات واضحة', 'The information is clear'), t('الخدمة سهلة الاستخدام', 'The service is easy to use'), t('وجدت ما أبحث عنه', 'I found what I needed')];
  const negative = [t('المعلومات غير كافية', 'I need more information'), t('واجهت صعوبة في الاستخدام', 'The page was difficult to use'), t('لم أجد ما أبحث عنه', 'I could not find what I needed')];
  return <section className="feedback-section" aria-labelledby="feedback-title"><div className="container">
    <div className="feedback-heading"><div><h2 id="feedback-title">{t('هل كانت هذه الصفحة مفيدة؟', 'Was this page useful?')}</h2><p>{t('رأيك يساعد في توضيح تجربة المشاركة الرقمية.', 'Your feedback demonstrates a more participatory digital experience.')}</p></div>
      {!done && <div className="feedback-choices" role="group" aria-label={t('هل كانت الصفحة مفيدة؟', 'Was this page useful?')}><button className="button secondary" aria-pressed={answer === 'yes'} onClick={() => { setAnswer('yes'); setReason(''); }}>{t('نعم', 'Yes')}</button><button className="button secondary" aria-pressed={answer === 'no'} onClick={() => { setAnswer('no'); setReason(''); }}>{t('لا', 'No')}</button></div>}
      {done && <p className="feedback-thanks" role="status"><Check size={20} aria-hidden="true" />{t('شكرًا لك. سُجّلت ملاحظتك في هذه الجلسة فقط.', 'Thank you. Feedback recorded in this session only.')}</p>}
    </div>
    {answer && !done && <form className="feedback-form" onSubmit={event => { event.preventDefault(); if (reason) setDone(true); }}><fieldset><legend>{t('ما السبب؟ اختر إجابة واحدة.', 'Why? Choose one reason.')}</legend><div className="reason-options">{(answer === 'yes' ? positive : negative).map((label, index) => <label key={label} className="choice-label"><input type="radio" name="feedback-reason" value={String(index)} checked={reason === String(index)} onChange={event => setReason(event.target.value)} required />{label}</label>)}</div></fieldset><div className="feedback-form-bottom"><p>{t('عرض محلي فقط؛ لا تُرسل الملاحظات إلى أي جهة.', 'Local demonstration only; feedback is not sent anywhere.')}</p><button type="submit" className="button primary" disabled={!reason}>{t('تسجيل الملاحظة التجريبية', 'Record demo feedback')}</button></div></form>}
  </div></section>;
}

export function Footer({ fontScale, theme, contrast, onFontScale, onTheme, onContrast }: { fontScale: number; theme: 'light' | 'dark'; contrast: boolean; onFontScale: (value: number) => void; onTheme: () => void; onContrast: () => void }) {
  const { t, date, number } = useI18n();
  return <footer className="site-footer"><div className="container">
    <div className="accessibility-tools"><div className="footer-tools-title"><Accessibility size={22} aria-hidden="true" /><span>{t('تجربة تناسب الجميع', 'An experience for everyone')}</span></div>
      <div className="tool-group" role="group" aria-label={t('حجم الخط', 'Text size')}><span>{t('حجم الخط', 'Text size')}</span><button type="button" className="footer-icon-button" disabled={fontScale === 100} onClick={() => onFontScale(Math.max(100, fontScale - 10))} aria-label={t('تصغير حجم الخط', 'Decrease text size')}><Minus size={18} aria-hidden="true" /></button><button type="button" className="font-reset" onClick={() => onFontScale(100)} aria-label={t('إعادة حجم الخط إلى 100 بالمئة', 'Reset text size to 100 percent')}><bdi>{number(fontScale)}%</bdi></button><button type="button" className="footer-icon-button" disabled={fontScale === 120} onClick={() => onFontScale(Math.min(120, fontScale + 10))} aria-label={t('تكبير حجم الخط', 'Increase text size')}><Plus size={18} aria-hidden="true" /></button></div>
      <div className="preference-group" role="group" aria-label={t('مظهر المنصة', 'Display appearance')}>
        <button type="button" className="contrast-button" onClick={onContrast} aria-pressed={contrast}><Contrast size={20} aria-hidden="true" />{t('تباين عالٍ', 'High contrast')}{contrast && <Check size={16} aria-hidden="true" />}</button>
        <button type="button" className="theme-button" onClick={onTheme} aria-pressed={theme === 'dark'} aria-label={theme === 'dark' ? t('الوضع الداكن: مفعّل', 'Dark mode: on') : t('الوضع الداكن: غير مفعّل', 'Dark mode: off')} aria-describedby={contrast ? 'theme-contrast-note' : undefined}>{theme === 'dark' ? <Moon size={20} aria-hidden="true" /> : <Sun size={20} aria-hidden="true" />}{theme === 'dark' ? t('داكن', 'Dark') : t('فاتح', 'Light')}</button>
      </div>
      {contrast && <span className="sr-only" id="theme-contrast-note" role="status">{t('التباين العالي يعلو مؤقتًا على ألوان الوضع المختار. سيعود الوضع الداكن عند إيقاف التباين العالي.', 'High contrast temporarily overrides the selected theme colors. Dark mode will return when high contrast is turned off.')}</span>}
    </div>
    <div className="footer-main"><div className="footer-brand"><Brand compact /><p>{t('تفاصيل مدروسة. وصول أسهل. نموذج مفتوح لتجربة الخدمات الرقمية، مبني بإضافة dga-kit.', 'Thoughtful details. Easier access. An open digital services showcase, built with the dga-kit plugin.')}</p><span className="footer-demo-label">{t('نموذج تجريبي غير رسمي', 'Unofficial demonstration')}</span></div>
      <div className="footer-links"><h2>{t('استكشف وصل', 'Explore WASL')}</h2><a href="#/services">{t('جميع الخدمات', 'All services')}</a><a href="#/track">{t('متابعة طلب تجريبي', 'Track a demo request')}</a><a href="#/about">{t('كيف بُنيت التجربة', 'How the showcase was built')}</a></div>
      <div className="footer-links"><h2>{t('معلومات تهمّك', 'Good to know')}</h2><a href="#/accessibility">{t('إمكانية الوصول', 'Accessibility')}</a><a href="#/privacy">{t('الخصوصية والبيانات', 'Privacy and data')}</a><a href="https://github.com/mohamedsamy911/dga-kit">{t('المشروع على GitHub', 'Project on GitHub')}<ArrowUpRight size={15} aria-hidden="true" /></a></div>
    </div>
    <div className="footer-bottom"><p>{t('وصل © 2026 · صُنع لعرض ما تصنعه التفاصيل.', 'WASL © 2026 · A showcase of the details that matter.')}</p><div className="updated-dates"><span>{t('آخر تحديث للصفحة:', 'Page updated:')} <time dateTime={PAGE_UPDATED}>{date(PAGE_UPDATED)}</time></span><span>{t('آخر تحديث للمنصة:', 'Platform updated:')} <time dateTime={PLATFORM_UPDATED}>{date(PLATFORM_UPDATED)}</time></span></div></div>
  </div></footer>;
}
