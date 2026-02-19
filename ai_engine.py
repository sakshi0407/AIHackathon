# ai_engine.py
import json
import time
import re
from gpt4all import GPT4All

# --------------------------------------------------
# CONFIG
# --------------------------------------------------
MODEL_DIR = r"C:\Users\sakshi.suryavanshi\AppData\Local\nomic.ai\GPT4All"
MODEL_NAME = "Llama-3.2-1B-Instruct-Q4_0"

print("[INIT] Loading GPT4All model...")
llm = GPT4All(
    model_name=MODEL_NAME,
    model_path=MODEL_DIR,
    allow_download=False,
    device="cpu"
)
print("[INIT] GPT4All model loaded successfully.")


# --------------------------------------------------
# DETERMINISTIC FINANCIAL LOGIC
# --------------------------------------------------
def calculate_financials(ticket_dict):

    suggested_fix = ""
    amount_impact = 0.0
    highlight_fields = []
    leak_types = set()

    # ---------------- FARE ----------------
    if ticket_dict["Our_Fare"] != ticket_dict["Agent_Fare"]:
        diff = ticket_dict["Our_Fare"] - ticket_dict["Agent_Fare"]
        suggested_fix += f"Collect fare shortfall {abs(diff):.2f}. "
        amount_impact += abs(diff)
        highlight_fields += ["Our_Fare", "Agent_Fare"]
        leak_types.add("fare")

    # ---------------- TAX ZK ----------------
    if ticket_dict.get("NoShow") and ticket_dict.get("Agent_Tax_ZK", 0) > 0:
        suggested_fix += f"Reclaim {ticket_dict['Agent_Tax_ZK']:.2f} ZK tax. "
        amount_impact += ticket_dict["Agent_Tax_ZK"]
        highlight_fields += ["Agent_Tax_ZK"]
        leak_types.add("tax")

    # ---------------- TAX YQ ----------------
    if ticket_dict.get("Our_Tax_YQ", 0) != ticket_dict.get("Agent_Tax_YQ", 0):
        diff = ticket_dict.get("Our_Tax_YQ", 0) - ticket_dict.get("Agent_Tax_YQ", 0)
        suggested_fix += f"Adjust YQ tax by {abs(diff):.2f}. "
        amount_impact += abs(diff)
        highlight_fields += ["Our_Tax_YQ", "Agent_Tax_YQ"]
        leak_types.add("tax")

    # ---------------- COMMISSION ----------------
    if ticket_dict["Tourcode"] == "TC0":
        expected_comm = 0.0
    elif ticket_dict["Tourcode"] == "TC5":
        expected_comm = ticket_dict["Our_Fare"] * 0.05
    else:
        expected_comm = ticket_dict["Our_Fare"] * 0.10

    if abs(ticket_dict["Agent_Comm"] - expected_comm) > 1:
        diff = ticket_dict["Agent_Comm"] - expected_comm
        suggested_fix += f"Adjust commission by {-diff:.2f}. "
        amount_impact += abs(diff)
        highlight_fields += ["Agent_Comm"]
        leak_types.add("commission")

    return {
        "leak_type": "|".join(sorted(leak_types)) if leak_types else "none",
        "suggested_fix": suggested_fix.strip(),
        "amount_impact": round(amount_impact, 2),
        "highlight_fields": list(set(highlight_fields))
    }


# --------------------------------------------------
# Build AI prompt (UNCHANGED)
# --------------------------------------------------
def build_prompt_for_ticket(ticket_dict, rules_dict):
    print("[PROMPT] Building prompt...")

    rules_text = ""
    for key, rules in rules_dict.items():
        rules_text += f"\n{key.upper()}:\n"
        for r in rules:
            rules_text += f"- {r}\n"

    ticket_text = ""
    for k, v in ticket_dict.items():
        ticket_text += f"{k}: {v}\n"

    prompt = f"""
You are an experienced airline revenue auditor.

IMPORTANT:
- Output ONLY valid JSON
- Do NOT explain
- Do NOT add code
- Do NOT add text before or after JSON

You must use the rules and ticket facts below to:
1) Decide status: OK or ERROR
2) Write a short auditor comment
3) Identify ONE primary leak_type
4) Include numeric impact if ERROR

Rules:
{rules_text}

Ticket:
{ticket_text}

Output JSON exactly in this format:
{{
  "status": "OK or ERROR",
  "comment": "human-like explanation",
  "leak_type": "fare | tax | commission | penalty | waiver | proration | none",
  "suggested_fix": "text or empty",
  "amount_impact": number,
  "highlight_fields": []
}}
"""
    print("[PROMPT] Prompt built successfully.")
    return prompt


# --------------------------------------------------
# Analyze a ticket
# --------------------------------------------------
def analyze_ticket(ticket_dict, rules_dict):
    print("[ANALYZE] Starting ticket analysis...")
    prompt = build_prompt_for_ticket(ticket_dict, rules_dict)

    try:
        print("[LLM] Sending prompt to GPT4All...")
        start_time = time.time()

        response = llm.generate(
            prompt,
            max_tokens=250,
            temp=0.0,
            top_k=40,
            top_p=0.9
        )

        elapsed = round(time.time() - start_time, 2)
        print(f"[LLM] Response received in {elapsed} sec")
        print("[LLM RAW OUTPUT]")
        print(response)

        response = response.strip()

        json_matches = re.findall(r"\{.*?\}", response, flags=re.DOTALL)

        if json_matches:
            parsed = json.loads(json_matches[0])
            print("[LLM] JSON parsed successfully.")

            # 🔥 Override financial fields deterministically
            financials = calculate_financials(ticket_dict)

            parsed["leak_type"] = financials["leak_type"]
            parsed["suggested_fix"] = financials["suggested_fix"]
            parsed["amount_impact"] = financials["amount_impact"]
            parsed["highlight_fields"] = financials["highlight_fields"]

            # If no financial impact, force OK
            if parsed["amount_impact"] == 0:
                parsed["status"] = "OK"
                parsed["leak_type"] = "none"

            return parsed

        print("[WARN] No JSON detected.")
        raise ValueError("No JSON detected")

    except Exception as e:
        print("[ERROR] LLM failed:", str(e))
        print("[FALLBACK] Running deterministic audit only.")

        financials = calculate_financials(ticket_dict)

        if financials["amount_impact"] == 0:
            return {
                "status": "OK",
                "comment": "All amounts and rules appear to match. No action required.",
                **financials
            }

        return {
            "status": "ERROR",
            "comment": "Financial discrepancy detected based on audit rules.",
            **financials
        }
