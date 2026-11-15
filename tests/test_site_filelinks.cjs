// Local/hosted behavior at the new generated-site depth, without browser mocks
// that make filesystem path rewriting pass by construction.
const fs=require('node:fs');
const path=require('node:path');
const vm=require('node:vm');
const assert=require('node:assert/strict');
const root=path.resolve(__dirname,'..');
const script=fs.readFileSync(path.join(root,'.build/starter/.build/docs/html/assets/filelinks.js'),'utf8');
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

// Publication removes repository metadata from admitted source links. Without
// a remote, HTTP preview must preserve those exact exported paths as well as
// the builder's logical source paths that still carry repository metadata.
const noRemoteScript=fs.readFileSync(path.join(root,'theme/components/filelinks.js'),'utf8')
  .replace('{{GH_REPO}}','').replace('{{GH_REF}}','main');
for(const protocol of ['http:','file:']){
  const links=[
    new Link({href:'notes/record.md#kept'}),
    new Link({href:'src/check.py#L8'}),
    new Link({href:'notes/'}),
    new Link({href:'data/result.json'}),
    new Link({href:'record.html#kept'}),
    new Link({href:'../../notes/record.md#kept','data-repo-path':'notes/record.md','data-repo-fragment':'kept'})
  ];
  const before=links.map(link=>({...link.attrs}));
  vm.runInNewContext(noRemoteScript,{location:{protocol,pathname:'/preview/index.html'},
    document:{querySelectorAll(selector){return selector==='a[href]'?links:[];}}});
  assert.deepEqual(links.map(link=>link.attrs),before);
  assert.ok(links.every(link=>link.title===undefined));
}
console.log('No-remote source links pass: HTTP/file exports preserve Markdown, Python, directory, JSON, HTML and source metadata paths.');

// With a remote, links the publication exporter pointed at their published copy
// keep that address: they carry data-repo-exported instead of data-repo-path.
const remoteScript=fs.readFileSync(path.join(root,'theme/components/filelinks.js'),'utf8')
  .replace('{{GH_REPO}}','https://github.com/example/project').replace('{{GH_REF}}','main');
for(const protocol of ['https:','file:']){
  const links=[
    new Link({href:'tools/fit.py','data-repo-exported':''}),
    new Link({href:'notes/record.md#kept','data-repo-exported':''}),
    new Link({href:'../../tools/other.py'})
  ];
  vm.runInNewContext(remoteScript,{location:{protocol,pathname:'/site/guide.html'},
    document:{querySelectorAll(selector){return selector==='a[href]'?links:[];}}});
  assert.equal(links[0].attrs.href,'tools/fit.py');
  assert.equal(links[1].attrs.href,'notes/record.md#kept');
  assert.equal(links[0].title,undefined);
  if(protocol==='https:') assert.equal(links[2].attrs.href,'https://github.com/example/project/blob/main/tools/other.py');
}
console.log('Exported source links pass: with a remote, exported Markdown and Python links keep their published address.');
