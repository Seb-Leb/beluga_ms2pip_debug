from ms2pip.ms2pipC import MS2PIP
import pdb

peprec_filename = '/mnt/psm_report.peprec'
mgf_filename = '/mnt/b10771/b10771.mgf'

ms2pip_options = {
    "model": "HCD",
    "frag_error": 0.02,
    "modifications": [
      {
        "name": "Acetyl",
        "unimod_accession": 1,
        "mass_shift": 42.010565,
        "amino_acid": None,
        "n_term": True,
        "c_term": False
      },
      {
        "name": "Pyro-carbamidomethyl",
        "unimod_accession": 26,
        "mass_shift": 39.994915,
        "amino_acid": "C",
        "n_term": False,
        "c_term": False
      },
      {
        "name": "Glu->pyro-Glu",
        "unimod_accession": 27,
        "mass_shift": -18.010565,
        "amino_acid": "E",
        "n_term": True,
        "c_term": False
      },
      {
        "name": "Gln->pyro-Glu",
        "unimod_accession": 28,
        "mass_shift": -17.026549,
        "amino_acid": "Q",
        "n_term": True,
        "c_term": False
      },
      {
        "name": "Oxidation",
        "unimod_accession": 35,
        "mass_shift": 15.994915,
        "amino_acid": "M",
        "n_term": False,
        "c_term": False
      }
    ]
  }

def make_ms2pip_config_dict(options):
    ms2pip_config = {
        "ms2pip": {
            "model": options["model"],
            "frag_error": options["frag_error"],
            "ptm": [],
            "sptm": [],
            "gptm": [],
        }
    }

    for mod in options["modifications"]:
        if mod["amino_acid"] is None and mod["n_term"]:
            aa = "N-term"
        elif mod["amino_acid"] is None and mod["c_term"]:
            aa = "C-term"
        else:
            aa = mod["amino_acid"]
        ms2pip_config["ms2pip"]["ptm"].append(
            ",".join([mod["name"], str(mod["mass_shift"]), "opt", aa])
        )
    return ms2pip_config

ms2pip = MS2PIP(
    peprec_filename,
    spec_file=mgf_filename,
    params=make_ms2pip_config_dict(ms2pip_options),
    num_cpu=4,
    add_retention_time=False,
    compute_correlations=False,
    model_dir='/home/.ms2pip'
)
try:
    ms2pip.run()
finally:
    ms2pip.cleanup()