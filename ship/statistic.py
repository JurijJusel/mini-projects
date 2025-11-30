from typing import List


def calculate_statistics(results: List[str]) -> dict:
    """
    Skaičiuoja šaudymo statistiką iš rezultatų sąrašo.

    Args:
        results (List[str]): šūvių rezultatų sąrašas (pvz. ["Miss(A,1)", "Hit(B,2)", ...])
        FROM
    Returns:
        dict: {
            'first_hit_shot': int - kuris šūvis buvo pirmas pataikymas,
            'total_shots': int - viso šūvių,
            'hits': int - pataikytų šūvių (Hit + Sunk),
            'misses': int - praėjusių šūvių (Miss),
            'ships': int - laivų kiekis,
            'already': int - jau šautų pozicijų,
            'hit_percentage': float - pataikymo procentas,
            'miss_percentage': float - praėjimo procentas
        }
    """
    total_shots = len(results)

    # Hit ir Sunk = pataikymai
    hits = sum(1 for shot in results if "Hit" in shot or "Sunk" in shot)
    misses = sum(1 for shot in results if "Miss" in shot)
    sunks = sum(1 for shot in results if "Sunk" in shot)  # Kiek laivų paskandinta
    already = sum(1 for shot in results if "Already" in shot)

    # Pirmas pataikymas
    first_hit_shot = None
    for i, shot in enumerate(results, start=1):
        if "Hit" in shot or "Sunk" in shot:
            first_hit_shot = i
            break

    # Procentai (skaičiuojame tik iš Hit, Sunk, Miss - be Already)
    actual_shots = total_shots - already

    hit_percentage = (hits / actual_shots * 100) if actual_shots > 0 else 0
    miss_percentage = (misses / actual_shots * 100) if actual_shots > 0 else 0

    return {
        'first_hit_shot': first_hit_shot,
        'total_shots': total_shots,
        'hits': hits,
        'misses': misses,
        'ships': sunks,
        'already': already,
        'hit_percentage': round(hit_percentage, 2),
        'miss_percentage': round(miss_percentage, 2)
    }


def print_statistics(results: List[str]):
    """
    Atspausdina gražią statistikos lentelę iš rezultatų sąrašo.

    Args:
        results (List[str]): šūvių rezultatų sąrašas
    """
    stats = calculate_statistics(results)

    print("\n" + "="*40)
    print("📊 ŠAUDYMO STATISTIKA")
    print("="*40)
    print(f"🎯 Pirmas pataikymas: {stats['first_hit_shot']} šūvis")
    print(f"📍 Viso šūvių: {stats['total_shots']}")
    print(f"✅ Pataikyta (Hit + Sunk): {stats['hits']}")
    print(f"💥 Paskandinta laivų: {stats['ships']}")
    print(f"❌ Praėjo (Miss): {stats['misses']}")
    print(f"🔁 Jau šautas (Already): {stats['already']}")
    print(f"📈 Pataikymo %: {stats['hit_percentage']}%")
    print(f"📉 Praėjimo %: {stats['miss_percentage']}%")
    print("="*40 + "\n")
