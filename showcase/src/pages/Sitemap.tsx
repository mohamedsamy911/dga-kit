import { services } from '../data';
import { useI18n } from '../i18n';
import { Breadcrumb, ExternalMark, PageIntro } from '../components/ui';

type Entry = { href: string; label: string; children?: Entry[] };

// DGA's sitemap template: filled points for main pages, empty for subpages; main links Medium,
// subpages Small; subpages indented 16px per level from the right (inline-start in RTL).
export function SitemapPage() {
  const { t, local } = useI18n();
  const entries: Entry[] = [
    { href: '#/', label: t('الرئيسية', 'Home') },
    { href: '#/services', label: t('الخدمات', 'Services'), children: services.map(service => ({ href: `#/services/${service.id}`, label: local(service.title), children: [{ href: `#/apply/${service.id}`, label: t('طلب تجريبي', 'Demo request') }] })) },
    { href: '#/track', label: t('متابعة طلب', 'Track a request') },
    { href: '#/about', label: t('عن التجربة', 'About the showcase') },
    { href: '#/accessibility', label: t('إمكانية الوصول', 'Accessibility') },
    { href: '#/privacy', label: t('الخصوصية والبيانات', 'Privacy and data') },
    { href: '#/sitemap', label: t('خريطة الموقع', 'Sitemap') },
  ];
  const external: Entry[] = [
    { href: 'https://github.com/mohamedsamy911/dga-kit', label: t('المشروع على GitHub', 'Project on GitHub') },
    { href: 'https://github.com/mohamedsamy911/dga-kit/issues', label: t('الإبلاغ عن مشكلة في النموذج', 'Report a showcase issue') },
  ];
  const item = (entry: Entry, level: number) => <li key={entry.href} className={level ? 'sitemap-sub' : 'sitemap-main'}>
    <a href={entry.href}>{entry.label}{/^https?:/.test(entry.href) && <ExternalMark />}</a>
    {entry.children && <ul>{entry.children.map(child => item(child, level + 1))}</ul>}
  </li>;
  return <div className="container page-content"><Breadcrumb items={[{ label: t('الرئيسية', 'Home'), href: '#/' }, { label: t('خريطة الموقع', 'Sitemap') }]} />
    <PageIntro eyebrow={t('معلومات تهمّك', 'GOOD TO KNOW')} title={t('خريطة الموقع', 'Sitemap')} description={t('جميع صفحات وصل في مكان واحد، بالترتيب نفسه المستخدم في التنقل ومسار التصفح.', 'Every WASL page in one place, in the same structure as the navigation and breadcrumbs.')} />
    <nav className="sitemap" aria-label={t('خريطة الموقع', 'Sitemap')}><h2>{t('صفحات وصل', 'WASL pages')}</h2><ul>{entries.map(entry => item(entry, 0))}</ul>
      <h2>{t('مصادر خارجية', 'External resources')}</h2><ul>{external.map(entry => item(entry, 0))}</ul></nav>
  </div>;
}
