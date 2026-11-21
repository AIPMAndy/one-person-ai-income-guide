/* AIPMAndy / one-person-ai-income-guide: offline-only cashflow calculation.
 * Confirmed receipts ONLY. No telemetry, no server requests. */
(function (root) {
  'use strict';
  const WEEKS = 13, MAX_YUAN = 10000000000;
  function toCents(value) {
    const s = String(value).trim();
    if (!/^(?:0|[1-9]\d{0,10})(?:\.\d{1,2})?$/.test(s)) throw new Error('金额必须是非负数字，最多两位小数，不支持科学记数法。');
    const n = Number(s);
    if (!Number.isFinite(n) || n > MAX_YUAN) throw new Error('单项金额不得超过一百亿元。');
    return Math.round(n * 100);
  }
  function compute(input) {
    if (!input || !Array.isArray(input.weeks) || input.weeks.length !== WEEKS) throw new Error('必须填写完整的13周计划。');
    const opening = toCents(input.opening), reserve = toCents(input.reserve);
    let balance = opening, trough = opening, troughWeek = 0, firstBreach = opening < reserve ? 0 : -1;
    const weeks = input.weeks.map(function (row, i) {
      if (!row || row.receipt === undefined || row.payment === undefined) throw new Error('第' + (i + 1) + '周输入不完整。');
      const receipt = toCents(row.receipt), payment = toCents(row.payment);
      balance += receipt - payment;
      if (!Number.isSafeInteger(balance)) throw new Error('金额过大，无法精确计算。');
      if (balance < trough) { trough = balance; troughWeek = i + 1; }
      if (firstBreach === -1 && balance < reserve) firstBreach = i + 1;
      return { week: i + 1, receipt, payment, closing: balance, belowReserve: balance < reserve };
    });
    return { opening, reserve, weeks, ending: balance, trough, troughWeek, firstBreach };
  }
  const format = cents => '¥' + (cents / 100).toLocaleString('zh-CN', {minimumFractionDigits:2,maximumFractionDigits:2});
  const api = {WEEKS, toCents, compute, format};
  if (typeof module !== 'undefined' && module.exports) module.exports = api;
  if (!root || !root.document) return;
  const d = root.document, tbody = d.getElementById('weeks');
  if (!tbody) return;
  const key = 'ai-solo-cashflow:13-weeks:v1';
  const el = id => d.getElementById(id);
  function addInput(row, name, n) {
    const td = d.createElement('td'), label = d.createElement('label');
    label.className = 'sr-only'; label.htmlFor = name + n;
    label.textContent = '第' + n + '周' + (name === 'receipt' ? '确定到账' : '必须支付');
    const input = d.createElement('input');
    input.type='number'; input.min='0'; input.max=String(MAX_YUAN);
    input.step='0.01'; input.inputMode='decimal'; input.value='0'; input.id=name + n;
    td.append(label, input);row.append(td);
    input.addEventListener('input',render);
  }
  for (let i=1;i<=WEEKS;i++) {
    const tr=d.createElement('tr'), num=d.createElement('th');num.scope='row';num.textContent='第 '+i+' 周';
    tr.append(num);addInput(tr,'receipt',i);addInput(tr,'payment',i);
    const closing=d.createElement('td'), status=d.createElement('td');
    const b=d.createElement('strong');b.id='closing'+i;closing.append(b);status.id='status'+i;
    tr.append(closing,status);tbody.append(tr);
  }
  function snapshot() {
    return {opening:el('opening').value,reserve:el('reserve').value,weeks:Array.from({length:WEEKS},(_,i)=>({
      receipt:el('receipt'+(i+1)).value,payment:el('payment'+(i+1)).value
    }))};
  }
  function render() {
    try {
      const data=snapshot(), result=compute(data);
      for (const row of result.weeks) {
        el('closing'+row.week).textContent=format(row.closing);
        const status=el('status'+row.week);status.textContent=row.belowReserve?'低于底线':'未低于底线';
        status.className=row.belowReserve?'status-danger':'status-good';
      }
      el('ending').textContent=format(result.ending);
      el('trough').textContent=format(result.trough);
      el('breach').textContent=result.firstBreach === -1 ? '未观察到' : result.firstBreach === 0 ? '期初' : '第 '+result.firstBreach+' 周';
      const hasFlow=result.weeks.some(r=>r.receipt!==0||r.payment!==0);
      el('summaryNote').textContent=!hasFlow?'尚未录入任何收支。当前结果只是初始数字，不能推断有足够现金。':result.firstBreach !== -1?'按已输入的确定现金流，出现低于储备底线的周次；应提前调整支出或核实确定到账。':'已输入的现金流没有跌破储备底线；仍须核查未录入的税费、退款和不确定付款。';
      return result;
    } catch(e) {
      el('ending').textContent=el('trough').textContent=el('breach').textContent='输入无效';
      el('summaryNote').textContent='请修正输入：'+e.message;
      for (let i=1;i<=WEEKS;i++){el('closing'+i).textContent='—';el('status'+i).textContent='待核对';el('status'+i).className='';}
      return null;
    }
  }
  function message(s){el('message').textContent=s;}
  function downloadCSV(){
    const r=render();if(!r){message('输入无效，未导出。');return;}
    const rows=[['周次','确定到账元','必须支付元','期末现金元','低于储备底线'],
      ...r.weeks.map(x=>[x.week,(x.receipt/100).toFixed(2),(x.payment/100).toFixed(2),(x.closing/100).toFixed(2),x.belowReserve?'是':'否'])];
    // Cells are fixed labels or validated numeric values; no user-provided formula strings.
    const csv='\ufeff'+rows.map(row=>row.join(',')).join('\r\n')+'\r\n';
    const url=URL.createObjectURL(new Blob([csv],{type:'text/csv;charset=utf-8'}));
    const a=d.createElement('a');a.href=url;a.download='一人AI创业-13周现金流.csv';
    d.body.append(a);a.click();a.remove();root.setTimeout(()=>URL.revokeObjectURL(url),1000);
    message('已下载当前计算的 CSV。请自行保存备份；没有上传任何数字。');
  }
  el('opening').addEventListener('input',render);el('reserve').addEventListener('input',render);
  el('exportCsv').addEventListener('click',downloadCSV);
  el('saveLocal').addEventListener('click',function(){
    if (!render()) {message('数据有误，未保存。');return;}
    try {root.localStorage.setItem(key,JSON.stringify(snapshot()));message('已保存到当前浏览器本地。清除浏览器数据会丢失，建议另存 CSV。');}
    catch(e){message('浏览器禁止本地存储：未保存。仍可导出 CSV。');}
  });
  el('resetAll').addEventListener('click',function(){
    if(!root.confirm('确认清空所有13周输入和本浏览器的现金流记录？此操作不能撤销。'))return;
    try {root.localStorage.removeItem(key);} catch(e){}
    el('opening').value='0';el('reserve').value='0';
    for(let i=1;i<=WEEKS;i++){el('receipt'+i).value='0';el('payment'+i).value='0';}
    render();message('已清空当前输入；没有修改其他页面的任务进度。');
  });
  try {
    const raw=root.localStorage.getItem(key);
    if (raw) {
      const previous=JSON.parse(raw);
      compute(previous);
      el('opening').value=previous.opening;el('reserve').value=previous.reserve;
      previous.weeks.forEach((w,i)=>{el('receipt'+(i+1)).value=w.receipt;el('payment'+(i+1)).value=w.payment;});
      message('已载入本浏览器上次主动保存的现金流记录。');
    }
  } catch(e) {message('旧版本地数据不完整，已忽略。');}
  render();
})(typeof window !== 'undefined' ? window : undefined);
