import { useMemo, useState } from 'react';
import { ArrowUpRight, Check, CircleCheck, Layers3, MousePointer2, Search, ShieldCheck, Sparkles, Waypoints, X } from 'lucide-react';
import { services, type Category } from '../data';
import { useI18n } from '../i18n';
import { EmptyResults, FlowArrow, ServiceCard, ServiceFilters } from '../components/ui';

function HeroArt() {
  const { t } = useI18n();
  return <div className="hero-art" aria-hidden="true">
    <div className="art-grid"><span /><span /><span /><span /><span /><span /><span /><span /><span /></div>
    <div className="art-topline"><span className="art-mini-mark"><span /><span /><span /><span /></span><span>{t('مصمّمة حولك', 'Designed around you')}</span></div>
    <div className="art-arch arch-one" /><div className="art-arch arch-two" /><div className="art-arch arch-three" />
    <div className="art-small-tile"><Waypoints size={32} strokeWidth={1.5} /><span>{t('كل خطوة، أقرب', 'Closer, at every step')}</span></div>
    <div className="art-request-card"><div className="art-card-top"><span className="art-check"><Check size={24} /></span><div><strong>{t('طلبك في المسار الصحيح', 'Your request is on track')}</strong><span>{t('تجربة أوضح. من البداية.', 'Clarity. From the first step.')}</span></div></div><div className="art-progress"><span /><span /><span /></div><div className="art-card-bottom"><span>{t('تم استلام الطلب', 'Request received')}</span><bdi>01 / 03</bdi></div></div>
    <div className="art-bottom-label"><span className="dot-grid">···<br />···<br />···</span><span>{t('وصول بلا تعقيد', 'Simply connected')}</span><span className="art-orbit">↗</span></div>
  </div>;
}

export function HomePage() {
  const { t, local } = useI18n();
  const [query, setQuery] = useState('');
  const [heroQuery, setHeroQuery] = useState('');
  const [category, setCategory] = useState<Category>('all');
  const filtered = useMemo(() => services.filter(service => (category === 'all' || service.category === category) && `${local(service.title)} ${local(service.description)}`.toLocaleLowerCase().includes(query.trim().toLocaleLowerCase())), [category, query, local]);
  return <>
    <section className="hero"><div className="container hero-layout"><div className="hero-content"><span className="hero-eyebrow"><span />{t('تجربة رقمية للجميع', 'A digital experience for everyone')}</span><h1>{t('خدمات أقرب.', 'Services, closer.')}<br /><span>{t('حياة أسهل.', 'Life, simpler.')}</span></h1><p className="hero-description">{t('كل ما تحتاجه، بخطوات واضحة وفي مكان واحد. استكشف خدمات مصمّمة لتسهّل يومك وتقرّبك من إنجازك.', 'Everything you need, in one place and a few clear steps. Explore services designed to make your day easier and move you forward.')}</p>
      <form className="hero-search" role="search" onSubmit={event => { event.preventDefault(); window.location.hash = `/services?q=${encodeURIComponent(heroQuery)}`; }}><Search size={21} aria-hidden="true" /><input type="search" value={heroQuery} onChange={event => setHeroQuery(event.target.value)} onKeyDown={event => { if (event.key === 'Escape') setHeroQuery(''); }} aria-label={t('ابحث عن الخدمة التي تحتاجها', 'Find the service you need')} placeholder={t('ما الخدمة التي تبحث عنها؟', 'What can we help you with?')} />{heroQuery && <button type="button" className="icon-button" onClick={() => setHeroQuery('')} aria-label={t('مسح بحث الخدمات', 'Clear service search')}><X size={18} aria-hidden="true" /></button>}<button type="submit" className="button primary">{t('بحث', 'Search')}<FlowArrow /></button></form>
      <div className="popular-search"><span>{t('الأكثر بحثًا:', 'Popular:')}</span><a href="#/services/home-permit">{t('تصريح منزل', 'Home permit')}</a><span aria-hidden="true">·</span><a href="#/services/municipal-appointment">{t('حجز موعد', 'Appointment')}</a><span aria-hidden="true">·</span><a href="#/track">{t('متابعة طلب', 'Track request')}</a></div>
    </div><HeroArt /></div></section>
    <div className="container"><div className="trust-strip"><div><span className="trust-icon"><MousePointer2 size={23} aria-hidden="true" /></span><div><strong>{t('خطوات واضحة', 'Clear at every step')}</strong><span>{t('من اختيار الخدمة إلى متابعة الطلب', 'From finding a service to tracking it')}</span></div></div><div><span className="trust-icon"><ShieldCheck size={23} aria-hidden="true" /></span><div><strong>{t('خصوصيتك أولًا', 'Your privacy comes first')}</strong><span>{t('تجربة محلية دون إرسال بياناتك', 'A local demo that never sends your data')}</span></div></div><div><span className="trust-icon"><Layers3 size={23} aria-hidden="true" /></span><div><strong>{t('مصمّمة للجميع', 'Designed to include everyone')}</strong><span>{t('عربية وإنجليزية. وعلى كل شاشة.', 'Arabic and English. On every screen.')}</span></div></div></div></div>
    <section className="services-section section-space" aria-labelledby="home-services-title"><div className="container"><div className="section-heading"><div><span className="eyebrow">{t('نبدأ بما تحتاجه', 'START WITH WHAT YOU NEED')}</span><h2 id="home-services-title">{t('خدمات تناسب يومك', 'Services for your everyday')}</h2><p>{t('للأفراد والأعمال والمجتمع. اختر خدمتك وابدأ تجربتك.', 'For individuals, businesses, and communities. Choose a service and explore.')}</p></div><a className="text-action" href="#/services">{t('عرض جميع الخدمات', 'View All services')}<FlowArrow /></a></div>
      <ServiceFilters query={query} onQuery={setQuery} category={category} onCategory={setCategory} />
      <p className="sr-only" role="status">{t('الخدمات المعروضة:', 'Services shown:')} {filtered.length}</p>
      {filtered.length ? <div className="service-grid">{filtered.map(service => <ServiceCard key={service.id} service={service} />)}</div> : <EmptyResults onReset={() => { setQuery(''); setCategory('all'); }} />}
      <p className="catalog-disclaimer">{t('خدمات ومدة إنجاز توضيحية؛ لا تمثّل إجراءات أو رسومًا رسمية.', 'Illustrative services and timeframes; these do not represent official procedures or fees.')}</p>
    </div></section>
    <section className="journey-section"><div className="container journey-layout"><div><span className="eyebrow">{t('من الفكرة إلى الإنجاز', 'A LITTLE LESS EFFORT')}</span><h2>{t('رحلتك أوضح،', 'A clearer journey,')}<br />{t('خطوة بخطوة.', 'step by step.')}</h2><p>{t('لا حاجة لتخمين الخطوة التالية. تعرف على المتطلبات، جرّب تقديم الطلب، ثم تابع تقدّمه من مكان واحد.', 'No guessing what comes next. Understand the requirements, try a request, and follow its progress in one place.')}</p><a className="text-action" href="#/services">{t('ابدأ باستكشاف الخدمات', 'Start exploring services')}<FlowArrow /></a></div><ol className="journey-steps"><li><span>01</span><div><h3>{t('اختر خدمتك', 'Find your service')}</h3><p>{t('تصفّح الخدمات واطّلع على التفاصيل والمتطلبات.', 'Browse the catalog and review the details and requirements.')}</p></div></li><li><span>02</span><div><h3>{t('جرّب تقديم طلب', 'Try a demo request')}</h3><p>{t('املأ نموذجًا مبسّطًا ببيانات خيالية، وراجعها قبل التأكيد.', 'Complete a simple form with fictional details, then review it.')}</p></div></li><li><span><CircleCheck size={25} aria-hidden="true" /></span><div><h3>{t('تابع كل خطوة', 'Follow every step')}</h3><p>{t('استخدم رقمك المرجعي لمشاهدة حالة الطلب التجريبي.', 'Use your reference to view the progress of your demo request.')}</p></div></li></ol></div></section>
    <section className="kit-section section-space"><div className="container"><div className="kit-banner"><div className="kit-banner-icon"><Sparkles size={32} strokeWidth={1.5} aria-hidden="true" /></div><div><span className="eyebrow">{t('خلف هذه التجربة', 'BEHIND THE EXPERIENCE')}</span><h2>{t('تفاصيل صغيرة. فرق كبير.', 'Small details. A meaningful difference.')}</h2><p>{t('رموز تصميم موثّقة، لغة عربية أصيلة، وإمكانية وصول مدمجة. شاهد كيف تحوّل إضافة dga-kit الإرشادات إلى تجربة حيّة.', 'Documented design tokens, Arabic from the start, and built-in accessibility. See how dga-kit turns guidance into a working experience.')}</p></div><a className="button secondary" href="#/about">{t('اكتشف الإضافة', 'Discover the plugin')}<ArrowUpRight size={19} aria-hidden="true" /></a></div></div></section>
  </>;
}

