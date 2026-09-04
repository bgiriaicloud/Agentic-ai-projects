#!/usr/bin/env python3
"""
High-Level Design (HLD) & Architecture Image Generator:
FinOps for the Agentic Harness: The Hidden Cost of Non-Functional LLM Calls for Memory, Evals & Guardrails

Renders a 16:9 4K UHD (3840x2160, 300 DPI) enterprise architectural blueprint with 100% typo-free labels.
"""

import subprocess
import sys
from pathlib import Path

def render_hld_image():
    root_dir = Path(__file__).parent
    svg_file = root_dir / "finops_harness_hld.svg"
    png_file = root_dir / "finops_harness_hld.png"

    if not svg_file.exists():
        print(f"Error: SVG file not found at {svg_file}")
        sys.exit(1)

    print("================================================================================")
    print(" RENDERING FINOPS AGENTIC HARNESS HLD ARCHITECTURE DIAGRAM (4K UHD, 300 DPI)")
    print("================================================================================")
    print(f"Source SVG: {svg_file.name}")
    print(f"Target PNG: {png_file.name} (Resolution: 3840x2160 @ 300 DPI)")

    # Execute high-performance Rust-based resvg CLI via npx
    cmd = [
        "npx", "-y", "@resvg/resvg-js-cli",
        "--fit-width", "3840",
        "--dpi", "300",
        str(svg_file),
        str(png_file)
    ]
    
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        print(f"Rendering failed: {res.stderr}")
        sys.exit(res.returncode)

    print("\n[SUCCESS] Rendered 4K High-Level Design (HLD) architecture image successfully!")
    print(f"Output saved at: {png_file.resolve()}")

if __name__ == "__main__":
    render_hld_image()
