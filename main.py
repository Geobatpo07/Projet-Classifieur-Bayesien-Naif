from data import data
from index import calculer_probabilite, calculer_probabilite_conditionnelle, predire, parse_query_to_text

def main():
    prob_achat, prob_non_achat = calculer_probabilite(data)
    print(f'Les probabilités d\'achat et de non-achat sont respectivement: {prob_achat} et {prob_non_achat}.')

    probabilite_conditionnelle = calculer_probabilite_conditionnelle(data)
    print('Les probabilités conditionnelles sont:')
    print(probabilite_conditionnelle)

    requete = input('Entrez une description de l\'objet que vous recherchez:')
    requete = parse_query_to_text(requete)

    result = predire(requete, prob_achat, prob_non_achat, probabilite_conditionnelle)
    print(result)

if __name__ == '__main__':
    main()