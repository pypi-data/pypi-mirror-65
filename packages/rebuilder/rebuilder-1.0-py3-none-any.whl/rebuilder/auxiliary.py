import random
import re
import sys


def generate_fasta_dictionary(fasta_filename):
    """Iterates fasta file and yields a tuple giving ID and sequence"""
    fasta_dict = {}
    sequence = ""
    cutoff = 0.95
    with open(fasta_filename, "r") as file:
        for line in file:
            if line.startswith(">"):
                if sequence:
                    fasta_dict.setdefault(str(fasta_id), sequence)
                    sequence = ""
                fasta_id = line.strip()
                search = re.search('(?<=:)(.*?)(?=[|])', fasta_id)
                if search:
                    fasta_id = search.group()
                else:
                    search = re.search('(?<=_)(.*?)(?=[|])', fasta_id)
                    fasta_id = search.group()
            else:
                sequence += line.strip()
    fasta_dict.setdefault(str(fasta_id), sequence)
    return fasta_dict


def get_stoichiometry(fasta_dict):
    print("Generating stoichiometry dictionary as you have added the -s flag to the command.\n")
    stoichiometry_dict = {}
    for fasta_id, sequence in fasta_dict.items():
        value = input("For fasta_id '{}', which identifies sequence '{}(...)' with a sequence length of {},"
                      " how many chains would the model have?\n".format(fasta_id, sequence[0:20], len(sequence)))
        try:
            value = int(value)
            stoichiometry_dict[fasta_id] = value
        except ValueError:
            print("\n\nThe value provided, '{}', is not an integer. Please refrain from using anything other than that"
                  .format(value))
            print("Restarting stoichiometry assignment...\n\n")
            get_stoichiometry(fasta_dict)
    print("Stoichiometry dictionary complete. Is this correct?")
    print(stoichiometry_dict)
    check = input("\nIf it is correct, type 'y', if you want to try again, type 'n'\n")
    if check.lower() == "y" or check.lower() == "yes":
        print("\nThank you! Saving dictionary for future steps.\n")
        return stoichiometry_dict
    elif check.lower() == "n" or check.lower() == "no":
        print("\n\nSorry! Maybe then you want to try again:\n")
        get_stoichiometry(fasta_dict)
    else:
        print("Sorry, the value '{}' is not understood by the program".format(check))
        sys.exit()
#
#
# def generate_unique_id(id_list):
#     """Returns ID for the chain object."""
#     characters = 'abcdefghijklmnopqrstuvwxyz123456789'
#     for character in characters:
#         if character not in id_list:
#             return character


def choose_seed(updated_list_of_objects, chain_with_more_models):
    list_of_seeds = []
    for model in updated_list_of_objects:
        if chain_with_more_models in [chain.id for chain in model.get_iterator()]:
            list_of_seeds.append(model)
    seed = random.choice(list_of_seeds)
    return seed


def remove_duplicate_models(updated_list_of_models, stoichiometry, id_list, stoichiometry_dict):
    filtered_list_of_models = []
    dict_of_models = {}
    filtered_id_list = []
    print(id_list)
    for model in updated_list_of_models:
        if None in [chain.id for chain in model.get_iterator()]:
            pass
        else:
            chains_per_model = [chain.id for chain in model]
            dict_of_models.setdefault((tuple(chains_per_model)), model)
            if dict_of_models[tuple(chains_per_model)] == model:
                filtered_list_of_models.append(model)
    if stoichiometry:
        for fasta_id, value in stoichiometry_dict.items():
            for model in filtered_list_of_models:
                for chain in model:
                    if chain.id == fasta_id and stoichiometry_dict[fasta_id] == 0:
                        filtered_list_of_models.remove(model)
        for chain_id in id_list:
            if stoichiometry_dict[chain_id] != 0:
                filtered_id_list.append(chain_id)
    else:
        filtered_id_list = id_list
    return filtered_list_of_models, filtered_id_list
