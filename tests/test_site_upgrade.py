import pathlib
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]

class SiteUpgradeTests(unittest.TestCase):
    def test_actionable_offline_site(self):
        source=(ROOT/'assets/site-template.html').read_text(encoding='utf-8')
        page=(ROOT/'index.html').read_text(encoding='utf-8')
        required=['id="first-order"','id="downloadPlan"','id="planBuyer"',
                  'id="planPain"','id="planOutput"','id="planChannel"',
                  'id="planBoundary"','id="backup"','id="restore"',
                  'id="restoreInput"','id="chapterSearch"','id="chapterCount"',
                  "ai-solo-task-backup","completedTasks","new Set(p.completedTasks)",
                  'role="progressbar"','aria-valuenow','rel="canonical"',
                  'property="og:image"','class="skip-link"']
        for marker in required:
            with self.subTest(marker=marker):
                self.assertIn(marker,source)
                self.assertIn(marker,page)

    def test_new_features_have_no_network_submission(self):
        source=(ROOT/'assets/site-template.html').read_text(encoding='utf-8')
        for marker in ['<form action=', 'XMLHttpRequest(', 'sendBeacon(', 'fetch(']:
            self.assertNotIn(marker,source)
        self.assertNotIn('<script src=',source)

    def test_audit_is_findable(self):
        readme=(ROOT/'README.md').read_text(encoding='utf-8')
        report=(ROOT/'audit/REDTEAM-2026-10-22.md').read_text(encoding='utf-8')
        for marker in ['第一单作战卡','JSON 备份','章节标题搜索','REDTEAM-2026-10-22']:
            self.assertIn(marker,readme)
        for marker in ['P0','待验证','来源','核验','Pages']:
            self.assertIn(marker,report)

if __name__ == '__main__':
    unittest.main()
