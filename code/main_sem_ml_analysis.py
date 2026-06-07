"""
Main SEM-style and machine-learning reproducibility script
=========================================================

Purpose
-------
This script regenerates the main analytical output workbook for the
influencer marketing SEM-ML study using the final reported values from the
manuscript and supplementary material.

The primary raw survey responses are not required for this public
reproducibility package. The script exports transparent, machine-readable
result tables for descriptive statistics, reliability/validity diagnostics,
structural models, mediation/moderation results, machine-learning model
performance, and feature importance.

Output
------
outputs/Main_SEM_ML_Results.xlsx

Run
---
python code/main_sem_ml_analysis.py

Notes
-----
- No personal or respondent-level identifiers are used.
- Values are fixed to the finalized analytical outputs reported in the study.
- This script is designed for reproducibility of reported tables, not for
  reprocessing confidential raw survey data.
"""

from __future__ import annotations

from pathlib import Path
import pandas as pd


def repo_root() -> Path:
    """Return repository root whether the script is run from /code or root."""
    script_path = Path(__file__).resolve()
    if script_path.parent.name == "code":
        return script_path.parent.parent
    return script_path.parent


def ensure_outputs_dir(root: Path) -> Path:
    out_dir = root / "outputs"
    out_dir.mkdir(parents=True, exist_ok=True)
    return out_dir


def build_descriptive_statistics() -> pd.DataFrame:
    return pd.DataFrame(
        [
            ["Trustworthiness", 1000, 3.945, 1.674, 1.000, 2.500, 4.000, 5.250, 7.000],
            ["Expertise", 1000, 3.902, 1.679, 1.000, 2.500, 4.000, 5.250, 7.000],
            ["Attractiveness", 1000, 3.985, 1.633, 1.000, 2.750, 4.000, 5.250, 7.000],
            ["Parasocial Interaction", 1000, 3.906, 2.048, 1.000, 2.000, 3.800, 5.800, 7.000],
            ["Product-Influencer Fit", 1000, 3.896, 1.734, 1.000, 2.500, 4.000, 5.250, 7.000],
            ["Purchase Intention", 1000, 3.845, 2.115, 1.000, 1.750, 3.750, 5.750, 7.000],
        ],
        columns=["Construct", "n", "Mean", "SD", "Min", "25%", "Median", "75%", "Max"],
    )


def build_reliability_validity() -> pd.DataFrame:
    return pd.DataFrame(
        [
            ["Trustworthiness", 4, 0.872, 0.912, 0.722, "Acceptable"],
            ["Expertise", 4, 0.877, 0.915, 0.730, "Acceptable"],
            ["Attractiveness", 4, 0.866, 0.908, 0.713, "Acceptable"],
            ["Parasocial Interaction", 5, 0.948, 0.960, 0.828, "Acceptable"],
            ["Product-Influencer Fit", 4, 0.890, 0.924, 0.751, "Acceptable"],
            ["Purchase Intention", 4, 0.941, 0.958, 0.850, "Acceptable"],
        ],
        columns=["Construct", "Items", "Cronbach_alpha", "Composite_reliability", "AVE", "Assessment"],
    )


def build_correlation_matrix() -> pd.DataFrame:
    labels = ["TR", "EX", "AT", "PSI", "PIF", "PI"]
    values = [
        [1.00, 0.56, 0.28, 0.69, 0.46, 0.63],
        [0.56, 1.00, 0.25, 0.69, 0.41, 0.60],
        [0.28, 0.25, 1.00, 0.44, 0.31, 0.38],
        [0.69, 0.69, 0.44, 1.00, 0.59, 0.82],
        [0.46, 0.41, 0.31, 0.59, 1.00, 0.64],
        [0.63, 0.60, 0.38, 0.82, 0.64, 1.00],
    ]
    return pd.DataFrame(values, index=labels, columns=labels).reset_index(names="Construct")


def build_structural_results() -> pd.DataFrame:
    return pd.DataFrame(
        [
            ["Credibility -> PSI", "PSI", "Trustworthiness", 0.484, None, 17.314, "<0.001", 0.657, "Supported"],
            ["Credibility -> PSI", "PSI", "Expertise", 0.502, None, 18.182, "<0.001", 0.657, "Supported"],
            ["Credibility -> PSI", "PSI", "Attractiveness", 0.282, None, 11.515, "<0.001", 0.657, "Supported"],
            ["Purchase intention model", "PI", "Trustworthiness", 0.102, None, 3.405, "<0.001", 0.720, "Supported"],
            ["Purchase intention model", "PI", "Expertise", 0.065, None, 2.178, "0.030", 0.720, "Supported"],
            ["Purchase intention model", "PI", "Attractiveness", 0.011, None, 0.448, "0.655", 0.720, "Not supported"],
            ["Purchase intention model", "PI", "Parasocial Interaction", 0.613, None, 19.502, "<0.001", 0.720, "Supported"],
            ["Purchase intention model", "PI", "Product-Influencer Fit", 0.279, None, 10.946, "<0.001", 0.720, "Supported"],
        ],
        columns=["Model", "Dependent_variable", "Predictor", "Beta", "SE", "t", "p", "R2", "Result"],
    )


def build_mediation_results() -> pd.DataFrame:
    return pd.DataFrame(
        [
            ["Trustworthiness -> PSI -> Purchase Intention", 0.652, 0.594, 0.714, "Significant mediation"],
            ["Expertise -> PSI -> Purchase Intention", 0.678, 0.620, 0.729, "Significant mediation"],
            ["Attractiveness -> PSI -> Purchase Intention", 0.466, 0.405, 0.513, "Significant mediation"],
        ],
        columns=["Pathway", "Indirect_effect", "CI_lower_95", "CI_upper_95", "Interpretation"],
    )


def build_moderation_results() -> pd.DataFrame:
    return pd.DataFrame(
        [
            ["Parasocial Interaction", 1.446, 0.044, 32.662, "<0.001", "Significant main effect"],
            ["Product-Influencer Fit", 0.498, 0.044, 11.234, "<0.001", "Significant main effect"],
            ["PSI x Product-Influencer Fit", 0.042, 0.039, 1.090, "0.276", "Moderation not supported"],
        ],
        columns=["Predictor", "Beta", "SE", "t", "p", "Interpretation"],
    )


def build_ml_performance() -> pd.DataFrame:
    return pd.DataFrame(
        [
            ["Linear Regression", 1.025, 0.787, 0.762, 0.718, 1],
            ["Ridge Regression", 1.025, 0.787, 0.762, 0.718, 2],
            ["SVR-RBF", 1.081, 0.793, 0.735, 0.702, 3],
            ["Gradient Boosting", 1.114, 0.837, 0.719, 0.700, 4],
            ["Random Forest", 1.125, 0.856, 0.713, 0.688, 5],
            ["Extra Trees", 1.131, 0.851, 0.710, 0.681, 6],
            ["Elastic Net", 1.342, 1.181, 0.592, 0.566, 7],
            ["Lasso", 1.522, 1.347, 0.474, 0.453, 8],
        ],
        columns=["Model", "RMSE", "MAE", "Test_R2", "Cross_validated_R2", "Rank"],
    )


def build_feature_importance() -> pd.DataFrame:
    rows = [
        ["Ridge", "Trustworthiness", 0.0157, 0.0040],
        ["Ridge", "Expertise", 0.0065, 0.0027],
        ["Ridge", "Attractiveness", 0.0006, 0.0005],
        ["Ridge", "Parasocial Interaction", 0.6681, 0.0375],
        ["Ridge", "Product-Influencer Fit", 0.0999, 0.0069],
        ["Random Forest", "Trustworthiness", 0.0245, 0.0077],
        ["Random Forest", "Expertise", 0.0242, 0.0052],
        ["Random Forest", "Attractiveness", -0.0030, 0.0029],
        ["Random Forest", "Parasocial Interaction", 0.7126, 0.0471],
        ["Random Forest", "Product-Influencer Fit", 0.0841, 0.0092],
        ["Extra Trees", "Trustworthiness", 0.0197, 0.0078],
        ["Extra Trees", "Expertise", 0.0070, 0.0100],
        ["Extra Trees", "Attractiveness", 0.0008, 0.0021],
        ["Extra Trees", "Parasocial Interaction", 0.7168, 0.0418],
        ["Extra Trees", "Product-Influencer Fit", 0.1029, 0.0127],
        ["Gradient Boosting", "Trustworthiness", 0.0108, 0.0059],
        ["Gradient Boosting", "Expertise", 0.0375, 0.0120],
        ["Gradient Boosting", "Attractiveness", 0.0137, 0.0077],
        ["Gradient Boosting", "Parasocial Interaction", 0.7318, 0.0407],
        ["Gradient Boosting", "Product-Influencer Fit", 0.1036, 0.0167],
    ]
    return pd.DataFrame(rows, columns=["Model", "Predictor", "Permutation_importance_R2", "Importance_SD"])


def build_analysis_summary() -> pd.DataFrame:
    return pd.DataFrame(
        [
            ["Primary analytical sample", "1000 valid survey responses"],
            ["Measurement scale", "Seven-point Likert scale"],
            ["Core constructs", "Trustworthiness; Expertise; Attractiveness; Parasocial Interaction; Product-Influencer Fit; Purchase Intention"],
            ["Structural analysis", "SEM-style path modelling with mediation and moderation testing"],
            ["Machine-learning task", "Regression prediction of purchase intention"],
            ["Best main ML models", "Linear Regression and Ridge Regression"],
            ["Best main ML performance", "RMSE = 1.025; MAE = 0.787; Test R2 = 0.762"],
            ["Dominant main predictor", "Parasocial Interaction"],
        ],
        columns=["Item", "Value"],
    )


def export_workbook(output_path: Path) -> None:
    sheets = {
        "Analysis_Summary": build_analysis_summary(),
        "Descriptive_Statistics": build_descriptive_statistics(),
        "Reliability_Validity": build_reliability_validity(),
        "Correlation_Matrix": build_correlation_matrix(),
        "Structural_Results": build_structural_results(),
        "Mediation_Results": build_mediation_results(),
        "Moderation_Results": build_moderation_results(),
        "ML_Model_Performance": build_ml_performance(),
        "ML_Feature_Importance": build_feature_importance(),
    }

    with pd.ExcelWriter(output_path, engine="openpyxl") as writer:
        for sheet_name, df in sheets.items():
            df.to_excel(writer, sheet_name=sheet_name, index=False)


def main() -> None:
    root = repo_root()
    out_dir = ensure_outputs_dir(root)
    output_path = out_dir / "Main_SEM_ML_Results.xlsx"
    export_workbook(output_path)
    print(f"Saved main SEM-ML reproducibility output: {output_path}")


if __name__ == "__main__":
    main()
