import cobra
from cobra.io import read_sbml_model
from cobra.sampling import sample, OptGPSampler, ACHRSampler

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

def exchange_reactions(model):
    exchange_reactions_list = []
    for r in model.reactions: #All exchange reactions in the e_coli_core model
        if 'EX' in r.id:
            exchange_reactions_list.append(r.id)

    return exchange_reactions_list

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


    model.medium = {
        k: v for k, v in medium.items()
        if k in model.reactions
    }

    model.medium = medium

def varying_substrate(model, substrate, lower, upper, step):
    """
    Vary a substrate uptake bound and record growth rate.

    Parameters:
        model      : cobra.Model
        substrate  : str (e.g. "EX_o2_e")
        lower      : float (start value)
        upper      : float (end value, inclusive if step fits)
        step       : float (increment)

    Returns:
        list of tuples -> [(substrate_value, growth_rate), ...]
    """

    results = []

    with model:
        medium = model.medium.copy()  # avoid in-place mutation

        # --- Error handling: substrate check ---
        if substrate not in medium:
            raise ValueError(
                f"{substrate} not found in model.medium.\n"
                f"Available keys: {list(medium.keys())[:10]}..."
            )

        val = lower
        while val <= upper:
            medium[substrate] = float(val)
            model.medium = medium

            try:
                growth = model.slim_optimize()

                # handle infeasible / None / nan
                if growth is None:
                    growth = 0.0
                else:
                    growth = round(float(growth), 3)

            except Exception:
                growth = 0.0

            results.append((float(val), growth))
            val += step

    return results

def flux_sampling(model, n, sampler_object='optgp'):
    return sample(model, n, sampler_object)