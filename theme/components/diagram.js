// Diagram tools on every .diagram-wrap: zoom (buttons / Ctrl+scroll / pinch),
// drag-pan, freehand draw layer, fullscreen.
(function(){
  var SVGNS = 'http://www.w3.org/2000/svg';
  document.querySelectorAll('.diagram-wrap').forEach(function(w){
    var svg = w.querySelector('svg');
    if (!svg) return;
    var drawLayer = document.createElementNS(SVGNS, 'g');
    svg.appendChild(drawLayer);

    var zoom = 1, baseW = 0, drawMode = false;

    function setZoom(z, cx, cy){
      z = Math.max(0.35, Math.min(4, z));
      if (!baseW) baseW = svg.getBoundingClientRect().width / zoom;
      if (cx === undefined){ cx = w.clientWidth / 2; cy = w.clientHeight / 2; }
      var px = (w.scrollLeft + cx) / zoom, py = (w.scrollTop + cy) / zoom;
      zoom = z;
      if (z === 1){
        svg.style.width = ''; svg.style.minWidth = ''; svg.style.maxWidth = '';
        baseW = 0;
      } else {
        svg.style.width = (baseW * zoom) + 'px';
        svg.style.minWidth = '0';
        svg.style.maxWidth = 'none';
      }
      w.scrollLeft = px * zoom - cx;
      w.scrollTop = py * zoom - cy;
    }

    var tools = document.createElement('div');
    tools.className = 'dia-tools';
    function btn(txt, title, fn){
      var b = document.createElement('button');
      b.textContent = txt; b.title = title;
      b.addEventListener('click', fn);
      tools.appendChild(b);
      return b;
    }
    btn('−', 'Zoom out', function(){ setZoom(zoom / 1.25); });
    btn('+', 'Zoom in (or Ctrl+scroll / pinch)', function(){ setZoom(zoom * 1.25); });
    btn('1:1', 'Reset zoom', function(){ setZoom(1); });
    var drawBtn = btn('✏ draw', 'Toggle draw mode — drag to sketch on the diagram', function(){
      drawMode = !drawMode;
      drawBtn.classList.toggle('on', drawMode);
      w.classList.toggle('drawing', drawMode);
    });
    btn('🗑', 'Clear drawings', function(){
      while (drawLayer.firstChild) drawLayer.removeChild(drawLayer.firstChild);
    });
    var fsBtn = btn('⛶', 'Toggle fullscreen (Esc to exit)', function(){
      if (document.fullscreenElement) document.exitFullscreen();
      else w.requestFullscreen();
    });
    document.addEventListener('fullscreenchange', function(){
      fsBtn.textContent = document.fullscreenElement === w ? '✕' : '⛶';
    });
    w.appendChild(tools);

    // Ctrl+scroll / pinch zoom anchored at the cursor.
    w.addEventListener('wheel', function(ev){
      if (!ev.ctrlKey) return;
      ev.preventDefault();
      var r = w.getBoundingClientRect();
      setZoom(zoom * (ev.deltaY < 0 ? 1.15 : 1 / 1.15), ev.clientX - r.left, ev.clientY - r.top);
    }, { passive: false });

    function vbPoint(ev){
      var p = new DOMPoint(ev.clientX, ev.clientY).matrixTransform(svg.getScreenCTM().inverse());
      return p.x.toFixed(1) + ',' + p.y.toFixed(1);
    }
    var pan = null, stroke = null;
    w.addEventListener('mousedown', function(ev){
      if (ev.button !== 0 || ev.target.closest('.dia-tools')) return;
      ev.preventDefault();
      if (drawMode){
        stroke = document.createElementNS(SVGNS, 'polyline');
        stroke.setAttribute('class', 'draw-stroke');
        stroke.setAttribute('points', vbPoint(ev));
        drawLayer.appendChild(stroke);
      } else {
        // Drag: pan the scroll container.
        pan = { x: ev.clientX, y: ev.clientY, sl: w.scrollLeft, st: w.scrollTop };
        w.classList.add('panning');
      }
    });
    window.addEventListener('mousemove', function(ev){
      if (stroke){
        stroke.setAttribute('points', stroke.getAttribute('points') + ' ' + vbPoint(ev));
      } else if (pan){
        w.scrollLeft = pan.sl - (ev.clientX - pan.x);
        w.scrollTop = pan.st - (ev.clientY - pan.y);
      }
    });
    window.addEventListener('mouseup', function(){
      if (stroke && stroke.getAttribute('points').indexOf(' ') === -1) drawLayer.removeChild(stroke);
      stroke = null; pan = null;
      w.classList.remove('panning');
    });
  });
})();
