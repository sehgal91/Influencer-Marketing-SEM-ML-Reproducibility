# Documentation

## Overview

This folder contains documentation files supporting the reproducibility package for the influencer marketing SEM–ML study. The documentation explains the analysis workflow, data availability approach, external validation source, and reproducibility notes.

## Files in This Folder

- `README.md`: Overview of the documentation folder.
- `analysis_workflow.md`: Description of the analytical workflow used in the study.
- `reproducibility_notes.md`: Notes on data sharing, confidentiality, reproducibility, and script execution.
- `variable_dictionary.md`: Description of key variables and constructs used in the analysis.

## Documentation Purpose

The documentation is provided to help readers understand how the repository materials are organized and how the reported analytical outputs can be inspected or reproduced. The repository includes Python scripts, Excel outputs, supplementary material, and external validation documentation.

## External Dataset Documentation

The external validation dataset source is documented in the `data/` folder. The independent external dataset used for robustness validation is publicly available from Mendeley Data:

Saima. (2020). *Effect of Social Media Influencer Marketing on Purchase Intention and the Mediation Effect of Credibility*. Mendeley Data, V1. https://doi.org/10.17632/gdd9htg5gb.1

## Reproducibility Notes

The primary survey raw responses are not publicly released to protect participant confidentiality. Processed analytical outputs and documentation are provided to support transparent inspection of the reported results. External validation was used only for predictive robustness, as the external dataset does not reproduce the full SEM measurement structure of the primary survey.

## Related Repository Folders

- `code/`: Python scripts for the analysis workflow.
- `data/`: Data documentation and external dataset source information.
- `outputs/`: Excel output files generated from the analysis.
- `supplementary_material/`: Supplementary Material PDF associated with the study.
## How to Reproduce the Results

The Python scripts are provided in the `code/` folder. Users may either inspect the generated Excel outputs directly from the `outputs/` folder or rerun the scripts to regenerate the analytical outputs.

### Run external robustness validation

```bash
python code/external_validation_option_A.py
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

The code is shared for academic and reproducibility purposes. External datasets remain subject to their original licenses and citation requirements.
## Contact

For questions related to the study or repository, please contact the corresponding author listed in the associated manuscript.

