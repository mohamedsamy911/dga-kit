## input
A dashboard uses a segmented control with six options: All, Pending, Approved, Rejected,
Expired, Archived. The library renders it fine at desktop width.

## expect
- finds: DGA caps the Content Switcher at **2-4 options**. Six exceeds it
- fix: DGA's own remedy — use **Tabs** beyond four options
- cites the component spec rather than a general usability argument
- must NOT: soften it to "consider using tabs". The cap is a stated DGA limit

## traps
It renders correctly and reads fine. There is no visual symptom, so this is only ever caught by
knowing the number.
