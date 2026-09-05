# SmartServe — Brand Theme, Color System & Design Prompt

> **Shareable Reference for Project Co-Owners & Design/Dev Teams**  
> **Brand Essence:** *"Your home, well cared for."*  
> **Aesthetic Philosophy:** Warm, organic, editorial hospitality meets trustworthy Indian home care services. Moves far away from cold corporate SaaS blues or sterile utilitarian layouts into an elevated, calm, and reassuring domestic sanctuary feel.

---

## 1. Core Color Palette

| Token Name | Hex Code | RGB | HSL | Semantic Role & Usage |
|---|---|---|---|---|
| **Ivory Base (Canvas)** | `#FAF7F0` | `250, 247, 240` | `42°, 43%, 96%` | Primary application & page background. Warm, serene canvas replacing stark clinical `#FFFFFF`. |
| **Ivory Surface (Secondary)** | `#F2EDE1` | `242, 237, 225` | `42°, 38%, 94%` | Card surfaces, section backgrounds, subtle dividers, pill containers. |
| **Forest Green (Primary Brand)** | `#2F5233` | `47, 82, 51` | `127°, 27%, 25%` | Primary brand color, primary CTA buttons, brand badges, strong anchor text. |
| **Warm Ink (Typography)** | `#1F2A1E` | `31, 42, 30` | `115°, 17%, 14%` | Primary headings and high-contrast text. Deep botanical near-black instead of harsh pure black `#000000`. |
| **Sage Green (Accent / Hover)** | `#7A9E6E` | `122, 158, 110` | `105°, 20%, 53%` | Eyebrow text, secondary links, hover accents, subtle progress indicators, active borders. |
| **Warm Gold (Luxury Highlight)** | `#C9A15A` | `201, 161, 90` | `38°, 52%, 57%` | Star ratings (★), trust numerals ("01", "02"), guarantee insignias. *Use sparingly; never for body text.* |
| **Emerald Live Status** | `#10B981` | `16, 185, 129` | `160°, 84%, 39%` | Real-time live status indicator ("Arriving on time", "Verified pro"). |

---

## 2. Typography System

### Display & Editorial Headings
- **Font Family:** `DM Serif Display`, Georgia, serif
- **Styles:** Regular, Italic (used strategically for emotional punch, e.g. *"People who care."*)
- **Usage:** Main hero title (H1), primary section headlines (H2), pull quotes.
- **Letter Spacing:** `-0.01em` to `-0.02em` (tight, editorial feeling).

### UI, Body & Micro-Copy
- **Font Family:** `Plus Jakarta Sans`, system-ui, sans-serif
- **Weights:** `400` (Regular), `500` (Medium), `600` (Semi-Bold), `700` (Bold), `800` (Extra-Bold for logos)
- **Usage:** Sub-headings, body copy, card labels, pricing, CTA buttons, forms.
- **Line Height:** `1.6` to `1.7` for body text to maintain airy, relaxed readability.

---

## 3. UI Styling & Component Rules

### Glassmorphism & Cards
- **Backdrop:** `background: rgba(255, 255, 255, 0.88)` or `rgba(250, 247, 240, 0.92)`
- **Blur:** `backdrop-filter: blur(14px - 18px); -webkit-backdrop-filter: blur(14px - 18px);`
- **Border:** `1px solid rgba(255, 255, 255, 0.9)` or subtle `1px solid rgba(31, 42, 30, 0.08)`
- **Border Radius:**
  - Standard cards: `20px - 28px`
  - Featured / Hero frames: `28px - 32px`
  - Badges / Buttons: `9999px` (fully rounded pills)
- **Shadows:** Soft layered diffuse shadows:
  ```css
  box-shadow: 0 20px 48px -12px rgba(31, 42, 30, 0.14), 0 6px 18px -6px rgba(47, 82, 51, 0.06);
  ```

### Primary Buttons (Forest Green)
```css
background: #2F5233;
color: #FFFFFF;
font-weight: 600;
border-radius: 9999px;
padding: 0.875rem 2rem;
box-shadow: 0 2px 12px rgba(47, 82, 51, 0.25);
transition: all 0.2s ease;
```
- **Hover:** `background: #3D6B42; box-shadow: 0 4px 20px rgba(47, 82, 51, 0.35);`

### Ghost / Secondary Buttons
```css
background: transparent;
color: #1F2A1E;
font-weight: 600;
border: 1.5px solid rgba(31, 42, 30, 0.2);
border-radius: 9999px;
padding: 0.875rem 1.5rem;
```
- **Hover:** `border-color: #2F5233; background: rgba(47, 82, 51, 0.06);`

---

## 4. Imagery & Visual Assets Guidelines

- **Style:** Serene, sun-drenched, clean Japandi and warm Scandinavian minimalist domestic spaces.
- **Textures:** Natural oak wood, warm ivory linen curtains, healthy potted plants (monstera, olive tree), soft morning light.
- **Strictly Avoid:**
  - ❌ Cold tech corporate office blues or flat neon gradients.
  - ❌ Weird abstract distorted 3D meshes (e.g. slimy green blobs).
  - ❌ Literal cartoon clip-art (clipart wrenches, spray bottles, or exaggerated cartoon mascots).
  - ❌ Stark, sterile, or overly industrial textures.

---

## 5. Ready-to-Use Code Tokens

### CSS Variables (`:root` / `.smartserve-theme`)
```css
:root {
  --ss-ivory:       #FAF7F0;
  --ss-ivory-warm:  #F2EDE1;
  --ss-ink:         #1F2A1E;
  --ss-forest:      #2F5233;
  --ss-forest-hover:#3D6B42;
  --ss-sage:        #7A9E6E;
  --ss-gold:        #C9A15A;
  --ss-border:      rgba(31, 42, 30, 0.08);
  --ss-font-display:'DM Serif Display', Georgia, serif;
  --ss-font-body:   'Plus Jakarta Sans', system-ui, sans-serif;
}
```

### Tailwind CSS Config Extension (`tailwind.config.js`)
```javascript
module.exports = {
  theme: {
    extend: {
      colors: {
        smartserve: {
          ivory: '#FAF7F0',
          surface: '#F2EDE1',
          ink: '#1F2A1E',
          forest: '#2F5233',
          forestHover: '#3D6B42',
          sage: '#7A9E6E',
          gold: '#C9A15A',
        },
      },
      fontFamily: {
        display: ['"DM Serif Display"', 'Georgia', 'serif'],
        body: ['"Plus Jakarta Sans"', 'system-ui', 'sans-serif'],
      },
      borderRadius: {
        'organic': '1.75rem',
        'pill': '9999px',
      },
    },
  },
};
```

---

## 6. Copy-Paste AI Theme Prompt

> 💡 **Instructions for Co-Owner / Designers / AI Agents:**  
> Whenever prompting an AI assistant (e.g. Claude, ChatGPT, v0, Gemini) to generate or refactor any frontend page, UI component, or mobile screen for SmartServe, paste the prompt below:

```text
You are designing UI components for SmartServe — an elevated home wellness and care platform with the tagline: "Your home, well cared for."

Follow this exact design system and theme specifications:

1. BRAND PALETTE:
   - Primary Background: Warm Ivory (#FAF7F0)
   - Secondary Surface / Cards: Warm Sand Ivory (#F2EDE1)
   - Primary Brand / Main CTAs: Deep Forest Green (#2F5233, hover: #3D6B42)
   - Typography & Headings: Warm Near-Black Ink (#1F2A1E)
   - Secondary Accents / Subtitles: Soft Sage Green (#7A9E6E)
   - Luxury Highlights / Star Ratings: Warm Gold (#C9A15A)
   - Live Status: Emerald Green (#10B981)

2. TYPOGRAPHY:
   - Display Headings (H1/H2): "DM Serif Display", serif with occasional italic emphasis (e.g. "People who care.")
   - Body, Navigation, Inputs & Buttons: "Plus Jakarta Sans", sans-serif (weights: 500, 600, 700)

3. AESTHETICS & SHAPE:
   - Modern editorial layout with generous breathing room (padding 4rem - 6rem for sections).
   - Generously rounded corners: 24px - 32px for cards, 9999px for pills and buttons.
   - Glassmorphism: Frosted glass panels with `background: rgba(255, 255, 255, 0.88)`, `backdrop-filter: blur(16px)`, `border: 1px solid rgba(255, 255, 255, 0.95)`.
   - Soft diffuse drop shadows: `0 20px 48px -12px rgba(31, 42, 30, 0.12)`.
   - Visual imagery must depict warm, sunlit, clean Japandi/minimalist home interiors with natural oak, cream linens, and greenery.

4. DO NOT USE:
   - No cold tech corporate blues (#0066FF, #2563EB) or flat neon colors.
   - No pure black text (#000000) or pure white backgrounds (#FFFFFF) for main canvas.
   - No literal cartoon repair icons or distorted slimy 3D blobs.
   - Design must feel calm, reassuring, pristine, and hospital-grade reliable wrapped in luxury hospitality warmth.
```
