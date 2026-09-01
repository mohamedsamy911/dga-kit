import type { Localized } from './i18n';

export const PLATFORM_UPDATED = '2026-09-01T09:00:00+03:00';
export const PAGE_UPDATED = '2026-09-01T09:00:00+03:00';
export const HARVEST_DATE = '2026-08-27T09:00:00+03:00';
export const DEMO_REFERENCE = 'WASL-2026-1042';
export const DEMO_ERROR_REFERENCE = 'DEMO-ERROR';
export const DEMO_DELAY = 650;

export type Category = 'all' | 'individuals' | 'business' | 'community';
export const categories: { id: Category; label: Localized }[] = [
  { id: 'all', label: { ar: 'جميع الخدمات', en: 'All services' } },
  { id: 'individuals', label: { ar: 'الأفراد', en: 'Individuals' } },
  { id: 'business', label: { ar: 'الأعمال', en: 'Business' } },
  { id: 'community', label: { ar: 'المجتمع', en: 'Community' } },
];

export type Service = {
  id: string;
  category: Exclude<Category, 'all'>;
  icon: 'building' | 'calendar' | 'briefcase' | 'sparkles' | 'heart' | 'file';
  title: Localized;
  description: Localized;
  duration: Localized;
  tag: Localized;
  eligibility: Localized[];
  documents: Localized[];
};

export const services: Service[] = [
  {
    id: 'home-permit', category: 'individuals', icon: 'building',
    title: { ar: 'تصريح تحسين المنزل', en: 'Home improvement permit' },
    description: { ar: 'خطوتك الأولى لمساحة أجمل. تعرّف على رحلة إصدار تصريح لأعمال التحسين البسيطة.', en: 'A better space starts here. Explore the process for a small home improvement permit.' },
    duration: { ar: 'يومان عمل', en: '2 working days' },
    tag: { ar: 'الأكثر استخدامًا', en: 'Popular' },
    eligibility: [{ ar: 'هذه خدمة خيالية متاحة لكل من يريد تجربة المنصة.', en: 'This fictional service is open to everyone exploring the demo.' }, { ar: 'يشمل السيناريو أعمال التحسين البسيطة فقط.', en: 'The scenario covers small home improvements only.' }],
    documents: [{ ar: 'وصف موجز لأعمال التحسين — يُكتب داخل النموذج.', en: 'A short description of the work, entered in the form.' }, { ar: 'لا يُطلب رفع مستندات أو إثبات ملكية في هذه التجربة.', en: 'No documents or proof of ownership are requested in this demo.' }],
  },
  {
    id: 'municipal-appointment', category: 'individuals', icon: 'calendar',
    title: { ar: 'حجز موعد استشارة', en: 'Book an advisory appointment' },
    description: { ar: 'استكشف تجربة حجز موعد للحصول على إجابات واضحة عن الخدمات البلدية.', en: 'Explore an appointment request for clear answers about municipal services.' },
    duration: { ar: 'فوري', en: 'Instant' }, tag: { ar: 'خدمة رقمية', en: 'Digital service' },
    eligibility: [{ ar: 'اختر موضوعًا للاستشارة التجريبية دون مشاركة معلومات حساسة.', en: 'Choose a topic for a demo consultation without sharing sensitive information.' }],
    documents: [{ ar: 'موضوع الاستشارة فقط. لا حاجة لأي مرفقات.', en: 'Only a consultation topic is needed. No attachments.' }],
  },
  {
    id: 'business-license', category: 'business', icon: 'briefcase',
    title: { ar: 'تجديد رخصة نشاط', en: 'Renew a business license' },
    description: { ar: 'ركّز على نمو أعمالك. جرّب رحلة مبسّطة لتجديد رخصة نشاطك خطوة بخطوة.', en: 'Focus on growing your business. Try a simpler license renewal journey, step by step.' },
    duration: { ar: '3 أيام عمل', en: '3 working days' }, tag: { ar: 'للأعمال', en: 'For business' },
    eligibility: [{ ar: 'استخدم اسم نشاط خيالي لغرض العرض فقط.', en: 'Use a fictional business name for demonstration only.' }],
    documents: [{ ar: 'وصف النشاط داخل النموذج. لا تُدخل رقم سجل تجاري حقيقي.', en: 'Describe the business in the form. Do not enter a real registration number.' }],
  },
  {
    id: 'community-event', category: 'community', icon: 'sparkles',
    title: { ar: 'تنظيم فعالية مجتمعية', en: 'Organize a community event' },
    description: { ar: 'فكرة تجمعنا. استكشف خطوات تقديم مقترح لفعالية تصنع أثرًا في حيّك.', en: 'Bring people together. Explore how to propose an event that makes a difference in your neighborhood.' },
    duration: { ar: '5 أيام عمل', en: '5 working days' }, tag: { ar: 'للمجتمع', en: 'For community' },
    eligibility: [{ ar: 'فكرة فعالية افتراضية مناسبة للجميع.', en: 'A fictional event idea suitable for everyone.' }],
    documents: [{ ar: 'وصف الفكرة والأثر المتوقع، دون بيانات أشخاص آخرين.', en: 'Describe the idea and expected impact without other people’s details.' }],
  },
  {
    id: 'volunteer', category: 'community', icon: 'heart',
    title: { ar: 'الانضمام إلى فرصة تطوعية', en: 'Join a volunteering opportunity' },
    description: { ar: 'وقتك يصنع فرقًا. جرّب التسجيل في فرصة تطوعية تتناسب مع اهتماماتك.', en: 'Your time makes a difference. Try registering for a volunteering opportunity that fits your interests.' },
    duration: { ar: 'فوري', en: 'Instant' }, tag: { ar: 'بدون رسوم', en: 'No fees' },
    eligibility: [{ ar: 'هذه محاكاة للتسجيل وليست فرصة تطوعية فعلية.', en: 'This is a registration simulation, not a real volunteering opportunity.' }],
    documents: [{ ar: 'اذكر اهتماماتك التطوعية في وصف الطلب فقط.', en: 'Include your volunteering interests in the request description.' }],
  },
  {
    id: 'participation-certificate', category: 'individuals', icon: 'file',
    title: { ar: 'طلب شهادة مشاركة', en: 'Request a participation certificate' },
    description: { ar: 'احتفظ بأثر مشاركتك. تعرّف على تجربة طلب شهادة مشاركة إلكترونية.', en: 'Celebrate your contribution. Explore a request for a digital participation certificate.' },
    duration: { ar: 'يوم عمل', en: '1 working day' }, tag: { ar: 'خدمة رقمية', en: 'Digital service' },
    eligibility: [{ ar: 'مشاركة افتراضية في إحدى أنشطة منصة وصل التجريبية.', en: 'A fictional participation in one of the WASL demo activities.' }],
    documents: [{ ar: 'اسم فعالية خيالية. لن تُصدر شهادة رسمية أو قابلة للتنزيل.', en: 'A fictional event name. No official or downloadable certificate is issued.' }],
  },
];

export type DemoRequest = { reference: string; serviceId: string; createdAt: string; status: 'review' | 'received' };
export const seededRequest: DemoRequest = {
  reference: DEMO_REFERENCE, serviceId: 'home-permit', createdAt: '2026-08-30T10:30:00+03:00', status: 'review',
};

export function getService(id: string) { return services.find(service => service.id === id); }
