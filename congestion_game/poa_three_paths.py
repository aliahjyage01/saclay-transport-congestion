import numpy as np
import matplotlib.pyplot as plt

# --- 1. Définition des Coûts Unitaires (Latences c_e(x)) ---
# Ces fonctions décrivent le prix payé par un utilisateur sur un chemin donné.
# Elles sont déduites de votre fonction manuscrite (qui est le Potentiel).

def c_x(x):
    # Chemin X : 25 jusqu'à 40, puis 27, puis 37 au-delà de 100
    if x <= 40: return 25
    elif x <= 100: return 27
    else: return 37

def c_y(y):
    # Chemin Y : 27 jusqu'à 40, puis 37
    if y <= 40: return 27
    else: return 37

def c_z(z):
    # Chemin Z : 10 jusqu'à 96, puis 12, puis 15 au-delà de 400
    if z <= 96: return 10
    elif z <= 400: return 12
    else: return 15

# --- 2. Fonctions Objectifs (Définitions du Cours) ---

def social_cost(x, y, z):
    """
    Coût Social Total (Slide 35).
    C'est ce que l'OPTIMUM cherche à minimiser.
    Formule : Somme des (Flux * Latence).
    """
    cost_x = x * c_x(x) if x > 0 else 0
    cost_y = y * c_y(y) if y > 0 else 0
    cost_z = z * c_z(z) if z > 0 else 0
    return cost_x + cost_y + cost_z

# --- 3. Calcul du PoA ---

n_values = range(1, 451)
poa_values = []

print("Calcul en cours...")

for n in n_values:
    # --- A. Équilibre de Nash (NE) ---
    # Propriété : Dans un jeu de congestion atomique, l'équilibre de Nash
    # est atteint quand chaque nouvel utilisateur choisit le chemin le moins cher
    # pour LUI (Greedy Approach). Cela minimise la fonction de Potentiel (Slide 20).
    
    x_ne, y_ne, z_ne = 0, 0, 0
    for _ in range(n):
        # Quel sera mon coût si je vais sur X, Y ou Z ?
        cost_if_x = c_x(x_ne + 1)
        cost_if_y = c_y(y_ne + 1)
        cost_if_z = c_z(z_ne + 1)
        
        # Je choisis le moins cher (Meilleure réponse)
        if cost_if_z <= cost_if_x and cost_if_z <= cost_if_y:
            z_ne += 1
        elif cost_if_x <= cost_if_y:
            x_ne += 1
        else:
            y_ne += 1
            
    # On calcule le Coût Social de cet état d'équilibre
    cs_nash = social_cost(x_ne, y_ne, z_ne)

    # --- B. Optimum Social (SO) ---
    # On cherche la répartition (x, y, z) qui minimise le Coût Social Total.
    # Comme la fonction n'est pas parfaitement convexe (sauts), on fait une 
    # recherche exhaustive intelligente pour être sûr du résultat.
    
    min_cs = float('inf')
    
    # On limite la recherche car on sait que Z est dominant (moins cher).
    # X et Y ne prendront jamais plus de 200 passagers vu leurs coûts.
    limit = min(n, 200)
    
    for x in range(limit + 1):
        remaining = n - x
        for y in range(min(remaining, 150) + 1):
            z = remaining - y
            current_cs = social_cost(x, y, z)
            if current_cs < min_cs:
                min_cs = current_cs
    
    cs_opt = min_cs

    # --- C. Ratio PoA ---
    poa = cs_nash / cs_opt
    poa_values.append(poa)

# --- 4. Affichage ---
plt.figure(figsize=(10, 6))
plt.plot(n_values, poa_values, label='Price of Anarchy (PoA)', color='blue', linewidth=2)

# Repères visuels pour l'explication
plt.axvline(x=97, color='red', linestyle=':', label='Saut Z (96->97)')
plt.axvline(x=401, color='red', linestyle=':', label='Saut Z (400->401)')

plt.xlabel('Population totale ($n$)')
plt.ylabel('Price of Anarchy')
plt.title('Évolution du PoA (Conforme aux définitions du cours)')
plt.legend()
plt.grid(True, alpha=0.3)

plt.show()