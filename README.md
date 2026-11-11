# Lumen Clinic — demo website

Static, 8-page clinic website template (fictional brand, sample text and original illustrative imagery).
Pages: Home, The Clinic, Our Concept, Our Treatments, Orthodontics, Aesthetics, Regenerating, Academy.

## Hosting
Publish the folder as-is (GitHub Pages or any static host), or open `index.html` locally.

## Animations (matched to the reference design)
- Page transition: centre mask reveal on load, cover on internal link clicks.
- Headings: line-by-line word reveal. Elements: fade-in from bottom/left/right, fade-in, grow-in, with staggered delays.
- Rotating words (home intro, treatment heroes), hero scroll movement, background parallax.
- Clinic photo slider (drag/swipe), clip-path reveal on the video band, counters, hover cards, image zoom,
  scroll-linked sticky tabs with moving indicator, testimonial slider, one-at-a-time FAQ accordion, Leaflet map.

## Scroll fix (vs. the reference site)
The reference combined `body { overflow: hidden }` with `html, body { overscroll-behavior: none }`.
That makes <body> a scroll container that swallows mouse-wheel/trackpad scrolling in Chrome and Edge
(the page only scrolls over the header, with the keyboard or the scrollbar). This template uses
`overflow-x: clip` instead and never sets `overscroll-behavior: none` on html/body. Don't reintroduce that pair.

## Editing
- Edit `_build.py` and `_src/`, then run `python3 _build.py` to generate the eight pages and shared assets in `dist/`. GitHub Pages serves the generated HTML and shared assets checked into the repository root.
- `assets/media/` contains generated clinic photography and a silent motion preview assembled from that imagery. The video plays on demand on the Our Concept page. The imagery depicts a fictional clinic.
