import os
import copy
from Bio import PDB
from Bio.PDB import MMCIFIO
from Bio.PDB.PDBIO import PDBIO
from rebuilder.classes import DerivedChain, DerivedModel
from rebuilder.auxiliary import get_stoichiometry, remove_duplicate_models, choose_seed, generate_fasta_dictionary


def parse_pdb(directory, verbose=True):
    # READ PDBs
    print("Starting file parsing...\n")
    if verbose:
        print("Checking file directory...\n")
    if os.path.isdir(directory):
        if verbose:
            print("Looking for files inside the '{}' folder.\n".format(os.path.basename(os.path.normpath(directory))))
        p = PDB.PDBParser(PERMISSIVE=False, QUIET=True)
        directory_files = os.listdir(directory)
        if directory_files:
            if verbose:
                print("Searching pdb files...")
            i = 0
            list_of_models = []
            if any(file.endswith(".pdb") for file in directory_files):
                for file in directory_files:
                    if file.endswith(".pdb"):
                        if verbose:
                            print("Parsing {}".format(file))
                        i += 1
                        model = p.get_structure(file, os.path.join(directory, file))[0]
                        if len(model.get_list()) != 2:
                            print("The file {} contains the {} chains. In concrete {} chains. "
                                  "Just 2 chains are expected by the program.".format(
                                    file, [chain for chain in model.get_chains()], len(model.get_list())))
                        else:
                            list_of_models.append(model)
                if verbose:
                    print("\nParsing of pdb files is complete, {} pdb files were parsed in total.\n".format(i))
                return list_of_models
            else:
                raise Exception("There is no pdb file among the file(s) inside the '{}' directory".format
                                (os.path.basename(os.path.normpath(directory))))
        else:
            raise Exception("There are no files in '{}'".format(os.path.basename(os.path.normpath(directory))))
    else:
        raise Exception("The directory '{}' doesn't exist".format(os.path.basename(os.path.normpath(directory))))


def remove_redundant_id(list_of_models, fasta_dict, stoichiometry, stoichiometry_dict, verbose=True):
    # UNIFY ID'S
    print("\nRemoving redundant chain names...")
    unique_chains = []
    id_list = []
    updated_list_of_models = []
    for n in range(len(list_of_models)):
        model = list_of_models[n]
        if verbose:
            print("\n--Model {} comes from pdb {} and contains two chains, chain {} and chain {}.--".
                  format(n, model.parent, model.get_list()[0].id, model.get_list()[1].id))
        derived_model = DerivedModel(str(n))
        for chain in model.get_iterator():
            if verbose:
                print("\nRenaming chain {}...\n".format(chain.id))
            chain.__class__ = DerivedChain
            chain.parent = None
            if not unique_chains:
                former_chain_id = chain.id
                fasta_character = chain.search_fasta_dict(fasta_dict, verbose=verbose)
                chain.id = fasta_character
                # else:
                #     chain.id = generate_unique_id(id_list)
                if verbose:
                    print("Name generated for first chain.")
                    print("Chain {} --> Chain {}".format(former_chain_id, chain.id))
                id_list.append(chain.id)
                unique_chains.append(chain)
            else:
                former_chain_id = chain.id
                fasta_character = chain.search_fasta_dict(fasta_dict, verbose=verbose)
                # homologue = chain.has_homology(unique_chains)
                chain.id = fasta_character
                # elif not fasta_character and homologue:
                #     chain.id = homologue.get_id()
                #     if verbose:
                #         print("Homologue found for chain {}. Chain {} is the highest score homologue."
                #               .format(former_chain_id, homologue.id))
                # else:
                #     chain.id = generate_unique_id(id_list)
                #     if verbose:
                #         print("Homologue not found for chain {}. Generating new name...".format(former_chain_id))
                if verbose:
                    print("Renaming chain to {}...".format(chain.id))
                    print("Chain {} --> Chain {}".format(former_chain_id, chain.id))
                id_list.append(chain.id)
                unique_chains.append(chain)
            derived_model.add(chain)
        updated_list_of_models.append(derived_model)
    if verbose:
        print("\n\nRenaming Complete, removing duplicates from the list of models")
    updated_list_of_models, id_list = \
        remove_duplicate_models(updated_list_of_models, stoichiometry, id_list=id_list, stoichiometry_dict=stoichiometry_dict)
    if verbose:
        print("\n\nRedundancy Removed, the following is the curated list of models with their updated chain names:")
    for model in updated_list_of_models:
        chain1 = model.get_list()[0]
        chain2 = model.get_list()[1]
        if verbose:
            print("Model {} has chains {} and {}.".format(model.id, chain1.id, chain2.id))
    return updated_list_of_models, id_list


def generate_dict_of_pairs(updated_list_of_models, id_list, verbose=True):
    if verbose:
        print("\n\nGenerating a dictionary of pairs...")
    chain_to_models_dict = {}
    for chain_id in id_list:
        if chain_id is not None:
            chain_to_models_dict.setdefault(chain_id, [])
    for model in updated_list_of_models:
        for chain_id in chain_to_models_dict.keys():
            if chain_id in [chain.id for chain in model]:
                chain_to_models_dict[chain_id].append(model)
    if verbose:
        print("\nDictionary of pairs finished:")
    max_model_length = 0
    chain_with_more_models = ""
    for chain_id, models in chain_to_models_dict.items():
        if verbose:
            print("{} appears in {} models: {}".format(chain_id, len(models), models))
        if len(models) > max_model_length:
            max_model_length = len(models)
            chain_with_more_models = chain_id
    return chain_to_models_dict, chain_with_more_models


def loop(seed, chain_to_models_dict, stoichiometry_dict, verbose, stoichiometry):
    print("\n\nStarting model builder...")
    count_dict = {}
    super_imposer = PDB.Superimposer()
    model = copy.deepcopy(seed)
    if stoichiometry:
        for fasta_id in stoichiometry_dict.keys():
            count_dict.setdefault(fasta_id, 0)
        for chain in model.get_iterator():
            count_dict[chain.id] += 1
    chains_added = 2
    chain_location_iterator = 0
    if verbose:
        print("<< The model selected as seed for the building model is model number {},"
              " which contains chains {} and {} >>".format(model.id, model.get_list()[0].id, model.get_list()[1].id))
    for chain in model:
        chain_location_iterator += 1
        if chains_added < 200:
            if not chain.superimposed:
                if verbose:
                    print("\n** Now, the superimposition will be performed on chain {},"
                          " chain number {} of the building model. **".format(chain.id, chain_location_iterator))
                for chain_model in chain_to_models_dict[chain.id]:
                    new = copy.deepcopy(chain_model)
                    if verbose:
                        print("\n-->The model to be superimposed to the building model is model number {}, "
                              "which contains chains {} and {}."
                              .format(chain_model.id, new.get_list()[0].id, new.get_list()[1].id))
                    fixed = next(ch for ch in new if ch.id == chain.id)
                    moving = next(ch for ch in new if ch is not fixed)
                    if verbose:
                        print("The fixed chain is chain {}. The moving chain is chain {}".format(fixed.id, moving.id))
                        print("Trying to add moving chain {}.".format(moving.id))
                    if stoichiometry:
                        if count_dict[moving.id] == stoichiometry_dict[moving.id]:
                            print(stoichiometry_dict)
                            print(count_dict)
                            continue
                    chain_atoms = chain.backbone_atoms()
                    fixed_atoms = fixed.backbone_atoms()
                    len_chain = len(chain_atoms)
                    len_fixed = len(fixed_atoms)
                    if len_chain > len_fixed:
                        chain_atoms = chain_atoms[:len_fixed]
                    elif len_fixed > len_chain:
                        fixed_atoms = fixed_atoms[:len_chain]
                    super_imposer.set_atoms(chain_atoms, fixed_atoms)
                    moving_copy = copy.copy(moving)
                    super_imposer.apply(moving_copy)
                    moving_copy.parent = None
                    if not model.has_clashes_with(moving_copy):
                        model.add(moving_copy)
                        chains_added += 1
                        if stoichiometry:
                            count_dict[moving_copy.id] += 1
                        if verbose:
                            print("New chain {} correctly rotated and superimposed!".format(moving_copy.id))
                        print("Total chains added to the model = {}".format(chains_added))
                    else:
                        if verbose:
                            print("The new chain {} clashes with the previous model so chain is not added.".format(moving_copy.id))
                chain.superimposed = True
    if not stoichiometry:
        for chain in model.get_iterator():
            count_dict.setdefault(chain.id, 0)
            count_dict[chain.id] += 1
    print("\nModel generated! The stechiometry of the given model for the input chains detected is {}".format(count_dict))
    return model


# def save_modeling(model, output):
#     print("\nSaving model in cif format...")
#     path = os.getcwd()
#     model.save_to_mmcif(path + "/" + output)
#     print("Done\n".format(output))
def save_model(model, name, output_directory):
    print("Model length is {}".format(len(model.get_list())))
    if len(model.get_list()) < 50:
        io = PDBIO()
        extension = "pdb"
    else:
        io = MMCIFIO()
        extension = "cif"
    io.set_structure(model)
    print("\nSaving model in {} format...".format(extension))
    os.chdir(output_directory)
    io.save("{}.{}".format(name, extension))
    print("Done\n")


def run(fasta_file, has_stoichiometry, directory, verbosity, output_directory):
    fasta_dict = generate_fasta_dictionary(fasta_file)
    if has_stoichiometry:
        stoichiometry_dict = get_stoichiometry(fasta_dict)
    else:
        stoichiometry_dict = None
    list_of_models = parse_pdb(directory, verbose=verbosity)
    updated_list_of_models, id_list = \
        remove_redundant_id(list_of_models, fasta_dict, stoichiometry=has_stoichiometry, stoichiometry_dict=stoichiometry_dict, verbose=verbosity)
    chain_to_models_dict, chain_with_more_models = generate_dict_of_pairs(updated_list_of_models, id_list, verbose=verbosity)
    seed = choose_seed(updated_list_of_models, chain_with_more_models)
    model = loop(seed, chain_to_models_dict, verbose=verbosity, stoichiometry=has_stoichiometry, stoichiometry_dict=stoichiometry_dict)
    name = os.path.basename(os.path.normpath(directory))
    save_model(model, name, output_directory)
