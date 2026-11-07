// Run the vendored math renderer with the built page's actual configuration.
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');
const root = path.resolve(__dirname, '..');
const katex = require(path.join(root,'theme/assets/vendor/katex/katex.min.js'));
class DomNode {
  constructor(type,name='',text='') {this.nodeType=type;this.nodeName=name.toUpperCase();this.className='';this.childNodes=[];this.value=text;this.parentNode=null;}
  get textContent() {return this.nodeType===3?this.value:this.childNodes.map(n=>n.textContent).join('');}
  get nextSibling() {if(!this.parentNode)return null;return this.parentNode.childNodes[this.parentNode.childNodes.indexOf(this)+1]||null;}
  appendChild(child) {if(child.nodeType===11) child.childNodes.slice().forEach(n=>this.appendChild(n));else {child.parentNode=this;this.childNodes.push(child);}return child;}
  replaceChild(child,old) {const i=this.childNodes.indexOf(old),fresh=child.nodeType===11?child.childNodes:[child];fresh.forEach(n=>n.parentNode=this);this.childNodes.splice(i,1,...fresh);old.parentNode=null;}
  remove() {this.parentNode.childNodes.splice(this.parentNode.childNodes.indexOf(this),1);this.parentNode=null;}
}
const text=s=>new DomNode(3,'',s);
const element=(tag,...children)=>{const n=new DomNode(1,tag);children.forEach(c=>n.appendChild(typeof c==='string'?text(c):c));return n;};
const inline=element('span',String.raw`\(10^{-`,String.raw`9}\)`);inline.className='math-inline';
const display=element('div',String.raw`$$\mathbf{B}'=(1-l\kappa)\mathbf{t}+l'\mathbf{n}$$`);display.className='math';
const ignored=['pre','code','script','style'].map(tag=>element(tag,String.raw`$$do_not_render$$ \(also_literal\)`));
const currency=element('p','Costs $10 and $20.');
const content=element('main',element('p','Above ',inline,'.'),display,currency,...ignored);
const calls=[];
const document={createDocumentFragment:()=>new DomNode(11),createTextNode:text,createElement:tag=>element(tag),querySelector(selector) {assert.equal(selector,'.content');return content;},addEventListener(event,callback) {assert.equal(event,'DOMContentLoaded');callback();}};
const adapter={ParseError:katex.ParseError,render(formula,node,options) {node.rendered=katex.renderToString(formula,{...options,throwOnError:true});calls.push({formula,display:options.displayMode});}};
const moduleObject={exports:{}};
vm.runInNewContext(fs.readFileSync(path.join(root,'theme/assets/vendor/katex/contrib/auto-render.min.js'),'utf8'),{module:moduleObject,exports:moduleObject.exports,require:name=>{assert.equal(name,'katex');return adapter;},document,Node:{TEXT_NODE:3},console});
const page=fs.readFileSync(path.join(root,'.build/starter/.build/docs/html/guide.html'),'utf8');
const script=[...page.matchAll(/<script>([\s\S]*?)<\/script>/g)].find(m=>m[1].includes('renderMathInElement(document.querySelector'))[1];
vm.runInNewContext(script,{document,renderMathInElement:moduleObject.exports});
assert.deepEqual(calls.map(c=>c.display),[false,true]);
assert.equal(calls[0].formula,'10^{-9}');assert.ok(inline.childNodes[0].rendered.includes('class="katex"'));
assert.equal(currency.textContent,'Costs $10 and $20.');
ignored.forEach(n=>assert.equal(n.textContent,String.raw`$$do_not_render$$ \(also_literal\)`));
const decode=s=>s.replace(/&(?:amp|lt|gt|quot|#x27|#39);/g,e=>({'&amp;':'&','&lt;':'<','&gt;':'>','&quot;':'"','&#x27;':"'",'&#39;':"'"}[e]));
let inlineCount=0,displayCount=0;
for (const file of fs.readdirSync(path.join(root,'.build/starter/.build/docs/html')).filter(n=>n.endsWith('.html'))) {
  const html=fs.readFileSync(path.join(root,'.build/starter/.build/docs/html',file),'utf8');
  for(const m of html.matchAll(/<span class="math-inline">\\\(([\s\S]*?)\\\)<\/span>/g)) {
    assert.ok(!m[1].includes('<'),`${file}: formula split by Markdown`);
    katex.renderToString(decode(m[1]),{throwOnError:true,displayMode:false});inlineCount++;
  }
  for(const m of html.matchAll(/<div class="math">\$\$([\s\S]*?)\$\$<\/div>/g)) {
    katex.renderToString(decode(m[1]),{throwOnError:true,displayMode:true});displayCount++;
  }
}
assert.ok(inlineCount>=1&&displayCount>=1,'Starter must exercise both inline and display math');
const ids=[...page.matchAll(/(?<![\w-])id="([^"]+)"/g)].map(m=>m[1]);
assert.equal(new Set(ids).size,ids.length,'Starter page and figure anchors must be unique');
assert.ok(page.includes('id="fig-pipeline"'),'Starter ownership flow must remain present');
console.log(`Vendored auto-render passes inline/display and split-text integration, preserves currency/code; ${inlineCount} inline and ${displayCount} display formulas compile across built pages; new diagram IDs are unique.`);
