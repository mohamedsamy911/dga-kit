import { useEffect, useRef, useState, type FormEvent } from 'react';
import { CircleCheck, Clock3, FileCheck2, Info, LoaderCircle, Search, TriangleAlert } from 'lucide-react';
import { DEMO_DELAY, DEMO_ERROR_REFERENCE, DEMO_REFERENCE, getService, seededRequest, type DemoRequest } from '../data';
import { useI18n } from '../i18n';
import { Breadcrumb, DemoNote, PageIntro } from '../components/ui';

type TrackState = { status: 'idle' | 'loading' | 'not-found' | 'error' } | { status: 'found'; request: DemoRequest };

export function TrackPage({ initialReference, requests }: { initialReference: string; requests: DemoRequest[] }) {
  const { t, local, date } = useI18n();
  const [reference, setReference] = useState(initialReference);
  const [invalid, setInvalid] = useState(false);
  const [state, setState] = useState<TrackState>({ status: 'idle' });
  const timer = useRef<ReturnType<typeof setTimeout> | null>(null);
  const referenceInput = useRef<HTMLInputElement>(null);
  const resultHeading = useRef<HTMLHeadingElement>(null);
  useEffect(() => () => { if (timer.current) clearTimeout(timer.current); }, []);
  useEffect(() => { if (state.status !== 'idle' && state.status !== 'loading') resultHeading.current?.focus(); }, [state]);
  function search(rawReference: string) {
    const normalized = rawReference.trim().toUpperCase();
    if (!normalized) { setInvalid(true); referenceInput.current?.focus(); return; }
    setInvalid(false);
    if (timer.current) clearTimeout(timer.current);
    setState({ status: 'loading' });
    timer.current = setTimeout(() => {
      if (normalized === DEMO_ERROR_REFERENCE) { setState({ status: 'error' }); return; }
      const found = [seededRequest, ...requests].find(request => request.reference === normalized);
      setState(found ? { status: 'found', request: found } : { status: 'not-found' });
    }, DEMO_DELAY);
  }
  useEffect(() => { if (initialReference) search(initialReference); }, [initialReference]);
  function submit(event: FormEvent<HTMLFormElement>) { event.preventDefault(); search(reference); }
  function useSample() { setReference(DEMO_REFERENCE); search(DEMO_REFERENCE); }
  return <div className="container page-content"><Breadcrumb items={[{ label: t('الرئيسية', 'Home'), href: '#/' }, { label: t('متابعة طلب', 'Track a request') }]} /><PageIntro eyebrow={t('معك في كل خطوة', 'WITH YOU AT EVERY STEP')} title={t('أين وصل طلبك؟', 'Where is your request?')} description={t('أدخل رقم الطلب التجريبي لمعرفة آخر المستجدات. وضوح أكثر، وانتظار أقل.', 'Enter your demo reference to see the latest progress. More clarity, less guesswork.')} />
    <div className="track-layout"><section className="track-form-card" aria-labelledby="track-form-title"><span className="icon-tile large"><Search size={28} aria-hidden="true" /></span><h2 id="track-form-title">{t('متابعة الطلب', 'Track your request')}</h2><p>{t('الأرقام المرجعية الجديدة تعمل حتى تحديث الصفحة فقط.', 'New references work only until this page is reloaded.')}</p><form noValidate onSubmit={submit}><div className="form-field"><label htmlFor="request-reference">{t('الرقم المرجعي للطلب', 'Request reference')}</label><input ref={referenceInput} id="request-reference" name="reference" dir="ltr" autoComplete="off" maxLength={40} value={reference} placeholder="WASL-2026-1042" onChange={event => { setReference(event.target.value); if (invalid && event.target.value.trim()) setInvalid(false); }} onBlur={() => setInvalid(!reference.trim())} aria-describedby={`reference-hint${invalid ? ' reference-error' : ''}`} aria-invalid={invalid} required /><p id="reference-hint" className="field-hint">{t('انسخ الرقم من شاشة تأكيد الطلب، أو جرّب المثال أدناه.', 'Copy the reference from your confirmation, or try the example below.')}</p>{invalid && <p className="field-error" id="reference-error">{t('أدخل رقم الطلب للمتابعة.', 'Enter a request reference to continue.')}</p>}</div><button className="button primary full-width" type="submit" disabled={state.status === 'loading'}>{state.status === 'loading' ? <LoaderCircle className="spinner" size={19} aria-hidden="true" /> : <Search size={19} aria-hidden="true" />}{state.status === 'loading' ? t('جارٍ البحث...', 'Searching…') : t('متابعة الطلب', 'Track request')}</button></form><div className="sample-reference"><span>{t('تريد تجربة سريعة؟', 'Just exploring?')}</span><button className="inline-button" onClick={useSample}>{t('استخدم رقمًا تجريبيًا', 'Use a demo reference')} <bdi>{DEMO_REFERENCE}</bdi></button></div><details className="demo-scenarios"><summary>{t('استكشاف حالات الواجهة', 'Explore interface states')}</summary><p>{t('اختبر حالة تعذّر الاتصال بأمان. لا يوجد خادم فعلي.', 'Safely preview a connection error. There is no real server.')}</p><button className="button secondary" onClick={() => { setReference(DEMO_ERROR_REFERENCE); search(DEMO_ERROR_REFERENCE); }}>{t('محاكاة خطأ اتصال', 'Simulate a connection error')}</button></details></section>
    <section className="track-result" aria-label={t('نتيجة متابعة الطلب', 'Request tracking result')} aria-busy={state.status === 'loading'}>
      {state.status === 'idle' && <div className="track-placeholder"><div className="tracking-illustration" aria-hidden="true"><span /><span /><span /><FileCheck2 size={56} strokeWidth={1.2} /></div><h2>{t('كل التفاصيل في مكان واحد', 'All the details in one place')}</h2><p>{t('ستظهر هنا حالة الطلب وخطواته فور البحث عن الرقم المرجعي.', 'Your request status and milestones will appear here when you search for a reference.')}</p></div>}
      {state.status === 'loading' && <div className="track-placeholder" role="status"><LoaderCircle className="spinner" size={40} aria-hidden="true" /><h2>{t('نبحث عن طلبك التجريبي', 'Finding your demo request')}</h2><p>{t('هذه محاكاة قصيرة لحالة التحميل.', 'This briefly simulates a loading state.')}</p></div>}
      {state.status === 'not-found' && <div className="track-placeholder"><span className="icon-tile large"><Search size={28} aria-hidden="true" /></span><h2 ref={resultHeading} tabIndex={-1}>{t('لم نعثر على هذا الطلب', 'We couldn’t find that request')}</h2><p>{t('تحقّق من الرقم وحاول مرة أخرى. الطلبات التي أُنشئت قبل تحديث الصفحة لا تُحفظ.', 'Check the reference and try again. Requests created before a page reload are not saved.')}</p><button className="button secondary" onClick={useSample}>{t('تجربة طلب نموذجي', 'Try a sample request')}</button></div>}
      {state.status === 'error' && <div className="track-placeholder error-state"><span className="icon-tile large"><TriangleAlert size={28} aria-hidden="true" /></span><h2 ref={resultHeading} tabIndex={-1}>{t('تعذّر تحميل حالة الطلب', 'The request status couldn’t load')}</h2><p>{t('هذا خطأ تجريبي متعمّد. استخدم إعادة المحاولة لاستعراض حالة ناجحة بالرقم النموذجي.', 'This is an intentional demo error. Retry to preview a successful result with the sample reference.')}</p><button className="button primary" onClick={useSample}>{t('إعادة المحاولة بالطلب النموذجي', 'Retry with sample request')}</button></div>}
      {state.status === 'found' && <div className="request-result-card"><div className="request-result-top"><span className="eyebrow">{t('حالة الطلب التجريبي', 'DEMO REQUEST STATUS')}</span><span className="status-pill"><Clock3 size={15} aria-hidden="true" />{state.request.status === 'review' ? t('قيد المراجعة', 'Under review') : t('تم الاستلام', 'Received')}</span></div><h2 ref={resultHeading} tabIndex={-1}>{local(getService(state.request.serviceId)!.title)}</h2><bdi className="request-reference">{state.request.reference}</bdi><p className="request-date">{t('تاريخ الإنشاء:', 'Created:')} {date(state.request.createdAt)}</p><ol className="tracking-timeline"><li className="complete"><span><CheckCircle /></span><div><h3>{t('تم استلام الطلب', 'Request received')}</h3><p>{t('أُنشئ الطلب بنجاح في البيئة التجريبية.', 'The request was created in the demo environment.')}</p></div></li><li className={state.request.status === 'review' ? 'current' : ''} aria-current={state.request.status === 'review' ? 'step' : undefined}><span><Clock3 size={19} aria-hidden="true" /></span><div><h3>{t('مراجعة الطلب', 'Request review')}</h3><p>{state.request.status === 'review' ? t('محاكاة لمراجعة البيانات — هذه هي المرحلة الحالية.', 'Simulated review of the details — this is the current stage.') : t('المرحلة التالية في السيناريو التوضيحي.', 'The next stage in the illustrative scenario.')}</p></div></li><li><span><FileCheck2 size={19} aria-hidden="true" /></span><div><h3>{t('اكتمال الخدمة', 'Service completion')}</h3><p>{t('مرحلة توضيحية فقط؛ لا يُصدر مستند رسمي.', 'Illustrative stage only; no official document is issued.')}</p></div></li></ol><div className="tracking-note"><Info size={18} aria-hidden="true" /><p>{t('الحالة ثابتة لغرض العرض، ولا تعبّر عن إجراء حكومي حقيقي.', 'This status is fixed for demonstration and does not represent a real government process.')}</p></div></div>}
    </section></div><DemoNote />
  </div>;
}

function CheckCircle() { return <CircleCheck size={19} aria-hidden="true" />; }
