import { ArrowLeft, ArrowRight, Building2, CalendarDays, BriefcaseBusiness, Sparkles, HeartHandshake, FileCheck2, Clock3, CircleCheck, Search, X, ChevronLeft, ChevronRight } from 'lucide-react';
import type { ReactNode } from 'react';
import { useI18n } from '../i18n';
import { categories, type Category, type Service } from '../data';

export function FlowArrow({ back = false }: { back?: boolean }) {
  const { locale } = useI18n();
  const Icon = (locale === 'ar') !== back ? ArrowLeft : ArrowRight;
  return <Icon size={20} aria-hidden="true" />;
}

const serviceIcons = { building: Building2, calendar: CalendarDays, briefcase: BriefcaseBusiness, sparkles: Sparkles, heart: HeartHandshake, file: FileCheck2 };

export function ServiceIcon({ name, size = 26 }: { name: Service['icon']; size?: number }) {
  const Icon = serviceIcons[name];
  return <Icon size={size} strokeWidth={1.65} aria-hidden="true" />;
}

export function Brand({ compact = false }: { compact?: boolean }) {
  const { t } = useI18n();
  return <span className={`brand ${compact ? 'brand-compact' : ''}`}>
    <svg className="brand-mark" viewBox="0 0 48 48" fill="none" aria-hidden="true"><path d="M10 10h12v12H10zM26 26h12v12H26z" fill="currentColor" /><path d="M30 10h8v12H26v-8a4 4 0 0 1 4-4ZM10 26h12v12h-8a4 4 0 0 1-4-4v-8Z" fill="currentColor" opacity=".55" /></svg>
    <span className="brand-wordmark"><span className="brand-name"><span lang="ar">وصل</span><bdi lang="en">WASL</bdi></span><span className="brand-descriptor">{t('خدمات رقمية. بتجربة إنسانية.', 'Digital services. A human experience.')}</span></span>
  </span>;
}

export function Breadcrumb({ items }: { items: { label: string; href?: string }[] }) {
  const { locale, t } = useI18n();
  const Chevron = locale === 'ar' ? ChevronLeft : ChevronRight;
  const previous = items[items.length - 2];
  return <nav className="breadcrumbs" aria-label={t('مسار التنقل', 'Breadcrumb')}>
    <ul>{items.map((item, index) => <li key={item.label} className={index === items.length - 2 ? 'previous-crumb' : ''}>
      {index > 0 && <Chevron className="crumb-separator" size={14} aria-hidden="true" />}
      {item.href ? <a href={item.href}>{item.label}</a> : <span aria-current="page">{item.label}</span>}
    </li>)}</ul>
    {previous && <a className="mobile-breadcrumb" href={previous.href}><FlowArrow back />{previous.label}</a>}
  </nav>;
}

export function PageIntro({ eyebrow, title, description, children }: { eyebrow?: string; title: string; description?: string; children?: ReactNode }) {
  return <div className="page-intro">{eyebrow && <span className="eyebrow">{eyebrow}</span>}<h1>{title}</h1>{description && <p>{description}</p>}{children}</div>;
}

export function ServiceCard({ service }: { service: Service }) {
  const { t, local } = useI18n();
  return <article className="service-card">
    <div className="service-card-top"><span className={`icon-tile icon-${service.icon}`}><ServiceIcon name={service.icon} /></span><span className="small-tag">{local(service.tag)}</span></div>
    <h3><a href={`#/services/${service.id}`}>{local(service.title)}</a></h3>
    <p>{local(service.description)}</p>
    <div className="service-meta"><span><Clock3 size={16} aria-hidden="true" />{local(service.duration)}</span><span><CircleCheck size={16} aria-hidden="true" />{t('بدون رسوم للتجربة', 'Free to explore')}</span></div>
    <a className="card-action" href={`#/services/${service.id}`}>{t('تفاصيل الخدمة', 'Service details')}<FlowArrow /></a>
  </article>;
}

export function ServiceFilters({ query, onQuery, category, onCategory }: { query: string; onQuery: (query: string) => void; category: Category; onCategory: (category: Category) => void }) {
  const { t, local } = useI18n();
  return <div className="catalog-controls">
    <div className="filter-buttons" role="group" aria-label={t('تصفية حسب الفئة', 'Filter by category')}>
      {categories.map(item => <button type="button" key={item.id} onClick={() => onCategory(item.id)} aria-pressed={category === item.id} className={category === item.id ? 'filter active' : 'filter'}>{local(item.label)}</button>)}
    </div>
    <div className="search-field"><Search size={20} aria-hidden="true" /><input type="search" aria-label={t('البحث في الخدمات', 'Search services')} value={query} onChange={event => onQuery(event.target.value)} onKeyDown={event => { if (event.key === 'Escape') onQuery(''); }} placeholder={t('ابحث عن خدمة...', 'Search for a service…')} />{query && <button type="button" className="icon-button" onClick={() => onQuery('')} aria-label={t('مسح البحث', 'Clear search')}><X size={18} aria-hidden="true" /></button>}</div>
  </div>;
}

export function EmptyResults({ onReset }: { onReset: () => void }) {
  const { t } = useI18n();
  return <div className="empty-state" role="status"><span className="icon-tile"><Search size={28} aria-hidden="true" /></span><h3>{t('لم يتم العثور على بيانات', 'No Data Found')}</h3><p>{t('جرّب كلمات أخرى أو اعرض جميع الخدمات المتاحة.', 'Try another search or explore all available services.')}</p><button className="button secondary" onClick={onReset}>{t('إعادة تعيين التصفية', 'Reset Filter')}</button></div>;
}

export function DemoNote({ children }: { children?: ReactNode }) {
  const { t } = useI18n();
  return <div className="demo-note"><span className="demo-dot" aria-hidden="true" /><p>{children || t('تجربة توضيحية فقط. جميع الخدمات والطلبات خيالية، ولا تُرسل أي بيانات إلى جهة حكومية.', 'Demonstration only. All services and requests are fictional; no data is sent to a government entity.')}</p></div>;
}

