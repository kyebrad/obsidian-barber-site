"""
Cinematic Sites Agent
=====================
Replicates the RUBRIC Flows "Cinematic Sites" kit.

4-step pipeline:
  [1] Brand Analysis   — generates brand brief from business info
  [2] Scene Generation — reads cinematic modules, produces design spec
  [3] Website Build    — assembles complete single-file site
  [4] Deploy to Vercel — deploys or provides deploy instructions

Requirements:
  pip install claude-agent-sdk anyio anthropic

Usage:
  python cinematic_agent.py
"""

import anyio
import os
import json
from claude_agent_sdk import query, ClaudeAgentOptions, ResultMessage

# ── Config ────────────────────────────────────────────────────────────────────

MODULES_DIR = r"c:\Users\KyeronBradley\Desktop\Kyeron\cinematic-site-components"
OUTPUT_DIR  = r"c:\Users\KyeronBradley\Desktop\Kyeron\barber-site"
MODEL       = "claude-opus-4-6"

BUSINESS = {
    "type":  "barber shop",
    "mood":  "sleek & minimal",
    "theme": "dark",
}

# ── Helpers ───────────────────────────────────────────────────────────────────

async def run_agent(prompt: str, cwd: str = None, tools: list = None) -> str:
    result = ""
    async for msg in query(
        prompt=prompt,
        options=ClaudeAgentOptions(
            model=MODEL,
            cwd=cwd or OUTPUT_DIR,
            allowed_tools=tools or [],
            permission_mode="acceptEdits",
        ),
    ):
        if isinstance(msg, ResultMessage):
            result = msg.result
    return result


# ── Step 1: Brand Analysis ────────────────────────────────────────────────────

async def brand_analysis(business: dict) -> dict:
    print("\n[1/4] Brand Analysis...")
    raw = await run_agent(f"""
You are the Brand Analysis agent.
Business: {business['type']}
Mood: {business['mood']}
Theme: {business['theme']}

Return a JSON brand brief with:
  brand_name, tagline, colors (primary/secondary/accent/background/surface/text as hex),
  fonts (heading/body as Google Fonts names), services (array of {{name, price}}),
  about_copy, hero_headline, hero_subtext, cta_text, nav_links

Respond ONLY with raw JSON.
""")
    # strip markdown fences if present
    raw = raw.strip().lstrip("```json").lstrip("```").rstrip("```").strip()
    return json.loads(raw)


# ── Step 2: Scene Generation ──────────────────────────────────────────────────

async def scene_generation(brand: dict) -> dict:
    print("\n[2/4] Scene Generation...")
    raw = await run_agent(
        prompt=f"""
You are the Scene Generation agent.
Read these cinematic module files:
  - {MODULES_DIR}/curtain-reveal.html
  - {MODULES_DIR}/spotlight-border.html
  - {MODULES_DIR}/mesh-gradient.html

Brand: {json.dumps(brand, indent=2)}

For each module extract: css_vars to swap, js_summary, html_structure.
Also output a layout_order array.
Respond ONLY with raw JSON with keys: curtain, spotlight, mesh, layout_order.
""",
        cwd=MODULES_DIR,
        tools=["Read"],
    )
    raw = raw.strip().lstrip("```json").lstrip("```").rstrip("```").strip()
    return json.loads(raw)


# ── Step 3: Website Build ─────────────────────────────────────────────────────

async def website_build(brand: dict, scene: dict) -> str:
    print("\n[3/4] Website Build...")
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    result = await run_agent(
        prompt=f"""
You are the Website Build agent.

READ these source modules (copy their JS/CSS faithfully):
  - {MODULES_DIR}/curtain-reveal.html
  - {MODULES_DIR}/spotlight-border.html
  - {MODULES_DIR}/mesh-gradient.html

Brand brief:
{json.dumps(brand, indent=2)}

Scene spec:
{json.dumps(scene, indent=2)}

Build a complete, production-ready single-file barber shop website:
- Mesh gradient as full-page fixed canvas background
- Curtain reveal hero section
- Spotlight border cards for services (4 cards)
- About section, CTA section, footer
- Dark nav bar with brand name and nav links
- Apply all brand colors, fonts (Google Fonts), and copy
- Fully responsive

WRITE to: {OUTPUT_DIR}/index.html
""",
        cwd=MODULES_DIR,
        tools=["Read", "Write", "Bash"],
    )
    return result


# ── Step 4: Deploy ────────────────────────────────────────────────────────────

async def deploy_to_vercel() -> str:
    print("\n[4/4] Deploy to Vercel...")
    result = await run_agent(
        prompt=f"""
You are the Deploy agent.

1. Write this vercel.json to {OUTPUT_DIR}:
   {{"version":2,"builds":[{{"src":"index.html","use":"@vercel/static"}}],"routes":[{{"src":"/(.*)","dest":"/index.html"}}]}}

2. Run: vercel --version
   - If available: run `vercel --yes --prod` from {OUTPUT_DIR}
   - If not: write DEPLOY.md with drag-and-drop Vercel instructions

Report the outcome.
""",
        cwd=OUTPUT_DIR,
        tools=["Read", "Write", "Bash"],
    )
    return result


# ── Orchestrator ──────────────────────────────────────────────────────────────

async def main():
    print("=" * 55)
    print("  CINEMATIC SITES AGENT  |  Powered by Claude Opus 4.6")
    print("=" * 55)

    brand  = await brand_analysis(BUSINESS)
    print(f"  Brand: {brand.get('brand_name')}  —  {brand.get('tagline')}")

    scene  = await scene_generation(brand)
    print(f"  Layout: {' → '.join(scene.get('layout_order', []))}")

    await website_build(brand, scene)
    print(f"  Built: {OUTPUT_DIR}/index.html")

    deploy = await deploy_to_vercel()
    print(f"\n  Deploy result:\n{deploy}")

    print("\n" + "=" * 55)
    print("  DONE")
    print("=" * 55)


if __name__ == "__main__":
    anyio.run(main)
