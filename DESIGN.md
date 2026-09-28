---
name: Obsidian Cybernetic
colors:
  surface: '#0f131c'
  surface-dim: '#0f131c'
  surface-bright: '#353943'
  surface-container-lowest: '#0a0e17'
  surface-container-low: '#181b25'
  surface-container: '#1c1f29'
  surface-container-high: '#262a34'
  surface-container-highest: '#31353f'
  on-surface: '#dfe2ef'
  on-surface-variant: '#b9cacb'
  inverse-surface: '#dfe2ef'
  inverse-on-surface: '#2c303a'
  outline: '#849495'
  outline-variant: '#3b494b'
  surface-tint: '#00dbe9'
  primary: '#dbfcff'
  on-primary: '#00363a'
  primary-container: '#00f0ff'
  on-primary-container: '#006970'
  inverse-primary: '#006970'
  secondary: '#adc6ff'
  on-secondary: '#002e6a'
  secondary-container: '#0566d9'
  on-secondary-container: '#e6ecff'
  tertiary: '#d8ffe7'
  on-tertiary: '#003824'
  tertiary-container: '#65f2b5'
  on-tertiary-container: '#006d4a'
  error: '#ffb4ab'
  on-error: '#690005'
  error-container: '#93000a'
  on-error-container: '#ffdad6'
  primary-fixed: '#7df4ff'
  primary-fixed-dim: '#00dbe9'
  on-primary-fixed: '#002022'
  on-primary-fixed-variant: '#004f54'
  secondary-fixed: '#d8e2ff'
  secondary-fixed-dim: '#adc6ff'
  on-secondary-fixed: '#001a42'
  on-secondary-fixed-variant: '#004395'
  tertiary-fixed: '#6ffbbe'
  tertiary-fixed-dim: '#4edea3'
  on-tertiary-fixed: '#002113'
  on-tertiary-fixed-variant: '#005236'
  background: '#0f131c'
  on-background: '#dfe2ef'
  surface-variant: '#31353f'
typography:
  display-hero:
    fontFamily: Plus Jakarta Sans
    fontSize: 48px
    fontWeight: '700'
    lineHeight: 56px
    letterSpacing: -0.03em
  headline-lg:
    fontFamily: Plus Jakarta Sans
    fontSize: 32px
    fontWeight: '600'
    lineHeight: 40px
    letterSpacing: -0.02em
  headline-lg-mobile:
    fontFamily: Plus Jakarta Sans
    fontSize: 26px
    fontWeight: '600'
    lineHeight: 34px
    letterSpacing: -0.02em
  headline-md:
    fontFamily: Plus Jakarta Sans
    fontSize: 22px
    fontWeight: '600'
    lineHeight: 28px
    letterSpacing: -0.015em
  headline-sm:
    fontFamily: Plus Jakarta Sans
    fontSize: 18px
    fontWeight: '600'
    lineHeight: 24px
    letterSpacing: -0.01em
  body-lg:
    fontFamily: Inter
    fontSize: 16px
    fontWeight: '400'
    lineHeight: 26px
    letterSpacing: -0.005em
  body-md:
    fontFamily: Inter
    fontSize: 14px
    fontWeight: '400'
    lineHeight: 22px
    letterSpacing: 0em
  body-sm:
    fontFamily: Inter
    fontSize: 12px
    fontWeight: '400'
    lineHeight: 18px
    letterSpacing: 0.005em
  code-inline:
    fontFamily: JetBrains Mono
    fontSize: 13px
    fontWeight: '500'
    lineHeight: 20px
    letterSpacing: -0.01em
  code-block:
    fontFamily: JetBrains Mono
    fontSize: 13px
    fontWeight: '400'
    lineHeight: 22px
    letterSpacing: 0em
  label-md:
    fontFamily: JetBrains Mono
    fontSize: 12px
    fontWeight: '500'
    lineHeight: 16px
    letterSpacing: 0.02em
  label-sm:
    fontFamily: JetBrains Mono
    fontSize: 10px
    fontWeight: '600'
    lineHeight: 14px
    letterSpacing: 0.06em
rounded:
  sm: 0.125rem
  DEFAULT: 0.25rem
  md: 0.375rem
  lg: 0.5rem
  xl: 0.75rem
  full: 9999px
spacing:
  gutter: 1rem
  gutter-lg: 1.5rem
  margin: 1rem
  margin-md: 1.5rem
  margin-lg: 2.5rem
  space-xs: 0.25rem
  space-sm: 0.5rem
  space-md: 0.75rem
  space-lg: 1.25rem
  space-xl: 2rem
  space-2xl: 3rem
---

## Brand & Style

This design system is tailored for an elite, high-velocity developer audience requiring deep-focus code analysis, automated intelligence, and contextual code tutoring. The visual aesthetic fuses cinematic science-fiction ergonomics with the hyper-utilitarian discipline of tools like Linear, Raycast, and modern code editors. 

The mood is nocturnal, focused, and instrument-grade. It pairs deep obsidian voids with razor-sharp luminescence. The UI prioritizes information density without visual clutter, leaning into subtle translucent backdrops, calibrated glowing borders, hairline dividers, and high-visibility status indicators. Interactions feel instantaneous, tactile, and engineered with millisecond precision to honor developer flow state.

## Colors

The palette establishes an ultra-dark canvas structured into distinct tonal tiers of obsidian and void navy, accented by functional photon-glow signals:

- **Base Canvas & Surfaces**:
  - Root Canvas (`#090D16`): The bedrock environment, providing maximum contrast for syntax tokens.
  - Surface Mid (`#0D111D`): Primary panel, drawer, and side-dock background.
  - Surface High (`#131B2E`): Floating inspection layers, elevated card bodies, code block wells.
  - Surface Overlay (`#1A243D`): Active states, hovers, and popovers.

- **Accent Matrix**:
  - Primary Cyan (`#00F0FF`): Primary interactive focus, AI suggestions, and streaming tokens.
  - Electric Blue (`#3B82F6`): Structural highlights, multi-selection, and secondary actions.
  - Emerald Safe (`#10B981`): Passing lint rules, safe dependencies, performance boosts.
  - Amber Caution (`#F59E0B`): Deprecation notices, algorithmic debt warnings, review notes.
  - Ruby Critical (`#EF4444`): Vulnerabilities, breaking syntax errors, security CVE tags.

- **Content & Stroke Semantics**:
  - Content High-Contrast (`#F8FAFC`): Active code and primary headers.
  - Content Muted (`#94A3B8`): Inline descriptions, metadata, and gutter line numbers.
  - Content Dim (`#475569`): Inactive symbols, hidden whitespace, comment syntax.
  - Hairline Stroke (`rgba(255, 255, 255, 0.08)`): Base surface separation.
  - Active Glow Stroke (`rgba(0, 240, 255, 0.35)`): Focused panels and AI-modified code hunks.

## Typography

Typography functions as both interface instrument and syntax carrier:

- **Display & Section Headers (`Plus Jakarta Sans`)**: Delivers geometric crispness with modern proportions. Letter-spacing tightens at larger scales to evoke a focused, technical magazine feel.
- **Narrative & Explanation (`Inter`)**: Serves as the high-legibility workhorse for conversational AI code explanations, vulnerability breakdowns, and documentation panels.
- **Syntactic & Operational Labels (`JetBrains Mono`)**: Applied to all raw code displays, inline refactors, diff line counts, keyboard shortcut chips, metrics, and terminal traces. Ligatures should be active in code views, with optical alignment preserving vertical column integrity.

## Layout & Spacing

The layout is built on a high-density, multi-pane workbench paradigm. Rather than traditional sprawling page-based structures, the layout behaves as a responsive IDE canvas:

- **Panels & Canvases**: Dynamic flex-split columns for File Explorer, Code Diff Reviewer, and AI Explainer/Chat Dock.
- **Breakpoints & Adaptation**:
  - `Desktop (> 1280px)`: Full 3-pane workbench (Left tree 240px, Center code diff fluid, Right inspector/terminal 380px fixed).
  - `Tablet (768px - 1279px)`: Split-pane with collapsable overlay drawers for navigation and AI chat; priority is given to the syntax canvas.
  - `Mobile (< 768px)`: Stacked tabbed layout switching between Code, AI Explanations, and Problems tabs, using compact edge margins (`1rem`).
- **Rhythm**: Component interiors maintain strict 4px/8px incremental padding, ensuring strict baseline alignments between line numbers and code review threads.

## Elevation & Depth

Visual hierarchy does not rely on heavy drop shadows; it relies on surface luminance, translucent backplates, and perimeter photon glows:

- **Layer 0 (Canvas Base - `#090D16`)**: Pure flat foundation.
- **Layer 1 (Recessed Code Wells - `#06090F`)**: Sunken syntax viewports featuring an inner hairline inset stroke `inset 0 1px 1px rgba(0,0,0,0.6)`.
- **Layer 2 (Standard Cards & Inspect Panels)**: Translucent glass panels with `background: rgba(13, 17, 29, 0.75)`, `backdrop-filter: blur(16px)`, bounded by a 1px border of `rgba(255, 255, 255, 0.07)`.
- **Layer 3 (Floating Command Palettes & Overlays)**: Surface `#131B2E` with `backdrop-filter: blur(24px)`, elevated by a soft dual-boundary shadow: `0 16px 40px -10px rgba(0, 0, 0, 0.7), 0 0 0 1px rgba(255, 255, 255, 0.12)`.
- **Active Glow Elevation**: When an AI review suggestion or inline security diagnostic is selected, the element projects an ambient volumetric glow: `0 0 24px -4px rgba(0, 240, 255, 0.25), 0 0 0 1px rgba(0, 240, 255, 0.6)`.

## Shapes

The shape system adopts a sleek, low-radius aesthetic (`0.25rem` / 4px base radius) evoking physical chassis hardware and high-precision developer monitors. 

- **Interactive Inputs & Action Buttons**: 4px border radius for compact, surgical control elements.
- **Panels, Modals & Surface Cards (`rounded-lg`)**: 8px (0.5rem) border radius, softening exterior frames while maintaining dense internal grid lines.
- **Pill Badges & Status Tags**: Fully pill-shaped (9999px) for status indicators, tag chips, and vulnerability badges, visually isolating meta-data from rectangular code structures.

## Components

- **Buttons**:
  - *Primary (Cybernetic Pulse)*: Solid Cyan (`#00F0FF`) background with Obsidian text (`#090D16`), bold font, with a soft cyan hover plume `box-shadow: 0 0 16px rgba(0, 240, 255, 0.4)`.
  - *Secondary (Glass Frame)*: Translucent dark background (`rgba(19, 27, 46, 0.6)`), 1px border (`rgba(255, 255, 255, 0.1)`), light text. Shifts to white border and cyan text on hover.
  - *Ghost / Command*: Borderless, muted text; gains subtle background tint on hover with keyboard shortcut chips rendered inline.

- **Status & Vulnerability Chips**:
  - Pill-shaped badges with semi-transparent tinted fills (`rgba(color, 0.12)`), solid 1px tinted borders, and high-visibility status dots:
    - Ruby (`#EF4444`): Critical Security CVE / Syntax Error.
    - Amber (`#F59E0B`): Performance Alert / Logic Warning.
    - Emerald (`#10B981`): Test Passed / Optimized.
    - Cyan (`#00F0FF`): AI Suggested Refactor.

- **Diff Viewports & Code Blocks**:
  - Gutter with sticky line numbers in muted slate.
  - Added lines: Soft green highlight (`rgba(16, 185, 129, 0.08)`) with a 2px solid emerald left border marker.
  - Removed lines: Soft red highlight (`rgba(239, 68, 68, 0.08)`) with a 2px solid ruby left border marker.
  - AI Suggested Replacement: Tinted cyan panel embedded inline with quick actions ("Apply Fix", "Explain", "Reject").

- **Terminal & Console Windows**:
  - Fixed dark glass canvas (`#06090F`) with header tabs, live blinking cyan cursor (`#00F0FF`), and JetBrains Mono monospace output styled by status color.

- **Inputs & Prompt Fields**:
  - Obsidian surface (`#0D111D`), 1px muted border (`rgba(255, 255, 255, 0.1)`). 
  - Focus state triggers an electric blue/cyan outline glow without layout shift.
  - Prefix icons (e.g., prompt stars, search lens) colored in muted steel, turning bright cyan on active entry.

- **Review Cards & Inspection Threads**:
  - Glass-surfaced modules docked directly to code lines.
  - Contain user or AI avatar, timestamp label, markdown-rendered explanation, and code patch blocks with syntax highlighting.