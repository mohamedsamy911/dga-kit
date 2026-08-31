import { useEffect, useRef, useState, type FormEvent } from 'react';
import { Check, CircleCheck, Info, LoaderCircle, Pencil } from 'lucide-react';
import { DEMO_DELAY, type DemoRequest, type Service } from '../data';
import { useI18n } from '../i18n';
import { Breadcrumb, DemoNote, FlowArrow } from '../components/ui';

type FormFields = { name: string; email: string; description: string };
type FieldKey = keyof FormFields;
type ErrorCode = 'required' | 'short' | 'email' | 'long';
type FieldErrors = Partial<Record<FieldKey, ErrorCode>>;
const FIELD_LIMITS = { name: 80, email: 120, description: 500 };
const FORM_FIELDS: FieldKey[] = ['name', 'email', 'description'];

function validateField(field: FieldKey, raw: string): ErrorCode | undefined {
  const value = raw.trim();
  if (!value) return 'required';
  if (value.length > FIELD_LIMITS[field]) return 'long';
  if (field === 'email' && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value)) return 'email';
  if (field === 'name' && value.length < 2 || field === 'description' && value.length < 10) return 'short';
}

function ApplicationProgress({ step }: { step: number }) {
  const { t } = useI18n();
  const steps = [t('بيانات الطلب', 'Request details'), t('المراجعة', 'Review'), t('التأكيد', 'Confirmation')];
  return <><ol className="application-progress" aria-label={t('مراحل الطلب', 'Request progress')}>{steps.map((title, index) => <li key={title} aria-current={step === index + 1 ? 'step' : undefined} className={step > index + 1 ? 'completed' : step === index + 1 ? 'current' : ''}><span>{step > index + 1 ? <Check size={18} aria-hidden="true" /> : index + 1}</span><div><strong>{title}</strong><span className="sr-only">{step > index + 1 ? t('مكتملة', 'Completed') : step === index + 1 ? t('الحالية', 'Current') : t('قادمة', 'Upcoming')}</span></div></li>)}</ol><div className="mobile-progress" role="progressbar" aria-valuemin={1} aria-valuemax={3} aria-valuenow={step} aria-valuetext={steps[step - 1]} aria-label={t('مراحل الطلب', 'Request progress')}><span className="mobile-step-ring"><bdi>{step}/3</bdi></span><div><strong>{steps[step - 1]}</strong><span>{t('خطوة واضحة في كل مرحلة', 'Clarity at every step')}</span></div></div></>;
}

export function ApplicationPage({ service, onCreate }: { service: Service; onCreate: (serviceId: string) => DemoRequest }) {
  const { t, local, number } = useI18n();
  const [step, setStep] = useState(1);
  const [fields, setFields] = useState<FormFields>({ name: '', email: '', description: '' });
  const [errors, setErrors] = useState<FieldErrors>({});
  const [validationAttempt, setValidationAttempt] = useState(0);
  const [pending, setPending] = useState(false);
  const [request, setRequest] = useState<DemoRequest | null>(null);
  const errorSummary = useRef<HTMLDivElement>(null);
  const stepHeading = useRef<HTMLHeadingElement>(null);
  const timer = useRef<ReturnType<typeof setTimeout> | null>(null);
  useEffect(() => () => { if (timer.current) clearTimeout(timer.current); }, []);
  useEffect(() => { if (validationAttempt > 0 && Object.keys(errors).length) errorSummary.current?.focus(); }, [validationAttempt]);
  useEffect(() => { if (step > 1) stepHeading.current?.focus(); }, [step]);

  const labels: Record<FieldKey, string> = { name: t('اسم تجريبي', 'Demo name'), email: t('بريد إلكتروني تجريبي', 'Demo email'), description: t('وصف الطلب', 'Request description') };
  function errorText(field: FieldKey, code?: ErrorCode) {
    if (code === 'required') return t('هذا الحقل مطلوب.', 'This field is required.');
    if (code === 'email') return t('أدخل بريدًا تجريبيًا بصيغة صحيحة، مثل demo@example.com.', 'Enter a valid demo email, such as demo@example.com.');
    if (code === 'short') return field === 'name' ? t('أدخل حرفين على الأقل للاسم التجريبي.', 'Enter at least 2 characters for the demo name.') : t('اكتب وصفًا من 10 أحرف على الأقل.', 'Enter a description of at least 10 characters.');
    if (code === 'long') return t('تجاوزت الحد الأقصى للأحرف.', 'The character limit has been exceeded.');
    return '';
  }
  function updateField(field: FieldKey, value: string) {
    setFields(previous => ({ ...previous, [field]: value }));
    // Once a field has an error, clear or update it while typing. Waiting until
    // blur could move the submit button between pointer-down and pointer-up.
    if (errors[field]) setErrors(previous => ({ ...previous, [field]: validateField(field, value) }));
  }
  function blurField(field: FieldKey) { setErrors(previous => ({ ...previous, [field]: validateField(field, fields[field]) })); }
  function review(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    const nextErrors: FieldErrors = {};
    for (const field of FORM_FIELDS) { const error = validateField(field, fields[field]); if (error) nextErrors[field] = error; }
    setErrors(nextErrors);
    if (Object.keys(nextErrors).length) { setValidationAttempt(value => value + 1); return; }
    setStep(2);
  }
  function confirm() {
    setPending(true);
    timer.current = setTimeout(() => { setRequest(onCreate(service.id)); setPending(false); setStep(3); }, DEMO_DELAY);
  }
  const errorFields = FORM_FIELDS.filter(field => errors[field]);
  return <div className="container page-content"><Breadcrumb items={[{ label: t('الرئيسية', 'Home'), href: '#/' }, { label: t('الخدمات', 'Services'), href: '#/services' }, { label: local(service.title), href: `#/services/${service.id}` }, { label: t('طلب تجريبي', 'Demo request') }]} />
    <div className="application-layout"><div className="application-heading"><span className="eyebrow">{t('رحلة الخدمة', 'SERVICE JOURNEY')}</span><h1>{local(service.title)}</h1><p>{t('جرّب الخطوات ببيانات خيالية فقط. لا حاجة إلى تسجيل دخول.', 'Try the journey with fictional details only. No sign-in is needed.')}</p></div><ApplicationProgress step={step} />
    <div className="application-card">
      {step === 1 && <form noValidate onSubmit={review}><div className="form-heading"><h2 ref={stepHeading} tabIndex={-1}>{t('لنبدأ ببيانات الطلب', 'Let’s start with the details')}</h2><p>{t('جميع الحقول مطلوبة. استخدم بيانات خيالية لا تخص شخصًا حقيقيًا.', 'All fields are required. Use fictional details that do not belong to a real person.')}</p></div>
        <DemoNote>{t('لا تُدخل رقم هوية أو عنوانًا أو أي بيانات حساسة. تبقى مدخلاتك في ذاكرة الصفحة فقط.', 'Do not enter an ID number, address, or sensitive information. Your inputs stay in page memory only.')}</DemoNote>
        {errorFields.length > 0 && <div className="error-summary" role="alert" ref={errorSummary} tabIndex={-1}><h3>{t('راجع الحقول التالية قبل المتابعة', 'Check these fields before continuing')}</h3><ul>{errorFields.map(field => <li key={field}><a href={`#${field}`} onClick={event => { event.preventDefault(); document.getElementById(field)?.focus(); }}>{labels[field]}: {errorText(field, errors[field])}</a></li>)}</ul></div>}
        <div className="form-field"><label htmlFor="name">{labels.name} <span aria-hidden="true">*</span></label><input id="name" name="name" autoComplete="off" value={fields.name} maxLength={FIELD_LIMITS.name} onChange={event => updateField('name', event.target.value)} onBlur={() => blurField('name')} aria-invalid={Boolean(errors.name)} aria-describedby={`name-hint${errors.name ? ' name-error' : ''}`} required /><p id="name-hint" className="field-hint">{t('مثال: مستفيد تجريبي. من حرفين إلى 80 حرفًا.', 'Example: Demo Visitor. Between 2 and 80 characters.')}</p>{errors.name && <p id="name-error" className="field-error">{errorText('name', errors.name)}</p>}</div>
        <div className="form-field"><label htmlFor="email">{labels.email} <span aria-hidden="true">*</span></label><input id="email" name="email" type="email" autoComplete="off" dir="ltr" value={fields.email} maxLength={FIELD_LIMITS.email} onChange={event => updateField('email', event.target.value)} onBlur={() => blurField('email')} aria-invalid={Boolean(errors.email)} aria-describedby={`email-hint${errors.email ? ' email-error' : ''}`} required /><p id="email-hint" className="field-hint">{t('استخدم عنوانًا مثل', 'Use an address such as')} <bdi>demo@example.com</bdi>{t('. لن نرسل أي رسائل.', '. No messages will be sent.')}</p>{errors.email && <p id="email-error" className="field-error">{errorText('email', errors.email)}</p>}</div>
        <div className="form-field"><label htmlFor="description">{labels.description} <span aria-hidden="true">*</span></label><textarea id="description" name="description" rows={4} value={fields.description} maxLength={FIELD_LIMITS.description} onChange={event => updateField('description', event.target.value)} onBlur={() => blurField('description')} aria-invalid={Boolean(errors.description)} aria-describedby={`description-hint${errors.description ? ' description-error' : ''}`} required /><div className="field-hint-row"><p id="description-hint" className="field-hint">{t('اكتب فكرة تجريبية من 10 إلى 500 حرف.', 'Write a demo description of 10–500 characters.')}</p><span><bdi>{number(fields.description.length)} / {number(FIELD_LIMITS.description)}</bdi></span></div>{errors.description && <p id="description-error" className="field-error">{errorText('description', errors.description)}</p>}</div>
        <div className="form-actions"><a className="button secondary" href={`#/services/${service.id}`}><FlowArrow back />{t('تفاصيل الخدمة', 'Service details')}</a><button className="button primary" type="submit">{t('مراجعة الطلب', 'Review request')}<FlowArrow /></button></div>
      </form>}
      {step === 2 && <div><div className="form-heading"><h2 ref={stepHeading} tabIndex={-1}>{t('كل شيء واضح؟', 'Does everything look right?')}</h2><p>{t('راجع بياناتك التجريبية قبل التأكيد. يمكنك الرجوع لتعديل أي حقل.', 'Review your demo details before confirming. You can return to edit any field.')}</p></div><dl className="review-details">{FORM_FIELDS.map(field => <div key={field}><dt>{labels[field]}</dt><dd><bdi>{fields[field].trim()}</bdi></dd></div>)}</dl><DemoNote>{t('سيُنشأ رقم مرجعي تجريبي في هذه الجلسة. لن يُرسل طلب رسمي أو بريد إلكتروني، وستُفقد البيانات عند تحديث الصفحة.', 'A demo reference will be created for this session. No official request or email will be sent. Data is lost when the page reloads.')}</DemoNote><div className="form-actions"><button className="button secondary" disabled={pending} onClick={() => { setStep(1); setTimeout(() => stepHeading.current?.focus(), 0); }}><Pencil size={18} aria-hidden="true" />{t('تعديل البيانات', 'Edit details')}</button><button className="button primary" onClick={confirm} disabled={pending}>{pending ? <LoaderCircle className="spinner" size={19} aria-hidden="true" /> : <Check size={19} aria-hidden="true" />}{pending ? t('جارٍ إنشاء الطلب التجريبي...', 'Creating demo request…') : t('تأكيد الطلب التجريبي', 'Confirm demo request')}</button></div>{pending && <p className="sr-only" role="status">{t('جارٍ إنشاء الطلب التجريبي', 'Creating demo request')}</p>}</div>}
      {step === 3 && request && <div className="confirmation"><span className="success-icon"><CircleCheck size={42} strokeWidth={1.5} aria-hidden="true" /></span><span className="eyebrow">{t('اكتملت التجربة', 'DEMO COMPLETE')}</span><h2 ref={stepHeading} tabIndex={-1}>{t('تم إنشاء طلبك التجريبي', 'Your demo request is ready')}</h2><p>{t('خطوة جميلة نحو تجربة أوضح. يمكنك الآن متابعة الطلب باستخدام الرقم المرجعي أدناه.', 'One step closer to a clearer experience. You can now track this request using the reference below.')}</p><div className="reference-box"><span>{t('رقم الطلب التجريبي', 'Demo request reference')}</span><strong><bdi>{request.reference}</bdi></strong></div><p className="confirmation-note"><Info size={18} aria-hidden="true" />{t('هذا ليس إيصالًا رسميًا. يعمل الرقم خلال هذه الجلسة فقط.', 'This is not an official receipt. The reference works in this session only.')}</p><div className="confirmation-actions"><a className="button primary" href={`#/track?ref=${request.reference}`}>{t('متابعة الطلب التجريبي', 'Track demo request')}<FlowArrow /></a><a className="button secondary" href="#/services">{t('استكشاف خدمات أخرى', 'Explore more services')}</a></div></div>}
    </div><p className="application-footnote"><Info size={16} aria-hidden="true" />{t('بياناتك التجريبية لا تغادر هذه الصفحة.', 'Your demo details never leave this page.')}</p></div>
  </div>;
}



