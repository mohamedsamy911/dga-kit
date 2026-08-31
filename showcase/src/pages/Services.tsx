import { useState } from 'react';
import { Check, CircleCheck, Clock3, FileText, Info, ListChecks, ShieldCheck } from 'lucide-react';
import { services, type Category, type Service } from '../data';
import { useI18n } from '../i18n';
import { Breadcrumb, DemoNote, EmptyResults, FlowArrow, PageIntro, ServiceCard, ServiceFilters, ServiceIcon } from '../components/ui';

export function ServicesPage({ initialQuery }: { initialQuery: string }) {
  const { t, local, number } = useI18n();
  const [query, setQuery] = useState(initialQuery);
  const [category, setCategory] = useState<Category>('all');
  const filtered = services.filter(service => (category === 'all' || service.category === category) && `${local(service.title)} ${local(service.description)}`.toLocaleLowerCase().includes(query.trim().toLocaleLowerCase()));
  return <div className="container page-content"><Breadcrumb items={[{ label: t('الرئيسية', 'Home'), href: '#/' }, { label: t('الخدمات', 'Services') }]} /><PageIntro eyebrow={t('الخدمات الرقمية', 'DIGITAL SERVICES')} title={t('بماذا نساعدك اليوم؟', 'How can we help today?')} description={t('خدمات مصمّمة حول احتياجاتك. استكشف رحلة رقمية كاملة ببيانات تجريبية.', 'Services designed around your needs. Explore a complete digital journey with demo data.')} />
    <ServiceFilters query={query} onQuery={setQuery} category={category} onCategory={setCategory} /><p className="results-count" role="status">{t('عدد الخدمات:', 'Services found:')} <bdi>{number(filtered.length)}</bdi></p>
    {filtered.length > 0 ? <div className="service-grid">{filtered.map(service => <ServiceCard key={service.id} service={service} />)}</div> : <EmptyResults onReset={() => { setQuery(''); setCategory('all'); }} />}
    <DemoNote />
  </div>;
}

export function ServiceDetailPage({ service }: { service: Service }) {
  const { t, local } = useI18n();
  const sections = [
    { id: 'overview-title', label: t('عن الخدمة', 'About the service') },
    { id: 'eligibility-title', label: t('قبل أن تبدأ', 'Before you start') },
    { id: 'documents-title', label: t('المتطلبات', 'Requirements') },
    { id: 'steps-title', label: t('الخطوات', 'Steps') },
  ];
  const steps = [
    { title: t('أدخل بيانات تجريبية', 'Enter demo details'), body: t('استخدم اسمًا وبريدًا خياليين، ثم اكتب وصفًا موجزًا للطلب.', 'Use a fictional name and email, then briefly describe the request.') },
    { title: t('راجع ثم أكّد', 'Review and confirm'), body: t('تأكّد من البيانات في صفحة المراجعة قبل إنشاء الطلب محليًا.', 'Check the review screen before creating a request locally.') },
    { title: t('تابع حالة الطلب', 'Track the request'), body: t('احصل على رقم مرجعي يعمل خلال هذه الجلسة فقط.', 'Receive a reference that works during this session only.') },
  ];
  return <div className="container page-content"><Breadcrumb items={[{ label: t('الرئيسية', 'Home'), href: '#/' }, { label: t('الخدمات', 'Services'), href: '#/services' }, { label: local(service.title) }]} /><div className="detail-heading"><span className={`icon-tile large icon-${service.icon}`}><ServiceIcon name={service.icon} size={32} /></span><span className="small-tag">{local(service.tag)}</span></div><PageIntro title={local(service.title)} description={local(service.description)} />
    <nav className="page-toc" aria-label={t('في هذه الصفحة', 'On this page')}><strong>{t('في هذه الصفحة', 'On this page')}</strong>{sections.map(section => <a href={`#${section.id}`} key={section.id} onClick={event => { event.preventDefault(); const heading = document.getElementById(section.id); heading?.focus(); heading?.scrollIntoView({ block: 'start' }); }}>{section.label}</a>)}</nav>
    <div className="detail-layout"><div className="detail-body"><section className="content-section" aria-labelledby="overview-title"><h2 id="overview-title" tabIndex={-1}><Info size={23} aria-hidden="true" />{t('عن الخدمة', 'About this service')}</h2><p>{t('توضّح هذه الخدمة الخيالية كيف يمكن أن تكون رحلة المستفيد بسيطة وواضحة: معلومات قبل البدء، نموذج ميسّر، ومتابعة بعد التأكيد. يمكنك تجربة الرحلة كاملة دون تسجيل دخول.', 'This fictional service demonstrates a clear, simple journey: useful information before starting, an accessible form, and tracking after confirmation. You can explore the entire journey without signing in.')}</p><DemoNote /></section>
      <section className="content-section" aria-labelledby="eligibility-title"><h2 id="eligibility-title" tabIndex={-1}><ShieldCheck size={23} aria-hidden="true" />{t('قبل أن تبدأ', 'Before you start')}</h2><ul className="check-list">{service.eligibility.map(item => <li key={item.en}><Check size={18} aria-hidden="true" /><span>{local(item)}</span></li>)}</ul></section>
      <section className="content-section" aria-labelledby="documents-title"><h2 id="documents-title" tabIndex={-1}><FileText size={23} aria-hidden="true" />{t('ما الذي ستحتاجه؟', 'What will you need?')}</h2><ul className="check-list">{service.documents.map(item => <li key={item.en}><Check size={18} aria-hidden="true" /><span>{local(item)}</span></li>)}</ul></section>
      <section className="content-section" aria-labelledby="steps-title"><h2 id="steps-title" tabIndex={-1}><ListChecks size={23} aria-hidden="true" />{t('خطوات التجربة', 'The demo journey')}</h2><ol className="detail-steps">{steps.map((step, index) => <li key={step.title}><span className="step-number">{index + 1}</span><div><h3>{step.title}</h3><p>{step.body}</p></div></li>)}</ol></section>
    </div><aside className="service-summary" aria-labelledby="summary-title"><h2 id="summary-title">{t('الخدمة في لمحة', 'At a glance')}</h2><dl><div><dt><Clock3 size={19} aria-hidden="true" />{t('المدة التوضيحية', 'Illustrative timeframe')}</dt><dd>{local(service.duration)}</dd></div><div><dt><CircleCheck size={19} aria-hidden="true" />{t('رسوم التجربة', 'Demo fees')}</dt><dd>{t('بدون رسوم', 'Free')}</dd></div><div><dt><ShieldCheck size={19} aria-hidden="true" />{t('تسجيل الدخول', 'Sign-in')}</dt><dd>{t('غير مطلوب', 'Not required')}</dd></div></dl><a className="button primary full-width" href={`#/apply/${service.id}`}>{t('ابدأ الخدمة التجريبية', 'Start demo service')}<FlowArrow /></a><p className="summary-disclaimer">{t('لا ينشئ هذا الإجراء طلبًا رسميًا. لا ترفع مستندات أو تُدخل بيانات شخصية حقيقية.', 'This does not create an official request. Do not upload documents or enter real personal details.')}</p><a className="text-action" href="#/track">{t('لديك رقم طلب تجريبي؟', 'Already have a demo reference?')}</a></aside></div>
  </div>;
}


