import cobra
from cobra.io import read_sbml_model

def load_model(model_path: str) -> cobra.Model:
    """
    Load a metabolic model from an SBML file.

    Parameters
    ---------
    model_path : str
        Path to the SBML model file (.xml)

    Returns
    -------
    cobra.Model
        Loaded COBRA model
    """
    try:
        model = read_sbml_model(model_path)
        return model
    except Exception as e:
        raise RuntimeError(f"Failed to load model from {model_path}") from e

def biomass_reaction(model) -> cobra.Reaction:
    biomass_rxn = model.reactions.get_by_id("BIOMASS_Ecoli_core_w_GAM")
    return biomass_rxn