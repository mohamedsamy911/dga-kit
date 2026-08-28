#!/usr/bin/env python3
"""Every DGA quote in the skills must still say what DGA said.

WHY THIS EXISTS
---------------
This kit's failure mode is not DGA changing. It is *us* drifting from DGA. Three times:

  * `letter-spacing: -2%` shipped as invalid CSS
  * the template count asserted as 19 when the harvest held 17
  * a launch-gate quote that dropped DGA's word "typically", turning "typically cannot proceed
    to deployment" into an unconditional deployment block

No amount of monitoring design.dga.gov.sa catches any of those. They are caught by comparing
what a reference file *claims DGA said* against what was *actually captured*. That is this file.

HOW IT WORKS
------------
Corpus  : the passages of every `harvest/raw/*.md` capture that are explicitly fenced as DGA
          text, kept as SEPARATE blocks with their source page.

              <!-- dga -->
              > ...DGA's own words...
              <!-- /dga -->

          A capture also carries this repo's commentary - method notes, corrections, why a
          finding matters. That prose is deliberately OUTSIDE the fences, so it can never be
          what a quote is 'verified' against. Unfenced is ours by default, which is the safe
          direction, and a blockquote left outside a fence is reported as an error rather than
          silently ignored.
Targets : every blockquote paragraph in `skills/**/*.md`.

Most blockquotes in this kit are the kit's OWN commentary (the "⚠️" / "\U0001f6a9" notes), not DGA text,
so the check first has to work out which is which. It does that by similarity, not by a marker:

  similarity = (longest run shared with the corpus) / (length of the quote)

  >= QUOTE_THRESHOLD  -> this paragraph is reproducing captured text. Verify it exactly.
  <  QUOTE_THRESHOLD  -> kit commentary that happens to share a phrase. Skip.

A paragraph that is *clearly derived from* a capture but not identical to it is precisely the
"you paraphrased a quote" signal, and it is the only thing this file fails on.

SCOPE - state it plainly rather than implying more:
  * It can only check quotes whose source page has a raw capture. Most of the 2026-08-26 harvest
    has none, so those quotes are UNVERIFIABLE and the report counts them.
  * TWO figures are reported, and they answer different questions.
      - BLOCKQUOTE coverage: denominator is every blockquote in skills/, most of which are the
        kit's own commentary. Reading it as "the kit is 8% evidenced" understates the truth.
      - DGA-MARKED coverage: denominator is the blockquotes fenced as DGA's own words. That is a
        claim of authorship, so a marked quote with no capture behind it is a real finding - and
        the one this file most wants to surface, and it FAILS --ci. A fenced quote with no
        capture behind it is an uncited DGA claim, which is the one thing this kit may never
        ship. Fix it by capturing the page, or by rewriting the passage as the kit's own words
        and dropping the fence - never by unmarking text that still reads as DGA's wording.
    The marks were bootstrapped from quotes already proven verbatim, so the second figure reads
    100% until someone marks a quote on judgement. Marking DGA quotes in skills/ - the same fence
    the captures use - would make a real evidence-coverage figure possible. TODO.
  * It cannot tell a correct quote from a correctly-transcribed quote of a page that has since
    changed. That is the sentinel's job, not this one's.
  * Every fragment of an elided quote must come from the SAME captured passage. A quote whose
    fragments are all captured but never together is reported as STITCHED - it presents as one
    statement something DGA says in two different places, and it fails.

  python3 evals/check-quote-fidelity.py           # report
  python3 evals/check-quote-fidelity.py --ci      # exit 1 on drift
  python3 evals/check-quote-fidelity.py --verbose # list verified + unverifiable quotes too
"""
import difflib
import glob
import io
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# DGA is a bilingual source, so quotes carry Arabic. A Windows console defaults to cp1252 and
# raises UnicodeEncodeError on the first Arabic character - which killed --verbose. Ask for
# UTF-8, and fall back to replacing what the terminal genuinely cannot draw.
if hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    except (ValueError, OSError):
        pass

# A paragraph sharing this fraction of itself with a capture is reproducing it, not alluding
# to it. Tuned against the current corpus: real DGA quotes land at 0.90+, kit commentary that
# happens to share a phrase lands below 0.45. See --verbose for the spread.
QUOTE_THRESHOLD = 0.60
MIN_LEN = 40        # shorter paragraphs carry too little signal to classify
MIN_FRAGMENT = 25   # an elided fragment shorter than this proves nothing

ELISION = re.compile(r'\[…\]|\[\.\.\.\]|…')


def norm(s):
    """Strip presentation so only DGA's words remain.

    Both sides get this: a capture stores DGA text as a markdown blockquote with our own bolding,
    and a reference file re-bolds different words. Neither is drift.
    """
    s = s.replace('—', '-').replace('–', '-')
    s = s.replace('’', "'").replace('‘', "'")
    s = s.replace('“', '"').replace('”', '"')
    s = re.sub(r'\[([^\]]*)\]\([^)]*\)', r'\1', s)                      # md links
    s = s.replace('**', '').replace('`', '')
    s = re.sub(r'(?<![A-Za-z0-9])\*([^*]+)\*(?![A-Za-z0-9])', r'\1', s)  # italics
    return re.sub(r'\s+', ' ', s).strip()


FENCE_OPEN, FENCE_CLOSE = '<!-- dga -->', '<!-- /dga -->'
# Sentinel source label for a fence problem, so malformed markers travel the same channel as
# passages instead of being dropped.
MALFORMED = object()


def dga_blocks(text, origin):
    """Yield (source_label, passage) for each fenced DGA passage, plus any stray blockquote.

    Blocks stay SEPARATE. Concatenating them would let a quote be assembled out of two things
    DGA said on different pages, which is exactly the misrepresentation this check should catch.

    A blockquote outside a fence is yielded with source None - the caller reports it as an
    error. Silently skipping it would let DGA text drift out of the corpus unnoticed, and
    silently including it would put our own commentary back in.
    """
    heading, inside, buf, start_h, open_at = '', False, [], '', 0
    for n, line in enumerate(text.split('\n'), 1):
        st = line.strip()
        if st.startswith('#'):
            heading = st.lstrip('#').strip()
            continue
        if st == FENCE_OPEN:
            # A second open before a close means the first passage would be dropped on the
            # floor. Report it rather than silently losing captured DGA text.
            if inside:
                yield MALFORMED, f'{origin}:{open_at} opened a fence that line {n} reopens'
            inside, buf, start_h, open_at = True, [], heading, n
            continue
        if st == FENCE_CLOSE:
            if not inside:
                yield MALFORMED, f'{origin}:{n} closes a fence that was never opened'
                continue
            if buf:
                yield f'{origin} > {start_h}' if start_h else origin, ' '.join(buf)
            inside, buf = False, []
            continue
        if st.startswith('>'):
            buf.append(st.lstrip('>').strip())
        elif buf:
            if inside:
                continue          # blank line inside a fence separates paragraphs of one passage
            yield None, ' '.join(buf)
            buf = []
    if inside:
        # An unclosed fence swallows its passage: it is never yielded, so nothing can be
        # verified against it and coverage silently drops. That must fail, not pass quietly.
        yield MALFORMED, f'{origin}:{open_at} fence is never closed'
    elif buf:
        yield None, ' '.join(buf)


def load_corpus():
    """-> (files, blocks, strays, malformed); blocks is [(source_label, normalised_text)]."""
    files = sorted(glob.glob(os.path.join(ROOT, 'harvest', 'raw', '*.md')))
    blocks, strays, malformed = [], [], []
    for f in files:
        origin = os.path.basename(f)
        for src, body in dga_blocks(io.open(f, encoding='utf-8').read(), origin):
            if src is MALFORMED:
                malformed.append(body)
                continue
            if not body.strip():
                continue
            (blocks if src else strays).append((src or origin, norm(body)))
    return files, blocks, strays, malformed


def marked_lines(path):
    """Line numbers inside <!-- dga --> ... <!-- /dga --> fences in a SKILL file.

    The captures use these fences to say "these are DGA's words". Until now skills/ did not, so
    the coverage figure had to use every blockquote as its denominator - and most blockquotes in
    skills/ are the kit's own commentary. That made 8% look like "8% of the kit is evidenced",
    which understates the truth by an amount nothing could measure. A marked quote is a CLAIM of
    DGA authorship, and it is checkable.
    """
    inside, out = False, set()
    for i, line in enumerate(io.open(path, encoding='utf-8').read().split('\n'), 1):
        st = line.strip()
        if st == FENCE_OPEN:
            inside = True
            continue
        if st == FENCE_CLOSE:
            inside = False
            continue
        if inside:
            out.add(i)
    return out


def blockquotes(path):
    """(line, paragraph) for each run of consecutive `>` lines."""
    buf, start = [], None
    for i, line in enumerate(io.open(path, encoding='utf-8').read().split('\n'), 1):
        if line.startswith('>'):
            if start is None:
                start = i
            buf.append(line.lstrip('>').strip())
        elif buf:
            yield start, norm(' '.join(buf))
            buf, start = [], None
    if buf:
        yield start, norm(' '.join(buf))


def longest_run(a, b):
    m = difflib.SequenceMatcher(None, a, b, autojunk=False)
    return max((bl.size for bl in m.get_matching_blocks()), default=0)


def main():
    files, blocks, strays, malformed = load_corpus()
    if not blocks:
        print('No fenced DGA passages in harvest/raw/ - nothing to check against.')
        print('Wrap captured DGA text in <!-- dga --> ... <!-- /dga --> so it can be cited.')
        return 1 if '--ci' in sys.argv else 0

    verified, drift, stitched, unverifiable, marked = [], [], [], [], []
    elided = []
    for d, _, fs in os.walk(os.path.join(ROOT, 'skills')):
        for fn in sorted(fs):
            if not fn.endswith('.md'):
                continue
            p = os.path.join(d, fn)
            rel = os.path.relpath(p, ROOT).replace('\\', '/')
            _marked = marked_lines(p)
            for line, q in blockquotes(p):
                if len(q) < MIN_LEN:
                    continue
                if line in _marked:
                    marked.append((rel, line))
                frags = [f.strip() for f in ELISION.split(q) if len(f.strip()) >= MIN_FRAGMENT]
                # Every fragment must come from ONE captured block. Checking against the whole
                # corpus would accept a quote stitched together from two unrelated DGA passages.
                # An ELIDED quote (one containing an ellipsis) is not verbatim, even when every
                # fragment sits in the same captured passage. The old rule accepted exactly that:
                #   "To integrate Platforms Code UI React into your project… npm install …"
                # spliced the opening of one sentence onto a command from further down the page,
                # and would have reported VERIFIED VERBATIM. It escaped only because the quote
                # wrapped the command in backticks the capture lacks. Elision is legitimate
                # quoting; claiming it is verbatim is not. Fragments must also appear IN ORDER,
                # or the ellipsis is concealing a reordering of what DGA wrote.
                def _in_order(body, parts):
                    at = -1
                    for part in parts:
                        nxt = body.find(part, at + 1)
                        if nxt <= at:
                            return False
                        at = nxt + len(part) - 1
                    return True

                hit = next((src for src, body in blocks
                            if frags and all(f in body for f in frags)
                            and _in_order(body, frags)), None)
                if hit:
                    (elided if len(frags) > 1 else verified).append((rel, line, q, hit))
                    continue
                _scrambled = next((src for src, body in blocks
                                   if frags and all(f in body for f in frags)), None)
                if _scrambled:
                    stitched.append((rel, line, q, [_scrambled]))
                    continue
                # Every fragment is captured, but no ONE passage holds them all: the quote joins
                # things DGA said in different places into a single blockquote. Report it as its
                # own failure - letting it fall through to UNVERIFIABLE would read as "we never
                # captured this", when in fact we captured both halves and the quote invented the
                # join.
                if len(frags) > 1:
                    where = {}
                    for f in frags:
                        where[f] = [src for src, body in blocks if f in body]
                    if all(where[f] for f in frags):
                        stitched.append((rel, line, q, sorted({s2 for v in where.values()
                                                               for s2 in v})))
                        continue
                best_src, best = None, 0.0
                for src, body in blocks:
                    r = longest_run(q, body) / len(q)
                    if r > best:
                        best_src, best = src, r
                (drift if best >= QUOTE_THRESHOLD else unverifiable).append((rel, line, q, best, best_src))

    out = sys.stdout
    chars = sum(len(b) for _, b in blocks)
    out.write('Quote fidelity - do the skills still say what DGA said?\n')
    out.write(f'corpus: {len(blocks)} fenced DGA passage(s) across {len(files)} capture(s), '
              f'{chars:,} chars\n\n')

    if malformed:
        out.write(f'MALFORMED FENCES in captures ({len(malformed)}) - captured DGA text is being\n')
        out.write('lost. Every <!-- dga --> needs a matching <!-- /dga -->.\n')
        for m in malformed:
            out.write(f'  {m}\n')
        out.write('\n')

    if strays:
        out.write(f'Outside the fences: {len(strays)} blockquote(s) in captures are treated as '
                  f'this repo\'s commentary,\nnot as DGA text, and nothing can be verified '
                  f'against them. That is the intended state.\nIf one of them is actually DGA\'s '
                  f'wording, wrap it in <!-- dga --> ... <!-- /dga -->.\n')
        out.write('Run --verbose to list them.\n\n')

    if drift:
        out.write(f'DRIFT - reproduces a capture but does not match it ({len(drift)})\n')
        for rel, line, q, sim, src in sorted(drift, key=lambda x: -x[3]):
            out.write(f'  {rel}:{line}  similarity {sim:.2f}  vs {src}\n')
            out.write(f'    quote: {q[:160]}\n')
            body = next((b for s2, b in blocks if s2 == src), '')
            if body:
                m = difflib.SequenceMatcher(None, q, body, autojunk=False)
                bl = max(m.get_matching_blocks(), key=lambda x: x.size)
                lo = max(0, bl.b - 30)
                out.write(f'    source: ...{body[lo:bl.b + bl.size + 60]}...\n')
    else:
        out.write('DRIFT (0) - none\n')

    if stitched:
        out.write(f'\nSTITCHED - one blockquote joining separate DGA passages ({len(stitched)})\n')
        out.write('  Every fragment is captured, but no single passage contains them all, so the\n')
        out.write('  quote presents as one statement something DGA says in different places.\n')
        for rel, line, q, srcs in stitched:
            out.write(f'  {rel}:{line}\n    quote:   {q[:150]}\n')
            for src in srcs:
                out.write(f'    drawn from: {src}\n')

    # Coverage asks whether every blockquote has source evidence. An ellided quote has evidence
    # but is intentionally not counted as verbatim, so include it here while reporting it
    # separately above.
    checked = len(verified) + len(elided) + len(drift) + len(stitched)
    total = checked + len(unverifiable)
    out.write(f'\nVERIFIED verbatim against a capture: {len(verified)}\n')
    if elided:
        out.write(f"VERIFIED but ELIDED - DGA's fragments, in order, joined by an "
                  f'ellipsis: {len(elided)}\n')
        out.write('  Legitimate quoting, but NOT verbatim: DGA did not write these as one\n'
                  '  sentence. Check each reads fairly rather than implying a claim DGA\n'
                  '  made only in pieces.\n')
        for _er, _el, _eq, _esrc in elided:
            out.write(f'    {_er}:{_el}  <- {_esrc}\n')
    out.write(f'UNVERIFIABLE - no capture covers the source page: {len(unverifiable)}\n')
    if total:
        out.write(f'\nBlockquote coverage: {checked}/{total} blockquote paragraphs in skills/ '
                  f'({100 * checked // total}%) could be\nmatched to a captured DGA passage.\n')
        out.write('\n\u26a0 This is NOT "how much of the kit is evidence-backed". The denominator is\n'
                  'every blockquote, and most of them are the kit\'s own commentary rather than DGA\n'
                  'quotes - so the true share of DGA quotes that are evidenced is higher than this,\n'
                  'by an amount nothing here measures. A real evidence-coverage figure needs DGA\n'
                  'quotes marked in skills/ the way they are marked in captures.\n')

    # The honest figure: of the blockquotes that CLAIM to be DGA's words, how many are backed by
    # a capture. Denominator is a claim of authorship, not a count of paragraphs.
    _mk = {(r, l) for r, l in marked}
    _backed = {(r, l) for r, l, _q, _h in verified} | {(r, l) for r, l, _q, _h in elided}
    _mk_ok = len(_mk & _backed)
    out.write(f'\nDGA-marked quotes: {len(_mk)} blockquote(s) in skills/ are fenced as DGA\'s '
              f'own words.\n')
    if _mk:
        _mk_verb = len(_mk & {(r, l) for r, l, _q, _h in verified})
        _mk_elid = _mk_ok - _mk_verb
        out.write(f'  {_mk_ok}/{len(_mk)} ({_mk_ok * 100 // len(_mk)}%) are backed by a capture'
                  + (f' ({_mk_verb} verbatim, {_mk_elid} elided).\n' if _mk_elid
                     else ', all verbatim.\n'))
        if _mk_ok == len(_mk):
            out.write('  ⚠ That 100% is TAUTOLOGICAL while the marked set is exactly the proven\n'
                      '  set. The fences were bootstrapped from quotes this checker had already\n'
                      '  matched, so nothing marked COULD be unbacked. The number starts meaning\n'
                      '  something the moment a maintainer marks a quote on their own judgement:\n'
                      '  if no capture backs it, it is listed here as an unsubstantiated claim of\n'
                      '  DGA authorship. Mark quotes as you write them; do not wait for a capture.\n')
        _unbacked = sorted(_mk - _backed)
        if _unbacked:
            out.write(f'  {len(_unbacked)} marked quote(s) have NO capture behind them - a claim '
                      f'of DGA authorship\n  this repo cannot substantiate. That is the violation '
                      f'this whole kit exists to\n  prevent, so it FAILS --ci. Two honest '
                      f'remedies, and one that is not:\n'
                      f'    1. capture the page, so the quote is backed;\n'
                      f'    2. rewrite the passage as the KIT\'s words, not DGA\'s, and drop the '
                      f'fence.\n'
                      f'  Removing the fence while leaving the text presented as DGA\'s wording is '
                      f'NOT a fix -\n  it hides the same claim from the only check that looks for '
                      f'it.\n')
            for r, l in _unbacked[:15]:
                out.write(f'    {r}:{l}\n')
    else:
        out.write('  Nothing is fenced yet. Wrap a DGA quote in <!-- dga --> ... <!-- /dga --> to\n'
                  '  put it in this denominator.\n')
    out.write('Raising the numerator means capturing more raw pages, never editing a reference.\n')

    if '--verbose' in sys.argv:
        out.write('\n--- VERIFIED ---\n')
        for rel, line, q, src in verified:
            out.write(f'  {rel}:{line}  <- {src}\n      {q[:100]}\n')
        if strays:
            out.write('\n--- OUTSIDE THE FENCES (treated as repo commentary) ---\n')
            for src, body in strays:
                out.write(f'  {src}: {body[:90]}\n')
        out.write('\n--- UNVERIFIABLE (highest similarity first - check the top of this list\n')
        out.write('    if you are tuning QUOTE_THRESHOLD) ---\n')
        for rel, line, q, sim, src in sorted(unverifiable, key=lambda x: -x[3])[:20]:
            out.write(f'  {sim:.2f}  {rel}:{line}  {q[:90]}\n')

    # Only drift fails. An unfenced blockquote is commentary by design; a genuinely mis-filed
    # DGA passage shows up as falling coverage, which is visible rather than silent.
    # `unbacked` joins the fatal set on review. The earlier reasoning for excluding it was that
    # the fix is a capture run rather than an edit, so failing the build would pressure someone
    # into deleting the mark instead of capturing the page. That is a real risk, but it does not
    # survive the kit's own rule: a blockquote fenced as DGA's own words with nothing behind it IS
    # an uncited DGA claim, which is exactly what cite-or-omit forbids. The pressure argument also
    # cuts both ways - unmarking hides the claim rather than removing it, so tolerating it bought
    # nothing. The message above names the two honest remedies instead.
    _unbacked_fatal = [(r, l) for r, l in marked
                       if (r, l) not in {(r2, l2) for r2, l2, _q, _h in verified}]
    if '--ci' in sys.argv and (drift or stitched or malformed or _unbacked_fatal):
        return 1
    return 0


if __name__ == '__main__':
    sys.exit(main())
