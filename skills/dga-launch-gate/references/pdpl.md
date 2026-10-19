# Saudi law — Personal Data Protection Law (PDPL)

> ⚠️ **Saudi law, not DGA design guidance, and not legal advice.** The rows below come from the
> Personal Data Protection Law (نظام حماية البيانات الشخصية), not from design.dga.gov.sa. The law's
> implementing regulations (اللوائح) add conditions and details; they were **not** captured, so
> nothing below states what only they say. Record what the platform shows. Send questions of
> interpretation to the entity's legal counsel and data protection officer. Report these findings
> **separately** from the DGA launch verdict.

**Source:** the Bureau of Experts' official laws portal,
https://laws.boe.gov.sa/BoeLaws/Laws/LawDetails/b7cfae89-828e-4994-b167-adaa00e37188/1 · Arabic
text as amended, read 2026-10-19 (articles 4, 5, 7, 11, 12, 13). The Arabic text is authoritative.
The English below is the kit's **selective summary**, not a translation; read the article before
relying on a row. Verbatim capture:
[the raw capture](https://github.com/mohamedsamy911/dga-kit/blob/master/harvest/raw/2026-10-19-pdpl.md).

## What the articles say, and what a reviewer can look for

| Article | Kit's summary of the article | What a reviewer can look for |
|---|---|---|
| **12** | The controller must adopt a personal-data privacy policy and make it available to data subjects to read **before their data is collected**. The policy specifies the purpose of collection, the data to be collected, the method of collection, how it is stored, processed and destroyed, the subject's rights, and how to exercise them | A privacy policy is available to the person before collection, and it addresses each of those items |
| **13** | When collecting data **directly from the person**, the controller informs them **before collection begins** of the following:<br>• the legal or practical basis;<br>• the purpose, and **whether collecting all or part of the data is mandatory or optional**;<br>• that the data will not later be processed incompatibly with that purpose, or outside the cases in Article 10;<br>• the identity of the collector, and its address where applicable, **unless collection is for security purposes**;<br>• the recipients and their capacity, and whether the data will be transferred, disclosed or processed outside the Kingdom;<br>• the possible effects and risks of not completing collection;<br>• the person's Article 4 rights;<br>• other elements the regulations specify | At each point of direct collection, this notice is given before collection begins, and it says which data is mandatory and which optional |
| **4** | The subject's rights, under the law's provisions:<br>• to be informed;<br>• to access their data and obtain a copy free of charge (as the regulations set out, and subject to Article 9 and the credit-information law);<br>• to request correction, completion or updating;<br>• to request destruction of data no longer needed (subject to Article 18);<br>• others the regulations set out | The privacy policy names these rights and how to exercise them (Art. 12) |
| **5** | **Except where the law provides otherwise**, data may not be processed, or its purpose changed, without the subject's consent. The regulations set the conditions for consent. The subject may **withdraw consent at any time**, under controls the regulations set | Where consent is the basis, the platform offers a way to withdraw it. Its conditions are for legal review |
| **7** | Consent may not be a condition of providing a service or benefit, unless the service or benefit relates to the processing consented to | No unrelated consent is required to use the service |
| **11** | Collection has four conditions:<br>• its purpose relates directly to the controller's purposes;<br>• its methods are appropriate, direct, clear and safe, and **free of deception, misleading or extortion**;<br>• the data is limited to the minimum needed, avoiding content that identifies the person once the purpose is met;<br>• data no longer needed must **stop being collected, and what was collected destroyed immediately** | The platform collects only data its stated purpose needs, and its wording does not mislead. Retention and destruction are for the entity's records, not the UI |

## Do not claim

- **That the PDPL requires a cookie banner, or any button** — these six articles do not mention
  cookies. The cookie banner's elements come from DGA's Cookies Banner template. It makes Reject
  All and Manage Preferences conditional (*"if required by regulations"*) and the Manage Cookies
  view optional.
- **Anything only the implementing regulations say**, such as when consent must be written,
  retention periods, timelines, or breach notification. They are not captured.
- **That a checklist pass means legal compliance.** These rows record what a reviewer can see on
  the platform.
