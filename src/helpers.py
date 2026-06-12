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

def m9_media(model):
    """
    Set the model medium to canonical M9 (aerobic, glucose).
    Intended to be used inside a `with model:` context.
    """
    medium = {
        "EX_glc__D_e": 10.0,
        "EX_nh4_e": 10.0,
        "EX_pi_e": 10.0,
        "EX_so4_e": 10.0,
        "EX_o2_e": 20.0,
        "EX_h2o_e": 1000.0,
        "EX_h_e": 1000.0,
        "EX_k_e": 1000.0,
        "EX_na1_e": 1000.0,
        "EX_mg2_e": 1000.0,
        "EX_ca2_e": 1000.0,
    }

    model.medium = medium