<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/banner-dark.svg">
  <img alt="Shivam Randive: machine learning for materials discovery. Integrated M.Sc. Physics, SVNIT Surat; research intern, Spin Theory Group, NIMS Japan." src="assets/banner-light.svg" width="100%">
</picture>

<p align="center">
  <a href="https://shivamrandive747.github.io"><img alt="Website" src="https://img.shields.io/badge/Website-shivamrandive747.github.io-1b3a5c?style=flat-square"></a>
  <a href="https://doi.org/10.48550/arXiv.2610.18179"><img alt="arXiv" src="https://img.shields.io/badge/arXiv-2610.18179-b31b1b?style=flat-square&logo=arxiv&logoColor=white"></a>
  <a href="https://orcid.org/0009-0005-1403-4484"><img alt="ORCID" src="https://img.shields.io/badge/ORCID-0009--0005--1403--4484-a6ce39?style=flat-square&logo=orcid&logoColor=white"></a>
  <a href="https://scholar.google.com/citations?user=g3rGf_MAAAAJ"><img alt="Google Scholar" src="https://img.shields.io/badge/Google%20Scholar-profile-4285F4?style=flat-square&logo=googlescholar&logoColor=white"></a>
  <a href="mailto:i22ph019@phy.svnit.ac.in"><img alt="Email" src="https://img.shields.io/badge/Email-i22ph019%40phy.svnit.ac.in-555555?style=flat-square&logo=gmail&logoColor=white"></a>
</p>

I discover new alloys in the Heusler family and predict their properties for thermoelectric applications,
and I test every machine-learning prediction against first-principles calculations and experiment. Two
first-author papers submitted so far, and now transfer learning of universal interatomic potentials at NIMS, Japan.

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/stats-dark.svg">
  <img alt="At a glance: 2 first-author papers submitted; 106,235 Heusler structures screened; 3,625 DFT transport calculations; 9,495 thermal-conductivity values; 4 research institutes in 2 countries." src="assets/stats-light.svg" width="100%">
</picture>

## Projects

<p align="center">
  <a href="https://shivamrandive747.github.io/#research"><picture>
    <source media="(prefers-color-scheme: dark)" srcset="assets/card-nims-dark.svg">
    <img alt="Current, NIMS 2026: new alkali- and alkaline-earth Heusler thermoelectrics with transfer-learned universal interatomic potentials." src="assets/card-nims-light.svg" width="49%">
  </picture></a>
  <a href="https://doi.org/10.48550/arXiv.2610.18179"><picture>
    <source media="(prefers-color-scheme: dark)" srcset="assets/card-screening-dark.svg">
    <img alt="Submitted, preprint on arXiv 2026: ML-guided thermoelectric screening of 106,235 Heusler structures. About 4 times fewer DFT runs per hit; 80 candidates, 61 never measured." src="assets/card-screening-light.svg" width="49%">
  </picture></a>
</p>
<p align="center">
  <a href="https://github.com/Shivamrandive747/half-heusler-kappa-calibration"><picture>
    <source media="(prefers-color-scheme: dark)" srcset="assets/card-kappa-dark.svg">
    <img alt="Submitted 2026: making ML predictions of thermal conductivity match experiment. 33% median error versus 46 to 47% for baselines." src="assets/card-kappa-light.svg" width="49%">
  </picture></a>
  <a href="https://drive.google.com/file/d/1dD-fT1N9dyx78ICVK90nR-8M5JnDo-rm/view?usp=sharing"><picture>
    <source media="(prefers-color-scheme: dark)" srcset="assets/card-srfp-dark.svg">
    <img alt="Report, SRFP 2025: do graph neural networks work on unseen materials? Specialists fell from over 92% to about 48%; a pretrained model held about 80%." src="assets/card-srfp-light.svg" width="49%">
  </picture></a>
</p>
<p align="center">
  <a href="https://drive.google.com/file/d/1rd77ryVKYCl4dzaDe2QpezefqtLPjPC3/view?usp=sharing"><picture>
    <source media="(prefers-color-scheme: dark)" srcset="assets/card-descriptors-dark.svg">
    <img alt="Project, SVNIT 2025: physical descriptors as first predictors for perovskites and half-Heusler alloys." src="assets/card-descriptors-light.svg" width="49%">
  </picture></a>
  <a href="https://drive.google.com/file/d/1M_lOCsnlSuaVTfAMZrHsLm-JbuOtV_dY/view?usp=sharing"><picture>
    <source media="(prefers-color-scheme: dark)" srcset="assets/card-strain-dark.svg">
    <img alt="Internship, IIT Bhilai 2024: strain in silicon thin films for stretchable electronics, modelled in COMSOL." src="assets/card-strain-light.svg" width="49%">
  </picture></a>
</p>

<sub>Click a card to open the paper, code or report. Full descriptions are below.</sub>

<details>
<summary><b>New alkali- and alkaline-earth Heusler thermoelectrics</b> · NIMS, Tsukuba · Spin Theory Group, Prof. Terumasa Tadano · 2026</summary>

<br>

- **Idea:** build new alkali- and alkaline-earth-metal Heusler compositions combinatorially and rank them by
  predicted Seebeck coefficient and lattice thermal conductivity, using universal machine-learned interatomic
  potentials (eSEN, EquiformerV3) that already learned chemistry from millions of DFT calculations.
- **Approach:** keep the pretrained network frozen and train a small model on its inner features, finding
  which layers, and which design (convolution or attention), best capture transport.
- **Status:** work in progress.

</details>

<details>
<summary><b>ML-guided thermoelectric screening of 106,235 Heusler structures</b> · submitted · preprint <a href="https://doi.org/10.48550/arXiv.2610.18179">arXiv:2610.18179</a></summary>

<br>

- **Problem:** transport calculations are too expensive for whole databases, so candidates are shortlisted from
  the cheaper density of states (DOS), often predicted by ML. This shortcut had never been tested at scale.
- **What I did:** trained 30 ALIGNN graph neural networks to predict the DOS of 54,978 structures (held-out
  *r* = 0.90 vs. 0.49–0.61 for simple baselines), and judged the shortlist with 3,625 first-principles transport
  calculations from my own Quantum ESPRESSO + BoltzTraP2 workflow.
- **Result:** a DOS-based Seebeck indicator finds the good compounds with about **4× fewer expensive
  calculations**, giving **80 candidate thermoelectrics** (61 never measured); 10 of 11 known half-Heusler
  thermoelectrics pass the same checks.
- **Message:** ML spectra miss most band gaps (recall 0.15) even when standard scores look good, so they can
  rank candidates but only a band-structure calculation can confirm a gap.
- **Code:** [heusler-dos-te-screening](https://github.com/yednaph/heusler-dos-te-screening)

</details>

<details>
<summary><b>Making ML predictions of thermal conductivity match experiment</b> · submitted to a journal</summary>

<br>

- **Problem:** ML models of lattice thermal conductivity (κ<sub>L</sub>) learn from calculated values, which
  overestimate experiment by a median **1.69×** (29 of 34 half-Heuslers).
- **What I did:** built a source-tracked dataset of 9,495 κ<sub>L</sub> values for 960 compounds from five databases
  and the literature (1,178 values read by multimodal LLMs, each physics-checked), and a simple two-parameter
  correction from calculation to experiment.
- **Result:** predictions of measured κ<sub>L</sub> reach **33% median error vs. 46–47% for baselines** (cubic
  18-electron compounds), close to the disagreement between two labs; the correction also cuts an independent ML
  force field's error from 101% to 37%. Released 10 testable predictions with 90% prediction intervals.
- **Code and data:** [half-heusler-kappa-calibration](https://github.com/Shivamrandive747/half-heusler-kappa-calibration)
  · [Zenodo](https://doi.org/10.5281/zenodo.23333947)

</details>

<details>
<summary><b>Do graph neural networks work on unseen materials?</b> · SRFP 2025, S. N. Bose National Centre, Kolkata</summary>

<br>

- Built a full ALIGNN pipeline (crystal file → graph → prediction) and compared one broadly pretrained model with
  "specialist" models trained only on narrow perovskite families.
- **Result:** the specialists scored over 92% on familiar data but dropped to about 48% on new double
  perovskites, while the pretrained model kept about 80%.
- **Message:** breadth of training data matters more for discovery than high accuracy on a narrow test set.
- Supervised by Prof. Tanusri Saha-Dasgupta · [report](https://drive.google.com/file/d/1dD-fT1N9dyx78ICVK90nR-8M5JnDo-rm/view?usp=sharing)

</details>

<details>
<summary><b>Physical descriptors as first predictors</b> · semester project, SVNIT, 2025</summary>

<br>

- Support-vector classifier for perovskite formability from ionic radii and the tolerance factor (≈90% accuracy).
- Reproduced a Gaussian-process model of lattice constants for 137 half-Heusler compounds from four descriptors.
- [Report](https://drive.google.com/file/d/1rd77ryVKYCl4dzaDe2QpezefqtLPjPC3/view?usp=sharing) ·
  earlier literature survey: [Mini-project-1-](https://github.com/Shivamrandive747/Mini-project-1-)

</details>

<details>
<summary><b>Strain in silicon thin films for stretchable electronics</b> · internship, IIT Bhilai, 2024</summary>

<br>

- COMSOL finite-element model of a silicon film on a flexible polyimide substrate in a pressure cell; the strain
  maps were used by a collaborator as input for DFT calculations of how strain changes the film's electronic
  properties.
- [Report](https://drive.google.com/file/d/1M_lOCsnlSuaVTfAMZrHsLm-JbuOtV_dY/view?usp=sharing)

</details>

## Journey

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/journey-dark.svg">
  <img alt="Journey: 2024 IIT Bhilai, summer research intern; 2025 SVNIT Surat, student researcher; 2025 S. N. Bose Centre, SRFP fellow; 2026 NIMS Japan, research intern; 2027 IIT Delhi, semester exchange (upcoming)." src="assets/journey-light.svg" width="100%">
</picture>

## Toolbox

<p>
  <img alt="Python" src="https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white">
  <img alt="PyTorch" src="https://img.shields.io/badge/PyTorch-EE4C2C?style=flat-square&logo=pytorch&logoColor=white">
  <img alt="scikit-learn" src="https://img.shields.io/badge/scikit--learn-F7931E?style=flat-square&logo=scikitlearn&logoColor=white">
  <img alt="NumPy" src="https://img.shields.io/badge/NumPy-013243?style=flat-square&logo=numpy&logoColor=white">
  <img alt="pandas" src="https://img.shields.io/badge/pandas-150458?style=flat-square&logo=pandas&logoColor=white">
  <img alt="DGL" src="https://img.shields.io/badge/DGL-graph%20learning-1b3a5c?style=flat-square">
  <img alt="fairchem" src="https://img.shields.io/badge/fairchem-MLIPs-1b3a5c?style=flat-square">
  <img alt="CatBoost" src="https://img.shields.io/badge/CatBoost-LightGBM%20%C2%B7%20GPs-1b3a5c?style=flat-square">
  <br>
  <img alt="Quantum ESPRESSO" src="https://img.shields.io/badge/Quantum%20ESPRESSO-DFT-2f7d7a?style=flat-square">
  <img alt="VASP" src="https://img.shields.io/badge/VASP-DFT-2f7d7a?style=flat-square">
  <img alt="BoltzTraP2" src="https://img.shields.io/badge/BoltzTraP2-transport-2f7d7a?style=flat-square">
  <img alt="Phonopy" src="https://img.shields.io/badge/Phonopy%20%2F%20Phono3py-phonons-2f7d7a?style=flat-square">
  <img alt="Linux" src="https://img.shields.io/badge/Linux-SLURM%20GPU%20clusters-333333?style=flat-square&logo=linux&logoColor=white">
  <img alt="Git" src="https://img.shields.io/badge/Git-F05032?style=flat-square&logo=git&logoColor=white">
  <img alt="LaTeX" src="https://img.shields.io/badge/LaTeX-008080?style=flat-square&logo=latex&logoColor=white">
</p>

---

<p align="center">
  <b>Open to PhD positions in machine learning for materials.</b><br>
  <a href="mailto:i22ph019@phy.svnit.ac.in">Email</a> ·
  <a href="https://shivamrandive747.github.io">Website</a> ·
  <a href="https://shivamrandive747.github.io/assets/Shivam_Randive_CV.pdf">CV</a> ·
  <a href="https://shivamrandive747.github.io/statement.html">Research statement</a> ·
  <a href="https://orcid.org/0009-0005-1403-4484">ORCID</a> ·
  <a href="https://scholar.google.com/citations?user=g3rGf_MAAAAJ">Google Scholar</a>
</p>
