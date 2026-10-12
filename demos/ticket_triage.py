#!/usr/bin/env python3
"""Local, standard-library-only demonstration. Processes SYNTHETIC ticket CSV into a review CSV.
No model/API/network access, no emails, no account writes, no payment actions.
Only process fake or otherwise legitimately handled local data.
"""
import argparse
import csv
from collections import Counter
from pathlib import Path

REVIEW_TERMS = ('退款', '投诉', '赔偿', '转账', '忽略规则', '汇款', '删库', '私钥', '验证码')
LOGISTIC_TERMS = ('发货', '物流', '签收', '快递', '破损')

def classify(rows):
    ids=Counter(r.get('ticket_id', '').strip() for r in rows if r.get('ticket_id', '').strip())
    results=[]
    for row in rows:
        ticket_id=row.get('ticket_id','').strip()
        summary=row.get('summary','').strip()
        status=row.get('status','').strip()
        reasons=[]
        if not ticket_id or not summary:reasons.append('关键字段为空')
        if ticket_id and ids[ticket_id]>1:reasons.append('重复单号')
        if any(word in summary for word in REVIEW_TERMS):reasons.append('需人工判断的敏感操作/异常内容')
        if status and status not in {'open','pending','closed'}:reasons.append('状态值异常')
        if reasons:
            category='需人工审核'
        elif any(word in summary for word in LOGISTIC_TERMS):
            category='物流咨询'
        else:
            category='普通咨询'
        results.append({'ticket_id':ticket_id,'summary':summary,'suggested_category':category,
                        'review_required':'是' if reasons else '否',
                        'review_reason':'；'.join(reasons)})
    return results

def process_file(source,destination):
    with source.open('r',encoding='utf-8-sig',newline='') as f:
        reader=csv.DictReader(f)
        required={'ticket_id','summary','status'}
        if not required.issubset(set(reader.fieldnames or [])):
            raise ValueError('CSV 必须包含 ticket_id,summary,status 三列')
        rows=list(reader)
        if len(rows)>10000: raise ValueError('演示最多处理10000行；大量数据应先做独立安全审查')
    result=classify(rows)
    destination.parent.mkdir(parents=True,exist_ok=True)
    with destination.open('w',encoding='utf-8-sig',newline='') as f:
        writer=csv.DictWriter(f,fieldnames=['ticket_id','summary','suggested_category','review_required','review_reason'])
        writer.writeheader();writer.writerows(result)
    return len(result),sum(1 for x in result if x['review_required']=='是')

if __name__=='__main__':
    parser=argparse.ArgumentParser(description='安全的离线虚构工单分类演示。不发送邮件、不退款、不连接真实客户系统。')
    parser.add_argument('--input',default=str(Path(__file__).with_name('tickets-demo.csv')))
    parser.add_argument('--output',default=str(Path(__file__).with_name('review-demo.csv')))
    args=parser.parse_args()
    source,dest=Path(args.input),Path(args.output)
    if source.resolve()==dest.resolve():parser.error('不能覆盖源文件')
    count,flag=process_file(source,dest)
    print(f'完成 {count} 条虚构工单，{flag} 条进入人工审核。结果保存在 {dest}')
