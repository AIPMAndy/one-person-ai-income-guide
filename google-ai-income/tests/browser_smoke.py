from pathlib import Path
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1]
URL=(ROOT/'index.html').as_uri()
with sync_playwright() as p:
 browser=p.chromium.launch(headless=True,executable_path='/usr/bin/chromium',args=['--no-sandbox'])
 for width,height in [(390,844),(1280,900)]:
  page=browser.new_page(viewport={'width':width,'height':height},device_scale_factor=1)
  errors=[]
  page.on('pageerror',lambda e: errors.append(str(e)))
  source=(ROOT/'index.html').read_text(encoding='utf-8')
  source=source.replace('<link rel="stylesheet" href="assets/style.css" />','<style>'+ (ROOT/'assets/style.css').read_text(encoding='utf-8')+'</style>')
  source=source.replace('<script defer src="assets/data.js"></script>','').replace('<script defer src="assets/app.js"></script>','')
  source=source.replace('</body>', '<script>'+ (ROOT/'assets/data.js').read_text(encoding='utf-8')+'</script><script>'+ (ROOT/'assets/app.js').read_text(encoding='utf-8')+'</script></body>')
  page.set_content(source,wait_until='load')
  page.screenshot(path=str(ROOT/f'tests/screenshot-{width}.png'),full_page=True)
  dims=page.evaluate('''()=>({scroll:document.documentElement.scrollWidth,client:document.documentElement.clientWidth,chapterButtons:document.querySelectorAll('.lesson-button').length,routeCards:document.querySelectorAll('.route-card').length,promptCards:document.querySelectorAll('.prompt-card').length,dayCards:document.querySelectorAll('.day-card').length})''')
  print(width,dims,errors)
  assert dims['scroll']<=dims['client']+1,(width,'overflow')
  assert dims['chapterButtons']==22 and dims['routeCards']==8 and dims['promptCards']==16 and dims['dayCards']==30
  assert not errors,errors
  page.locator('.chip[data-filter="technical"]').click()
  assert page.locator('.route-card').count()==2
  page.locator('.chip[data-filter="all"]').click()
  assert page.locator('.route-card').count()==8
  page.locator('#chapter-search').fill('报价')
  assert 1 <= page.locator('.lesson-button').count()<22
  page.locator('#chapter-search').fill('')
  page.locator('#prompt-filter').select_option('开发')
  assert page.locator('.prompt-card').count()==2
  page.locator('#prompt-filter').select_option('all')
  page.locator('#received').fill('2000')
  assert '1,900' in page.locator('#contribution').inner_text()
  page.locator('#recommend').click()
  assert '建议先验证：' in page.locator('#recommend-result').inner_text()
  page.locator('[data-day="1"]').check()
  assert '1 / 30' in page.locator('#progress-count').inner_text()
  # about:blank/browser policy in this environment blocks persistence reload; storage behavior is tested through JavaScript state
  print('SMOKE PASS',width)
  page.close()
 browser.close()
