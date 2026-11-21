import pathlib
import unittest
import xml.etree.ElementTree as ET
import json
import re

ROOT = pathlib.Path(__file__).resolve().parents[1]
BASE = "https://aipmandy.github.io/one-person-ai-income-guide/"

class CashflowPageTests(unittest.TestCase):
    def test_site_links_and_metadata(self):
        page = (ROOT / "cashflow.html").read_text(encoding="utf-8")
        source = (ROOT / "assets/site-template.html").read_text(encoding="utf-8")
        published = (ROOT / "index.html").read_text(encoding="utf-8")
        for html in (source, published):
            self.assertIn('href="cashflow.html"', html)
            self.assertIn('href="pdf/one-person-ai-income-guide-guide.pdf"', html)
            self.assertIn('https://www.a6no1.cn/', html)
        for marker in [
            'rel="canonical" href="' + BASE + 'cashflow.html"',
            'https://metaver.vip/services', 'https://www.a6no1.cn/', 'AIPMAndy',
            'type="application/ld+json"', 'id="weeks"', 'id="saveLocal"',
            'id="exportCsv"', 'id="resetAll"', 'src="assets/cashflow.js"'
        ]:
            with self.subTest(marker=marker):
                self.assertIn(marker, page)
        ld = re.search(r'<script type="application/ld\+json">(.*?)</script>', page, re.S)
        self.assertIsNotNone(ld)
        data = json.loads(ld.group(1))
        self.assertEqual(data["@type"], "WebApplication")
        self.assertEqual(data["url"], BASE + "cashflow.html")
        self.assertTrue(data["isAccessibleForFree"])
        self.assertIn("https://www.a6no1.cn/", data["publisher"]["url"])

    def test_sitemap_and_robots(self):
        tree = ET.parse(ROOT / "sitemap.xml")
        ns = {"s": "http://www.sitemaps.org/schemas/sitemap/0.9"}
        urls = [node.text for node in tree.findall(".//s:loc", ns)]
        self.assertEqual(urls.count(BASE + "cashflow.html"), 1)
        self.assertEqual(urls.count(BASE), 1)
        self.assertIn(BASE + "sitemap.xml", (ROOT / "robots.txt").read_text())

    def test_pdf_version_not_silently_changed(self):
        edition = json.loads((ROOT / "pdf/edition.json").read_text())
        self.assertEqual(edition["date"], "2026-11-13")
        self.assertEqual(edition["pages"], 199)
        self.assertEqual(edition["pdf_path"], "pdf/one-person-ai-income-guide-guide.pdf")

    def test_no_remote_or_user_data_collection(self):
        page = (ROOT / "cashflow.html").read_text()
        js = (ROOT / "assets/cashflow.js").read_text()
        for marker in ("fetch(", "XMLHttpRequest", "sendBeacon(", "analytics", "gtag("):
            self.assertNotIn(marker, js)
        self.assertNotIn('<form action=', page)
        self.assertNotIn('https://fonts.googleapis.com/', page)

if __name__ == "__main__":
    unittest.main()
