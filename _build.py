#!/usr/bin/env python3
"""Generates the Lumen Clinic demo site (8 pages) into dist/."""
import os, shutil, html

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, "dist")

BRAND = "Lumen Clinic"
ADDRESS = "12 Rue de l’Exemple, 75008 Paris"
PHONE = "01 00 00 00 00"

ICON = {
 "pin": '<svg viewBox="0 0 24 24"><path d="M12 21s-7-6.2-7-11.5A7 7 0 0 1 19 9.5C19 14.8 12 21 12 21z"/><circle cx="12" cy="9.5" r="2.5"/></svg>',
 "phone": '<svg viewBox="0 0 24 24"><path d="M5 3h4l2 5-2.5 1.5a11 11 0 0 0 6 6L16 13l5 2v4a2 2 0 0 1-2 2A16 16 0 0 1 3 5a2 2 0 0 1 2-2z"/></svg>',
 "user": '<svg viewBox="0 0 24 24"><circle cx="12" cy="8" r="4"/><path d="M4 21c1.5-4 4.5-6 8-6s6.5 2 8 6"/></svg>',
 "ig": '<svg viewBox="0 0 24 24"><rect x="3" y="3" width="18" height="18" rx="5"/><circle cx="12" cy="12" r="4"/><circle cx="17.5" cy="6.5" r=".8"/></svg>',
 "chev": '<svg class="chev" viewBox="0 0 24 24"><path d="M5 9l7 7 7-7"/></svg>',
 "cal": '<svg viewBox="0 0 24 24"><rect x="3" y="5" width="18" height="16" rx="1"/><path d="M3 10h18M8 3v4M16 3v4M7 14h2M11 14h2M15 14h2M7 17h2M11 17h2"/></svg>',
 "chair": '<svg viewBox="0 0 24 24"><path d="M5 12h9l3-6h2l-3 8H6zM8 14v6M14 14v6M4 20h14"/></svg>',
 "scan": '<svg viewBox="0 0 24 24"><rect x="6" y="3" width="12" height="18" rx="2"/><path d="M9 8h6M9 12h6M10 16h4"/></svg>',
 "lab": '<svg viewBox="0 0 24 24"><circle cx="10" cy="10" r="6"/><path d="M14.5 14.5L21 21"/></svg>',
 "steam": '<svg viewBox="0 0 24 24"><path d="M4 14h16v6H4zM8 14c0-3 2-3 2-6M12 14c0-3 2-3 2-6M16 14c0-3 2-3 2-6"/></svg>',
 "drop": '<svg viewBox="0 0 24 24"><path d="M12 3s6 7 6 11a6 6 0 0 1-12 0c0-4 6-11 6-11z"/></svg>',
 "clock": '<svg viewBox="0 0 24 24"><circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/></svg>',
 "book": '<svg viewBox="0 0 24 24"><path d="M3 5h7a2 2 0 0 1 2 2v12a2 2 0 0 0-2-2H3zM21 5h-7a2 2 0 0 0-2 2v12a2 2 0 0 1 2-2h7z"/></svg>',
 "news": '<svg viewBox="0 0 24 24"><rect x="3" y="4" width="18" height="16"/><path d="M7 8h5v4H7zM14 8h3M14 11h3M7 15h10"/></svg>',
 "people": '<svg viewBox="0 0 24 24"><circle cx="8" cy="9" r="3"/><circle cx="16" cy="9" r="3"/><path d="M2 20c1-3 3.5-5 6-5s5 2 6 5M10 20c1-3 3.5-5 6-5s5 2 6 5"/></svg>',
}

NAV = [
 ("Home", "", None),
 ("The Clinic", "the-clinic/", None),
 ("Our Concept", "our-concept/", None),
 ("Our Treatments", "our-treatments/", [("Orthodontics","orthodontics/"),("Aesthetics","aesthetics/"),("Regenerating","regenerating/")]),
 ("Academy", "academy/", [("Research","academy/#research"),("Publications","academy/#publications"),("Journal","academy/#journal"),("FAQ","academy/#faq")]),
]

def e(s): return html.escape(s, quote=True)

PHOTOS = {
    "interior": ("clinic-interior.webp", "Light-filled clinic reception with an oak desk"),
    "treatment": ("clinic-treatment.webp", "Bright orthodontic treatment suite with a dental chair"),
    "consultation": ("clinic-consultation.webp", "Illustration of an orthodontic consultation"),
}
PHOTO_VARIANTS = {
    "v1": "interior", "v2": "treatment", "v3": "treatment",
    "v4": "consultation", "v5": "consultation", "v6": "interior",
}

def photo(P, key, *, eager=False, decorative=False):
    file, alt = PHOTOS[key]
    loading = 'loading="eager" fetchpriority="high"' if eager else 'loading="lazy"'
    return f'<img src="{P}assets/media/{file}" alt="{e("" if decorative else alt)}" {loading} decoding="async">'

def ph(P, cls="v1", style="", extra=""):
    key = PHOTO_VARIANTS.get(cls.split()[0])
    if key is None:
        return f'<div class="ph {cls}" style="{style}" aria-hidden="true"{extra}></div>'
    return f'<div class="ph noicon {cls}" style="{style}"{extra}>{photo(P, key)}</div>'

def hero_photo(P, key, cls="", extra="", eager=False):
    return f'<div class="vid has-photo {cls}" aria-hidden="true"{extra}>{photo(P, key, eager=eager, decorative=True)}</div>'

def btn(label, href="#", side="", light=False, book=False):
    cls = "btn" + (" r" if side == "r" else "") + (" light" if light else "")
    data = ' data-book' if book else ''
    return f'<a class="{cls}" href="{href}"{data}>{e(label)}</a>'

def header(P, current, dark=False):
    items = []
    for label, href, sub in NAV:
        cur = ' class="current"' if href == current else ''
        chev = ICON["chev"] if sub else ''
        subhtml = ''
        if sub:
            subhtml = '<ul class="sub">' + ''.join(f'<li><a href="{P}{h}">{e(l)}</a></li>' for l, h in sub) + '</ul>'
        items.append(f'<li{cur}><a href="{P}{href}">{e(label)}{chev}</a>{subhtml}</li>')
    items.append(f'<li><a href="#" data-book>{ICON["cal"]}Make an appointment</a></li>')
    side = []
    for label, href, sub in NAV:
        current_page = ' aria-current="page"' if href == current else ''
        sublinks = ''
        if sub:
            sublinks = '<div class="subl">' + ''.join(f'<a href="{P}{h}">{e(l)}</a>' for l, h in sub) + '</div>'
        side.append(f'<div class="side-group"><a href="{P}{href}"{current_page}>{e(label)}</a>{sublinks}</div>')
    side.append('<div class="side-group"><a href="#" data-book>Make an appointment</a></div>')
    return f'''
<a class="sr-only" href="#main">Skip to content</a>
<header class="site-header{' dark-text' if dark else ''}">
  <div class="inner">
    <a class="logo" href="{P}" aria-label="{BRAND} — home"><span class="w1">LUMEN</span><span class="w2">CLINIC</span></a>
    <div class="right">
      <div class="topbar">
        <a href="#">{ICON["pin"]}{e(ADDRESS)}</a>
        <a href="#">{ICON["phone"]}{PHONE}</a>
        <a href="#">{ICON["user"]}Patient login</a>
        <a class="lang" href="#">Français</a>
        <a class="ig" href="#" aria-label="Instagram">{ICON["ig"]}</a>
      </div>
      <nav class="nav" aria-label="Main"><ul>{''.join(items)}</ul></nav>
    </div>
    <button class="menu-toggle" type="button" aria-controls="clinic-menu" aria-expanded="false"><span class="menu-lines" aria-hidden="true"></span>Menu</button>
  </div>
</header>
<div class="scrim" aria-hidden="true"></div>
<aside class="side" id="clinic-menu" role="dialog" aria-modal="true" aria-label="Navigation menu" aria-hidden="true" inert><button class="close" type="button" aria-label="Close menu">×</button><nav aria-label="Main navigation">{''.join(side)}</nav></aside>'''

def footer(P):
    return f'''
<footer class="site-footer">
  <div class="foot-grid" data-anim="fade-in">
    <div><div class="mark ghost">L</div><h6 style="margin-top:28px">Visit us</h6><address>{BRAND}<br>{e(ADDRESS).replace(', ', '<br>')}<br>{PHONE}</address></div>
    <div><div class="sub-mark"><b>LUMEN</b><i>CONCEPT</i></div><h6>Our story</h6><a href="{P}the-clinic/">The Clinic</a><a href="{P}the-clinic/#team">The Team</a></div>
    <div><div class="sub-mark"><b>LUMEN</b><i>CARE</i></div><h6>Our technology</h6><a href="{P}orthodontics/">Orthodontics</a><a href="{P}aesthetics/">Aesthetics</a><a href="{P}regenerating/">Regeneration</a></div>
    <div><div class="sub-mark"><b>LUMEN</b><i>ACADEMY</i></div><h6>Research</h6><a href="{P}academy/#research">Conferences</a><a href="{P}academy/#publications">Articles</a><a href="{P}academy/#faq">FAQ</a></div>
    <div class="foot-legal"><h6>Legal information</h6><a href="#">Privacy policy</a><a href="#">Legal notice</a></div>
    <div class="foot-legal"><h6>Client experience</h6><a href="#">Patient space</a><a href="#" data-book>New patient</a></div>
  </div>
  <div class="foot-bottom"><span>© {BRAND} — demo website, fictional clinic and illustrative imagery.</span><span>Website by Deux Rives Web</span></div>
</footer>
<div class="modal" role="dialog" aria-modal="true" aria-label="Book an appointment"><div class="card"><button class="x" type="button" aria-label="Close">×</button>
  <h3>In need of an appointment?</h3><p>Book online in a few clicks, or call the clinic and our team will find a slot with you.</p>
  <div class="btn-row">{btn("Book online", "#")}{btn("Call " + PHONE, "#", "r")}</div></div></div>
<script src="{P}assets/main.js"></script>'''

def page(path, title, desc, body, current, dark=False):
    P = "../" if path else ""
    doc = f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)} — {BRAND}</title>
<meta name="description" content="{e(desc)}">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@500&family=Inter:wght@400;500;600&family=Lato:wght@400;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{P}assets/style.css">
<noscript><style>.page-trans{{display:none}}[data-anim],.reveal{{opacity:1!important;transform:none!important}}</style></noscript>
</head>
<body>
<div class="page-trans" aria-hidden="true"></div>
{header(P, current, dark)}
<main id="main">
{body(P)}
</main>
{footer(P)}
</body>
</html>
'''
    full = os.path.join(OUT, path, "index.html") if path else os.path.join(OUT, "index.html")
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w", encoding="utf-8") as f:
        f.write(doc)

# ---------------------------------------------------------------- HOME
def home(P):
    treat = [
        ("Orthodontic treatments", "orthodontics/", ["External braces", "Internal braces", "Clear aligners", "Orthodontics for children"], False, ""),
        ("Aesthetic treatments", "aesthetics/", ["Gummy smile correction", "Smile symmetry", "Smile brightening"], True, " round"),
        ("Regenerating treatments", "regenerating/", ["Smile ageing prevention", "Volume loss prevention", "Lines around the mouth"], False, ""),
    ]
    blocks = []
    variants = ["v1", "v2", "v3", "v4", "v5", "v6"]
    for n, (title, href, items, flip, media_cls) in enumerate(treat):
        links = ''.join(f'<a href="{P}{href}">{e(i)}</a>' for i in items)
        imgs = ''.join(ph(P, variants[(n + k) % 6] + (" on" if k == len(items) else "")) for k in range(len(items) + 1))
        blocks.append(f'''<section class="treat{' flip' if flip else ''}" data-anim="fade-in-from-left" data-delay="300">
  <div class="txt"><a href="{P}{href}"><h2 class="t-xl">{e(title).replace(' ', '<br>', 1)}</h2></a><div class="list">{links}</div></div>
  <div class="media{media_cls}">{imgs}</div>
</section>''')
        if n < 2:
            blocks.append('<div class="rule"></div>')
    return f'''
<section class="hero">
  {hero_photo(P, "interior", eager=True)}
  <div class="content hero-split" data-scrollmove="0.1" data-fromtop><h1 class="t-hero">A confident<br>smile</h1><h1 class="t-hero">for every<br>stage of life</h1></div>
  <div class="hero-actions">{btn("Appointment", "#", light=True, book=True)}{btn("About us", P+"the-clinic/", "r", light=True)}</div>
</section>

<section class="intro">
  <div class="monogram" aria-hidden="true" data-scrollmove="0.12">L</div>
  <div class="copy">
    <h2 class="rw-title"><span class="rw" data-rotation="2000"><span class="rw-w">Orthodontics</span><span class="rw-w">Aesthetics</span><span class="rw-w">Regeneration</span></span></h2>
    <h4 data-split>Your smile is part of every important moment. Our team designs each treatment around your face, your habits and the result you are hoping for.</h4>
    {btn("Our concept", P+"our-concept/", "r")}
  </div>
</section>

<section class="clinic-split">
  <div class="simple-slider" aria-label="Clinic photos — drag to browse"><div class="ss-track">{''.join('<div class="ss-cell">'+ph(P, v)+'</div>' for v in ("v6","v3","v5"))}</div></div>
  <div class="txt"><h2 class="t-xl">The clinic</h2><h4 data-split>A calm, light-filled practice in the heart of the city, easy to reach by public transport and designed so every visit feels unhurried.</h4>{btn("Visit us", P+"the-clinic/#visit")}</div>
</section>

{''.join(blocks)}

<section class="quote-sec">
  <div class="zoom-wrap" data-anim="fade-in">{ph(P, "v5")}</div>
  <div data-anim="fade-in">
    <blockquote>“Our team brings together specialists who share one conviction: an accurate diagnosis comes first. Every plan we propose draws on current research and modern equipment, so each patient receives care that is both healthy and beautiful.”</blockquote>
    <div class="who"><span class="t-sm">Dr Claire Martin</span><span class="t-xs">Head of clinic</span></div>
    <h3 data-split>Read more</h3>
    <div class="btn-grid">{btn("Lumen Academy", P+"academy/")}{btn("Publications", P+"academy/#publications")}{btn("Research", P+"academy/#research")}{btn("FAQ", P+"academy/#faq")}</div>
  </div>
</section>

<section class="band-video clip-reveal">{hero_photo(P, "interior", "warm shade")}{btn("Come visit us", P+"the-clinic/#visit", "r", light=True)}</section>

<section class="cta-row">
  <p data-split>Ready to change your smile? We look at every smile as a balance between aesthetics, oral health and function. Book your first appointment and we will guide you towards a harmonious result, built to last and adapted to your daily life.</p>
  {btn("Patient login", "#", "r")}{btn("New patient", "#", "r", book=True)}
</section>'''

# ---------------------------------------------------------------- THE CLINIC
def clinic(P):
    rooms = [("chair", "4 modern treatment rooms"), ("scan", "Integrated imaging area"), ("lab", "On-site laboratory"), ("steam", "Sterilisation area"), ("drop", "Dedicated hygiene room")]
    descs = ["Calm, bright rooms designed for comfort.", "For instant diagnosis and maximum precision.", "Custom appliances made on site.", "Strict protocols for complete safety.", "A room reserved for professional cleaning."]
    cards = ''.join(f'<div class="room" data-anim="fade-in-from-bottom" data-delay="{k*100}">{ph(P, v)}<span class="lbl">{ICON[i]}<span class="t-sm" style="display:block">{e(t)}</span><span class="desc">{e(d)}</span></span></div>' for k, ((i, t), v, d) in enumerate(zip(rooms, ["v2", "v4", "v5", "v2", "v1"], descs)))
    people = [("Dr Claire Martin", "Head of clinic"), ("Sophie", "Coordinator"), ("Inès", "Dental assistant"), ("Laura", "Dental assistant")]
    team = ''.join(f'<div data-anim="fade-in-from-right" data-delay="{k*100}">{ph(P, "person")}<h4>{e(n)}</h4><div class="role">{e(r)}</div></div>' for k, (n, r) in enumerate(people))
    return f'''
<section class="hero hero-center">{hero_photo(P, "treatment", "dark", eager=True)}
  <div class="content"><h1 class="t-hero no-split" style="font-size:48px" data-anim="fade-in-from-bottom">The clinic</h1><p data-anim="fade-in-from-bottom" data-delay="100">Innovation, precision and care: the three pillars of our practice.</p></div>
</section>

<section class="sec bg-fade">
  <div class="two-col"><h2 class="t-lg">The practice</h2><p data-anim="fade-in-from-bottom">Located in the heart of the city, the clinic is easy to reach by public transport. We welcome you in an elegant, quiet space designed for your comfort. Opening hours are flexible to fit your schedule, and our team is always available to answer your questions.</p></div>
  <div class="cards5">{cards}</div>
</section>

<section class="tech bg-cream">
  <div data-anim="fade-in-from-right"><h2 class="t-lg">Modern<br>technology</h2>
    <p>Every detail matters. Our equipment and surroundings are chosen to make each treatment calm and precise, so every smile finds its balance.</p>
    <p><b>3D intraoral scanner:</b> accurate, comfortable impressions without paste.</p>
    <p><b>In-house 3D printing:</b> custom appliances made quickly and precisely.</p></div>
  <div data-anim="fade-in-from-right" data-delay="300">{ph(P, "v2", "height:334px")}</div>
</section>

<section class="story">
  <div data-anim="fade-in-from-left" data-delay="300" style="align-self:stretch">{ph(P, "v6", "height:100%")}</div>
  <div class="txt" data-anim="fade-in-from-left" style="padding:60px 0"><h2 class="t-lg">Our story</h2>
    <p>Founded more than ten years ago, the clinic has become a reference for discreet adult orthodontics. Guided by a clear vision, our founder introduced techniques that combine discretion and efficiency so that every smile fits the face naturally.</p>
    <p>Today we offer complete, personalised care for adults and children, using the most advanced techniques recognised internationally. We keep a careful balance between aesthetics, function and oral health for natural, lasting results.</p>
    <p>More than a clinic, it is a place where the art and science of the smile come together.</p></div>
</section>

<section class="team bg-cream" id="team">
  <div class="team-text" data-anim="fade-in-from-bottom"><h2 class="t-lg" style="margin-bottom:28px">The Lumen<br>team</h2>
    <p>Our team is made up of qualified practitioners who are passionate about modern orthodontics. They keep their skills up to date to offer personalised, safe and precise care, combining kindness and professionalism for long-lasting results.</p></div>
  <div class="people">{team}</div>
</section>

<section class="counters bg-cream" id="visit">
  <div><div class="counter"><div class="t-big-num"><span data-count="1200">1,200</span><sup>+</sup></div><div class="cap">Patients per year</div></div>
       <div class="counter"><div class="t-big-num"><span data-count="15">15</span><sup>%</sup></div><div class="cap">International patients</div></div></div>
  <div class="visit"><h2 class="t-xl">Come visit us</h2><div class="btn-row">{btn("Patient login", "#", "r")}{btn("New patient", "#", "r", book=True)}</div></div>
</section>

<section class="bg-cream" style="padding-bottom:1px">
  <div class="map" data-map="48.8722,2.3168" aria-label="Map"><div class="map-canvas"></div><span class="pin"></span>
    <div class="info"><h5 class="t-sm">Visit us</h5><h5 class="t-sm">Address</h5><p>{e(ADDRESS)}</p>
      <h5 class="t-sm">Transport</h5><p>Metro lines 1 and 9 → Example Station<br>Buses 22, 43, 52 → Example Square</p><p>Public car park on Avenue Example</p></div></div>
</section>'''

# ---------------------------------------------------------------- CONCEPT
def concept(P):
    return f'''
<section class="hero hero-center" style="min-height:632px">{hero_photo(P, "consultation", "sky", eager=True)}<div class="content"><h1 class="t-lg">Our concept</h1></div></section>

<section class="sec bg-blush">
  <div class="narrow"><h2 class="t-md" style="margin-bottom:24px">Our values</h2>
    <p class="t-lead">We believe a smile is much more than aligned teeth. It expresses personality, a delicate balance between harmony and emotion. Each smile is unique and should blend with the rest of the face.</p>
    <p class="t-lead">Our mission is to reveal the potential of every smile so it reflects each person’s natural beauty. Beyond appearance, we make sure every smile is balanced and comfortable, taking into account the jaw joints, chewing, speech and breathing.</p>
    <p class="t-lead">Our priority is a result that brings aesthetics and health together, for a smile you wear with confidence every day.</p></div>
</section>

<section class="sec bg-white diag">
  <div class="text"><h2 class="t-md" style="margin-bottom:24px">Smile and facial<br>structural diagnosis</h2>
    <p class="t-lead">Your smile deserves a global vision: attention to every line and every detail of your face. Our structural diagnosis is the moment where we read the geometry of your smile. Using modern imaging, we study how the smile and the face interact to plan a harmonious result.</p></div>
  <figure class="clinic-preview">
    <video controls playsinline preload="none" poster="{P}assets/media/clinic-consultation.webp" aria-label="Illustrative Lumen Clinic preview">
      <source src="{P}assets/media/clinic-preview.mp4" type="video/mp4">
      <a href="{P}assets/media/clinic-preview.mp4">Watch the clinic preview</a>
    </video>
    <figcaption>Illustrative preview of a fictional clinic. The video has no audio.</figcaption>
  </figure>
</section>

<section class="sec bg-blush" data-steps>
  <div class="diag"><div class="text"><h2 class="t-md" style="margin-bottom:24px">Analysis and<br>treatment plan</h2>
    <p class="t-lead">In the clinic or remotely, we design a treatment plan that follows your wishes and respects your needs. It is personalised in every detail and you are guided by our experts at each step, with close follow-up until the result matches your expectations.</p></div></div>
  <div class="steps">
    <div class="tabs"><span class="tab-line"></span><span class="tab on"><h4>In person</h4><p>By appointment at the clinic<br>{e(ADDRESS)}</p></span><span class="tab"><h4>Remote</h4><p>By video call via our<br>online booking platform</p></span></div>
    <div>
      <div class="step-body"><p>Would you like a face-to-face consultation with a specialist? Visit the clinic for a friendly first meeting with our team and our technology.</p><p>Once your patient file is created, we welcome you for an individual appointment with a full diagnosis and a follow-up plan built around your expectations.</p>{btn("Make an appointment", "#", book=True)}</div>
      <div class="step-body"><p>To make things easier, we also offer remote consultations. If you would like an appointment quickly, a first short visit can be used to prepare the administrative documents and create your patient file.</p><p>After that, most of the diagnosis and follow-up can take place remotely, from home. Secure, personalised tools keep the quality of care identical to an in-clinic visit.</p>{btn("Make an appointment", "#", book=True)}</div>
    </div>
    <div class="step-media">{ph(P, "v3")}{ph(P, "v5")}</div>
  </div>
</section>

<section class="cta-band"><h2 class="t-md">Come visit us</h2><div class="btn-row">{btn("Discover the clinic", P+"the-clinic/", "r")}{btn("Patient login", "#", "r")}</div></section>'''

# ---------------------------------------------------------------- TREATMENTS
def treatments(P):
    blocks = [
        ("Fixed or removable", "orthodontics/", "We offer a full range of orthodontic treatments for every need.",
         [("Fixed treatments", "A proven classic: whether on the outer or inner surface of the teeth, fixed appliances provide reliable, lasting correction. Available in metal or ceramic, with options tailored for comfort."),
          ("Removable treatments", "Clear aligners combine the effectiveness of conventional braces with the flexibility and hygiene of a removable appliance. For children, early treatment guides jaw growth and aligns teeth discreetly.")]),
        ("Brightness and balance", "aesthetics/", "Alongside orthodontics, we offer aesthetic care to refine the overall harmony of the smile.",
         [("Aesthetic care", "Smile symmetry, gum contouring and gentle brightening: each treatment is planned with the orthodontic result in mind, for a smile that looks natural.")]),
        ("A fresh start", "regenerating/", "To protect the long-term result, we help the smile and the surrounding tissues age well.",
         [("Regenerating care", "Whether it is to support the lips, restore volume or soften fine lines, our approach combines orthodontics and aesthetics for natural, lasting results.")]),
    ]
    tabs = ''.join(f'<a href="#t{i}"{" class=on" if i == 0 else ""}>{n}</a>' for i, n in enumerate(["Orthodontics", "Aesthetics", "Regeneration"]))
    body = ''
    for i, (title, href, lead, subs) in enumerate(blocks):
        s = ''.join(f'<h6 class="t-sm">{e(h)}</h6><p>{e(t)}</p>' for h, t in subs)
        body += f'<div class="tblock" id="t{i}"><h3 class="t-lg">{e(title)}</h3><p>{e(lead)}</p>{s}{btn("Discover more", P+href)}</div>'
    imgs = ''.join(ph(P, v) for v in ["v2", "v6", "v4"])
    reviews = [
        ("Very attentive with my son: everything was explained clearly to both of us and he was always at ease. I recommend the clinic.", "Patient A."),
        ("An elegant, calm practice. The team is warm and the doctor takes time to explain each step. Thank you for my new smile!", "Patient B."),
        ("My treatment lasted fourteen months and I am delighted with the result. Thanks to the whole team for their kindness.", "Patient C."),
        ("I have just finished my treatment with aligners. The follow-up was regular and very professional from start to finish.", "Patient D."),
    ]
    revs = ''.join(f'<div class="review"><div class="bubble"><span class="q">“</span><span>{e(t)}</span></div><span class="name">{e(n)}</span><span class="note">Sample testimonial</span></div>' for t, n in reviews)
    return f'''
<section class="hero hero-center" style="min-height:632px">{hero_photo(P, "consultation", "warm", eager=True)}<div class="content"><h1 class="t-xl">Lumen expertise</h1></div></section>

<section class="sec bg-blush"><div class="narrow"><h2 class="t-lg" style="margin-bottom:24px">Our expertise</h2>
  <p class="t-lead">Every smile is unique, and so is every treatment plan. We combine orthodontics, aesthetic care and prevention so that the result looks natural, works well and lasts. Each plan starts with a careful diagnosis and is adjusted at every visit.</p></div></section>

<section class="sec bg-white"><h2 class="t-lg">Our commitments</h2>
  <div class="commit">
    <div data-anim="fade-in-from-bottom"><h5 class="t-sm">01. Innovation</h5><p>Clinical excellence goes hand in hand with comfort. The practice is equipped with current technology so treatments are effective and pleasant.</p></div>
    <div data-anim="fade-in-from-bottom" data-delay="100"><h5 class="t-sm">02. Patient relationship</h5><p>We take a patient-centred approach with clear, open communication at every stage, so you always know what comes next.</p></div>
    <div data-anim="fade-in-from-bottom" data-delay="200"><h5 class="t-sm">03. Research</h5><p>To keep pace with medical progress, the team takes part in research, conferences and training throughout the year.</p></div>
  </div>
</section>

<section class="sec bg-blush" data-tlist><h2 class="t-lg">Our treatments</h2>
  <div class="tlist"><nav class="nav-side"><span class="tab-line"></span>{tabs}</nav><div>{body}</div><div class="timg">{imgs}</div></div>
</section>

<section class="bg-band">
  <div class="feedback-head"><h2 class="t-lg">Patient<br>feedback</h2><div class="btn-row">{btn("Read more", "#", "r")}{btn("Make an appointment", "#", "r", book=True)}</div></div>
  <div class="rule" style="margin:60px 6vw 0"></div>
  <div class="carousel"><div class="track">{revs}</div><div class="car-nav"><button type="button" data-prev aria-label="Previous">‹</button><button type="button" data-next aria-label="Next">›</button></div></div>
</section>'''

# ---------------------------------------------------------------- DETAIL TEMPLATE
def detail(title_lines, words, intro, explore, items):
    def body(P):
        cls = "c4" if len(items) == 4 else "c3"
        cards = ''.join(f'<a class="card" href="#d{i}" data-anim="fade-in-from-right" data-delay="{i*100}"><div class="imgw">{ph(P, v)}</div><h5 class="t-sm"><span>{e(it["name"])}</span></h5><p>{e(it["short"])}</p></a>' for i, (it, v) in enumerate(zip(items, ["v1", "v3", "v5", "v6"])))
        dc = ''
        for i, it in enumerate(items):
            lis = ''.join(f'<li><b>{e(a)}:</b> {e(b)}</li>' for a, b in it["points"])
            dc += f'''<article class="dcard" id="d{i}" data-word="{e(it['word'])}" data-text="{e(it['text'])}"><span class="num" aria-hidden="true">{i+1}</span>
  <h2>{e(it["name"])}</h2><div class="kind">{e(it["kind"])}</div><hr><ul>{lis}</ul>
  <div class="dur">{ICON["clock"]}<span>Treatment length: based on the initial assessment and your needs</span></div>
  {btn("Make an appointment", "#", book=True)}<div style="height:50px"></div></article>'''
        first = items[0]
        return f'''
<section class="d-hero">
  <div><h1 class="t-hero d-title">{title_lines}</h1><h5 class="t-md rw-title">For a <span class="rw" data-rotation="2500" data-delay="300">{''.join(f'<span class="rw-w">{e(w)}</span>' for w in words)}</span> smile</h5><h4 data-split>{e(intro)}</h4></div>
  {ph(P, "v6 arch")}
</section>
<section class="explore bg-sand"><span class="ghost" aria-hidden="true" data-anim="fade-in-from-bottom" data-delay="600">L</span>
  <h2 class="t-lg center" data-anim="fade-in-from-bottom" data-delay="600">{e(explore)}</h2><div class="cards {cls}">{cards}</div>
</section>
<section class="detail bg-sand" data-detail>
  <div class="stick"><div class="count">1 / {len(items)}</div><h3 class="t-lg">{e(first["word"])}</h3><p>{e(first["text"])}</p></div>
  <div class="dcards" data-anim="fade-in" data-delay="400"><div data-scrollmove="0.08">{dc}</div></div>
</section>'''
    return body

ORTHO = [
 {"name": "External braces", "short": "For precise, straightforward treatment", "kind": "Fixed treatment", "word": "Empower",
  "text": "External braces are ideal for precise, lasting corrections. Available in metal or ceramic for more discretion, they let us control every tooth movement and are especially suited to complex cases that need close follow-up.",
  "points": [("Choice", "metal or ceramic brackets"), ("Precision", "self-ligating brackets for an accurate fit"), ("Efficiency", "smooth sliding for faster tooth movement")]},
 {"name": "Internal braces", "short": "For discreet, invisible treatment", "kind": "Fixed treatment", "word": "Refine",
  "text": "Placed on the inner side of the teeth, internal braces are completely hidden. Each bracket is custom-made for the patient, combining discretion with the full control of a fixed appliance.",
  "points": [("Discreet", "invisible, fixed on the inner surface"), ("Fit", "brackets designed for each tooth"), ("Technology", "custom digital planning")]},
 {"name": "Clear aligners", "short": "For innovative, flexible treatment", "kind": "Removable treatment", "word": "Free",
  "text": "Clear aligners move teeth gradually with a series of transparent trays. They are easy to remove for meals and brushing, and digital planning lets you preview the result before starting.",
  "points": [("Digital", "3D planning of every step"), ("Hygiene", "easy to remove for eating and brushing"), ("Flexibility", "progressive, comfortable changes"), ("Aesthetics", "practically invisible")]},
 {"name": "Early treatment for children", "short": "For corrective treatment that guides growth", "kind": "Removable treatment", "word": "Guide",
  "text": "Early treatment helps correct problems while the jaws are still growing. Gentle appliances guide growth, improve essential functions and can reduce the need for heavier treatment later on.",
  "points": [("Early correction", "addresses issues from a young age"), ("Growth", "guides harmonious jaw development"), ("Functions", "supports breathing, chewing and speech"), ("Prevention", "light treatment to limit future work")]},
]
AESTH = [
 {"name": "Gummy smile correction", "short": "For a balanced gum line", "kind": "Aesthetic care", "word": "Harmonise",
  "text": "When too much gum shows when smiling, a gentle combined approach can rebalance the proportions between teeth, gums and lips for a softer smile.",
  "points": [("Balance", "harmonious proportions between teeth and gums"), ("Comfort", "minimally invasive techniques"), ("Natural", "a result that respects your features")]},
 {"name": "Smile symmetry", "short": "For a harmonious, even smile", "kind": "Aesthetic care", "word": "Balance",
  "text": "Small asymmetries can be corrected by combining tooth alignment with fine aesthetic adjustments, so the smile sits evenly within the face.",
  "points": [("Analysis", "digital study of facial proportions"), ("Precision", "targeted, gradual corrections"), ("Harmony", "a smile aligned with the face")]},
 {"name": "Smile brightening", "short": "For a luminous, healthy smile", "kind": "Aesthetic care", "word": "Illuminate",
  "text": "Gentle brightening treatments restore the natural shade of the teeth while protecting the enamel, as a finishing touch after orthodontic care or on their own.",
  "points": [("Gentle", "protocols that protect the enamel"), ("Personalised", "shade chosen with you"), ("Lasting", "simple maintenance advice")]},
]
REGEN = [
 {"name": "Smile ageing prevention", "short": "For a smile that stands the test of time", "kind": "Regenerating care", "word": "Rejuvenate",
  "text": "Keeping the teeth well aligned over time helps preserve a youthful smile. We combine retention and targeted care to protect your result.",
  "points": [("Technique", "maintaining alignment over the years"), ("Support", "natural support for the lips"), ("Long term", "a radiant smile that lasts")]},
 {"name": "Volume loss prevention", "short": "Give your smile a fresh start", "kind": "Regenerating care", "word": "Balance",
  "text": "Good dental alignment supports the lips and cheeks. Our treatments help restore lost volume and support the natural contours of the face.",
  "points": [("Restoration", "regain volume through alignment"), ("Strength", "support the contours of lips and cheeks"), ("Effectiveness", "lasting answers to facial ageing")]},
 {"name": "Lines around the mouth", "short": "For in-depth care", "kind": "Regenerating care", "word": "Plump up",
  "text": "Targeted treatments soften fine lines around the mouth while keeping expressions natural, planned together with your orthodontic follow-up.",
  "points": [("Targeted", "softens lines around the mouth"), ("Natural", "keeps your expressions"), ("Combined", "planned with your orthodontic care")]},
]

# ---------------------------------------------------------------- ACADEMY
def academy(P):
    faq = [
        ("What is orthodontics and why might I need it?", "Orthodontics corrects the position of the teeth and jaws. It improves appearance, but also chewing, speech and long-term oral health."),
        ("At what age should orthodontic treatment start?", "A first check is recommended around age 7. Treatment can then start at the right moment, and adults can be treated at any age."),
        ("What types of braces are available?", "External braces (metal or ceramic), internal braces placed behind the teeth, clear aligners and removable appliances for children."),
        ("What are clear aligners?", "A series of transparent, removable trays that move the teeth step by step according to a digital plan."),
        ("How long do I need to wear aligners each day?", "Usually around 22 hours a day, removing them only to eat and brush your teeth."),
        ("How long does orthodontic treatment last?", "Most treatments last between 12 and 24 months, depending on the complexity of the case."),
        ("Is orthodontic treatment painful?", "You may feel some pressure for a few days after each adjustment. It is usually mild and short-lived."),
        ("How often will I see the orthodontist?", "Generally every 6 to 10 weeks, with some follow-ups possible remotely."),
        ("Do I need special care during treatment?", "Careful brushing, regular check-ups and a few food precautions with fixed braces."),
    ]
    acc = ''.join(f'<details><summary>{e(q)}<i></i></summary><div class="ans"><p>{e(a)}</p></div></details>' for q, a in faq)
    return f'''
<section class="hero hero-center" style="min-height:632px">{hero_photo(P, "treatment", "lab shade", extra=' data-parallax="0.4"', eager=True)}
  <div class="content"><h1 class="t-lg">Lumen Academy</h1><p data-split>As dental technology evolves, the clinic is committed to research so our patients benefit from the latest advances.</p></div>
</section>

<section class="features bg-white">
  <div><div class="ico" data-anim="grow-in">{ICON["book"]}</div><h5 class="t-sm" data-anim="fade-in-from-bottom" data-delay="100">Publications &amp; congresses</h5><p data-anim="fade-in-from-bottom" data-delay="100">Our latest research and our participation in international congresses, where we share advances in orthodontics and aesthetics.</p></div>
  <div id="journal"><div class="ico" data-anim="grow-in" data-delay="200">{ICON["news"]}</div><h5 class="t-sm" data-anim="fade-in-from-bottom" data-delay="300">Our journal</h5><p data-anim="fade-in-from-bottom" data-delay="300">Articles on innovation and practical advice for a healthy, radiant smile. Follow our news and the latest trends.</p></div>
  <div><div class="ico" data-anim="grow-in" data-delay="400">{ICON["people"]}</div><h5 class="t-sm" data-anim="fade-in-from-bottom" data-delay="500">FAQ</h5><p data-anim="fade-in-from-bottom" data-delay="500">Detailed answers to the most frequent questions about our treatments, to support you at every stage.</p></div>
</section>

<section class="split-img bg-white" id="research">
  <div class="txt" data-anim="fade-in-from-bottom"><h2 class="t-md no-split">Conference attendance</h2>
    <p class="lead">Dr Martin regularly takes part in professional conferences, sharing her expertise and contributing to the progress of orthodontics. As a member of a national orthodontic society, she helps organise several annual meetings.</p>
    <div class="meta"><div><b>“Sharing knowledge is at the heart of our profession.”</b><span class="t-sm">Dr Martin</span><br><span class="t-xs muted">Head of clinic</span></div><div>Examples of conferences:<ul><li>Conference name</li><li>Conference name</li><li>Conference name</li></ul></div></div></div>
  <div class="pwrap" data-anim="fade-in">{ph(P, "v4", extra=' data-parallax="0.08"')}</div>
</section>

<section class="split-img alt" id="speaker">
  <div class="pwrap" data-anim="fade-in">{ph(P, "v1", extra=' data-parallax="0.08"')}</div>
  <div class="txt" data-anim="fade-in-from-bottom"><h2 class="t-md no-split">Speaker and trainer</h2>
    <p class="lead">Dr Martin also teaches courses for orthodontists who want to learn advanced techniques. These courses are recognised for their practical, hands-on approach.</p>
    <span class="logo-box">Partner logo</span>
    <div class="meta"><div><b>“Continuous learning is the key to quality care.”</b><span class="t-sm muted">Lumen statement</span></div><div>{btn("Read more", "#")}</div></div></div>
</section>

<section class="split-img bg-white" id="publications">
  <div class="txt" data-anim="fade-in-from-bottom"><h2 class="t-md no-split">Scientific articles</h2>
    <p class="lead">Alongside conferences, the team publishes articles in professional journals on orthodontic techniques and the link between aesthetics and function.</p>
    <div class="meta"><div><b>“Spreading knowledge helps every patient.”</b><span class="t-sm">Dr Martin</span><br><span class="t-xs muted">Head of clinic</span></div><div>Sample of articles:<ul><li>Article title</li><li>Article title</li><li>Article title</li></ul></div></div></div>
  <div class="pwrap" data-anim="fade-in">{ph(P, "v3", extra=' data-parallax="0.08"')}</div>
</section>

<section class="faq bg-white" id="faq">
  <div class="head"><h2 class="t-xl">Frequently<br>asked<br>questions</h2><p>For support<br>with peace of mind.</p></div>
  <div class="acc">{acc}</div>
</section>'''

# ---------------------------------------------------------------- BUILD
def build():
    if os.path.exists(OUT):
        shutil.rmtree(OUT)
    os.makedirs(os.path.join(OUT, "assets"))
    for f in ("style.css", "main.js"):
        shutil.copy(os.path.join(ROOT, "_src", f), os.path.join(OUT, "assets", f))
    shutil.copytree(os.path.join(ROOT, "assets", "media"), os.path.join(OUT, "assets", "media"))
    page("", "Home", "Orthodontics, aesthetic and regenerating care in a calm, modern clinic.", home, "")
    page("the-clinic", "The Clinic", "Discover the practice, the technology and the team.", clinic, "the-clinic/")
    page("our-concept", "Our Concept", "Our values, structural diagnosis and treatment planning.", concept, "our-concept/")
    page("our-treatments", "Our Treatments", "Orthodontic, aesthetic and regenerating treatments.", treatments, "our-treatments/")
    page("orthodontics", "Orthodontics", "External and internal braces, clear aligners and early treatment.",
         detail("Orthodontic<br>treatments", ["confident", "natural", "uninhibited"], "We put our expertise to work for your smile, with tailored care for every age.", "Explore our expertise", ORTHO), "our-treatments/", dark=True)
    page("aesthetics", "Aesthetics", "Gummy smile correction, smile symmetry and brightening.",
         detail("Our aesthetic<br>treatments", ["radiant", "balanced", "luminous"], "Our aesthetic treatments refine the harmony of the smile while respecting your natural features.", "Explore our treatments", AESTH), "our-treatments/", dark=True)
    page("regenerating", "Regenerating", "Preventive care for a smile that ages well.",
         detail("Our regenerating<br>treatments", ["timeless", "youthful", "lasting"], "Our regenerating care preserves the youth and harmony of the smile while softening the signs of time.", "Explore our treatments", REGEN), "our-treatments/", dark=True)
    page("academy", "Academy", "Research, publications, journal and frequently asked questions.", academy, "academy/")
    n = sum(1 for _, _, fs in os.walk(OUT) for f in fs if f == "index.html")
    print(f"Built {n} pages in {OUT}")

if __name__ == "__main__":
    build()
