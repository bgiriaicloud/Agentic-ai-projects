#!/usr/bin/env python3
"""
FinOps for Agentic Harness - CLI Simulation Runner & Executive Report Generator
Executes comparative simulation between Unmanaged and FinOps-Governed Harnesses,
printing detailed unit economics, token amplification factor, and enterprise savings.
"""

import sys
import json
from pathlib import Path
from .simulator import simulate_naive_harness, simulate_finops_harness
from .models import TurnSimulationResult

def print_header(title: str):
    print("\n" + "=" * 80)
    print(f" {title.upper()}")
    print("=" * 80)

def print_turn_breakdown(res: TurnSimulationResult):
    print(f"\n>>> SCENARIO: {res.scenario_name}")
    print("-" * 80)
    print(f"{'Harness Span / Call Name':<42} | {'Category':<16} | {'Tokens':<8} | {'Cost ($)':<10}")
    print("-" * 80)
    for s in res.spans:
        toks = s.input_tokens + s.output_tokens
        print(f"{s.name:<42} | {s.classification.value:<16} | {toks:>7,d} | ${s.cost_usd:>9.6f}")
    print("-" * 80)
    print(f"TOTAL PER TURN: {res.total_tokens:>7,d} Tokens | Cost: ${res.total_cost_usd:.6f}")
    print(f"  • Functional Tokens:     {res.functional_tokens:>7,d} ({res.functional_tokens/res.total_tokens*100:.1f}%) | Cost: ${res.functional_cost_usd:.6f}")
    print(f"  • Non-Functional Tokens: {res.non_functional_tokens:>7,d} ({res.non_functional_token_ratio:.1f}%) | Cost: ${res.non_functional_cost_usd:.6f}")
    print(f"  • Token Amplification Factor (TAF): {res.token_amplification_factor:.2f}x")
    print(f"  • Non-Functional Cost Ratio:       {res.non_functional_cost_ratio:.1f}%")

def print_executive_comparison(naive: TurnSimulationResult, finops: TurnSimulationResult, monthly_turns: int = 4_000_000):
    print_header("Enterprise Financial Impact (Monthly Scale: 4,000,000 Turns)")
    
    naive_monthly_cost = naive.total_cost_usd * monthly_turns
    finops_monthly_cost = finops.total_cost_usd * monthly_turns
    savings_monthly = naive_monthly_cost - finops_monthly_cost
    savings_pct = (savings_monthly / naive_monthly_cost) * 100.0
    
    print(f"{'Metric':<34} | {'Unmanaged Naive':<18} | {'FinOps-Governed':<18} | {'Delta / Variance':<16}")
    print("-" * 92)
    print(f"{'Cost Per Single Turn':<34} | ${naive.total_cost_usd:<17.6f} | ${finops.total_cost_usd:<17.6f} | -{savings_pct:.1f}%")
    print(f"{'Cost Per 1,000 Turns':<34} | ${naive.total_cost_usd*1000:<17.2f} | ${finops.total_cost_usd*1000:<17.2f} | -{savings_pct:.1f}%")
    print(f"{'Monthly Spend (4M Turns)':<34} | ${naive_monthly_cost:<17,.2f} | ${finops_monthly_cost:<17,.2f} | -${savings_monthly:,.2f}")
    print(f"{'Annual Run-Rate Spend':<34} | ${naive_monthly_cost*12:<17,.2f} | ${finops_monthly_cost*12:<17,.2f} | -${savings_monthly*12:,.2f}")
    print(f"{'Token Amplification Factor (TAF)':<34} | {naive.token_amplification_factor:<17.2f}x | {finops.token_amplification_factor:<17.2f}x | -{naive.token_amplification_factor - finops.token_amplification_factor:.2f}x")
    print(f"{'Non-Functional Token Ratio':<34} | {naive.non_functional_token_ratio:<17.1f}% | {finops.non_functional_token_ratio:<17.1f}% | -{naive.non_functional_token_ratio - finops.non_functional_token_ratio:.1f}%")
    print(f"{'Non-Functional Cost Ratio':<34} | {naive.non_functional_cost_ratio:<17.1f}% | {finops.non_functional_cost_ratio:<17.1f}% | -{naive.non_functional_cost_ratio - finops.non_functional_cost_ratio:.1f}%")
    print("-" * 92)
    print(f"\n💰 NET ANNUAL BOTTOM-LINE SAVINGS: ${savings_monthly * 12:,.2f} / YEAR")

def export_report_json(naive: TurnSimulationResult, finops: TurnSimulationResult, out_path: str = "finops_simulation_report.json"):
    data = {
        "monthly_turns": 4_000_000,
        "naive_harness": {
            "tokens_per_turn": naive.total_tokens,
            "cost_per_turn_usd": naive.total_cost_usd,
            "monthly_cost_usd": naive.total_cost_usd * 4_000_000,
            "taf": naive.token_amplification_factor,
            "non_functional_token_ratio_pct": naive.non_functional_token_ratio,
            "non_functional_cost_ratio_pct": naive.non_functional_cost_ratio,
            "breakdown": naive.get_category_breakdown()
        },
        "finops_harness": {
            "tokens_per_turn": finops.total_tokens,
            "cost_per_turn_usd": finops.total_cost_usd,
            "monthly_cost_usd": finops.total_cost_usd * 4_000_000,
            "taf": finops.token_amplification_factor,
            "non_functional_token_ratio_pct": finops.non_functional_token_ratio,
            "non_functional_cost_ratio_pct": finops.non_functional_cost_ratio,
            "breakdown": finops.get_category_breakdown()
        },
        "monthly_savings_usd": (naive.total_cost_usd - finops.total_cost_usd) * 4_000_000,
        "savings_percentage": ((naive.total_cost_usd - finops.total_cost_usd) / naive.total_cost_usd) * 100.0
    }
    with open(out_path, "w") as f:
        json.dump(data, f, indent=2)
    print(f"\n[Artifact Saved] JSON analysis report generated at: {out_path}")

def main():
    print_header("FinOps for Agentic Harness: Non-Functional Cost Simulation")
    naive_res = simulate_naive_harness(frontier_model="gpt-4o")
    finops_res = simulate_finops_harness(frontier_model="gpt-4o", eval_sampling_rate=0.05)
    
    print_turn_breakdown(naive_res)
    print_turn_breakdown(finops_res)
    print_executive_comparison(naive_res, finops_res, monthly_turns=4_000_000)
    
    export_path = Path(__file__).parent / "finops_simulation_report.json"
    export_report_json(naive_res, finops_res, str(export_path))

if __name__ == "__main__":
    main()
