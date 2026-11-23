import unittest,json,re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
D=json.loads((ROOT/'content.json').read_text(encoding='utf-8'))
class TestGuide(unittest.TestCase):
 def test_counts(self):
  self.assertEqual(len(D['routes']),8)
  self.assertEqual(len(D['chapters']),22)
  self.assertEqual(len(D['prompts']),16)
  self.assertEqual(len(D['plan']),30)
  self.assertGreaterEqual(len(D['sources']),10)
 def test_unique(self):
  for key in ('routes','chapters','prompts'):
   ids=[x['id'] for x in D[key]]
   self.assertEqual(len(ids),len(set(ids)))
  self.assertEqual([x['day'] for x in D['plan']],list(range(1,31)))
 def test_source_urls(self):
  for s in D['sources']:
   self.assertTrue(s['url'].startswith('https://'))
 def test_brand(self):
  alltext='\n'.join((ROOT/x).read_text(encoding='utf-8') for x in ['index.html','README.md','print.html'])
  for marker in ['AIPMAndy','metaver.vip','www.a6no1.cn','pdf/google-ai-income-handbook.pdf']:
   self.assertIn(marker,alltext)
 def test_no_keys(self):
  for p in ROOT.rglob('*'):
   if p.suffix in {'.html','.js','.json','.md'}:
    s=p.read_text(encoding='utf-8')
    self.assertNotRegex(s,r'AIza[0-9A-Za-z_-]{35}')
 def test_no_invalid_chapter(self):
  for x in D['chapters']:
   self.assertGreaterEqual(len(x['steps']),5)
   self.assertTrue(x['output'] and x['redline'])
 def test_print_and_script(self):
  self.assertTrue((ROOT/'print.html').exists())
  self.assertTrue((ROOT/'assets/app.js').exists())
if __name__=='__main__':unittest.main()
