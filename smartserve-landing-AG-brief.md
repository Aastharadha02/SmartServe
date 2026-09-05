# SmartServe Customer Landing Page — Creative Brief for Antigravity

Direction: ivory + green, organic/editorial 3D storytelling. Replaces the earlier
navy/shader-curtain direction for the **landing page specifically** — splash/login
inside the app can stay a separate decision.

---

## 1. Why this direction

SmartServe connects people to trusted humans for home services — the tone should feel
warm, grounded, and alive, not corporate-SaaS. Ivory + green reads as natural, trustworthy,
calm — closer to a wellness/hospitality brand than a fintech dashboard. It also pairs
well with the human, editorial copy voice already validated on smartserve-theta
("Your home, well cared for.", 01/02/03 steps, testimonial).

## 2. Palette

| Role | Color | Notes |
|---|---|---|
| Base / canvas | `#FAF7F0` (ivory) | primary background, not pure white |
| Secondary canvas | `#F2EDE1` | section alternation, cards |
| Ink / text | `#1F2A1E` | near-black warm charcoal-green, not pure black |
| Primary green | `#2F5233` | deep forest — CTAs, nav, key UI |
| Accent green | `#7A9E6E` | mid sage — hover states, secondary accents |
| Highlight | `#C9A15A` warm gold (optional) | sparing use — badges, small emphasis, echoes the amber accent already in the settled system |

Contrast-check ink-on-ivory and white-on-forest-green before locking — both need to
clear WCAG AA for body text.

## 3. Reference sites — what to steal from each

- **smartserve-theta.vercel.app** — keep this copy voice and section rhythm (hero →
  trust strip → services grid → 01/02/03 process → testimonial → closing CTA). This
  brief adds 3D depth and motion on top of that structure, it doesn't replace it.
- **Sleep Well Creative** (sleep-well-creatives.com) — scroll-driven illustrated 3D
  narrative, editorial pacing. Closest match to "warm storytelling" over "cold product
  render." Steal: pairing a soft illustration style with scroll-sequenced 3D so long
  content reads as one continuous piece, not a stack of cards.
- **Explore Primland** (explore.ownprimland.com) — cinematic terrain flythrough with
  atmospheric fog, camera gliding on scroll. Steal the *feeling* (organic, breathing,
  outdoors) more than the literal terrain — think abstract rolling organic forms /
  foliage-adjacent shapes rather than mountains.
- **Shopify Editions** (shopify.com/editions/spring2026) — scroll as the narrative
  device: each section is a staged beat (entrance → hold → exit) instead of a flat
  scroll. Apply this to the services grid and the 01/02/03 steps.
- **Oryzo** (oryzo.ai) — one hero object rendered with real weight/inertia beats a busy
  scene. If you do one 3D hero form (an abstract organic blob / leaf-like morph), give
  it real material response and camera easing rather than stacking multiple elements.

## 4. Stack

- **React Three Fiber + drei** — `MeshDistortMaterial` for an organic, liquid-morphing
  abstract hero form (fits green/nature mood far better than glass). Keep it to
  **one** smooth continuous form, no literal icon shapes (already learned from the v0
  rounds — same rule applies here).
- **Paper Shaders** (`@paper-design/shaders-react`) — animated organic gradient
  background in the ivory/green range behind the hero, instead of the previous
  navy shader curtain.
- **Lenis** — smooth-scroll wrapper, synced to GSAP ScrollTrigger (`lenis.on('scroll',
  ScrollTrigger.update)` + `gsap.ticker`). This is what makes section-as-beat scroll
  storytelling feel right.
- **GSAP + ScrollTrigger** — stage each section as entrance/hold/exit; pin the hero
  while the 3D form settles before releasing scroll to the next section.
- **Framer Motion** — micro-interactions: button hover/press, card lift, magnetic
  cursor pull on primary CTAs.
- Component sources already shortlisted (still valid): **react-bits** (general),
  **Aceternity UI** (hero drama), **Magic UI** (counters/marquees), **hover.dev**
  (testimonial cards), **21st.dev** (+ Shader Builder for the gradient background).

## 5. UX/UI details to specify for AG (things easy to miss)

- **Custom cursor** — small dot that expands/tints sage-green on hover over
  interactive elements; signals "this is alive" without being gimmicky.
- **Magnetic buttons** — primary CTAs pull slightly toward the cursor within a small
  radius (Framer Motion or a small magnetic-button hook), then spring back.
- **Button states** — rest / hover (fill shifts ivory→forest-green, or a subtle
  liquid-fill wipe) / press (scale 0.97, faster ease) / focus-visible (visible ring,
  don't drop this for accessibility).
- **Scroll-reveal choreography** — text/cards enter with a soft upward fade + slight
  blur-to-sharp, staggered by ~80–120ms per element; nothing should "pop."
- **Section pinning** — pin the hero section briefly so the 3D form finishes its
  intro morph before scroll hands off to section 2 (this is what makes Shopify
  Editions and Cartier feel intentional instead of just "a page with a canvas on it").
- **Preloader / transition in** — since a 3D scene + shader bg needs to load, use a
  short branded loader (reuse the existing canvas "S" mark) rather than a blank flash.
- **Reduced-motion fallback** — respect `prefers-reduced-motion`: swap the 3D hero
  for a static organic SVG/gradient, cut scroll-pin and parallax to simple fades.
- **Mobile/perf fallback** — the 3D hero should degrade to a lighter shader-only or
  static image on low-end devices/mobile; don't ship the full drei scene to a phone
  on 4G. Check Core Web Vitals once built — defer the 3D bundle so meaningful HTML
  paints first.
- **Contrast & accessibility** — ivory-on-ivory and green-on-green sections both need
  a real contrast check, not just an eyeballed one.

## 6. Master prompt — paste to Antigravity

```
Build the SmartServe customer landing page as a warm, organic, 3D-storytelling
experience — think Sleep Well Creative's editorial scroll-driven 3D pacing crossed
with the human copy tone of an "Your home, well cared for" wellness/hospitality brand,
NOT a cold SaaS/product-launch site.

Palette: ivory base (#FAF7F0 / #F2EDE1), warm near-black ink (#1F2A1E), deep forest
green (#2F5233) as the primary UI/CTA color, sage (#7A9E6E) for hover/secondary accents,
optional warm gold (#C9A15A) used sparingly for small highlights.

Hero: one continuous, smooth, abstract organic 3D form (React Three Fiber + drei
MeshDistortMaterial) — liquid, leaf/petal-adjacent, morphing gently. Explicitly NOT a
literal icon (no wrench/spray-bottle/service-icon shapes) and NOT a multi-primitive
assembly that reads as a toy. Behind it, an animated organic gradient shader
(Paper Shaders, @paper-design/shaders-react) cycling through the ivory/green palette,
not the previous navy tones.

Scroll behavior: Lenis smooth-scroll synced to GSAP ScrollTrigger. Pin the hero briefly
so the 3D form completes its intro morph, then release into a section-as-beat structure
(entrance → hold → exit) for: trust strip → services grid (Home cleaning, Plumbing,
Electrical, Beauty & wellness) → the existing 01/02/03 "Tell us what you need / We find
your fit / Feel the difference" steps → testimonial → closing CTA. Keep the existing
copy voice and structure from smartserve-theta.vercel.app — this is a visual/motion
upgrade of that page, not a rewrite of its content.

Micro-interactions: custom cursor that tints sage-green over interactive elements,
magnetic pull on primary CTA buttons, staggered upward-fade scroll reveals (80–120ms
stagger), button press states with real easing (no instant snaps).

Constraints: respect prefers-reduced-motion (static organic SVG/gradient fallback, no
pin/parallax); degrade the 3D hero to a lighter shader-only version on mobile/low-end
devices; defer the 3D bundle so real HTML paints first (Core Web Vitals matter — this
is a production commerce page, not a portfolio piece); WCAG AA contrast on all
ivory/green text pairings.

Component sources to pull from as needed: react-bits, Aceternity UI, Magic UI,
hover.dev, 21st.dev + Shader Builder. Do not introduce literal service-icon 3D clip-art
— that direction was already tried and rejected.

Ship this into `customer-frontend` (or wherever the customer app root ends up living)
as production code, not another disposable sandbox iteration.
```

## 7. Open items for you (Pushkar) to confirm before AG starts

- Splash/login screens: do they follow this ivory/green direction too, or keep the
  earlier dark navy "arrival moment" treatment and only the landing page (pre-login,
  public-facing) goes ivory/green? The prompt above is scoped to the public landing
  page only — say the word if it should extend further.
- Any actual green/ivory brand reference beyond smartserve-theta's copy tone (a logo,
  an existing swatch, a competitor you like) worth pointing AG at directly?
