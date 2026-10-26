# Shivam Randive

**Machine learning for materials discovery** · Integrated M.Sc. Physics, SVNIT Surat, India ·
Research intern, Spin Theory Group, NIMS, Japan

I discover new alloys in the Heusler family and predict their properties for thermoelectric
applications, and I test every machine-learning prediction against first-principles calculations and
experiment.

[![Website](https://img.shields.io/badge/Website-shivamrandive747.github.io-1b3a5c)](https://shivamrandive747.github.io)
[![arXiv](https://img.shields.io/badge/arXiv-2610.18179-b31b1b)](https://doi.org/10.48550/arXiv.2610.18179)
[![ORCID](https://img.shields.io/badge/ORCID-0009--0005--1403--4484-a6ce39)](https://orcid.org/0009-0005-1403-4484)
[![Email](https://img.shields.io/badge/Email-i22ph019%40phy.svnit.ac.in-555555)](mailto:i22ph019@phy.svnit.ac.in)

## Research

### ML-guided thermoelectric screening of 106,235 Heusler structures

[arXiv:2610.18179](https://doi.org/10.48550/arXiv.2610.18179) ·
[code](https://github.com/yednaph/heusler-dos-te-screening)

30 ALIGNN graph neural networks predict densities of states, and 3,625 first-principles transport
calculations judge the resulting screen. It needs about 4× fewer DFT runs per hit and yields 80
candidate thermoelectrics, 61 never measured.

### Making ML predictions of thermal conductivity match experiment

[code](https://github.com/Shivamrandive747/half-heusler-kappa-calibration) ·
[data](https://doi.org/10.5281/zenodo.23333947)

Published calculations overestimate measured lattice thermal conductivity by a median 1.69×. A
two-parameter correction with a CatBoost model reaches 33% median error against experiment, versus
46–47% for baselines, built on a provenance-tracked corpus of 9,495 values.

### Generalization of graph neural networks

SRFP 2025, S. N. Bose National Centre for Basic Sciences, Kolkata

Specialist models fell from over 92% to about 48% accuracy on unseen double perovskites, while a
broadly pretrained model held about 80%.

### Now, at NIMS

Exploring new alkali- and alkaline-earth Heusler alloys, predicting their Seebeck coefficient and
lattice thermal conductivity with transfer-learned universal interatomic potentials (eSEN,
EquiformerV3).

## Tools

- **Machine learning:** PyTorch · DGL · fairchem · scikit-learn · CatBoost · LightGBM · Gaussian processes
- **First principles:** Quantum ESPRESSO · VASP · BoltzTraP2 · Phonopy/Phono3py
- **Computing:** Python · Linux · SLURM GPU clusters · Git

---

Open to PhD positions in machine learning for materials. The best way to reach me is
[email](mailto:i22ph019@phy.svnit.ac.in).
