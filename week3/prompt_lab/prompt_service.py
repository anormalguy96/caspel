def get_temperature(mode: str) -> float:
    """Mode-a uyğun temperatur qaytarır."""
    modes = {
        "factual": 0.1,
        "balanced": 0.7,
        "creative": 1.0
    }
    return modes.get(mode.lower(), 0.7)


def get_system_prompt(mode: str) -> str:
    """Mode-a uyğun sistem promptunu qaytarır."""
    mode_lower = mode.lower()
    
    if mode_lower == "factual":
        return (
            "Azərbaycan dilində cavab ver.\n"
            "Əmin olmadığın faktları uydurma.\n"
            "Məlumatı bilmirsənsə bunu açıq şəkildə bildir."
        )
    elif mode_lower == "creative":
        return (
            "Azərbaycan dilində cavab ver.\n"
            "Yaradıcı, zəngin və müxtəlif nümunələrdən istifadə et."
        )
    else:  # balanced
        return "Azərbaycan dilində aydın, dəqiq və faydalı cavab ver."


def get_grounded_system_prompt() -> str:
    """Hallusinasiyanın qarşısını alan ciddi Grounded sistem promptu."""
    return (
        "Yalnız verilmiş CONTEXT əsasında cavab ver.\n"
        "Cavab context-də yoxdursa:\n"
        "\"Məlumat təqdim olunan kontekstdə yoxdur.\"\n"
        "de.\n"
        "Heç bir fakt uydurma."
    )


def build_grounded_user_prompt(context: str, question: str) -> str:
    """Context və Question-u vahid prompt şablonuna salır."""
    return f"CONTEXT:\n{context}\n\nQUESTION:\n{question}"
