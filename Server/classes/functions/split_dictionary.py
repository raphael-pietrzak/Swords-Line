import json


def split_dictionary(dictionary, size):
    """
    Splits a dictionary into smaller messages while preserving syntax.
    
    Args:
    - dictionary (dict): The dictionary to be split.
    - size (int): The maximum size of each message.
    
    Returns:
    - list: List of split dictionaries.
    """
    result = []
    current_size = 0
    current_dict = {}

    for cle, valeur in dictionary.items():
        # Convertit la clé et la valeur en chaînes de caractères
        cle_str = str(cle)
        valeur_str = str(valeur)

        # Calcule la taille estimée du message
        message_size = len(json.dumps({cle_str: valeur_str})) -2

        # Vérifie si le message peut être ajouté au dictionnaire en cours
        if current_size + message_size <= size:
            current_dict[cle] = valeur
            current_size += message_size
        else:
            # Ajoute le dictionnaire en cours à la liste de résultats
            result.append(current_dict)

            # Réinitialise le dictionnaire en cours
            current_dict = {cle: valeur}
            current_size = message_size

    # Ajoute le dernier dictionnaire en cours à la liste de résultats
    result.append(current_dict)

    is_fractionnable = all(len(json.dumps(message)) <= size for message in result)
    
    if not is_fractionnable:
        print("Le dictionnaire ne peut pas être fractionné.")

    return result


