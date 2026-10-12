#!/usr/bin/env python3
"""Build a no-dependency offline HTML guide from local Markdown and JSON source."""
from __future__ import annotations
import html
import json
import re
from pathlib import Path
from urllib.parse import quote, unquote, urlsplit, urlunsplit

ROOT=Path(__file__).resolve().parent
DOC_PATHS=[
 ROOT/'START-HERE.md',
 ROOT/'RESEARCH-2026.md',
 *sorted((ROOT/'guides').glob('*.md')),
 *sorted((ROOT/'playbooks').glob('*.md')),
 *sorted((ROOT/'prompts').glob('*.md')),
 *sorted((ROOT/'templates').glob('*.md')),
 *sorted((ROOT/'cases').glob('*.md')),
 ROOT/'SOURCES.md', ROOT/'audit/ADVERSARIAL_REVIEW.md'
]

def doc_id(p):
    return 'doc-'+str(p.relative_to(ROOT).with_suffix('')).replace('/','-').replace('_','-').lower()

def inline(text: str, source:Path) -> str:
    # Inline author-created Markdown only. Escape all literal markup first.
    slots=[]
    def code_repl(m):
        slots.append('<code>'+html.escape(m.group(1))+'</code>')
        return f'\x1a{len(slots)-1}\x1a'
    text=re.sub(r'`([^`\n]+)`',code_repl,text)
    text=html.escape(text,quote=True)
    def link_repl(m):
        label=m.group(1)
        url=html.unescape(m.group(2)).strip()
        if url.lower().startswith('javascript:') or url.lower().startswith('data:'):
            return label
        parts=urlsplit(url)
        if not parts.scheme and not parts.netloc:
            # Documents are embedded in index.html, so their local links must
            # resolve from the original Markdown directory before rebasing.
            if parts.path:
                rel=unquote(parts.path)
                target=((ROOT/rel.lstrip('/')) if rel.startswith('/') else (source.parent/rel)).resolve()
            else:
                target=source.resolve()
            if target in DOC_PATHS:
                url='#'+doc_id(target)
            elif parts.path:
                path=target.relative_to(ROOT).as_posix()
                url=urlunsplit(('', '', quote(path, safe='/'), parts.query, parts.fragment))
        attr=' target="_blank" rel="noopener noreferrer"' if url.startswith('http') else ''
        return '<a href="'+html.escape(url,quote=True)+'"'+attr+'>'+label+'</a>'
    text=re.sub(r'\[([^\]]+)\]\(([^)]+)\)',link_repl,text)
    text=re.sub(r'\*\*([^*\n]+)\*\*',r'<strong>\1</strong>',text)
    for i,s in enumerate(slots): text=text.replace(f'\x1a{i}\x1a',s)
    return text

def render_markdown(md: str,source:Path) ->str:
    lines=md.splitlines(); out=[]; in_code=False; code=[]; lst=None; para=[]; table=[]
    def flushpara():
        if para: out.append('<p>'+inline(' '.join(para),source)+'</p>');para.clear()
    def flushlist():
        nonlocal lst
        if lst:out.append(f'</{lst}>');lst=None
    def flushtable():
        if not table:return
        headers=table[0];cells=[headers]+table[1:]
        s='<div class="table-scroll"><table>'
        for n,one in enumerate(cells):
            s+='<tr>'+''.join(f'<{"th" if n==0 else "td"}>'+inline(c,source)+f'</{"th" if n==0 else "td"}>' for c in one)+'</tr>'
        out.append(s+'</table></div>');table.clear()
    i=0
    while i<len(lines):
        line=lines[i]; trim=line.strip()
        if trim.startswith('```'):
            flushpara();flushlist();flushtable()
            if not in_code:in_code=True;code=[]
            else:out.append('<pre><code>'+html.escape('\n'.join(code))+'</code></pre>');in_code=False
            i+=1;continue
        if in_code:code.append(line);i+=1;continue
        if re.fullmatch(r'\|?(?:\s*:?[-]{3,}:?\s*\|)+\s*',trim):i+=1;continue
        if trim.startswith('|') and trim.endswith('|'):
            flushpara();flushlist();table.append([c.strip() for c in trim.strip('|').split('|')]);i+=1;continue
        if table:flushtable()
        if not trim:flushpara();flushlist();i+=1;continue
        h=re.match(r'^(#{1,5})\s+(.+)$',trim)
        if h:
            flushpara();flushlist();n=len(h.group(1));out.append(f'<h{min(n+1,6)}>'+inline(h.group(2),source)+f'</h{min(n+1,6)}>');i+=1;continue
        if trim.startswith('>'):
            flushpara();flushlist();out.append('<blockquote>'+inline(trim.lstrip('> ').strip(),source)+'</blockquote>');i+=1;continue
        typ=None; item=None
        m=re.match(r'^[-*]\s+(.+)',trim)
        if m:typ='ul';item=m.group(1)
        m2=re.match(r'^\d+[.)]\s+(.+)',trim)
        if m2:typ='ol';item=m2.group(1)
        if typ:
            flushpara()
            if lst!=typ:flushlist();out.append(f'<{typ}>');lst=typ
            out.append('<li>'+inline(item,source)+'</li>');i+=1;continue
        flushlist();para.append(trim);i+=1
    flushpara();flushlist();flushtable()
    if in_code:out.append('<pre><code>'+html.escape('\n'.join(code))+'</code></pre>')
    return '\n'.join(out)

def build():
    tasks=json.loads((ROOT/'data/tasks.json').read_text(encoding='utf-8'))
    routes=json.loads((ROOT/'data/tracks.json').read_text(encoding='utf-8'))
    sections=[];toc=[]
    for path in DOC_PATHS:
        if not path.exists():raise FileNotFoundError(path)
        source=path.read_text(encoding='utf-8')
        heading=next((x.lstrip('#').strip() for x in source.splitlines() if x.startswith('# ')),path.stem)
        ident=doc_id(path)
        group=path.relative_to(ROOT).parts[0]
        sections.append(f'<details class="chapter" id="{ident}"><summary>{html.escape(heading)}</summary><div class="doc">{render_markdown(source,path)}</div></details>')
        toc.append(f'<a href="#{ident}">{html.escape(heading)}</a>')
    safe=lambda obj:json.dumps(obj,ensure_ascii=False,separators=(',',':')).replace('</','<\\/')
    template=(ROOT/'assets/site-template.html').read_text(encoding='utf-8')
    page=template.replace('<!--TOC-->','\n'.join(toc)).replace('<!--DOCS-->','\n'.join(sections)).replace('<!--TASKS_JSON-->',safe(tasks)).replace('<!--ROUTES_JSON-->',safe(routes))
    (ROOT/'index.html').write_text(page,encoding='utf-8')
    print(f"Built {ROOT/'index.html'} ({len(DOC_PATHS)} chapters, {len(tasks['tasks'])} tasks, {len(routes)} routes)")

if __name__=='__main__':build()
