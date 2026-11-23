#!/usr/bin/env python3
"""Build a complete, bookmarked, searchable Chinese PDF from content.json."""
from pathlib import Path
import json, html
from reportlab.platypus import BaseDocTemplate, PageTemplate, Frame, Paragraph, Spacer, PageBreak, KeepTogether, Table, TableStyle, HRFlowable
from reportlab.platypus.tableofcontents import TableOfContents
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase.cidfonts import UnicodeCIDFont
from reportlab.pdfbase import pdfmetrics
from reportlab.lib.enums import TA_LEFT, TA_CENTER
from reportlab.lib.units import mm
ROOT=Path(__file__).resolve().parent
pdfmetrics.registerFont(UnicodeCIDFont('STSong-Light'))
FONT='STSong-Light'
C={'ink':colors.HexColor('#14271B'),'mint':colors.HexColor('#42A574'),'sub':colors.HexColor('#647569'),'light':colors.HexColor('#EDF8F0'),'warm':colors.HexColor('#FFF5E5'),'line':colors.HexColor('#DDEADE')}
W,H=A4
MARGIN_X=21*mm
MARGIN_TOP=19*mm
MARGIN_BOTTOM=19*mm
styles={
 'coverTop':ParagraphStyle('coverTop',fontName=FONT,fontSize=11,leading=17,textColor=C['mint'],spaceAfter=19),
 'cover':ParagraphStyle('cover',fontName=FONT,fontSize=36,leading=48,textColor=C['ink'],spaceAfter=25,wordWrap='CJK'),
 'subtitle':ParagraphStyle('subtitle',fontName=FONT,fontSize=15,leading=26,textColor=C['sub'],spaceAfter=15,wordWrap='CJK'),
 'body':ParagraphStyle('body',fontName=FONT,fontSize=10.5,leading=18.5,textColor=C['ink'],spaceAfter=9,wordWrap='CJK'),
 'foot':ParagraphStyle('foot',fontName=FONT,fontSize=9.2,leading=16.5,textColor=C['sub'],spaceAfter=8,wordWrap='CJK'),
 'tocHead':ParagraphStyle('tocHead',fontName=FONT,fontSize=26,leading=36,textColor=C['ink'],spaceAfter=18),
 'section':ParagraphStyle('ChTitle',fontName=FONT,fontSize=21,leading=32,textColor=C['ink'],spaceBefore=8,spaceAfter=15,keepWithNext=True,wordWrap='CJK'),
 'subhead':ParagraphStyle('subhead',fontName=FONT,fontSize=12.3,leading=20,textColor=C['mint'],spaceBefore=13,spaceAfter=8,keepWithNext=True,wordWrap='CJK'),
 'list':ParagraphStyle('list',fontName=FONT,fontSize=10.3,leading=18.2,textColor=C['ink'],leftIndent=15,firstLineIndent=-14,spaceAfter=8,wordWrap='CJK'),
 'box':ParagraphStyle('box',fontName=FONT,fontSize=10.3,leading=18,textColor=C['ink'],wordWrap='CJK'),
 'prompt':ParagraphStyle('prompt',fontName=FONT,fontSize=10,leading=19,textColor=C['ink'],spaceAfter=10,wordWrap='CJK'),
 'toc':ParagraphStyle('toc',fontName=FONT,fontSize=11,leading=21,textColor=C['ink'],leftIndent=10,firstLineIndent=-10,spaceAfter=6,wordWrap='CJK'),
}

def normalize(text):
 return str(text).replace('·',' / ').replace('｜',' / ').replace('•',' - ').replace('→',' -> ').replace('—',' - ').replace('✓',' OK ')

def P(text,kind='body'):
 return Paragraph(html.escape(normalize(text)).replace('\n','<br/>'),styles[kind])

def box(label,text,bg):
 t=Table([[Paragraph('<b>'+html.escape(normalize(label))+'</b><br/>'+html.escape(normalize(text)).replace('\n','<br/>'),styles['box'])]],colWidths=[W-2*MARGIN_X-14],hAlign='LEFT')
 t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,-1),bg),('BOX',(0,0),(-1,-1),.4,C['line']),('LEFTPADDING',(0,0),(-1,-1),12),('RIGHTPADDING',(0,0),(-1,-1),12),('TOPPADDING',(0,0),(-1,-1),10),('BOTTOMPADDING',(0,0),(-1,-1),11)]))
 return t

class HandbookDoc(BaseDocTemplate):
 def __init__(self,path):
  super().__init__(str(path),pagesize=A4,rightMargin=MARGIN_X,leftMargin=MARGIN_X,topMargin=MARGIN_TOP,bottomMargin=MARGIN_BOTTOM,title='Google AI 赚钱保姆级实战攻略',author='AI 酋长 Andy / 星觉科技',subject='Google AI 商业实操与风险核验')
  frame=Frame(MARGIN_X,MARGIN_BOTTOM,W-2*MARGIN_X,H-MARGIN_TOP-MARGIN_BOTTOM,leftPadding=0,rightPadding=0,topPadding=0,bottomPadding=0,id='main')
  self.addPageTemplates(PageTemplate(id='main',frames=frame,onPage=self.draw_page))
 def draw_page(self,canv,doc):
  canv.saveState();canv.setFont(FONT,8.5)
  if doc.page>1:
   canv.setStrokeColor(C['line']);canv.line(MARGIN_X,H-13*mm,W-MARGIN_X,H-13*mm)
   canv.setFillColor(C['sub']);canv.drawString(MARGIN_X,H-10.5*mm,'GOOGLE AI INCOME HANDBOOK / FREE EDITION')
  canv.setStrokeColor(C['line']);canv.line(MARGIN_X,14*mm,W-MARGIN_X,14*mm)
  canv.setFillColor(C['sub']);canv.drawString(MARGIN_X,9*mm,'AI 酋长 Andy / 微信 AIPMAndy / metaver.vip / a6no1.cn')
  canv.drawRightString(W-MARGIN_X,9*mm,str(doc.page));canv.restoreState()
 def afterFlowable(self,flowable):
  if isinstance(flowable,Paragraph) and flowable.style.name=='ChTitle':
   key=getattr(flowable,'_bookmark',None)
   if key:
    self.canv.bookmarkPage(key);self.notify('TOCEntry',(0,flowable.getPlainText(),self.page,key))

def build():
 d=json.loads((ROOT/'content.json').read_text(encoding='utf-8'))
 path=ROOT/'pdf/google-ai-income-handbook.pdf'
 story=[]
 story += [Spacer(1,48*mm),P('AI CHIEF ANDY  /  FREE · OPEN SOURCE  /  2026.11','coverTop'),P('Google AI 赚钱\n保姆级实战攻略','cover'),P('从真实需求到可验收交付\n8 条业务路线 · 22 章 · 16 套 Prompt · 30 天计划','subtitle'),Spacer(1,13*mm),HRFlowable(width='90%',thickness=4,color=C['mint']),Spacer(1,14*mm),P('AI 酋长 Andy / 星觉科技','subhead'),P('微信：AIPMAndy ｜ 个人官网：https://metaver.vip/','body'),P('公司官网：https://www.a6no1.cn/ ｜ 教程免费开放','body'),Spacer(1,20*mm),P('本书不是 Google 官方材料，不包含任何收入保证。所有金额属于读者自行输入的经营假设；商业收入仅以实际到账、真实交付与成本核算为准。官方产品、价格、额度和适用规则请在使用前核验。','foot'),PageBreak()]
 story += [P('目录 / CONTENTS','tocHead'),P('先找一个真的愿意付钱的人；再用 AI 把交付成本降下来。','body'),Spacer(1,6*mm)]
 toc=TableOfContents();toc.levelStyles=[styles['toc']];story.append(toc);story.append(PageBreak())
 for c in d['chapters']:
  title=P(c['id']+'  '+c['title'],'section');title._bookmark='chapter_'+c['id'];story.append(title)
  story.append(P(c['lead']))
  if c['tools']:story.append(P('适用工具：'+c['tools'],'foot'))
  story.append(P('照着做 · '+str(len(c['steps']))+' 步','subhead'))
  for i,x in enumerate(c['steps'],1):story.append(P(str(i)+'.  '+x,'list'))
  story += [Spacer(1,6),box('最终应交付：',c['output'],C['light']),Spacer(1,8),box('不能越过的风险红线：',c['redline'],C['warm']),Spacer(1,15)]
  if c['example']:story.append(P('虚构演示：'+c['example'],'foot'))
  if c['check']:story.append(P('验收方式：'+c['check'],'foot'))
 story.append(PageBreak());p=P('附录 A  16 套完整 Prompt','section');p._bookmark='appendix_prompts';story.append(p);story.append(P('花括号表示待替换信息；只输入你有权使用的数据。无需购买提示词。','foot'))
 for o in d['prompts']:
  story += [P(f"{o['id']:02d} · {o['category']}｜{o['title']}",'subhead'),P(o['body'],'prompt')]
 story.append(PageBreak());p=P('附录 B  30 天行动计划','section');p._bookmark='appendix_plan';story.append(p);story.append(P('30 天只是可复盘的实验期限，即使全部打卡也不保证首单或收益。','foot'))
 for x in d['plan']:story.append(P(f"Day {x['day']:02d} · {x['phase']}｜{x['action']}｜证据：{x['proof']}",'list'))
 story.append(PageBreak());p=P('附录 C  官方来源与核查台账','section');p._bookmark='appendix_sources';story.append(p)
 for i,x in enumerate(d['sources'],1):
  story += [P(str(i)+'. '+x['title'],'subhead'),P(x['url'],'foot'),P(x['note'],'foot')]
 story.append(PageBreak());story += [Spacer(1,43*mm),P('教程免费。\n需要落地支持，再来找我。','cover'),P('AI 酋长 Andy / 星觉科技','subhead'),P('个人微信：AIPMAndy','body'),P('个人官网：https://metaver.vip/','body'),P('公司官网：https://www.a6no1.cn/','body'),P('服务与陪跑：https://metaver.vip/services','body'),Spacer(1,12*mm),box('再强调一次','本书所有教程、Prompt 和模板均免费使用。添加微信或购买咨询并非阅读前提。部分生成内容需人工核实授权、平台规则和经营利润，不能保证任何人的收入。',C['light'])]
 doc=HandbookDoc(path);doc.multiBuild(story)
 print(path,path.stat().st_size)
 return path
if __name__=='__main__':build()
