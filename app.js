const seedData = [
['2026-11-16','Lunch','13:00','Weekday',145,520,18,'No'],['2026-11-16','Dinner','20:00','Weekday',112,390,12,'No'],['2026-11-17','Lunch','13:00','Weekday',158,550,5,'No'],['2026-11-17','Dinner','20:00','Weekday',120,410,8,'No'],['2026-11-18','Lunch','13:00','Weekday',170,580,0,'Yes'],['2026-11-18','Dinner','20:00','Weekday',105,370,22,'No'],['2026-11-19','Lunch','13:00','Weekday',162,560,7,'No'],['2026-11-19','Dinner','20:00','Weekday',118,400,10,'No'],['2026-11-20','Lunch','13:00','Weekday',180,600,0,'Yes'],['2026-11-20','Dinner','20:00','Weekday',125,430,6,'No'],['2026-11-21','Lunch','13:00','Weekend',95,340,25,'No'],['2026-11-21','Dinner','20:00','Weekend',88,310,19,'No'],['2026-11-22','Lunch','13:00','Weekend',110,380,14,'No'],['2026-11-22','Dinner','20:00','Weekend',92,330,20,'No'],['2026-11-23','Lunch','13:00','Weekday',155,540,9,'No'],['2026-11-23','Dinner','20:00','Weekday',115,395,11,'No'],['2026-11-24','Lunch','13:00','Weekday',175,590,0,'Yes'],['2026-11-24','Dinner','20:00','Weekday',130,440,4,'No'],['2026-11-25','Lunch','13:00','Weekday',150,520,16,'No'],['2026-11-25','Dinner','20:00','Weekday',108,380,15,'No']
].map(r=>({date:r[0],meal:r[1],time:r[2],dayType:r[3],students:r[4],cooked:r[5],left:r[6],ranOut:r[7]}));

const STORAGE='jhelum-roti-records';
let records=JSON.parse(localStorage.getItem(STORAGE)||'null')||seedData;
const $=s=>document.querySelector(s);
const sum=(arr,key)=>arr.reduce((n,r)=>n+Number(r[key]),0);

function save(){localStorage.setItem(STORAGE,JSON.stringify(records));render();}
function average(arr,key){return arr.length?sum(arr,key)/arr.length:0}

function renderStats(){
  $('#recordCount').textContent=records.length;
  $('#avgStudents').textContent=Math.round(average(records,'students'));
  $('#avgCooked').textContent=Math.round(average(records,'cooked'));
  const cooked=sum(records,'cooked'),left=sum(records,'left');
  $('#wasteRate').textContent=cooked?((left/cooked)*100).toFixed(1)+'%':'0%';
}

function renderForecast(){
  const meal=$('#forecastMeal').value,day=$('#forecastDay').value;
  const students=Number($('#forecastStudents').value)||0;
  let matches=records.filter(r=>r.meal===meal&&r.dayType===day);
  if(!matches.length) matches=records.filter(r=>r.meal===meal);
  const consumedPerStudent=average(matches.map(r=>({...r,rate:(r.cooked-r.left)/r.students})),'rate');
  const ratio=consumedPerStudent||average(records.map(r=>({...r,rate:(r.cooked-r.left)/r.students})),'rate')||3.4;
  const suggested=Math.round(students*ratio*1.05);
  $('#suggestedRotis').innerHTML=`${suggested} <small>rotis</small>`;
  $('#forecastNote').textContent=matches.length?`Based on ${matches.length} similar observation${matches.length===1?'':'s'} + 5% buffer`:'Based on all observations + 5% buffer';
}

function renderChart(){
  const recent=[...records].sort((a,b)=>a.date.localeCompare(b.date)).slice(-10);
  const max=Math.max(...recent.flatMap(r=>[r.cooked,r.cooked-r.left]),1);
  $('#demandChart').innerHTML=recent.map(r=>{const consumed=r.cooked-r.left;const labels=r.date.slice(5).replace('-','/');return `<div class="bar-group"><div class="bar cooked" style="height:${r.cooked/max*82}%" title="Cooked: ${r.cooked}"></div><div class="bar consumed" style="height:${consumed/max*82}%" title="Consumed: ${consumed}"></div><span class="bar-label">${labels} ${r.meal[0]}</span></div>`}).join('');
}

function renderTable(){
  $('#recordsTable').innerHTML=[...records].reverse().map(r=>`<tr><td>${r.date}</td><td>${r.meal}</td><td>${r.students}</td><td>${r.cooked}</td><td>${r.left}</td><td>${r.cooked-r.left}</td><td class="${r.ranOut==='Yes'?'status-warn':'status-ok'}">${r.ranOut==='Yes'?'Ran out':'Adequate'}</td></tr>`).join('');
}

function render(){renderStats();renderForecast();renderChart();renderTable();}

$('#mealForm').addEventListener('submit',e=>{
  e.preventDefault();const f=new FormData(e.currentTarget);
  records.push({date:f.get('date'),meal:f.get('meal'),time:f.get('time'),dayType:f.get('dayType'),students:Number(f.get('students')),cooked:Number(f.get('cooked')),left:Number(f.get('left')),ranOut:f.get('ranOut')});
  e.currentTarget.reset();e.currentTarget.elements.date.value=new Date().toISOString().slice(0,10);e.currentTarget.elements.time.value='13:00';save();
  const toast=$('#toast');toast.classList.add('show');setTimeout(()=>toast.classList.remove('show'),1800);
});

['forecastMeal','forecastDay','forecastStudents'].forEach(id=>$('#'+id).addEventListener('input',renderForecast));
document.querySelectorAll('.nav-item').forEach(btn=>btn.addEventListener('click',()=>{
  document.querySelectorAll('.nav-item').forEach(b=>b.classList.remove('active'));btn.classList.add('active');
  const recordsView=btn.dataset.view==='records';$('#dashboardView').hidden=recordsView;$('#recordsView').hidden=!recordsView;$('#pageTitle').textContent=recordsView?'Records':'Dashboard';
}));
$('#resetData').addEventListener('click',()=>{if(confirm('Reset all observations to the sample data?')){records=[...seedData];save();}});

const now=new Date();$('#todayLabel').textContent=now.toLocaleDateString('en-IN',{day:'2-digit',month:'short',year:'numeric'});document.querySelector('[name=date]').value=now.toISOString().slice(0,10);render();
