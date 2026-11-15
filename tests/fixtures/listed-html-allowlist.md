# Allowlist

Every admitted tag with every admitted attribute:

<div id="d" title="t" align="center">
<p id="p" title="t" align="left">p <a id="a" title="t" align="left" href="target.md" name="n">a</a> <abbr id="ab" title="t" align="left">ab</abbr> <b id="b" title="t" align="left">b</b> <br id="br" title="t" align="left"> <code id="c" title="t" align="left">c</code> <del id="del" title="t" align="left">del</del> <em id="em" title="t" align="left">em</em> <i id="i" title="t" align="left">i</i> <ins id="ins" title="t" align="left">ins</ins> <kbd id="k" title="t" align="left">k</kbd> <mark id="m" title="t" align="left">m</mark> <s id="s" title="t" align="left">s</s> <small id="sm" title="t" align="left">sm</small> <span id="sp" title="t" align="left">sp</span> <strong id="st" title="t" align="left">st</strong> <sub id="sub" title="t" align="left">sub</sub> <sup id="sup" title="t" align="left">sup</sup> <u id="u" title="t" align="left">u</u> <img id="img" title="t" align="right" src="media/x.png" alt="x" width="10" height="20"></p>
<h1 id="h1" title="t" align="center">h1</h1>
<h2 id="h2" title="t" align="center">h2</h2>
<h3 id="h3" title="t" align="center">h3</h3>
<h4 id="h4" title="t" align="center">h4</h4>
<h5 id="h5" title="t" align="center">h5</h5>
<h6 id="h6" title="t" align="center">h6</h6>
<hr id="hr" title="t" align="center">
<blockquote id="q" title="t" align="left">q</blockquote>
<pre id="pre" title="t" align="left">pre</pre>
<details id="det" title="t" align="left" open><summary id="sum" title="t" align="left">summary</summary>body</details>
<ul id="ul" title="t" align="left"><li id="li" title="t" align="left">li</li></ul>
<ol id="ol" title="t" align="left"><li>ol</li></ol>
<dl id="dl" title="t" align="left"><dt id="dt" title="t" align="left">dt</dt><dd id="dd" title="t" align="left">dd</dd></dl>
<table id="tab" title="t" align="center" width="50%"><caption id="cap" title="t" align="top">cap</caption><thead id="th0" title="t" align="left"><tr id="tr" title="t" align="left"><th id="th" title="t" align="left" colspan="2" rowspan="1" width="9">th</th></tr></thead><tbody id="tb" title="t" align="left"><tr><td id="td" title="t" align="right" colspan="1" rowspan="2" width="8">td</td></tr></tbody><tfoot id="tf" title="t" align="left"><tr><td>tf</td></tr></tfoot></table>
</div>

Tags outside the allowlist show as text:

<script src="x.js">alert(1)</script>
<style>p { color: red }</style>
<iframe src="x.html"></iframe> <object data="x"></object> <embed src="x"> <link rel="stylesheet" href="x.css">
<meta http-equiv="refresh" content="0"> <base href="https://example.com/">
<svg><use href="#x"/></svg> <math><mi>x</mi></math> <image src="x.png">
<video src="x.mp4" poster="x.png"></video> <audio src="x.mp3"></audio> <source src="x"> <picture></picture>
<form action="x"><input type="image" src="x"><button formaction="x">b</button><textarea>t</textarea></form>
<template>t</template> <noscript>n</noscript> <center>c</center> <font color="red">f</font>

Attributes outside the allowlist are removed:

<p class="c" style="color: red" data-x="1" onclick="alert(1)" lang="en" dir="rtl" hidden role="note" aria-label="l" tabindex="0">p</p>
<img src="media/x.png" srcset="x.png 2x" lowsrc="x.png" longdesc="x" usemap="#m" ismap loading="lazy" crossorigin referrerpolicy="no-referrer" onerror="alert(1)">
<a href="target.md" target="_blank" rel="opener" ping="x" download type="text/html" referrerpolicy="unsafe-url">a</a>
<blockquote cite="https://example.com/">q</blockquote> <td background="x.png">cell</td> <details open ontoggle="alert(1)">d</details>
<img src="media/x.png" href="x" poster="x"> <a src="x" xlink:href="x" formaction="x">a</a>
