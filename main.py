#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Калькулятор молярной массы и массовых долей с детальным выводом атомных масс.
"""

import re

# Атомные массы (г/моль)
ATOMIC_MASSES = {
    'H': 1.008, 'He': 4.0026, 'Li': 6.94, 'Be': 9.0122, 'B': 10.81,
    'C': 12.011, 'N': 14.007, 'O': 15.999, 'F': 18.998, 'Ne': 20.180,
    'Na': 22.990, 'Mg': 24.305, 'Al': 26.982, 'Si': 28.085, 'P': 30.974,
    'S': 32.065, 'Cl': 35.45, 'Ar': 39.948, 'K': 39.098, 'Ca': 40.078,
    'Sc': 44.956, 'Ti': 47.867, 'V': 50.942, 'Cr': 51.996, 'Mn': 54.938,
    'Fe': 55.845, 'Co': 58.933, 'Ni': 58.693, 'Cu': 63.546, 'Zn': 65.38,
    'Ga': 69.723, 'Ge': 72.630, 'As': 74.922, 'Se': 78.971, 'Br': 79.904,
    'Kr': 83.798, 'Rb': 85.468, 'Sr': 87.62, 'Y': 88.906, 'Zr': 91.224,
    'Nb': 92.906, 'Mo': 95.95, 'Tc': 98, 'Ru': 101.07, 'Rh': 102.91,
    'Pd': 106.42, 'Ag': 107.87, 'Cd': 112.41, 'In': 114.82, 'Sn': 118.71,
    'Sb': 121.76, 'Te': 127.60, 'I': 126.90, 'Xe': 131.29, 'Cs': 132.91,
    'Ba': 137.33, 'La': 138.91, 'Ce': 140.12, 'Pr': 140.91, 'Nd': 144.24,
    'Pm': 145, 'Sm': 150.36, 'Eu': 151.96, 'Gd': 157.25, 'Tb': 158.93,
    'Dy': 162.50, 'Ho': 164.93, 'Er': 167.26, 'Tm': 168.93, 'Yb': 173.05,
    'Lu': 174.97, 'Hf': 178.49, 'Ta': 180.95, 'W': 183.84, 'Re': 186.21,
    'Os': 190.23, 'Ir': 192.22, 'Pt': 195.08, 'Au': 196.97, 'Hg': 200.59,
    'Tl': 204.38, 'Pb': 207.2, 'Bi': 208.98, 'Po': 209, 'At': 210,
    'Rn': 222, 'Fr': 223, 'Ra': 226, 'Ac': 227, 'Th': 232.04,
    'Pa': 231.04, 'U': 238.03, 'Np': 237, 'Pu': 244, 'Am': 243,
    'Cm': 247, 'Bk': 247, 'Cf': 251, 'Es': 252, 'Fm': 257,
    'Md': 258, 'No': 259, 'Lr': 266, 'Rf': 267, 'Db': 268,
    'Sg': 269, 'Bh': 270, 'Hs': 277, 'Mt': 278, 'Ds': 281,
    'Rg': 282, 'Cn': 285, 'Nh': 286, 'Fl': 289, 'Mc': 290,
    'Lv': 293, 'Ts': 294, 'Og': 294
}

def parse_formula(formula: str) -> dict:
    """Разбирает формулу, возвращает словарь {элемент: количество}."""
    formula = formula.replace(' ', '')
    tokens = re.findall(r'[A-Z][a-z]?|[()\[\]]|\d+', formula)
    stack = [{}]
    i = 0
    while i < len(tokens):
        token = tokens[i]
        if token in ('(', '['):
            stack.append({})
            i += 1
        elif token in (')', ']'):
            inner = stack.pop()
            if i + 1 < len(tokens) and tokens[i+1].isdigit():
                multiplier = int(tokens[i+1])
                i += 2
            else:
                multiplier = 1
                i += 1
            current = stack[-1]
            for elem, count in inner.items():
                current[elem] = current.get(elem, 0) + count * multiplier
        else:
            if token.isdigit():
                i += 1
                continue
            else:
                if i + 1 < len(tokens) and tokens[i+1].isdigit():
                    count = int(tokens[i+1])
                    i += 2
                else:
                    count = 1
                    i += 1
                current = stack[-1]
                current[token] = current.get(token, 0) + count
    if len(stack) != 1:
        raise ValueError("Несбалансированные скобки")
    return stack[0]

def molar_mass(formula: str) -> float:
    """Вычисляет молярную массу."""
    elements = parse_formula(formula)
    total = 0.0
    for elem, count in elements.items():
        if elem not in ATOMIC_MASSES:
            raise ValueError(f"Неизвестный элемент: {elem}")
        total += ATOMIC_MASSES[elem] * count
    return total

def get_element_details(formula: str):
    """
    Возвращает список кортежей (элемент, количество, атомная_масса, вклад, доля)
    и общую массу.
    """
    elements = parse_formula(formula)
    total = molar_mass(formula)
    details = []
    for elem, count in elements.items():
        atomic = ATOMIC_MASSES[elem]
        contrib = atomic * count
        fraction = contrib / total if total > 0 else 0
        details.append((elem, count, atomic, contrib, fraction))
    return details, total

def main():
    print("=" * 70)
    print("КАЛЬКУЛЯТОР МОЛЯРНОЙ МАССЫ С ДЕТАЛЬНЫМИ АТОМНЫМИ МАССАМИ")
    print("=" * 70)
    while True:
        print("\nВведите химическую формулу (например, H2O, (NH4)2SO4)")
        print("Или 'exit' для выхода.")
        formula = input("> ").strip()
        if formula.lower() in ('exit', 'quit', 'q'):
            print("До свидания!")
            break
        if not formula:
            continue
        try:
            details, total = get_element_details(formula)
            print(f"\nМолярная масса {formula} = {total:.4f} г/моль")
            print("\nДетали по элементам:")
            print(f"{'Элемент':<8} {'Кол-во':<6} {'A (г/моль)':<12} {'Вклад (г/моль)':<16} {'Массовая доля':<12}")
            print("-" * 70)
            for elem, count, atomic, contrib, frac in details:
                print(f"{elem:<8} {count:<6} {atomic:<12.4f} {contrib:<16.4f} {frac:<12.4%}")
            print("-" * 70)
            print(f"{'Итого':<8} {'':<6} {'':<12} {total:<16.4f} {1.0:<12.4%}")
            
            # Дополнительный запрос на конкретный элемент
            elem_q = input("\nВведите символ элемента для уточнения (или Enter для пропуска): ").strip()
            if elem_q:
                found = False
                for elem, count, atomic, contrib, frac in details:
                    if elem == elem_q:
                        print(f"\nЭлемент {elem}:")
                        print(f"  Атомная масса: {atomic:.4f} г/моль")
                        print(f"  Количество атомов: {count}")
                        print(f"  Вклад в общую массу: {contrib:.4f} г/моль")
                        print(f"  Массовая доля: {frac:.4%}")
                        found = True
                        break
                if not found:
                    print(f"Элемент '{elem_q}' не найден в формуле.")
        except Exception as e:
            print(f"Ошибка: {e}")

if __name__ == "__main__":
    main()