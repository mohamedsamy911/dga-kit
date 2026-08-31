import { createContext, useContext, type ReactNode } from 'react';

export type Locale = 'ar' | 'en';
export type Localized = { ar: string; en: string };

const LocaleContext = createContext<Locale>('ar');

export function LocaleProvider({ locale, children }: { locale: Locale; children: ReactNode }) {
  return <LocaleContext.Provider value={locale}>{children}</LocaleContext.Provider>;
}

export function useI18n() {
  const locale = useContext(LocaleContext);
  return {
    locale,
    t: (ar: string, en: string) => locale === 'ar' ? ar : en,
    local: (value: Localized) => value[locale],
    number: (value: number) => new Intl.NumberFormat(locale === 'ar' ? 'ar-SA-u-nu-latn' : 'en-GB').format(value),
    date: (value: string) => new Intl.DateTimeFormat(locale === 'ar' ? 'ar-SA-u-ca-gregory-nu-latn' : 'en-GB', {
      dateStyle: 'long', timeZone: 'Asia/Riyadh',
    }).format(new Date(value)),
  };
}
