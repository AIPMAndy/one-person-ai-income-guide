import json
import pathlib
import re
import unittest
from html.parser import HTMLParser
from urllib.parse import unquote, urlsplit

ROOT=pathlib.Path(__file__).resolve().parents[1]

class ProjectIntegrityTests(unittest.TestCase):
    def test_task_count_and_schemas(self):
        data=json.loads((ROOT/'data/tasks.json').read_text(encoding='utf-8'))
        self.assertEqual(len(data['tasks']),55)
        self.assertEqual(len({x['id'] for x in data['tasks']}),55)
        stages={s['id'] for s in data['phases']}
        self.assertEqual(len(stages),5)
        for row in data['tasks']:
            self.assertTrue({'id','phase','title','action','proof','blocked'}<=row.keys())
            self.assertIn(row['phase'],stages)
            self.assertTrue(all(row[x] for x in ['title','action','proof','blocked']))
    def test_tracks_and_sops(self):
        data=json.loads((ROOT/'data/tracks.json').read_text(encoding='utf-8'))
        self.assertEqual(len(data),7)
        self.assertEqual(len(list((ROOT/'playbooks').glob('0?-*.md'))),7)
        self.assertEqual(len(list((ROOT/'prompts').glob('??-*.md'))),16)
        self.assertEqual(len(list((ROOT/'guides').glob('*.md'))),24)
        self.assertTrue(all(r['risk'] and r['validation'] for r in data))
    def test_all_markdown_and_generated_html_file_links_resolve(self):
        issues=[]
        for p in ROOT.rglob('*.md'):
            source=p.read_text(encoding='utf-8')
            for uri in re.findall(r'\[[^\]]+\]\(([^)]+)\)',source):
                uri=unquote(uri.strip().split('#')[0])
                if not uri or uri.startswith(('http:','https:','mailto:')):continue
                target=(p.parent/uri).resolve()
                if not target.exists():issues.append(f'{p.relative_to(ROOT)} => {uri}')
        self.assertFalse(issues,'Broken links:\n'+'\n'.join(issues))
        class Links(HTMLParser):
            def __init__(self):
                super().__init__(); self.refs=[]; self.ids=set()
            def handle_starttag(self,tag,attrs):
                attrs=dict(attrs)
                self.ids.update([attrs['id']] if 'id' in attrs else [])
                self.refs.extend(attrs[key] for key in ['href','src'] if key in attrs)
        page=Links(); page.feed((ROOT/'index.html').read_text(encoding='utf-8'))
        for ref in page.refs:
            url=urlsplit(ref)
            if url.scheme or url.netloc:continue
            if url.path:
                self.assertTrue((ROOT/unquote(url.path)).exists(),ref)
            elif url.fragment:
                self.assertIn(unquote(url.fragment),page.ids,ref)
    def test_offline_site_has_no_external_dependencies(self):
        index=(ROOT/'index.html').read_text(encoding='utf-8')
        self.assertIn('一个人，一台电脑',index)
        self.assertIn('AI 酋长 Andy',index)
        self.assertIn('doc-playbooks-05-workflow-automation',index)
        self.assertNotRegex(index,r'<script[^>]+src=')
        self.assertNotRegex(index,r'<link[^>]+(?:stylesheet|preconnect)')
        self.assertNotRegex(index,r'\bfetch\s*\(')
        self.assertNotRegex(index,r'\bXMLHttpRequest\s*\(')
        self.assertNotIn('google-analytics',index.lower())
        self.assertNotIn('gtag(',index)
    def test_no_real_case_claims(self):
        for p in (ROOT/'cases').glob('0*.md'):
            first=p.read_text(encoding='utf-8')[:210]
            self.assertIn('虚构',first,p.name)
    def test_required_deep_dive_paths(self):
        for path in [
            'RESEARCH-2026.md','guides/12-from-zero-operating-manual.md',
            'guides/13-first-client-funnel.md','guides/14-pricing-unit-economics.md',
            'guides/19-failure-tree-and-red-team.md','guides/21-week-by-week-30day-plan.md',
            'guides/23-ai-business-anti-scam.md','templates/acceptance-form.md',
            'templates/data-handling-checklist.md','templates/13-week-cashflow.csv',
            'cases/04-complete-funnel-demo.md','audit/ADVERSARIAL_REVIEW.md']:
            self.assertTrue((ROOT/path).exists(),path)
    def test_research_scope_and_honest_cases(self):
        readme=(ROOT/'README.md').read_text(encoding='utf-8')
        research=(ROOT/'RESEARCH-2026.md').read_text(encoding='utf-8')
        for term in ['美国','搜索','2026-10-12','不能','Fiverr','Upwork']:
            self.assertIn(term,research)
        self.assertIn('所有示例人物',readme)
        self.assertIn('不保证任何人',readme)
        self.assertIn('55 项',readme)
    def test_new_capacity_ui_and_offline_markdown(self):
        index=(ROOT/'index.html').read_text(encoding='utf-8')
        for term in ['id="goalRevenue"','id="requiredOrders"','id="doc-guides-12-from-zero-operating-manual"',
                     'id="doc-research-2026"','id="progressNum"','本机']:
            self.assertIn(term,index)
        self.assertEqual(index.count('id="goalRevenue"'),1)
    def test_all_sensitive_workflow_guardrails(self):
        for p in (ROOT/'playbooks').glob('0?-*.md'):
            s=p.read_text(encoding='utf-8')
            self.assertGreater(len(s),1500,p.name)
            self.assertTrue(any(t in s for t in ['验收','核验']),p.name)
            self.assertTrue(any(t in s for t in ['虚构','演示']),p.name)
    def test_required_templates(self):
        for p in ['templates/leads.csv','templates/cashflow.csv','templates/quote.md','templates/offer.md','templates/unit-economics.csv','templates/qa-checklist.md','assets/social-preview.svg','audit/ADVERSARIAL_REVIEW.md']:
            self.assertTrue((ROOT/p).exists(),p)

    def test_real_story_evidence_cards_are_complete(self):
        cn=sorted((ROOT/'cases').glob('real-cn??.md'))
        en=sorted((ROOT/'cases').glob('real-en??.md'))
        self.assertEqual((len(cn),len(en)),(8,10))
        for p in cn+en:
            body=p.read_text(encoding='utf-8')
            self.assertIn('https://',body,p.name)
            for section in ['## 1.','## 2.','## 3.','## 4.','## 5.','## 6.']:
                self.assertIn(section,body,p.name)
            for term in ['没有','完成标准','核验']:
                self.assertIn(term,body,p.name)
            self.assertNotRegex(body,r'业务路径：\*\* 00[1-7]')
    def test_real_case_index_and_sop_cross_links(self):
        index=(ROOT/'cases/REAL-CASE-INDEX.md').read_text(encoding='utf-8')
        for p in sorted((ROOT/'cases').glob('real-*.md')):
            self.assertIn(p.name,index)
        for p in (ROOT/'playbooks').glob('0?-*.md'):
            self.assertIn('REAL-CASE-INDEX.md',p.read_text(encoding='utf-8'),p.name)
        self.assertIn('没有 A 级',index)
    def test_deep_dives_include_bad_outcomes_and_caveats(self):
        s=(ROOT/'cases/DEEP-DIVES.md').read_text(encoding='utf-8')
        self.assertEqual(s.count('## 故事'),6)
        for term in ['半年零收入','先拿出能看的','Marcus Grimm','Kinetic Investments','不能','未由本仓库审计']:
            self.assertIn(term,s)
        self.assertTrue((ROOT/'cases/CASE-AUDIT.md').exists())
        self.assertTrue((ROOT/'templates/real-case-register.csv').exists())
if __name__=='__main__':unittest.main()
