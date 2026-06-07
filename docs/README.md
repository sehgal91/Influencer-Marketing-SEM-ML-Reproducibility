# Influencer Marketing SEM–ML Reproducibility Repository

## Overview

This repository provides reproducibility materials for a study examining influencer credibility, parasocial interaction, product–influencer fit, and purchase intention in short-video and social-commerce contexts. The study integrates SEM-style explanatory modelling, supervised machine-learning prediction, and external robustness validation using an independent influencer-marketing dataset.

The repository contains supplementary material, Python scripts, processed analytical outputs, documentation files, and reproducibility notes required to inspect and reproduce the reported analytical workflow.

## Repository Contents

* `supplementary_material/`: Supplementary Material PDF associated with the study.
* `data/`: Data documentation and external dataset source information.
* `code/`: Python scripts for SEM-style analysis, machine-learning prediction, and external robustness validation.
* `outputs/`: Excel output files generated from the analysis workflow.
* `docs/`: Documentation files describing the workflow, reproducibility notes, and related supporting information.
* `requirements.txt`: Python package requirements for running the scripts.

## Study Components

The reproducibility package supports the following analytical components:

1. SEM-style explanatory modelling of influencer credibility, parasocial interaction, product–influencer fit, and purchase intention.
2. Mediation and moderation analysis for the proposed theoretical framework.
3. Machine-learning prediction of purchase intention using theoretically derived predictors.
4. External robustness validation using an independent influencer-marketing dataset.
5. Exported analytical outputs in Excel format for transparent checking.

## Data Availability

The primary survey raw responses are not publicly released to protect participant confidentiality. The repository provides processed analytical outputs and documentation sufficient to inspect the reported results and reproduce the computational workflow where ethically shareable.

The independent external dataset used for robustness validation is publicly available from Mendeley Data:

Saima. (2020). *Effect of Social Media Influencer Marketing on Purchase Intention and the Mediation Effect of Credibility*. Mendeley Data, V1. https://doi.org/10.17632/gdd9htg5gb.1

## External Robustness Validation

The external validation was conducted using Likert-scale purchase intention as the target variable. Conceptually related predictors associated with influencer expertise, trustworthiness, attractiveness/likeability, argument quality, information credibility, and entertainment value were used for machine-learning validation.

Because the external dataset does not reproduce the same full SEM measurement structure as the primary survey, it was used only for predictive robustness validation and not for full SEM replication.

## Analysis Workflow

The reproducibility workflow follows these stages:

1. Import processed analytical data and reported result structures.
2. Summarize construct-level descriptive statistics.
3. Report reliability and convergent validity diagnostics.
4. Summarize SEM-style structural, mediation, and moderation results.
5. Compare machine-learning models for purchase-intention prediction.
6. Conduct external robustness validation using an independent influencer-marketing dataset.
7. Export model-performance summaries and feature-importance outputs to Excel files.

## Software Requirements

The analysis was conducted using Python. Required packages are listed in `requirements.txt`.

Install the required packages using:

```bash
pip install -r requirements.txt
```

## How to Reproduce the Results

The Python scripts are provided in the `code/` folder. Users may inspect the generated Excel outputs directly from the `outputs/` folder or rerun the scripts to regenerate the analytical outputs.

### Generate external validation results

```bash
python code/external_validation_option_A.py
```

This script generates the external validation Excel output using the independent influencer-marketing dataset.

### Generate main SEM–ML result summaries

```bash
python code/main_sem_ml_analysis.py
```

This script generates the main Excel output containing the reported SEM-style, mediation, moderation, and machine-learning result summaries.

### Generate complete reproducibility summary

```bash
python code/reproducibility_workflow.py
```

This script generates the complete reproducibility workflow summary in the `outputs/` folder.

## Generated Outputs

The `outputs/` folder contains Excel files summarizing the main SEM–ML results, external validation results, and reproducibility workflow outputs. These files allow readers to inspect the reported analytical summaries without rerunning the scripts.

## Supplementary Material

The `supplementary_material/` folder contains the Supplementary Material PDF associated with the study.

## Reproducibility Notes

The repository is designed to support transparent and reproducible analysis. Random seeds are fixed where applicable in the Python scripts to improve reproducibility of machine-learning results.

The external validation dataset is documented in the `data/` folder. External datasets remain subject to their original licenses and citation requirements.

## Citation

This repository supports the reproducibility of a manuscript currently under preparation/submission. A formal citation with article DOI will be added after publication.

## License

The code is shared for academic and reproducibility purposes under the MIT License. External datasets remain subject to their original licenses and citation requirements.

## Contact

For questions related to the study or repository, please contact the corresponding author listed in the associated manuscript.
