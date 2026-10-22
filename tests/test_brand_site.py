import pathlib
import unittest
ROOT = pathlib.Path(__file__).resolve().parents[1]
class AppleBrandTests(unittest.TestCase):
    def test_contacts_are_visible_and_consistent(self):
        for path in ("assets/site-template.html", "index.html"):
            src = (ROOT / path).read_text(encoding="utf-8")
            for token in ("https://metaver.vip/", "https://metaver.vip/services", "AIPMAndy", "AI 酋长 Andy", 'id="contact"', 'class="floating-contact"', "data-copy-wechat", "navigator.clipboard", "document.execCommand", 'id="copyToast"'):
                with self.subTest(path=path, token=token):
                    self.assertIn(token, src)
            self.assertGreaterEqual(src.count("data-copy-wechat"), 5)
            self.assertIn("不承诺收入", src)
    def test_design_and_no_hidden_data_exfiltration(self):
        src = (ROOT / "assets/site-template.html").read_text(encoding="utf-8")
        for token in ("--light:#f5f5f7", "--blue:#0066cc", ".hero-visual", ".contact-showcase", "@media(max-width:600px)", "@media(max-width:850px)", "prefers-reduced-motion", "<!--TOC-->", "<!--DOCS-->", 'id="taskList"'):
            self.assertIn(token, src)
        self.assertNotIn("<script src=", src)
        self.assertNotIn("google-analytics", src.lower())
        self.assertNotIn("https://fonts.googleapis.com", src)
        self.assertNotIn("fetch(", src)
    def test_readme_and_audit_have_consistent_author_contact(self):
        src = (ROOT / "README.md").read_text(encoding="utf-8")
        for token in ("metaver.vip/services", "AIPMAndy", "无需先添加微信", "APPLE-BRAND-REVIEW-2026-10-22"):
            self.assertIn(token, src)
if __name__ == "__main__": unittest.main()