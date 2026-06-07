# Influencer Marketing SEM–ML Reproducibility Repository

## Overview

This repository provides reproducibility materials for a study examining influencer credibility, parasocial interaction, product–influencer fit, and purchase intention in short-video and social-commerce contexts. The study integrates SEM-style explanatory modelling, supervised machine-learning prediction, and external robustness validation using an independent influencer-marketing dataset.

## Repository Contents

- `supplementary_material/`: Supplementary Material PDF associated with the study.
- `data/`: Processed and documented datasets used for reproducibility.
- `code/`: Python scripts for SEM-style analysis, machine-learning prediction, and external robustness validation.
- `outputs/`: Excel output files generated from the analysis workflow.
- `docs/`: Documentation files describing the external dataset source, workflow, and reproducibility notes.

## Data Availability

The primary survey raw responses are not publicly released to protect participant confidentiality. Processed and anonymized construct-level data may be provided where ethically shareable. The external validation dataset is publicly available from Mendeley Data:

Saima. (2020). *Effect of Social Media Influencer Marketing on Purchase Intention and the Mediation Effect of Credibility*. Mendeley Data, V1. https://doi.org/10.17632/gdd9htg5gb.1

## External Robustness Validation

The external validation was conducted using Likert-scale purchase intention as the target variable. Conceptually related predictors associated with influencer expertise, trustworthiness, information credibility, argument quality, attractiveness/likeability, and entertainment value were used for machine-learning validation.

Because the external dataset does not reproduce the full SEM measurement structure of the primary survey, it was used only for predictive robustness validation, not for full SEM replication.

## Software Requirements

The Python packages required to run the analysis are listed in `requirements.txt`.

Install the required packages using:

```bash
pip install -r requirements.txt
**## How to Reproduce the Results**

The Python scripts are provided in the `code/` folder. Users may either inspect the generated Excel outputs directly from the `outputs/` folder or rerun the scripts to regenerate the analytical outputs.

### Run external robustness validation

```bash
python code/external_validation_option_A.py
**### Run complete reproducibility workflow**

```bash
python code/reproducibility_workflow.py
## How to Reproduce the Results

The Python scripts are provided in the `code/` folder. Users may either inspect the generated Excel outputs directly from the `outputs/` folder or rerun the scripts to regenerate the analytical outputs.

### Run external robustness validation

```bash
python code/external_validation_option_A.py
python code/main_sem_ml_analysis.py
python code/reproducibility_workflow.py
