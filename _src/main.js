/* Lumen Clinic demo — interactions and animations (mirrors the Salient/WPBakery behaviour of the reference design). */
(function(){
  var $=function(s,c){return (c||document).querySelector(s)}, $$=function(s,c){return Array.prototype.slice.call((c||document).querySelectorAll(s))};
  var reduce=window.matchMedia&&window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var EASE='cubic-bezier(.25,1,.5,1)';

  /* ---------- Page transition: centre mask reveal (in) / cover (out) ---------- */
  var trans=$('.page-trans');
  function reveal(){ if(trans){ trans.classList.remove('cover'); trans.classList.add('open'); } }
  if(document.readyState==='complete') setTimeout(reveal,60); else window.addEventListener('load',function(){setTimeout(reveal,60)});
  setTimeout(reveal,1800); // safety: never leave the page covered
  window.addEventListener('pageshow',function(e){ if(e.persisted) reveal(); });
  document.addEventListener('click',function(e){
    var a=e.target.closest('a'); if(!a||!trans||reduce) return;
    var href=a.getAttribute('href')||'';
    if(a.hasAttribute('data-book')||a.target==='_blank'||e.metaKey||e.ctrlKey||e.shiftKey||href.charAt(0)==='#'||/^(mailto|tel|javascript):/.test(href)||!href) return;
    var url=new URL(a.href,location.href);
    if(url.origin!==location.origin) return;
    if(url.pathname===location.pathname&&url.hash){ return; }
    e.preventDefault(); trans.classList.remove('open'); trans.classList.add('cover');
    setTimeout(function(){ location.href=a.href; },650);
  });

  /* ---------- Header: transparent at top, solid once scrolled ---------- */
  var header=$('.site-header');
  function onScroll(){ if(header) header.classList.toggle('scrolled', window.scrollY>40); }
  window.addEventListener('scroll', onScroll, {passive:true}); onScroll();

  /* ---------- Off-canvas navigation ---------- */
  var side=$('.side'), scrim=$('.scrim'), menuToggle=$('.menu-toggle');
  var menuOpen=false, closeMenuButton=side && $('.close',side);
  var menuBackground=[header,$('main'),$('.site-footer'),$('.sr-only')].filter(Boolean);

  function menu(open, restoreFocus){
    if(!side || menuOpen===open) return;
    menuOpen=open;
    side.classList.toggle('open',open);
    scrim.classList.toggle('open',open);
    document.documentElement.classList.toggle('menu-open',open);
    menuToggle.setAttribute('aria-expanded',String(open));
    side.inert=!open;
    side.setAttribute('aria-hidden',String(!open));
    menuBackground.forEach(function(element){ element.inert=open; });
    if(open) closeMenuButton.focus();
    else if(restoreFocus!==false) menuToggle.focus();
  }

  if(menuToggle){
    menuToggle.addEventListener('click',function(){menu(!menuOpen);});
    closeMenuButton.addEventListener('click',function(){menu(false);});
    scrim.addEventListener('click',function(){menu(false);});
    side.addEventListener('click',function(event){
      var link=event.target.closest('a[href]');
      if(!link || link.hasAttribute('data-book') || event.metaKey || event.ctrlKey || event.shiftKey || event.altKey) return;
      menu(false);
    });
    side.addEventListener('keydown',function(event){
      if(event.key!=='Tab' || !menuOpen) return;
      var links=$$('a[href]',side), last=links[links.length-1];
      if(event.shiftKey && document.activeElement===closeMenuButton){
        event.preventDefault();
        last.focus();
      } else if(!event.shiftKey && document.activeElement===last){
        event.preventDefault();
        closeMenuButton.focus();
      }
    });
    window.addEventListener('pageshow',function(){menu(false);});
  }

  /* ---------- Booking pop-up ---------- */
  var modal=$('.modal');
  $$('[data-book]').forEach(function(a){ a.addEventListener('click',function(e){ e.preventDefault(); var fromMenu=menuOpen; menu(false,!fromMenu); modal.classList.add('open'); if(fromMenu) $('.x',modal).focus(); }); });
  if(modal){ modal.addEventListener('click',function(e){ if(e.target===modal||e.target.closest('.x')) modal.classList.remove('open'); }); }
  document.addEventListener('keydown',function(e){ if(e.key==='Escape'){ modal&&modal.classList.remove('open'); menu(false);} });

  /* ---------- Split headings: line reveal by word ---------- */
  function splitEl(el){
    if(el.dataset.splitDone) return; el.dataset.splitDone='1';
    var nodes=Array.prototype.slice.call(el.childNodes);
    nodes.forEach(function(n){
      if(n.nodeType===3){
        var frag=document.createDocumentFragment();
        n.textContent.split(/(\s+)/).forEach(function(part){
          if(!part) return;
          if(/^\s+$/.test(part)){ frag.appendChild(document.createTextNode(' ')); return; }
          var w=document.createElement('span'); w.className='sw';
          var i=document.createElement('span'); i.className='si'; i.textContent=part; w.appendChild(i); frag.appendChild(w);
        });
        n.parentNode.replaceChild(frag,n);
      } else if(n.nodeType===1 && n.tagName!=='BR' && !n.classList.contains('rotator') && !n.classList.contains('rw')){
        splitEl(n);
      }
    });
    el.classList.add('split-ready');
  }
  var splitTargets=$$('main .t-hero, main .t-xl, main .t-lg, main .t-md, main [data-split]').filter(function(el){ return !el.closest('.btn')&&!el.closest('.rw-title')&&!el.classList.contains('no-split')&&!el.hasAttribute('data-anim'); });
  splitTargets.forEach(splitEl);

  /* ---------- Entrance animations (fade-in-from-bottom/left/right, fade-in, grow-in) ---------- */
  $$('.reveal').forEach(function(el){ if(!el.hasAttribute('data-anim')) el.setAttribute('data-anim','fade-in-from-bottom'); });
  var animated=$$('[data-anim]').concat(splitTargets);
  function play(el){
    if(el.classList.contains('split-ready')){
      // Reveal line by line (words on the same line move together), like Salient's "line reveal by space".
      var wrapDelay=+(el.getAttribute('data-delay')||0), line=-1, lastTop=null;
      $$('.sw',el).forEach(function(w){ var t=w.offsetTop; if(lastTop===null||Math.abs(t-lastTop)>4){ line++; lastTop=t; } w.firstChild.style.transitionDelay=(wrapDelay+line*90)+'ms'; });
    } else if(el.hasAttribute('data-delay')){ el.style.transitionDelay=el.getAttribute('data-delay')+'ms'; }
    el.classList.add('in');
  }
  if('IntersectionObserver' in window && !reduce){
    var io=new IntersectionObserver(function(es){ es.forEach(function(e){ if(e.isIntersecting){ play(e.target); io.unobserve(e.target);} }); },{rootMargin:'0px 0px -8% 0px',threshold:0});
    animated.forEach(function(el){io.observe(el)});
  } else animated.forEach(play);

  /* ---------- Rotating words (horizontal slide, Salient "rotating words title") ---------- */
  $$('.rw').forEach(function(box){
    var words=$$('.rw-w',box), i=0, rot=+(box.getAttribute('data-rotation')||2000), delay=+(box.getAttribute('data-delay')||0);
    if(words.length<2) return;
    function size(){ box.style.width=words[i].offsetWidth+'px'; }
    words.forEach(function(w,k){ w.classList.toggle('on',k===0); }); size();
    window.addEventListener('resize',size);
    setTimeout(function loop(){
      var cur=words[i]; i=(i+1)%words.length; var nxt=words[i];
      cur.classList.remove('on'); cur.classList.add('out');
      nxt.classList.remove('out'); nxt.classList.add('pre'); void nxt.offsetWidth; nxt.classList.remove('pre'); nxt.classList.add('on');
      size(); setTimeout(function(){ cur.classList.remove('out'); },850);
      setTimeout(loop,rot);
    },rot+delay);
  });

  /* ---------- Treatment lists: hovering the list hides the default image; each item reveals its own ---------- */
  $$('.treat').forEach(function(t){
    var list=$('.list',t), links=$$('.list a',t), imgs=$$('.media .ph',t), def=imgs[imgs.length-1];
    function show(i){ imgs.forEach(function(p,k){ p.classList.toggle('on',k===i); }); }
    list.addEventListener('mouseenter',function(){ show(-1); });
    list.addEventListener('mouseleave',function(){ show(imgs.length-1); });
    links.forEach(function(l,i){ l.addEventListener('mouseenter',function(){show(i)}); l.addEventListener('mouseleave',function(){show(-1)}); l.addEventListener('focus',function(){show(i)}); });
  });

  /* ---------- Simple slider (drag / swipe, no arrows or dots) ---------- */
  $$('.simple-slider').forEach(function(sl){
    var track=$('.ss-track',sl), cells=$$('.ss-cell',sl), i=0, x0=null, dx=0;
    function go(k){ i=Math.max(0,Math.min(cells.length-1,k)); track.style.transition='transform .8s '+EASE; track.style.transform='translateX('+(-i*100)+'%)'; }
    sl.addEventListener('pointerdown',function(e){ x0=e.clientX; dx=0; track.style.transition='none'; sl.setPointerCapture(e.pointerId); });
    sl.addEventListener('pointermove',function(e){ if(x0===null) return; dx=e.clientX-x0; track.style.transform='translateX(calc('+(-i*100)+'% + '+dx+'px))'; });
    function end(){ if(x0===null) return; var w=sl.clientWidth; go(dx<-w*0.15?i+1:dx>w*0.15?i-1:i); x0=null; }
    sl.addEventListener('pointerup',end); sl.addEventListener('pointercancel',end);
  });

  /* ---------- Scroll-linked tabs with moving line (Salient "scrolling tabs") ---------- */
  function scrollTabs(root, tabSel, blockSel){
    var tabs=$$(tabSel,root), blocks=$$(blockSel,root), line=$('.tab-line',root);
    function setActive(i){
      tabs.forEach(function(t,k){t.classList.toggle('on',k===i)});
      if(line&&tabs[i]){ line.style.transform='translateY('+tabs[i].offsetTop+'px)'; line.style.height=tabs[i].offsetHeight+'px'; }
    }
    tabs.forEach(function(t,k){ t.addEventListener('click',function(e){ e.preventDefault(); var y=blocks[k].getBoundingClientRect().top+window.scrollY-140; window.scrollTo({top:y,behavior:'smooth'}); }); });
    function check(){ var mid=window.innerHeight*0.45, act=0; blocks.forEach(function(b,k){ if(b.getBoundingClientRect().top<mid) act=k; }); setActive(act); }
    window.addEventListener('scroll',check,{passive:true}); window.addEventListener('resize',check); setTimeout(check,50);
  }
  $$('[data-steps]').forEach(function(s){ scrollTabs(s,'.tab','.step-body'); });
  $$('[data-tlist]').forEach(function(s){ scrollTabs(s,'.nav-side a','.tblock'); });
  $$('[data-detail]').forEach(function(s){
    var cards=$$('.dcard',s), count=$('.count',s), title=$('.stick h3',s), text=$('.stick p',s), cur=-1;
    function check(){ var mid=window.innerHeight*0.5, act=0; cards.forEach(function(c,k){ if(c.getBoundingClientRect().top<mid) act=k; });
      if(act===cur) return; cur=act; var c=cards[act];
      [title,text].forEach(function(e){e.style.opacity=0});
      setTimeout(function(){ count.textContent=(act+1)+' / '+cards.length; title.textContent=c.getAttribute('data-word'); text.textContent=c.getAttribute('data-text'); [title,text].forEach(function(e){e.style.opacity=1}); },250);
    }
    window.addEventListener('scroll',check,{passive:true}); setTimeout(check,50);
  });

  /* ---------- Parallax & scroll movement ---------- */
  var movers=$$('[data-scrollmove]'), bgs=$$('[data-parallax]');
  function frame(){
    var y=window.scrollY, vh=window.innerHeight;
    movers.forEach(function(el){ var k=+el.getAttribute('data-scrollmove'); var r=el.parentElement.getBoundingClientRect(); var off=el.hasAttribute('data-fromtop')?y:(vh/2-(r.top+r.height/2)); el.style.transform='translate3d(0,'+(-off*k).toFixed(1)+'px,0)'; });
    bgs.forEach(function(el){ var k=+el.getAttribute('data-parallax'); var r=el.parentElement.getBoundingClientRect(); if(r.bottom<0||r.top>vh) return; el.style.transform='translate3d(0,'+(-r.top*k).toFixed(1)+'px,0)'; });
    ticking=false;
  }
  var ticking=false;
  if(!reduce&&(movers.length||bgs.length)){ window.addEventListener('scroll',function(){ if(!ticking){ ticking=true; requestAnimationFrame(frame);} },{passive:true}); frame(); }

  /* ---------- Clip-path background reveal (video band) ---------- */
  if('IntersectionObserver' in window){
    var co=new IntersectionObserver(function(es){ es.forEach(function(e){ if(e.isIntersecting){ e.target.classList.add('clip-in'); co.unobserve(e.target);} }); },{threshold:.15});
    $$('.clip-reveal').forEach(function(el){co.observe(el)});
  } else $$('.clip-reveal').forEach(function(el){el.classList.add('clip-in')});

  /* ---------- Milestone counters ---------- */
  function countUp(el){
    var end=+el.getAttribute('data-count'), dur=2000, t0=null, fmt=function(n){return n.toLocaleString('en-US')};
    (function step(t){ if(!t0) t0=t; var p=Math.min(1,(t-t0)/dur), e=1-Math.pow(1-p,4); el.textContent=fmt(Math.round(end*e)); if(p<1) requestAnimationFrame(step); })(performance.now());
  }
  if('IntersectionObserver' in window){
    var mo=new IntersectionObserver(function(es){ es.forEach(function(e){ if(e.isIntersecting){ countUp(e.target); mo.unobserve(e.target);} }); },{threshold:.5});
    $$('[data-count]').forEach(function(el){ el.textContent='0'; mo.observe(el); });
  }

  /* ---------- Testimonial slider (arrows + drag) ---------- */
  $$('.carousel').forEach(function(c){
    var track=$('.track',c), items=$$('.review',c), i=Math.min(1,items.length-1), x0=null, dx=0;
    function go(k){ i=(k+items.length)%items.length; items.forEach(function(r,j){r.classList.toggle('on',j===i)});
      var it=items[i]; var off=it.offsetLeft-(c.clientWidth-it.offsetWidth)/2; track.style.transition='transform .6s '+EASE; track.style.transform='translateX('+(-off)+'px)'; }
    $$('[data-prev]',c).forEach(function(b){b.addEventListener('click',function(){go(i-1)})});
    $$('[data-next]',c).forEach(function(b){b.addEventListener('click',function(){go(i+1)})});
    items.forEach(function(r,j){ r.addEventListener('click',function(){ if(Math.abs(dx)<5) go(j); }); });
    track.addEventListener('pointerdown',function(e){ x0=e.clientX; dx=0; });
    window.addEventListener('pointerup',function(){ if(x0===null) return; if(dx<-60) go(i+1); else if(dx>60) go(i-1); x0=null; });
    window.addEventListener('pointermove',function(e){ if(x0!==null) dx=e.clientX-x0; });
    window.addEventListener('resize',function(){go(i)}); setTimeout(function(){go(i)},50);
  });

  /* ---------- FAQ accordion: one open at a time, animated height ---------- */
  $$('.acc').forEach(function(acc){
    $$('details',acc).forEach(function(d){
      var sum=$('summary',d), body=$('.ans',d);
      sum.addEventListener('click',function(e){
        e.preventDefault();
        var opening=!d.open;
        $$('details[open]',acc).forEach(function(o){ if(o!==d) close(o); });
        if(opening){ d.open=true; var h=body.scrollHeight; body.style.maxHeight='0px'; void body.offsetHeight; body.style.maxHeight=h+'px'; d.classList.add('is-open'); }
        else close(d);
      });
    });
    function close(o){ var b=$('.ans',o); b.style.maxHeight=b.scrollHeight+'px'; void b.offsetHeight; b.style.maxHeight='0px'; o.classList.remove('is-open'); setTimeout(function(){ o.open=false; },480); }
  });

  /* ---------- Map (Leaflet + OpenStreetMap when available, styled placeholder otherwise) ---------- */
  $$('[data-map]').forEach(function(el){
    var ll=el.getAttribute('data-map').split(',').map(Number);
    var s=document.createElement('script'); s.src='https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/leaflet.min.js';
    var l=document.createElement('link'); l.rel='stylesheet'; l.href='https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/leaflet.min.css';
    s.onload=function(){
      try{
        var holder=$('.map-canvas',el);
        var map=L.map(holder,{scrollWheelZoom:false,zoomControl:true,attributionControl:true}).setView(ll,15);
        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',{maxZoom:19,attribution:'&copy; OpenStreetMap'}).on('tileload',function(){el.classList.add('has-tiles')}).addTo(map);
        L.circleMarker(ll,{radius:9,color:'#011126',weight:6,opacity:.15,fillColor:'#011126',fillOpacity:1}).addTo(map);
      }catch(err){}
    };
    document.head.appendChild(l); document.head.appendChild(s);
  });
})();
