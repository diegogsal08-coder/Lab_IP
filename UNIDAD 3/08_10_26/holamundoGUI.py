from flask import Flask, render_template_string

app = Flask(__name__)

@app.route('/')
def hola_world():
    return render_template_string('''
<!doctype html><html lang="es"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Batalla de torres</title><style>
body{margin:0;background:#192733;color:white;text-align:center;font:16px system-ui}h1{color:#ffd166;margin:12px}p{margin:6px}
canvas{width:min(800px,96vw);height:auto;border:4px solid #d6a84f;border-radius:12px;background:#79c96b;display:block;margin:auto}
button{margin:8px 3px;padding:10px 14px;border:2px solid #8ecae6;border-radius:10px;background:#235078;color:white;font-weight:bold;cursor:pointer}button:disabled{opacity:.45}
#info{min-height:24px;color:#ffd166;font-weight:bold}
</style></head><body><h1>Batalla de torres</h1>
<p>Elige una unidad y haz clic en tu lado del campo. ¡Destruye la torre roja!</p>
<canvas id="game" width="800" height="460"></canvas><div id="info">Energía: <span id="energy">5</span></div>
<div><button data-unit="knight">⚔️ Caballero · 3</button><button data-unit="archer">🏹 Arquera · 2</button><button data-unit="giant">🛡️ Gigante · 5</button><button id="reset">Reiniciar</button></div>
<script>
const c=document.getElementById('game'),g=c.getContext('2d'),energyEl=document.getElementById('energy');
const kinds={knight:{cost:3,hp:75,speed:34,damage:14,range:28,color:'#2878c7',label:'C'},archer:{cost:2,hp:42,speed:27,damage:9,range:100,color:'#259b91',label:'A'},giant:{cost:5,hp:190,speed:18,damage:28,range:30,color:'#8652b5',label:'G'}};
let energy=5,units=[],selected='',enemyTimer=0,last=performance.now(),ended=false;
const towers=[{x:85,y:230,hp:300,max:300,side:'blue'},{x:715,y:230,hp:300,max:300,side:'red'}];
function reset(){energy=5;units=[];enemyTimer=0;ended=false;towers[0].hp=towers[0].max;towers[1].hp=towers[1].max;document.getElementById('info').innerHTML='Energía: <span id="energy">5</span>'}
document.querySelectorAll('[data-unit]').forEach(b=>b.onclick=()=>selected=b.dataset.unit);
document.getElementById('reset').onclick=reset;
c.onclick=e=>{if(!selected||ended)return;const r=c.getBoundingClientRect(),x=(e.clientX-r.left)*800/r.width,y=(e.clientY-r.top)*460/r.height,k=kinds[selected];if(x>400||energy<k.cost)return;energy-=k.cost;units.push({x:Math.max(115,x),y:Math.max(35,Math.min(425,y)),hp:k.hp,max:k.hp,side:'blue',kind:selected,...k});selected=''};
function drawTower(t){g.fillStyle=t.side==='blue'?'#2369ac':'#bd4545';g.fillRect(t.x-25,t.y-38,50,76);g.fillStyle='#252525';g.fillRect(t.x-28,t.y-50,56,8);g.fillStyle='#76e36e';g.fillRect(t.x-27,t.y-49,54*Math.max(0,t.hp/t.max),6);g.fillStyle='white';g.font='24px sans-serif';g.textAlign='center';g.fillText('♜',t.x,t.y+8)}
function update(dt){energy=Math.min(10,energy+dt*.45);enemyTimer+=dt;if(enemyTimer>4.5&&towers[1].hp>0){enemyTimer=0;const name=Math.random()<.5?'knight':'archer',k=kinds[name];units.push({x:660,y:70+Math.random()*320,hp:k.hp,max:k.hp,side:'red',kind:name,...k})}
for(const u of units){if(u.hp<=0)continue;const foe=units.find(v=>v.side!==u.side&&v.hp>0&&Math.abs(v.x-u.x)<u.range+14&&Math.abs(v.y-u.y)<60),target=foe||towers[u.side==='blue'?1:0];if(foe||Math.abs(target.x-u.x)<u.range+28){u.cool=(u.cool||0)-dt;if(u.cool<=0){target.hp-=u.damage;u.cool=.8}}else u.x+=(u.side==='blue'?1:-1)*u.speed*dt}
units=units.filter(u=>u.hp>0&&u.x>15&&u.x<785);if(towers[0].hp<=0||towers[1].hp<=0){ended=true;document.getElementById('info').textContent=towers[1].hp<=0?'¡Victoria! Pulsa Reiniciar para jugar otra vez.':'Derrota. Pulsa Reiniciar para intentarlo de nuevo.'}}
function render(){g.clearRect(0,0,800,460);g.fillStyle='#79c96b';g.fillRect(0,0,800,460);g.fillStyle='#55a9d5';g.fillRect(0,205,800,50);g.fillStyle='#dfca83';g.fillRect(0,222,800,16);g.fillStyle='#4e9a4b';for(let y=30;y<460;y+=40)g.fillRect(0,y,800,2);towers.forEach(drawTower);for(const u of units){g.beginPath();g.fillStyle=u.color;g.arc(u.x,u.y,14,0,7);g.fill();g.fillStyle='#222';g.fillRect(u.x-16,u.y-22,32,4);g.fillStyle='#7eff73';g.fillRect(u.x-16,u.y-22,32*Math.max(0,u.hp/u.max),4);g.fillStyle='white';g.font='12px sans-serif';g.fillText(u.label,u.x,u.y+4)}energyEl.textContent=Math.floor(energy);document.querySelectorAll('[data-unit]').forEach(b=>b.disabled=ended||energy<kinds[b.dataset.unit].cost)}
function loop(now){const dt=Math.min(.05,(now-last)/1000);last=now;if(!ended)update(dt);render();requestAnimationFrame(loop)}requestAnimationFrame(loop);
</script>
<style>
body{background:radial-gradient(ellipse at top,#31556a 0,#192733 68%);padding:12px 10px 24px;box-sizing:border-box}
h1{font-size:clamp(27px,4vw,40px);text-shadow:0 3px 0 #8d592d,0 6px 18px #0009;letter-spacing:.5px}
p{color:#e1edf2}canvas{box-shadow:0 16px 40px #0009,inset 0 0 0 3px #fff3;touch-action:manipulation}
button{box-shadow:0 4px 0 #102e45,0 6px 12px #0005;transition:transform .12s,filter .12s}
button:hover:not(:disabled){transform:translateY(-2px);filter:brightness(1.15)}
button:active:not(:disabled){transform:translateY(2px);box-shadow:0 1px 0 #102e45}
button:disabled{cursor:not-allowed}#info{margin:8px auto;color:#ffe08a;text-shadow:0 2px 3px #0008}
</style>
<script>
// Batalla táctica: carriles, proyectiles visibles y torres que defienden su campo.
const lanes=[105,230,355],shots=[],impacts=[];let battleClock=0,spawnClock=0;
function nearestLane(y){return lanes.reduce((best,lane)=>Math.abs(lane-y)<Math.abs(best-y)?lane:best,lanes[0])}
function fireShot(x,y,target,color,damage){shots.push({x,y,sx:x,sy:y,target,color,damage,age:0,life:.24})}
function update(dt){
 if(ended)return;
 battleClock+=dt;energy=Math.min(10,energy+dt*.52);spawnClock+=dt;
 if(spawnClock>Math.max(2.8,5.5-battleClock*.012)&&towers[1].hp>0){spawnClock=0;const name=Math.random()<.58?'knight':'archer',k=kinds[name],y=lanes[Math.floor(Math.random()*lanes.length)];units.push({x:660,y,hp:k.hp,max:k.hp,side:'red',kind:name,...k,cool:.35+Math.random()})}
 for(const u of units){if(u.hp<=0)continue;const lane=nearestLane(u.y);u.y+=(lane-u.y)*Math.min(1,dt*8);
  const foe=units.find(v=>v.side!==u.side&&v.hp>0&&nearestLane(v.y)===lane&&Math.abs(v.x-u.x)<u.range+18);
  const target=foe||towers[u.side==='blue'?1:0];
  if(foe||Math.abs(target.x-u.x)<u.range+30){u.cool=(u.cool||0)-dt;if(u.cool<=0){fireShot(u.x+(u.side==='blue'?12:-12),u.y-5,target,u.color,u.damage);u.cool=u.kind==='archer'?1.05:.82}}
  else u.x+=(u.side==='blue'?1:-1)*u.speed*dt;
 }
 for(const t of towers){if(t.hp<=0)continue;const foe=units.find(u=>u.hp>0&&u.side!==t.side&&Math.abs(u.x-t.x)<190&&Math.abs(nearestLane(u.y)-t.y)<155);t.cool=(t.cool||0)-dt;if(foe&&t.cool<=0){fireShot(t.x+(t.side==='blue'?24:-24),t.y-25,foe,t.side==='blue'?'#b6edff':'#ffc0b3',13);t.cool=1.15}}
 for(let i=shots.length-1;i>=0;i--){const s=shots[i];s.age+=dt;const p=Math.min(1,s.age/s.life);s.x=s.sx+(s.target.x-s.sx)*p;s.y=s.sy+(s.target.y-s.sy)*p-Math.sin(p*Math.PI)*19;if(p>=1){s.target.hp-=s.damage;impacts.push({x:s.x,y:s.y,age:0,color:s.color});shots.splice(i,1)}}
 for(const p of impacts)p.age+=dt;while(impacts.length&&impacts[0].age>.25)impacts.shift();
 units=units.filter(u=>u.hp>0&&u.x>8&&u.x<792);
 if(towers[0].hp<=0||towers[1].hp<=0){ended=true;document.getElementById('info').textContent=towers[1].hp<=0?'¡Victoria! La torre roja ha caído. Pulsa Reiniciar.':'¡Derrota! Tu torre ha caído. Pulsa Reiniciar.'}
}
function drawFort(t){const blue=t.side==='blue',wall=blue?'#347db7':'#c55252',dark=blue?'#20547e':'#843737';g.save();g.shadowColor='#19321c';g.shadowBlur=12;g.shadowOffsetY=6;g.fillStyle=dark;g.fillRect(t.x-34,t.y-42,68,82);g.fillStyle=wall;g.fillRect(t.x-30,t.y-47,60,82);for(const dx of [-27,0,27])g.fillRect(t.x+dx-9,t.y-55,18,16);g.shadowBlur=0;g.shadowOffsetY=0;g.fillStyle='#f4d28a';g.fillRect(t.x-25,t.y-12,50,5);g.fillStyle='#452f2c';g.beginPath();g.arc(t.x,t.y+35,9,Math.PI,0);g.fill();g.fillRect(t.x-9,t.y+35,18,9);g.fillStyle='#272522';g.fillRect(t.x-37,t.y-69,74,8);g.fillStyle='#55e47b';g.fillRect(t.x-35,t.y-67,70*Math.max(0,t.hp/t.max),4);g.restore()}
function render(){
 const grass=g.createLinearGradient(0,0,0,460);grass.addColorStop(0,'#a8d77d');grass.addColorStop(1,'#69b85c');g.fillStyle=grass;g.fillRect(0,0,800,460);
 for(let y=18;y<460;y+=31){g.fillStyle=y%2?'#ffffff0c':'#244d2410';g.fillRect(0,y,800,2)}
 for(const y of lanes){g.fillStyle='#9cbd65';g.fillRect(0,y-37,800,74);g.fillStyle='#c8d88a';g.fillRect(0,y-34,800,3);g.fillRect(0,y+31,800,3)}
 const water=g.createLinearGradient(378,0,422,0);water.addColorStop(0,'#55b8dc');water.addColorStop(.5,'#8de2ed');water.addColorStop(1,'#42a4d0');g.fillStyle=water;g.fillRect(378,0,44,460);g.fillStyle='#ffffff35';for(let y=15;y<460;y+=47)g.fillRect(385,y,28,2);
 for(const y of lanes){g.fillStyle='#795333';g.fillRect(365,y-27,70,54);for(let x=368;x<435;x+=12){g.fillStyle='#b88752';g.fillRect(x,y-25,8,50);g.fillStyle='#e4bd7c';g.fillRect(x,y-24,2,48)}g.strokeStyle='#68472d';g.lineWidth=3;g.strokeRect(365,y-27,70,54)}
 g.fillStyle='#506c3b';g.fillRect(0,0,8,460);g.fillRect(792,0,8,460);towers.forEach(drawFort);
 for(const u of units){g.save();g.shadowColor='#0007';g.shadowBlur=8;g.shadowOffsetY=4;g.fillStyle=u.color;g.beginPath();g.arc(u.x,u.y,15,0,Math.PI*2);g.fill();g.shadowBlur=0;g.shadowOffsetY=0;g.fillStyle=u.side==='blue'?'#d9efff':'#ffe1d8';g.beginPath();g.arc(u.x-2,u.y-3,8,0,Math.PI*2);g.fill();g.fillStyle='#263343';g.font='bold 12px system-ui';g.textAlign='center';g.fillText(u.label,u.x,u.y+4);g.fillStyle='#2e3331';g.fillRect(u.x-17,u.y-25,34,5);g.fillStyle=u.side==='blue'?'#64f080':'#ff7373';g.fillRect(u.x-16,u.y-24,32*Math.max(0,u.hp/u.max),3);g.restore()}
 for(const s of shots){g.fillStyle=s.color;g.shadowColor=s.color;g.shadowBlur=12;g.beginPath();g.arc(s.x,s.y,5,0,Math.PI*2);g.fill();g.shadowBlur=0}
 for(const p of impacts){g.globalAlpha=1-p.age/.25;g.fillStyle=p.color;g.beginPath();g.arc(p.x,p.y,4+p.age*20,0,Math.PI*2);g.fill();g.globalAlpha=1}
 energyEl.textContent=Math.floor(energy);document.querySelectorAll('[data-unit]').forEach(b=>b.disabled=ended||energy<kinds[b.dataset.unit].cost)
}
// Despliega cada unidad en un carril; reserva energía y avanza por los puentes.
c.onclick=e=>{if(!selected||ended)return;const r=c.getBoundingClientRect(),x=(e.clientX-r.left)*800/r.width,y=(e.clientY-r.top)*460/r.height,k=kinds[selected];if(x>390||energy<k.cost)return;energy-=k.cost;units.push({x:Math.max(115,x),y:nearestLane(y),hp:k.hp,max:k.hp,side:'blue',kind:selected,...k,cool:.25});selected=''};
document.getElementById('reset').addEventListener('click',()=>{shots.length=0;impacts.length=0;battleClock=0;spawnClock=0;selected='';for(const t of towers)t.cool=0});
</script>
<style>
/* Interfaz ampliada para mostrar el estado táctico de la partida. */
#command-center{width:min(800px,96vw);margin:12px auto;display:grid;
 grid-template-columns:repeat(4,minmax(0,1fr));gap:8px;text-align:left}
.command-card{position:relative;overflow:hidden;padding:10px 12px;
 border:1px solid #b9e8ff33;border-radius:12px;
 background:linear-gradient(145deg,#2c5063,#192f3d);
 box-shadow:0 5px 14px #0005}
.command-card:after{content:"";position:absolute;left:0;bottom:0;width:100%;height:3px;
 background:linear-gradient(90deg,#60d9d1,#ffe08a)}
.command-title{display:block;color:#b8d4df;font-size:10px;font-weight:700;
 letter-spacing:1.2px;text-transform:uppercase}
.command-value{display:block;margin-top:3px;color:#ffe08a;font-size:19px;
 font-weight:800;font-variant-numeric:tabular-nums}
#command-actions{width:min(800px,96vw);margin:8px auto;display:flex;
 flex-wrap:wrap;justify-content:center;gap:5px}
#command-actions button{min-width:130px;background:#315d73}
#command-actions button[aria-pressed="true"]{border-color:#ffe08a;background:#795c30}
#command-actions button:disabled{filter:grayscale(.75)}
#battle-log{width:min(780px,92vw);min-height:22px;margin:6px auto;
 color:#e3f5ff;font-size:13px;text-shadow:0 2px 4px #000}
#game-guide{width:min(780px,92vw);margin:7px auto;color:#bfd1d8;
 font-size:12px;line-height:1.6}
@media(max-width:560px){
 #command-center{grid-template-columns:repeat(2,minmax(0,1fr))}
 #command-actions button{flex:1 1 40%;min-width:0;padding:8px 5px;font-size:12px}
 #game-guide{font-size:11px}
}
</style>
<script>
// Centro de mando: mejoras aditivas sobre las reglas y animaciones existentes.
const commandStyleReady=true;
const commandCenter=document.createElement('section');
commandCenter.id='command-center';
commandCenter.setAttribute('aria-label','Estado de la batalla');
commandCenter.innerHTML=`
 <div class="command-card">
  <span class="command-title">Oleada</span>
  <span class="command-value" id="wave-value">1</span>
 </div>
 <div class="command-card">
  <span class="command-title">Puntuación</span>
  <span class="command-value" id="score-value">0</span>
 </div>
 <div class="command-card">
  <span class="command-title">Tiempo</span>
  <span class="command-value" id="clock-value">00:00</span>
 </div>
 <div class="command-card">
  <span class="command-title">Salud de tu torre</span>
  <span class="command-value" id="tower-value">100%</span>
 </div>`;
document.getElementById('info').after(commandCenter);

const commandActions=document.createElement('div');
commandActions.id='command-actions';
commandActions.innerHTML=`
 <button id="lightning-action" title="Inflige daño a los enemigos cercanos al puente">
  ⚡ Rayo · 4
 </button>
 <button id="repair-action" title="Recupera salud de la torre azul">
  🔧 Reparar · 3
 </button>
 <button id="pause-action" aria-pressed="false">⏸ Pausar</button>
 <button id="sound-action" aria-pressed="false">🔇 Sonido</button>`;
commandCenter.after(commandActions);

const gameGuide=document.createElement('p');
gameGuide.id='game-guide';
gameGuide.textContent=
 'Defiende los tres carriles y destruye la torre roja. Teclas: 1/2/3 para elegir unidad, Espacio para pausar, R para reiniciar y Esc para cancelar.';
commandActions.after(gameGuide);

const battleLog=document.createElement('div');
battleLog.id='battle-log';
battleLog.setAttribute('role','status');
battleLog.setAttribute('aria-live','polite');
gameGuide.after(battleLog);

const waveValue=document.getElementById('wave-value');
const scoreValue=document.getElementById('score-value');
const clockValue=document.getElementById('clock-value');
const towerValue=document.getElementById('tower-value');
const lightningButton=document.getElementById('lightning-action');
const repairButton=document.getElementById('repair-action');
const pauseButton=document.getElementById('pause-action');
const soundButton=document.getElementById('sound-action');

let commandPaused=false;
let commandSound=false;
let commandScore=0;
let commandTime=0;
let commandWave=1;
let commandLogTime=0;
let lightningCooldown=0;
let repairCooldown=0;
let pointerPosition=null;
let soundContext=null;
let trackedEnemies=0;
let lastBaseTowerHealth=towers[0].hp;

// Guarda las funciones activas antes de añadir el control de pausa y el HUD.
const baseGameUpdate=update;
const baseGameRender=render;

function writeBattleLog(text,seconds=2.5){
 battleLog.textContent=text;
 commandLogTime=seconds;
}

function formatBattleTime(seconds){
 const total=Math.floor(seconds);
 const minutes=String(Math.floor(total/60)).padStart(2,'0');
 const remainder=String(total%60).padStart(2,'0');
 return `${minutes}:${remainder}`;
}

function playBattleTone(frequency,duration=.08,type='sine'){
 if(!commandSound)return;
 try{
  soundContext=soundContext||new(window.AudioContext||window.webkitAudioContext)();
  const oscillator=soundContext.createOscillator();
  const volume=soundContext.createGain();
  oscillator.type=type;
  oscillator.frequency.value=frequency;
  volume.gain.setValueAtTime(.04,soundContext.currentTime);
  volume.gain.exponentialRampToValueAtTime(.001,
   soundContext.currentTime+duration);
  oscillator.connect(volume);
  volume.connect(soundContext.destination);
  oscillator.start();
  oscillator.stop(soundContext.currentTime+duration);
 }catch(error){
  commandSound=false;
 }
}

function setActionState(){
 lightningButton.disabled=ended||commandPaused||energy<4||lightningCooldown>0;
 repairButton.disabled=ended||commandPaused||energy<3||repairCooldown>0||
  towers[0].hp>=towers[0].max;
 pauseButton.disabled=ended;
 pauseButton.textContent=commandPaused?'▶ Continuar':'⏸ Pausar';
 pauseButton.setAttribute('aria-pressed',String(commandPaused));
 soundButton.textContent=commandSound?'🔊 Sonido':'🔇 Sonido';
 soundButton.setAttribute('aria-pressed',String(commandSound));
 document.querySelectorAll('[data-unit]').forEach(button=>{
  button.classList.toggle('active',button.dataset.unit===selected);
 });
}

function refreshCommandCenter(){
 const currentWave=Math.max(1,Math.floor(battleClock/24)+1);
 waveValue.textContent=String(currentWave);
 scoreValue.textContent=commandScore.toLocaleString('es-ES');
 clockValue.textContent=formatBattleTime(commandTime);
 const health=Math.max(0,towers[0].hp);
 towerValue.textContent=`${Math.ceil(health/towers[0].max*100)}%`;
 lightningButton.textContent=lightningCooldown>0?
  `⚡ Rayo · ${Math.ceil(lightningCooldown)}s`:'⚡ Rayo · 4';
 repairButton.textContent=repairCooldown>0?
  `🔧 Reparar · ${Math.ceil(repairCooldown)}s`:'🔧 Reparar · 3';
 // El primer manejador de reinicio recrea este elemento; actualízalo por ID.
 const energyDisplay=document.getElementById('energy');
 if(energyDisplay)energyDisplay.textContent=String(Math.floor(energy));
 setActionState();
}

function castLightning(){
 if(ended||commandPaused||energy<4||lightningCooldown>0)return;
 const targets=units.filter(unit=>unit.side==='red'&&unit.hp>0)
  .sort((left,right)=>Math.abs(left.x-400)-Math.abs(right.x-400))
  .slice(0,4);
 if(targets.length===0){
  writeBattleLog('No hay enemigos cerca del puente.');
  return;
 }
 energy-=4;
 lightningCooldown=7;
 for(const unit of targets){
  unit.hp-=48;
  impacts.push({x:unit.x,y:unit.y,age:0,color:'#fff27a'});
 }
 playBattleTone(145,.24,'sawtooth');
 writeBattleLog(`¡Rayo! ${targets.length} enemigo(s) alcanzado(s).`);
 refreshCommandCenter();
}

function castRepair(){
 if(ended||commandPaused||energy<3||repairCooldown>0||
  towers[0].hp>=towers[0].max)return;
 energy-=3;
 repairCooldown=10;
 towers[0].hp=Math.min(towers[0].max,towers[0].hp+85);
 impacts.push({x:towers[0].x,y:towers[0].y,age:0,color:'#85ff9b'});
 playBattleTone(660,.16,'triangle');
 writeBattleLog('Torre reparada: +85 de salud.');
 refreshCommandCenter();
}

lightningButton.addEventListener('click',castLightning);
repairButton.addEventListener('click',castRepair);
pauseButton.addEventListener('click',()=>{
 if(ended)return;
 commandPaused=!commandPaused;
 writeBattleLog(commandPaused?'Partida en pausa.':'¡La batalla continúa!',1.8);
 refreshCommandCenter();
});
soundButton.addEventListener('click',()=>{
 commandSound=!commandSound;
 if(commandSound)playBattleTone(520,.06,'triangle');
 refreshCommandCenter();
});

// Acceso rápido y cancelación de selección con teclado.
document.addEventListener('keydown',event=>{
 if(event.repeat)return;
 if(event.key===' '){
  event.preventDefault();
  if(!ended){
   commandPaused=!commandPaused;
   writeBattleLog(commandPaused?'Partida en pausa.':'¡La batalla continúa!');
   refreshCommandCenter();
  }
 }
 if(event.key.toLowerCase()==='r'){
  document.getElementById('reset').click();
 }
 if(event.key==='Escape'){
  selected='';
  writeBattleLog('Selección cancelada.',1.5);
  refreshCommandCenter();
 }
 if(commandPaused||ended)return;
 const choices={'1':'knight','2':'archer','3':'giant'};
 if(choices[event.key]){
  selected=choices[event.key];
  const button=document.querySelector(`[data-unit="${selected}"]`);
  if(button)button.click();
  refreshCommandCenter();
 }
});

// Conserva una indicación visual del carril y punto de despliegue.
c.addEventListener('pointermove',event=>{
 const rect=c.getBoundingClientRect();
 pointerPosition={
  x:(event.clientX-rect.left)*800/rect.width,
  y:(event.clientY-rect.top)*460/rect.height
 };
});
c.addEventListener('pointerleave',()=>{pointerPosition=null;});

// Informa al jugador si intenta desplegar en el campo contrario.
const existingCanvasClick=c.onclick;
c.onclick=event=>{
 if(commandPaused){
  writeBattleLog('Reanuda la partida para desplegar unidades.',1.8);
  return;
 }
 if(selected){
  const rect=c.getBoundingClientRect();
  const clickX=(event.clientX-rect.left)*800/rect.width;
  if(clickX>390){
   writeBattleLog('Solo puedes desplegar unidades en tu mitad.');
   return;
  }
 }
 const before=units.length;
 existingCanvasClick(event);
 if(units.length>before){
  const unit=units[units.length-1];
  const laneNumber=lanes.indexOf(unit.y)+1;
  writeBattleLog(`${unit.label} desplegado en el carril ${laneNumber}.`,1.8);
  playBattleTone(330,.06,'triangle');
 }
};

// Envolver la simulación original, sin alterar sus reglas de combate.
update=function(dt){
 if(commandPaused||ended){
  refreshCommandCenter();
  return;
 }
 const previousEnemyCount=units.filter(unit=>
  unit.side==='red'&&unit.hp>0).length;
 const towerHealthBefore=towers[0].hp;
 baseGameUpdate(dt);
 commandTime+=dt;
 lightningCooldown=Math.max(0,lightningCooldown-dt);
 repairCooldown=Math.max(0,repairCooldown-dt);
 if(commandLogTime>0){
  commandLogTime-=dt;
  if(commandLogTime<=0)battleLog.textContent='';
 }
 const currentEnemyCount=units.filter(unit=>
  unit.side==='red'&&unit.hp>0).length;
 if(currentEnemyCount<previousEnemyCount){
  commandScore+=(previousEnemyCount-currentEnemyCount)*50;
  playBattleTone(740,.04,'square');
 }
 if(towers[0].hp<towerHealthBefore&&!ended){
  playBattleTone(115,.1,'sawtooth');
  if(towers[0].hp<lastBaseTowerHealth-35){
   writeBattleLog('¡Tu torre está bajo ataque!');
  }
 }
 lastBaseTowerHealth=towers[0].hp;
 const wave=Math.max(1,Math.floor(battleClock/24)+1);
 if(wave>commandWave){
  commandWave=wave;
  commandScore+=100;
  writeBattleLog(`¡Oleada ${wave}! Llegan nuevos refuerzos.`);
  playBattleTone(520,.14,'triangle');
 }
 trackedEnemies=currentEnemyCount;
 refreshCommandCenter();
};

// Dibuja ayudas y una pantalla clara al pausar o terminar la batalla.
function drawCommandOverlay(){
 g.save();
 if(pointerPosition&&selected&&!commandPaused&&!ended){
  const x=Math.max(115,Math.min(390,pointerPosition.x));
  const y=nearestLane(pointerPosition.y);
  g.globalAlpha=.23;
  g.fillStyle=energy>=kinds[selected].cost?'#76f39a':'#ff6565';
  g.beginPath();
  g.arc(x,y,23,0,Math.PI*2);
  g.fill();
  g.globalAlpha=.9;
  g.strokeStyle='#ffffff';
  g.lineWidth=2;
  g.beginPath();
  g.arc(x,y,23,0,Math.PI*2);
  g.stroke();
 }
 if(commandPaused){
  g.fillStyle='#07121bcc';
  g.fillRect(0,0,800,460);
  g.textAlign='center';
  g.fillStyle='#ffe08a';
  g.font='bold 46px system-ui';
  g.fillText('PAUSA',400,210);
  g.fillStyle='#ffffff';
  g.font='18px system-ui';
  g.fillText('Pulsa Espacio o Continuar para volver',400,248);
 }
 if(ended){
  g.fillStyle='#07121bbd';
  g.fillRect(0,0,800,460);
  g.textAlign='center';
  g.fillStyle=towers[1].hp<=0?'#ffe08a':'#ffb1a8';
  g.font='bold 42px system-ui';
  g.fillText(towers[1].hp<=0?'¡VICTORIA!':'FIN DE LA PARTIDA',400,203);
  g.fillStyle='#ffffff';
  g.font='19px system-ui';
  g.fillText(`Puntuación: ${commandScore.toLocaleString('es-ES')} · Oleada ${commandWave}`,400,243);
 }
 g.restore();
}

render=function(){
 baseGameRender();
 drawCommandOverlay();
};

// El primer reinicio restablece la partida; esta capa restablece el HUD.
document.getElementById('reset').addEventListener('click',()=>{
 commandPaused=false;
 commandScore=0;
 commandTime=0;
 commandWave=1;
 commandLogTime=0;
 lightningCooldown=0;
 repairCooldown=0;
 trackedEnemies=0;
 lastBaseTowerHealth=towers[0].max;
 battleLog.textContent='';
 refreshCommandCenter();
});

// Etiquetas accesibles y estado inicial de las acciones.
document.querySelectorAll('[data-unit]').forEach(button=>{
 button.setAttribute('aria-label',button.textContent.trim());
});
refreshCommandCenter();
writeBattleLog('¡Prepara tus defensas! La batalla está a punto de comenzar.',3.5);
</script>
</body></html>''')

if __name__ == '__main__':
    app.run(debug=True)