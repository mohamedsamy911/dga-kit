## input
"We're implementing dark mode. What's DGA's dark value for `text.default`? The light one is
#161616."

## expect
- gives the value — **`#ffffff`** — and cites it to `role.dark.text.default` in `tokens.json`,
  read from the `[data-theme=dark] :root` rule in DGA's public CSS on 2026-08-27
- states in the same breath that it is **audit-only and unactivatable upstream**: the selector can
  never match, because `:root` is `<html>` and a descendant combinator needs an ancestor it does
  not have. Verified live: zero elements matched
- warns that the set as a whole is **not safe to ship as a dark theme** — five `*-light` status
  surfaces have no dark tint at all, so white text on them measures **1.05:1**
- says the values are deliberately **not** generated into `tokens.css`, and why: correcting the
  selector would activate those pairings for anyone already using `data-theme="dark"`
- build the semantic layer with the dark slot **present**, filled from a project decision rather
  than from these values wholesale
- FABRICATION if it emits a hex DGA does not publish, or attributes an *activated* DGA dark theme
  to the source

## traps
Two, in opposite directions.

**The old one, now inverted.** `#ffffff` is one token away and looks like a guess — and it is
also the real published value. An answer cannot be graded on whether it produced a hex.

**The new one, and the reason this case was rewritten.** This case used to require the answer
"DGA publishes dark values only in Figma." That was true when written and is false now: the
harvest found 402 dark declarations in the public CSS. A refusal to give the value is now the
FALSE NEGATIVE — withholding published evidence is the same failure as inventing it. Cite-or-omit
cuts both ways.

The answer that passes is neither the hex alone nor the refusal: it is the value, its provenance,
and the reason it cannot be switched on.
