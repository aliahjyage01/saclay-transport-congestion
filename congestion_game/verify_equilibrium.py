"""Controles de validite des deux modeles de jeu de congestion.

Les scripts poa_two_paths.py et poa_three_paths.py calculent l'equilibre de
Nash par insertion gloutonne : les usagers arrivent un par un et chacun prend
le chemin le moins cher a cet instant. Rien ne garantit a priori qu'un usager
arrive tot ne voudrait pas changer une fois tout le monde arrive.

Ce script verifie deux choses :

  1. l'allocation gloutonne satisfait la condition de Nash, c'est-a-dire
     qu'aucun usager ne reduit son cout en changeant unilateralement de chemin ;
  2. la recherche d'optimum social bornee de poa_three_paths.py (x <= 200,
     y <= 150) donne le meme resultat qu'une recherche exhaustive complete.

Il affiche aussi le PoA maximal et la population ou il est atteint.
"""


# --- Modele a 2 chemins (sans metro) ---------------------------------------

def c1(x):
    return 25 if x <= 40 else (27 if x <= 100 else 37)


def c2(y):
    return 27 if y <= 40 else (29 if y <= 100 else 37)


def glouton_2(n):
    x = y = 0
    for _ in range(n):
        if c1(x + 1) <= c2(y + 1):
            x += 1
        else:
            y += 1
    return x, y


def nash_2(x, y):
    """Aucun usager ne gagne a changer de chemin."""
    if x > 0 and c2(y + 1) < c1(x):
        return False
    if y > 0 and c1(x + 1) < c2(y):
        return False
    return True


def cout_2(x, y):
    return (x * c1(x) if x else 0) + (y * c2(y) if y else 0)


def optimum_2(n):
    return min(cout_2(x, n - x) for x in range(n + 1))


# --- Modele a 3 chemins (avec le metro) ------------------------------------

def c_x(x):
    return 25 if x <= 40 else (27 if x <= 100 else 37)


def c_y(y):
    return 27 if y <= 40 else 37


def c_z(z):
    return 10 if z <= 96 else (12 if z <= 400 else 15)


def glouton_3(n):
    x = y = z = 0
    for _ in range(n):
        cx, cy, cz = c_x(x + 1), c_y(y + 1), c_z(z + 1)
        if cz <= cx and cz <= cy:
            z += 1
        elif cx <= cy:
            x += 1
        else:
            y += 1
    return x, y, z


def nash_3(x, y, z):
    actuel = {'x': c_x(x), 'y': c_y(y), 'z': c_z(z)}
    si_jy_vais = {'x': c_x(x + 1), 'y': c_y(y + 1), 'z': c_z(z + 1)}
    for chemin, charge in (('x', x), ('y', y), ('z', z)):
        if charge == 0:
            continue
        for autre in ('x', 'y', 'z'):
            if autre != chemin and si_jy_vais[autre] < actuel[chemin]:
                return False
    return True


def cout_3(x, y, z):
    return ((x * c_x(x) if x else 0)
            + (y * c_y(y) if y else 0)
            + (z * c_z(z) if z else 0))


def optimum_3_borne(n):
    """La recherche telle qu'elle est faite dans poa_three_paths.py."""
    best = float('inf')
    for x in range(min(n, 200) + 1):
        reste = n - x
        for y in range(min(reste, 150) + 1):
            best = min(best, cout_3(x, y, reste - y))
    return best


def optimum_3_complet(n):
    best = float('inf')
    for x in range(n + 1):
        for y in range(n - x + 1):
            best = min(best, cout_3(x, y, n - x - y))
    return best


# --- Controles --------------------------------------------------------------

def main():
    print("=" * 66)
    print(" MODELE A 2 CHEMINS — n de 1 a 250")
    print("=" * 66)
    echecs = [n for n in range(1, 251) if not nash_2(*glouton_2(n))]
    poa = {n: cout_2(*glouton_2(n)) / optimum_2(n) for n in range(1, 251)}
    n_max = max(poa, key=poa.get)
    print(f"  Allocations gloutonnes qui ne sont pas un equilibre : {len(echecs)}")
    print(f"  PoA maximal : {poa[n_max]:.4f}  (atteint a n = {n_max})")

    print()
    print("=" * 66)
    print(" MODELE A 3 CHEMINS — n de 1 a 450")
    print("=" * 66)
    echecs = [n for n in range(1, 451) if not nash_3(*glouton_3(n))]
    ecarts = [n for n in range(1, 451)
              if optimum_3_borne(n) != optimum_3_complet(n)]
    poa = {n: cout_3(*glouton_3(n)) / optimum_3_complet(n)
           for n in range(1, 451)}
    n_max = max(poa, key=poa.get)
    pics = sorted(poa, key=poa.get, reverse=True)[:2]
    print(f"  Allocations gloutonnes qui ne sont pas un equilibre : {len(echecs)}")
    print(f"  n ou la recherche bornee rate l'optimum reel        : {len(ecarts)}")
    print(f"  PoA maximal : {poa[n_max]:.4f}  (atteint a n = {n_max})")
    print(f"  Deux plus hauts pics : "
          + ", ".join(f"n={n} -> {poa[n]:.4f}" for n in sorted(pics)))


if __name__ == "__main__":
    main()
