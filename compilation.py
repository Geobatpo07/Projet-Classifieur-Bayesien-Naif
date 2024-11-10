# Représentation des données sous forme de liste de dictionnaires
from data import data

# Fonction pour calculer les probabilités à partir des données
def calculate_probabilities(data):
    # Initialiser les compteurs
    total_entries = len(data)
    achat_count = sum(1 for entry in data if entry['achat'])
    non_achat_count = total_entries - achat_count

    # Probabilités a priori
    P_achat = achat_count / total_entries
    P_non_achat = non_achat_count / total_entries

    # Comptages pour probabilités conditionnelles
    pas_cher_given_achat = sum(1 for entry in data if entry['pas_cher'] and entry['achat'])
    pas_cher_given_non_achat = sum(1 for entry in data if entry['pas_cher'] and not entry['achat'])
    anglais_given_achat = sum(1 for entry in data if entry['anglais'] and entry['achat'])
    anglais_given_non_achat = sum(1 for entry in data if entry['anglais'] and not entry['achat'])

    # Calcul des probabilités conditionnelles avec lissage de Laplace
    P_pas_cher_given_achat = (pas_cher_given_achat + 1) / (achat_count + 2)
    P_pas_cher_given_non_achat = (pas_cher_given_non_achat + 1) / (non_achat_count + 2)
    P_anglais_given_achat = (anglais_given_achat + 1) / (achat_count + 2)
    P_anglais_given_non_achat = (anglais_given_non_achat + 1) / (non_achat_count + 2)

    return {
        'P_achat': P_achat,
        'P_non_achat': P_non_achat,
        'P_pas_cher_given_achat': P_pas_cher_given_achat,
        'P_pas_cher_given_non_achat': P_pas_cher_given_non_achat,
        'P_anglais_given_achat': P_anglais_given_achat,
        'P_anglais_given_non_achat': P_anglais_given_non_achat
    }

# Fonction pour faire une prédiction en utilisant le classifieur bayésien naïf
def predict(data, pas_cher, anglais):
    # Calcul des probabilités
    probs = calculate_probabilities(data)

    # Appliquer la formule de Bayes pour calculer les probabilités a posteriori
    P_achat_given_search = (probs['P_achat'] * probs['P_pas_cher_given_achat'] * probs['P_anglais_given_achat'])
    P_non_achat_given_search = (probs['P_non_achat'] * probs['P_pas_cher_given_non_achat'] * probs['P_anglais_given_non_achat'])

    # Normaliser les probabilités
    total_prob = P_achat_given_search + P_non_achat_given_search
    P_achat_given_search /= total_prob
    P_non_achat_given_search /= total_prob

    # Prédire l'achat si la probabilité d'achat est plus grande que celle de non-achat
    return "Envoyer la publicité" if P_achat_given_search > P_non_achat_given_search else "Ne pas envoyer la publicité"

# Exemple de prédiction pour une recherche contenant "pas cher" et "anglais"
print(predict(data, pas_cher=True, anglais=True))



def calculate_probabilities(data):
    total = len(data)
    achat_count = sum([1 for entry in data if entry["achat"]])
    non_achat_count = total - achat_count

    # Probabilité prioritaire pour achat et non-achat
    prob_achat = achat_count / total
    prob_non_achat = non_achat_count / total

    return prob_achat, prob_non_achat


def calculate_conditional_probabilities(data):
    # Comptage des occurrences pour chaque combinaison
    count = {
        "achat": {"pas_cher": 0, "anglais": 0, "total": 0},
        "non_achat": {"pas_cher": 0, "anglais": 0, "total": 0}
    }

    for entry in data:
        if entry["achat"]:
            count["achat"]["total"] += 1
            count["achat"]["pas_cher"] += entry["pas_cher"]
            count["achat"]["anglais"] += entry["anglais"]
        else:
            count["non_achat"]["total"] += 1
            count["non_achat"]["pas_cher"] += entry["pas_cher"]
            count["non_achat"]["anglais"] += entry["anglais"]

    # Probabilités conditionnelles
    prob_pas_cher_given_achat = count["achat"]["pas_cher"] / count["achat"]["total"]
    prob_anglais_given_achat = count["achat"]["anglais"] / count["achat"]["total"]

    prob_pas_cher_given_non_achat = count["non_achat"]["pas_cher"] / count["non_achat"]["total"]
    prob_anglais_given_non_achat = count["non_achat"]["anglais"] / count["non_achat"]["total"]

    return {
        "achat": {"pas_cher": prob_pas_cher_given_achat, "anglais": prob_anglais_given_achat},
        "non_achat": {"pas_cher": prob_pas_cher_given_non_achat, "anglais": prob_anglais_given_non_achat}
    }


def predict(query, prob_achat, prob_non_achat, conditional_probs):
    # Probabilité de chaque classe pour cette recherche
    prob_if_achat = prob_achat
    prob_if_non_achat = prob_non_achat

    # Probabilité conditionnelle selon les mots de la recherche
    for word, present in query.items():
        if present:
            prob_if_achat *= conditional_probs["achat"][word]
            prob_if_non_achat *= conditional_probs["non_achat"][word]
        else:
            # On utilise 1 - probabilité pour les mots absents
            prob_if_achat *= (1 - conditional_probs["achat"][word])
            prob_if_non_achat *= (1 - conditional_probs["non_achat"][word])

    return "achat" if prob_if_achat > prob_if_non_achat else "non_achat"

def calculate_probabilities(data):
    total = len(data)
    achat_count = sum([1 for entry in data if entry["achat"]])
    non_achat_count = total - achat_count

    # Probabilités a priori pour achat et non-achat
    prob_achat = achat_count / total
    prob_non_achat = non_achat_count / total

    return prob_achat, prob_non_achat

def calculate_conditional_probabilities(data):
    # Initialise le comptage avec lissage de Laplace
    count = {
        "achat": {"pas_cher": 1, "anglais": 1, "total": 2},  # Laplace: initialise à 1 et total à 2 (ajoute vocab_size)
        "non_achat": {"pas_cher": 1, "anglais": 1, "total": 2}
    }

    for entry in data:
        if entry["achat"]:
            count["achat"]["total"] += 1
            count["achat"]["pas_cher"] += entry["pas_cher"]
            count["achat"]["anglais"] += entry["anglais"]
        else:
            count["non_achat"]["total"] += 1
            count["non_achat"]["pas_cher"] += entry["pas_cher"]
            count["non_achat"]["anglais"] += entry["anglais"]

    # Taille du vocabulaire pour le lissage
    vocab_size = 2  # "pas_cher" et "anglais"

    # Probabilités conditionnelles avec lissage de Laplace
    prob_pas_cher_given_achat = count["achat"]["pas_cher"] / (count["achat"]["total"] + vocab_size)
    prob_anglais_given_achat = count["achat"]["anglais"] / (count["achat"]["total"] + vocab_size)

    prob_pas_cher_given_non_achat = count["non_achat"]["pas_cher"] / (count["non_achat"]["total"] + vocab_size)
    prob_anglais_given_non_achat = count["non_achat"]["anglais"] / (count["non_achat"]["total"] + vocab_size)

    return {
        "achat": {"pas_cher": prob_pas_cher_given_achat, "anglais": prob_anglais_given_achat},
        "non_achat": {"pas_cher": prob_pas_cher_given_non_achat, "anglais": prob_anglais_given_non_achat}
    }

def predict(query, prob_achat, prob_non_achat, conditional_probs):
    # Probabilité de chaque classe pour cette recherche
    prob_if_achat = prob_achat
    prob_if_non_achat = prob_non_achat

    # Probabilités conditionnelles selon les mots de la recherche
    for word, present in query.items():
        if present:
            prob_if_achat *= conditional_probs["achat"].get(word, 1 / (conditional_probs["achat"]["total"] + 2))  # Ajout du lissage
            prob_if_non_achat *= conditional_probs["non_achat"].get(word, 1 / (conditional_probs["non_achat"]["total"] + 2))
        else:
            prob_if_achat *= (1 - conditional_probs["achat"].get(word, 1 / (conditional_probs["achat"]["total"] + 2)))
            prob_if_non_achat *= (1 - conditional_probs["non_achat"].get(word, 1 / (conditional_probs["non_achat"]["total"] + 2)))

    return "achat" if prob_if_achat > prob_if_non_achat else "non_achat"


def parse_query_from_text(text):
    """
    Analyse le texte de l'utilisateur et identifie la présence de mots-clés.
    Retourne un dictionnaire de requête avec des indicateurs booléens pour chaque mot-clé.
    """
    keywords = {
        "pas_cher": any(word in text.lower() for word in ["pas cher", "bon marché", "économique"]),
        "anglais": any(word in text.lower() for word in ["anglais", "english"])
    }
    return keywords







# main.py

from data import data
from index import calculate_probabilities, calculate_conditional_probabilities, predict, parse_query_from_text

def main():
    # Calcul des probabilités a priori pour achat et non-achat
    prob_achat, prob_non_achat = calculate_probabilities(data)
    print(f"Probabilité d'achat: {prob_achat}")
    print(f"Probabilité de non-achat: {prob_non_achat}")

    # Calcul des probabilités conditionnelles avec le lissage de Laplace
    conditional_probs = calculate_conditional_probabilities(data)
    print("Probabilités conditionnelles :")
    print(conditional_probs)

    # Demander à l'utilisateur d'entrer une phrase de requête
    user_input = input("Entrez une description de l'objet que vous cherchez : ")
    query = parse_query_from_text(user_input)

    # Prédire le résultat d'achat ou de non-achat
    result = predict(query, prob_achat, prob_non_achat, conditional_probs)
    print("Résultat de la prédiction :", result)

if __name__ == "__main__":
    main()







# Liste des données représentant les recherches des utilisateurs
# Chaque dictionnaire contient les informations suivantes :
# - 'pas_cher' : True si le terme "pas cher" est présent, False sinon
# - 'anglais' : True si le terme "anglais" est présent, False sinon
# - 'achat' : True si l'utilisateur a effectué un achat, False sinon

data = [
    {'pas_cher': True, 'anglais': False, 'achat': True},   # Recherche pour un pantalon pas cher, achat effectué
    {'pas_cher': False, 'anglais': True, 'achat': False},  # Recherche pour un pantalon en anglais, pas d'achat
    {'pas_cher': False, 'anglais': True, 'achat': False},  # Recherche pour un pantalon en anglais, pas d'achat
    {'pas_cher': False, 'anglais': True, 'achat': False},  # Recherche pour un pantalon en anglais, pas d'achat
    {'pas_cher': True, 'anglais': False, 'achat': False},  # Recherche pour un pantalon pas cher, pas d'achat
    {'pas_cher': True, 'anglais': True, 'achat': True},    # Recherche pour un pantalon pas cher et en anglais, achat effectué
    {'pas_cher': True, 'anglais': False, 'achat': True},   # Recherche pour un pantalon pas cher, achat effectué
    {'pas_cher': True, 'anglais': False, 'achat': True}    # Recherche pour un pantalon pas cher, achat effectué
]



vocab = 2  # Le vocabulaire contient deux mots-clés : pas_cher, anglais

def calculer_probabilite(data):
    total_cardinal = len(data)
    qte_achat = sum(1 for entree in data if entree['achat'])
    qte_non_achat = total_cardinal - qte_achat

    prob_achat = qte_achat / total_cardinal
    prob_non_achat = qte_non_achat / total_cardinal

    return prob_achat, prob_non_achat

def calculer_probabilite_conditionnelle(data):
    # Initialisation du comptage avec le lissage de Laplace
    count = {'achat': {'pas_cher': 1, 'anglais': 1, 'total': 2},  # +1 pour chaque mot-clé, et +1 pour le total
             'non_achat': {'pas_cher': 1, 'anglais': 1, 'total': 2}  # même logique pour le non-achat
             }

    # Calcul des fréquences conditionnelles
    for entree in data:
        if entree['achat']:
            count['achat']['total'] += 1
            count['achat']['pas_cher'] += entree['pas_cher']
            count['achat']['anglais'] += entree['anglais']
        else:
            count['non_achat']['total'] += 1
            count['non_achat']['pas_cher'] += entree['pas_cher']
            count['non_achat']['anglais'] += entree['anglais']

    # Probabilités conditionnelles avec lissage de Laplace
    prob_pas_cher_sachant_achat = count['achat']['pas_cher'] / (count['achat']['total'] + vocab)
    prob_anglais_sachant_achat = count['achat']['anglais'] / (count['achat']['total'] + vocab)

    prob_pas_cher_sachant_non_achat = count['non_achat']['pas_cher'] / (count['non_achat']['total'] + vocab)
    prob_anglais_sachant_non_achat = count['non_achat']['anglais'] / (count['non_achat']['total'] + vocab)

    return {
        'achat': {'pas_cher': prob_pas_cher_sachant_achat, 'anglais': prob_anglais_sachant_achat},
        'non_achat': {'pas_cher': prob_pas_cher_sachant_non_achat, 'anglais': prob_anglais_sachant_non_achat}
    }

def predire(query, prob_achat, prob_non_achat, proba_conditionnelle):
    prob_si_achat = prob_achat
    prob_si_non_achat = prob_non_achat

    # Calcul des probabilités conditionnelles en fonction de la requête
    for mot, present in query.items():
        if present:
            prob_si_achat *= proba_conditionnelle['achat'].get(mot, 1 / (proba_conditionnelle['achat']['total'] + vocab))
            prob_si_non_achat *= proba_conditionnelle['non_achat'].get(mot, 1 / (proba_conditionnelle['non_achat']['total'] + vocab))
        else:
            prob_si_achat *= (1 - proba_conditionnelle['achat'].get(mot, 1 / (proba_conditionnelle['achat']['total'] + vocab)))
            prob_si_non_achat *= (1 - proba_conditionnelle['non_achat'].get(mot, 1 / (proba_conditionnelle['non_achat']['total'] + vocab)))

    # Retourne la classe avec la probabilité la plus élevée
    return "achat" if prob_si_achat > prob_si_non_achat else "non_achat"

def parse_query_to_text(query):
    mots_cle = {
        'pas_cher': any(mot in query.lower() for mot in ['pas cher', 'bon marché', 'bas prix']),
        'anglais': any(mot in query.lower() for mot in ['anglais', 'english'])
    }
    return mots_cle
