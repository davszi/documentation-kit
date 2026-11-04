// Local/hosted behavior at the new generated-site depth, without browser mocks
// that make filesystem path rewriting pass by construction.
const fs=require('node:fs');
const path=require('node:path');
const vm=require('node:vm');
const assert=require('node:assert/strict');
const root=path.resolve(__dirname,'..');
const script=fs.readFileSync(path.join(root,'examples/starter/.build/docs/html/assets/filelinks.js'),'utf8');
class Link {
  constructor(attrs,text=''){this.attrs={...attrs};this.textContent=text;}
  getAttribute(name){return this.attrs[name]??null;}
  setAttribute(name,value){this.attrs[name]=value;}
}
function run(protocol,pathname){
  const links=[
    new Link({href:'https://github.com/example/project/blob/commit/src/code.py#L12','data-repo-path':'src/code.py','data-repo-fragment':'L12'}),
    new Link({href:'https://github.com/example/project/blob/commit/docs/topics/guide/index.md#detail','data-repo-path':'docs/topics/guide/index.md','data-repo-fragment':'detail'}),
    new Link({href:'../../src/example.py'},'example.py:8'),
    new Link({href:'other.html#chapter'}),
    new Link({href:'https://example.org/paper'}),
    new Link({href:'../topics/guide/index.md#detail'})
  ];
  const media=new Link({'data-local-src':'experiments/capture.mp4'});
  vm.runInNewContext(script,{location:{protocol,pathname},document:{querySelectorAll(selector){return selector==='a[href]'?links:[media];}}});
  return {links,media};
}
const local=run('file:','/home/a%20name/project/.build/docs/html/guide.html');
assert.equal(local.links[0].attrs.href,'vscode://file/home/a name/project/src/code.py:12');
assert.equal(local.links[1].attrs.href,'file:///home/a%20name/project/docs/topics/guide/index.md#detail');
assert.equal(local.links[2].attrs.href,'vscode://file/home/a name/project/src/example.py:8');
assert.equal(local.links[3].attrs.href,'other.html#chapter');
assert.equal(local.links[5].attrs.href,'file:///home/a%20name/project/docs/topics/guide/index.md#detail');
assert.equal(local.media.attrs.src,'file:///home/a%20name/project/experiments/capture.mp4');
const hosted=run('https:','/project/html/guide.html');
assert.equal(hosted.links[0].attrs.href,'https://github.com/example/project/blob/commit/src/code.py#L12');
assert.equal(hosted.links[1].attrs.href,'https://github.com/example/project/blob/commit/docs/topics/guide/index.md#detail');
assert.ok(hosted.links[2].attrs.href.endsWith('/blob/'+encodeURIComponent(process.env.GITHUB_SHA || 'main')+'/src/example.py#L8'));
assert.equal(hosted.links[4].attrs.href,'https://example.org/paper');
assert.ok(hosted.links[5].attrs.href.endsWith('/blob/'+encodeURIComponent(process.env.GITHUB_SHA || 'main')+'/docs/topics/guide/index.md#detail'));
assert.equal(hosted.media.attrs.src,undefined);
console.log('Source links pass: local root, encoded spaces, editor lines, Markdown anchors, hosted pinned references, code chips and local-only capture access.');
