# -*- coding: utf-8 -*-
"""DNF BM 분석서 markdown -> 인쇄용 HTML. 본문 맑은고딕 / 코드 굴림체(고정폭)."""
import io, os, sys, markdown
sys.stdout.reconfigure(encoding="utf-8")
NL = chr(10)

SRC = r"C:\Users\MBC-501-08\Desktop\GameDesignStudy\SystemAnalysis\DNF_TropicalPackage_BM.md"
OUT = r"C:\Users\MBC-501-08\Desktop\GameDesignStudy\SystemAnalysis\DNF_TropicalPackage_BM.html"
raw = io.open(SRC, encoding="utf-8").read()
base = os.path.dirname(SRC).replace("\\", "/")
raw = raw.replace('src="./images/', 'src="file:///' + base + '/images/')

# 인용 블록 안의 줄바꿈을 살린다. 원문 행 구조가 뜻을 담고 있다.
lines = raw.split(NL)
brk = 0
for k in range(len(lines) - 1):
    a, b = lines[k], lines[k + 1]
    if (a.lstrip().startswith(">") and b.lstrip().startswith(">")
            and a.rstrip() != ">" and not a.endswith("  ")):
        lines[k] = a.rstrip() + "  "
        brk += 1
raw = NL.join(lines)
print("인용 강제 개행 {}곳".format(brk))

md = markdown.Markdown(
    extensions=["tables", "fenced_code", "toc", "sane_lists", "attr_list"],
    extension_configs={"toc": {"toc_depth": "2-3"}},
)
body = md.convert(raw)
toc = md.toc.strip().replace('<div class="toc">',
                             '<div class="toc"><div class="toctitle">목차</div>', 1)
# 1부 · 2부 · 부록 h1 에만 class="part"
import re as _re
def _mark(m):
    inner = m.group(2)
    if "부 ·" in inner or inner.strip() == "부록":
        return '<h1 class="part"' + m.group(1) + '>' + inner + '</h1>'
    return m.group(0)
body = _re.sub(r'<h1([^>]*)>(.*?)</h1>', _mark, body, flags=_re.S)
print("부 구분 표시 {}곳".format(body.count('class="part"')))

i = body.find("<hr />")
if i > 0:
    body = body[:i] + toc + NL + body[i:]
    print("목차 삽입 완료")
else:
    print("★ <hr /> 미발견 — 목차 없음")

CSS = """
@page { size: A4; margin: 18mm 15mm 20mm 15mm; }
* { box-sizing: border-box; }
html { -webkit-print-color-adjust: exact; print-color-adjust: exact; }
body { font-family: 'Malgun Gothic','맑은 고딕',sans-serif;
  font-size: 9.6pt; line-height: 1.62; color: #16181d;
  margin: 0; word-break: keep-all; overflow-wrap: anywhere; }
h1 { font-size: 19pt; line-height:1.35; margin: 0 0 6mm; padding-bottom: 4mm;
     border-bottom: 2.4pt solid #16181d; letter-spacing: -.4pt; }
/* 부(部) 구분만 새 쪽에서 시작한다. 장은 이어 흐르게 두어 아래 여백을 없앤다. */
h1.part { font-size: 15pt; margin: 0 0 5mm; padding-bottom: 3mm;
          border-bottom: 1.6pt solid #16181d; break-before: page; break-after: avoid; }
h1.part:first-of-type { break-before: auto; }
h2 { font-size: 13.4pt; margin: 7mm 0 3.2mm; padding: 2.2mm 0 2.2mm 3.2mm;
     border-left: 3.6pt solid #16181d; background:#f4f5f7;
     break-after: avoid; break-inside: avoid; letter-spacing: -.3pt; }
h2:first-child { margin-top: 0; }
h3 { font-size: 11.4pt; margin: 5.8mm 0 2.4mm; padding-bottom: 1.4mm;
     border-bottom: .7pt solid #c8ccd4; break-after: avoid; letter-spacing:-.2pt; }
h4 { font-size: 10.2pt; margin: 4.4mm 0 1.8mm; color:#3a4048;
     break-after: avoid; padding-left: 2mm; border-left: 2pt solid #c8ccd4; }
p { margin: 0 0 2.3mm; orphans: 2; widows: 2; }
a { color: #16181d; text-decoration: none; border-bottom: .5pt dotted #8b929e; }
hr { border: 0; border-top: .7pt solid #d4d8df; margin: 4.6mm 0; }
img { max-width: 46mm; height: auto; }
table { border-collapse: collapse; width: 100%; margin: 2.2mm 0 3.4mm;
        font-size: 8.7pt; break-inside: auto; }
thead { display: table-header-group; }
tr { break-inside: avoid; }
th, td { border: .6pt solid #b9bec8; padding: 1.5mm 2mm;
         vertical-align: top; line-height: 1.46; }
th { background: #eceef2; font-weight: 700; text-align: left; }
tr:nth-child(even) td { background: #fafbfc; }
pre { font-family: 'GulimChe','굴림체','D2Coding',Consolas,monospace;
      font-size: 8.4pt; line-height: 1.5; background: #f6f7f9;
      border: .6pt solid #d4d8df; border-left: 2.4pt solid #8b929e;
      padding: 2.2mm 3mm; margin: 2.2mm 0 3.4mm;
      white-space: pre; overflow-x: hidden; break-inside: avoid; }
pre code { font-family: inherit; font-size: inherit; background: none;
           padding: 0; border: 0; }
code { font-family: 'GulimChe','굴림체',Consolas,monospace; font-size: 8.6pt;
       background: #eef0f4; padding: .3mm 1mm; border-radius: 1pt;
       border: .4pt solid #dfe3e9; }
blockquote { margin: 2.2mm 0 3.4mm; padding: 2mm 3mm; font-size: 9.1pt;
             background: #f7f8fa; border-left: 2.4pt solid #b9bec8;
             color: #2f343d; break-inside: avoid; }
blockquote p { margin: 0 0 1.6mm; }
blockquote p:last-child { margin: 0; }
ul, ol { margin: 0 0 3mm; padding-left: 6.5mm; }
li { margin-bottom: 1.2mm; }
.toc { font-size: 9pt; margin: 6mm 0 0; }   /* 뒤의 1부가 이미 개행한다 */
.toc ul { padding-left: 0; list-style: none; margin: 0; }
.toc ul ul { padding-left: 5.5mm; }
.toc li { margin-bottom: 1.1mm; }
.toc > ul > li { font-weight: 700; margin-top: 2.4mm; }
.toc > ul > li ul li { font-weight: 400; }
.toc a { border: 0; }
.toctitle { font-size: 14pt; font-weight: 700; margin: 0 0 4mm;
            padding-bottom: 2.4mm; border-bottom: 1.4pt solid #16181d; }
"""
html = ('<!DOCTYPE html>' + NL + '<html lang="ko"><head><meta charset="utf-8">' + NL
        + '<title>던전앤파이터 트로피컬 바캉스 패키지 BM 분석</title>' + NL
        + '<style>' + CSS + '</style></head><body>' + NL + body + NL + '</body></html>')
io.open(OUT, "w", encoding="utf-8").write(html)
print("HTML {:,}자 · 표 {}개 · 코드블록 {}개 · 인용 {}개".format(
    len(html), body.count("<table>"), body.count("<pre>"), body.count("<blockquote>")))
