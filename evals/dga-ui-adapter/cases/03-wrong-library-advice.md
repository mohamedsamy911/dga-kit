## input
"We're building the government portal in **Vue 3 with PrimeVue**. How do we make the tab bar
DGA-compliant?"

## expect
- answers for the library actually in use, or states plainly that PrimeVue is not one of the four
  named in `component-mapping.md` and gives the **DGA rule** so it can be mapped onto whatever
  PrimeVue calls the component
- the DGA rule: a horizontal tablist **never scrolls and never wraps** — overflow goes to a
  "More" button. Most libraries default to scrolling
- also: six states including Focused, 44px targets, RTL mirroring
- FAIL (library confusion) if it answers with `Tabs` props from MUI, Chakra or Ant as though they
  were PrimeVue's, or invents a PrimeVue API

## traps
The skill names four libraries. A fifth must degrade to "here is the DGA rule, map it yourself",
not to confident invention of an API. Getting the *rule* right while admitting the API is unknown
is a full pass.
