import { useEffect, useRef, useState } from 'react';
import { Search } from 'lucide-react';
import { LocaleProvider, useI18n, type Locale } from './i18n';
import { getService, type DemoRequest } from './data';
import { Header, Footer, Feedback } from './components/Layout';
import { FlowArrow } from './components/ui';
import { HomePage } from './pages/Home';
import { ServiceDetailPage, ServicesPage } from './pages/Services';
import { ApplicationPage } from './pages/Application';
import { TrackPage } from './pages/Track';
import { AboutPage, InformationPage } from './pages/About';

function readLocation() { return window.location.hash.slice(1) || '/'; }

export function App() {
  const [locale, setLocale] = useState<Locale>(() => new URLSearchParams(window.location.search).get('lang') === 'en' ? 'en' : 'ar');
  const [location, setLocation] = useState(readLocation);
  const [fontScale, setFontScale] = useState(100);
  const [contrast, setContrast] = useState(false);
  const [requests, setRequests] = useState<DemoRequest[]>([]);
  const nextReference = useRef(2001);
  const main = useRef<HTMLElement>(null);
  const previousLocation = useRef(location);
  const [route, search = ''] = location.split('?');
  const params = new URLSearchParams(search);

  useEffect(() => {
    const change = () => setLocation(readLocation());
    window.addEventListener('hashchange', change);
    return () => window.removeEventListener('hashchange', change);
  }, []);
  useEffect(() => {
    document.documentElement.lang = locale;
    document.documentElement.dir = locale === 'ar' ? 'rtl' : 'ltr';
  }, [locale]);
  useEffect(() => {
    document.documentElement.style.fontSize = `${fontScale}%`;
    document.documentElement.dataset.contrast = contrast ? 'high' : 'standard';
  }, [fontScale, contrast]);
  useEffect(() => {
    if (previousLocation.current !== location) { main.current?.focus(); window.scrollTo({ top: 0, behavior: 'instant' }); }
    previousLocation.current = location;
  }, [location]);
  useEffect(() => {
    const service = getService(route.split('/')[2] || '');
    const pageTitle = route === '/' ? (locale === 'ar' ? 'خدمات أقرب. حياة أسهل.' : 'Services closer. Life simpler.') : service ? service.title[locale] : route === '/services' ? (locale === 'ar' ? 'الخدمات' : 'Services') : route === '/track' ? (locale === 'ar' ? 'متابعة طلب' : 'Track a request') : route === '/privacy' ? (locale === 'ar' ? 'الخصوصية' : 'Privacy') : route === '/accessibility' ? (locale === 'ar' ? 'إمكانية الوصول' : 'Accessibility') : (locale === 'ar' ? 'عن التجربة' : 'About the showcase');
    document.title = `${pageTitle} | ${locale === 'ar' ? 'وصل — نموذج تجريبي' : 'WASL — Demo showcase'}`;
  }, [locale, route]);
  function createRequest(serviceId: string) {
    const request: DemoRequest = { reference: `WASL-2026-${nextReference.current++}`, serviceId, createdAt: new Date().toISOString(), status: 'received' };
    setRequests(previous => [...previous, request]);
    return request;
  }
  const serviceId = route.split('/')[2] || '';
  const service = getService(serviceId);
  let page;
  if (route === '/') page = <HomePage />;
  else if (route === '/services') page = <ServicesPage initialQuery={params.get('q') || ''} />;
  else if (route.startsWith('/services/') && service) page = <ServiceDetailPage service={service} />;
  else if (route.startsWith('/apply/') && service) page = <ApplicationPage service={service} onCreate={createRequest} />;
  else if (route === '/track') page = <TrackPage initialReference={params.get('ref') || ''} requests={requests} />;
  else if (route === '/about') page = <AboutPage />;
  else if (route === '/privacy' || route === '/accessibility') page = <InformationPage kind={route === '/privacy' ? 'privacy' : 'accessibility'} />;
  else page = <NotFound />;
  return <LocaleProvider locale={locale}><Header key={`header:${route}`} route={route} onLanguage={() => setLocale(value => value === 'ar' ? 'en' : 'ar')} /><main id="main-content" ref={main} tabIndex={-1}><div key={location}>{page}</div></main><Feedback key={`feedback:${location}`} /><Footer fontScale={fontScale} contrast={contrast} onFontScale={setFontScale} onContrast={() => setContrast(value => !value)} /></LocaleProvider>;
}

function NotFound() {
  const { t } = useI18n();
  return <div className="container not-found"><span className="icon-tile large"><Search size={32} aria-hidden="true" /></span><span className="eyebrow">404</span><h1>{t('عذرًا، لم نجد هذه الصفحة.', 'Sorry, we couldn’t find that page.')}</h1><p>{t('ربما تغيّر الرابط. يمكنك العودة إلى الرئيسية واستكشاف الخدمات.', 'The link may have changed. Return home to explore the available services.')}</p><a className="button primary" href="#/">{t('العودة إلى الرئيسية', 'Back to the homepage')}<FlowArrow /></a></div>;
}

