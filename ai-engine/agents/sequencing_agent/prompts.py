# Sequencing is deterministic (arc-shape scoring over energy proxies), no
# LLM call is required for ordering itself. Reserved for an optional
# natural-language description of the arc shown in the UI.
ARC_DESCRIPTION_PROMPT = """Describe this listening arc in one sentence:
{arc_label}, starting energy {start_energy}, peak energy {peak_energy},
ending energy {end_energy}."""
