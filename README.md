# Lumen Clinic — demo website

Static, 8-page clinic website template (fictional brand, placeholder text and images).
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
- Shared design: `assets/style.css` and `assets/main.js`.
- Images are CSS placeholders (`.ph` blocks): put an `<img>` inside each block.
- Hero "videos" are animated placeholders (`.vid`): add `<video autoplay muted loop playsinline>` inside.
- To change the brand, address or copy everywhere at once: edit `_build.py` and `_src/`, then run `python3 _build.py`.
