# rag_engine/utils/formatting.py

def style_resume_for_display(content: str) -> str:
    styled = ""
    for line in content.strip().split("\n"):
        if line.strip().isupper() or ":" in line:
            styled += f"**{line.strip()}**\n"
        else:
            styled += f"{line.strip()}\n"
    return styled.strip()
