# Mobile

**Source:** /designing-for-mobile · **Retrieved:** 2026-08-26

DGA ships a **separate Mobile UI Kit** with components that do not exist in the web set. A
mobile screen built only from the web component list is missing DGA's own mobile vocabulary.

## Mobile-only components

| Component | Web equivalent |
|---|---|
| **Mobile Navigation Bar** | — |
| **Tap Bar** | — (bottom tab bar) |
| **Top Bar** | closest is Navigation Header, but distinct |
| **Splash Screen** | — |
| **Mobile Modal** | Modal, but a distinct mobile treatment |
| **Date Picker (mobile)** | Datepicker, distinct mobile variant |

`TODO(harvest)` — these have no public guideline pages; specs live in the **PC 1.0 Components –
Mobile UI Kit** Figma file. Get it before designing mobile screens.

## Responsive rules DGA states elsewhere

Gathered from the templates and components, since there is no consolidated mobile guideline:

| Context | Mobile behaviour |
|---|---|
| **Form steps** | **Radial Stepper** on mobile; Progress Indicator on large screens |
| **Breadcrumbs** | Back arrow + previous page link only |
| **Footer** | Stacks vertically below 600px |
| **Filtering** | Dropdown menu, not inline filters |
| **FAQ categories** | Max 5, then a dropdown |
| **Long titles** | Button below the content, stacked vertically — applied consistently |
| **Feedback section** | Buttons below the text |
| **Year of AI logo** | Stacked vertically (horizontal on desktop) |
| **Floating buttons** | Must not cover content; two stack vertically; 3+ go in an expandable menu |
| **Container padding** | 16px (32px desktop) |

## Responsive tokens

DGA's **radius and spacing semantic tokens resolve differently per breakpoint** (Desktop /
Tablet / Mobile). Those values are not exposed as CSS variables — only in the PC 1.0 Foundations
Figma variable collections. A React implementation treating them as constants is wrong on two of
three breakpoints. `TODO(harvest)`
