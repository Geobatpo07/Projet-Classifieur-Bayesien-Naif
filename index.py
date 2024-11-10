vocab = 2

def calculer_probabilite(data):
    total_cardinal = len(data)
    qte_achat = sum(1 for entree in data if entree['achat'])
    qte_non_achat = total_cardinal - qte_achat

    prob_achat = qte_achat / total_cardinal
    prob_non_achat = qte_non_achat / total_cardinal

    return prob_achat, prob_non_achat

def calculer_probabilite_conditionnelle(data):
    count = {'achat': {'pas_cher': 1, 'anglais': 1, 'total': 2},
             'non_achat': {'pas_cher': 1, 'anglais': 1, 'total': 2}
    }

    for entree in data:
        if entree['achat']:
            count['achat']['total'] += 1
            count['achat']['pas_cher'] += entree['pas_cher']
            count['achat']['anglais'] += entree['anglais']
        else:
            count['non_achat']['total'] += 1
            count['non_achat']['pas_cher'] += entree['pas_cher']
            count['non_achat']['anglais'] += entree['anglais']

    prob_pas_cher_sachant_achat = count['achat']['pas_cher'] / (count['achat']['total'] + vocab)
    prob_anglais_sachant_achat = count['achat']['anglais'] / (count['achat']['total'] + vocab)

    prob_pas_cher_sachant_non_achat = count['non_achat']['pas_cher'] / (count['non_achat']['total'] + vocab)
    prob_anglais_sachant_non_achat = count['non_achat']['anglais'] / (count['non_achat']['total'] + vocab)

    return {'achat': {'pas_cher': prob_pas_cher_sachant_achat, 'anglais': prob_anglais_sachant_achat, 'total': prob_pas_cher_sachant_achat + prob_anglais_sachant_achat},
            'non_achat': {'pas_cher': prob_pas_cher_sachant_non_achat, 'anglais': prob_anglais_sachant_non_achat, 'total': prob_pas_cher_sachant_non_achat + prob_anglais_sachant_non_achat},
            }

def predire(query, prob_achat, prob_non_achat, proba_conditionnelle):
    prob_si_achat = prob_achat
    prob_si_non_achat = prob_non_achat

    for mot, present in query.items():
        if present:
            prob_si_achat *= proba_conditionnelle['achat'].get(mot, 1 / (proba_conditionnelle['achat']['total'] + vocab))
            prob_si_non_achat *= proba_conditionnelle['non_achat'].get(mot, 1 / (proba_conditionnelle['non_achat']['total'] + vocab))
        else:
            prob_si_achat *= (1 - proba_conditionnelle['achat'].get(mot, 1 / (proba_conditionnelle['achat']['total'] + vocab)))
            prob_si_non_achat *= (1 - proba_conditionnelle['non_achat'].get(mot, 1 / (proba_conditionnelle['non_achat']['total'] + vocab)))

    return "achat" if prob_si_achat > prob_si_non_achat else "non_achat"

def parse_query_to_text(query):
    mots_cle = {
        'pas_cher': any(mot in query.lower() for mot in ['pas cher', 'bon marché', 'bon marche', 'bas prix']),
        'anglais': any(mot in query.lower() for mot in ['anglais', 'english'])
    }
    return mots_cle



