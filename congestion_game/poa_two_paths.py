import numpy as np
import matplotlib.pyplot as plt

# --- 1. Définition des Coûts Unitaires (Latences) ---
# Tirés de l'analyse du document EI.pdf
# Chemin 1 (x) : Coûts marginaux de 25, 27, 37
# Chemin 2 (y) : Coûts marginaux de 27, 29, 37

def c1(x):
    if x <= 40: return 25
    elif x <= 100: return 27
    else: return 37

def c2(y):
    if y <= 40: return 27
    elif y <= 100: return 29
    else: return 37

# --- 2. Fonction de Coût Social Total ---
# C'est la fonction que l'OPTIMUM cherche à minimiser.
# Formule : x * c1(x) + y * c2(y)

def total_social_cost(x, y):
    cost_x = x * c1(x) if x > 0 else 0
    cost_y = y * c2(y) if y > 0 else 0
    return cost_x + cost_y

# --- 3. Calcul du PoA ---

n_values = range(1, 251) # On regarde jusqu'à n=250
poa_values = []

print("Calcul en cours pour le modèle à 2 chemins (sans métro)...")

for n in n_values:
    # A. Équilibre de Nash (Approche Gloutonne / Minimisation du Potentiel)
    # Les utilisateurs arrivent un par un et choisissent le chemin le moins cher
    x_ne, y_ne = 0, 0
    for _ in range(n):
        # Coût marginal pour le prochain utilisateur
        cost_next_x = c1(x_ne + 1)
        cost_next_y = c2(y_ne + 1)
        
        # Choix égoïste
        if cost_next_x <= cost_next_y:
            x_ne += 1
        else:
            y_ne += 1
            
    # Calcul du coût social subit à l'équilibre de Nash
    cs_nash = total_social_cost(x_ne, y_ne)
    
    # B. Optimum Social (Recherche du minimum global)
    # On teste toutes les répartitions (x, y) possibles pour n personnes
    min_cs = float('inf')
    
    for x in range(n + 1):
        y = n - x
        current_cs = total_social_cost(x, y)
        if current_cs < min_cs:
            min_cs = current_cs
            
    cs_opt = min_cs
    
    # C. Ratio PoA
    poa = cs_nash / cs_opt
    poa_values.append(poa)

# --- 4. Affichage ---
plt.figure(figsize=(10, 6))
plt.plot(n_values, poa_values, label='Price of Anarchy (PoA)', color='green', linewidth=2)

# Annotation des pics (correspondant aux sauts de tarifs)
plt.axvline(x=40, color='red', linestyle=':', alpha=0.5, label='Seuil capacité 40')
plt.axvline(x=100, color='red', linestyle=':', alpha=0.5, label='Seuil capacité 100')

plt.xlabel('Population totale ($n$)')
plt.ylabel('Price of Anarchy')
plt.title('PoA - Cas à 2 Chemins (x, y)')
plt.legend()
plt.grid(True, alpha=0.3)

# Sauvegarde et affichage
plt.savefig('PoA_2chemins.png')
plt.show()

print("Terminé. Regardez les pics aux alentours de n=40 et n=100.")