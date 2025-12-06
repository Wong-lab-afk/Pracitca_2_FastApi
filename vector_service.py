def get_vector(text: str) -> list[float]:
    # Implementación simple sugerida: longitud del texto
    return [float(len(text))]

def calculate_similarity(vec_a: list[float], vec_b: list[float]) -> float:
    if not vec_a or not vec_b or vec_a[0] == 0 or vec_b[0] == 0:
        return 0.0
    # Fórmula simple del PDF [cite: 93]
    return 1 - abs(vec_a[0] - vec_b[0]) / max(vec_a[0], vec_b[0])