'use strict';
const test = require('node:test');
const assert = require('node:assert/strict');
const {compute,toCents,format,WEEKS} = require('../assets/cashflow.js');
const rows = (receipt='0',payment='0') => Array.from({length:WEEKS},()=>({receipt,payment}));
test('13 weeks and cents without binary float drift',()=>{
  const plan={opening:'1000.00',reserve:'400.00',weeks:rows('0.10','0.03')};
  const r=compute(plan);
  assert.equal(r.weeks.length,13);
  assert.equal(r.ending,100091);
  assert.equal(r.trough,100000);
  assert.equal(r.firstBreach,-1);
});
test('first week crossing minimum reserve',()=>{
  const w=rows();w[0].payment='40';w[1].payment='30';
  const r=compute({opening:'100',reserve:'50',weeks:w});
  assert.equal(r.firstBreach,2);assert.equal(r.trough,3000);assert.equal(r.ending,3000);
});
test('opening cash below reserve flagged before first week',()=>{
  const r=compute({opening:'30',reserve:'50',weeks:rows()});
  assert.equal(r.firstBreach,0);assert.equal(r.troughWeek,0);
});
test('negative balances allowed and shown as risk, not clamped',()=>{
  const w=rows();w[0].payment='101';
  const r=compute({opening:'100',reserve:'0',weeks:w});
  assert.equal(r.weeks[0].closing,-100);assert.equal(r.firstBreach,1);
});
test('confirmed receipt only - unknown proposals absent from computation',()=>{
  const w=rows();w[0].receipt='10';
  const r=compute({opening:'0',reserve:'0',weeks:w});
  assert.equal(r.ending,1000);
});
test('reject invalid or misleading inputs',()=>{
  for(const bad of ['','-1','1e5','NaN','12.345','1,000','Infinity','99999999999','  1.0?  ']){
    assert.throws(()=>toCents(bad),Error,'expected invalid '+bad);
  }
  assert.equal(toCents('10000000000.00'),1000000000000);
});
test('reject wrong week count and missing values',()=>{
  assert.throws(()=>compute({opening:'0',reserve:'0',weeks:rows().slice(1)}));
  const w=rows();w[4].receipt=undefined;
  assert.throws(()=>compute({opening:'0',reserve:'0',weeks:w}));
});
test('exact reserve equality is safe but one cent below is flagged',()=>{
  const w=rows();w[0].payment='0.01';
  const r=compute({opening:'50',reserve:'50',weeks:w});
  assert.equal(r.firstBreach,1);
  assert.match(format(r.ending),/49\.99/);
});
