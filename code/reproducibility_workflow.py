"""
Complete reproducibility workflow
=================================

Purpose
-------
Runs the reproducibility workflow for the influencer marketing SEM-ML study.
The workflow generates:

1. Main SEM-style and machine-learning output workbook
2. External robustness validation output workbook, if the external dataset and
   external validation script are available
3. A compact workflow summary file

Expected repository layout
--------------------------
Influencer-Marketing-SEM-ML-Reproducibility/
├── code/
│   ├── main_sem_ml_analysis.py
│   ├── external_validation_option_A.py
│   └── reproducibility_workflow.py
├── data/
│   └── Influencer marketing dataset.xlsx      optional location
└── outputs/

Run
---
python code/reproducibility_workflow.py

Notes
-----
The main SEM-ML script uses the fixed finalized analytical values reported in
manuscript/supplementary outputs. The external validation script reruns Option A
using the independent influencer-marketing dataset when the Excel file is present.
"""

from __future__ import annotations

from pathlib import Path
import shutil
import subprocess
import sys
import pandas as pd


EXPECTED_EXTERNAL_PERFORMANCE = pd.DataFrame(
    [
        ["Gradient Boosting", 0.668, 0.799, 0.030],
        ["Random Forest", 0.680, 0.816, 0.010],
        ["SVR", 0.666, 0.828, -0.045],
        ["Ridge Regression", 0.800, 0.954, -0.361],
        ["Linear Regression", 0.817, 0.977, -0.435],
    ],
    columns=["Model", "MAE", "RMSE", "R2"],
)

EXPECTED_EXTERNAL_IMPORTANCE = pd.DataFrame(
    [
        ["Entertainment_Value", 0.251],
        ["Trustworthiness", 0.091],
        ["Information_Credibility", 0.083],
        ["Argument_Quality", 0.046],
        ["Expertise", 0.035],
    ],
    columns=["Feature", "Importance"],
)


def repo_root() -> Path:
    script_path = Path(__file__).resolve()
    if script_path.parent.name == "code":
        return script_path.parent.parent
    return script_path.parent


def run_python(script: Path, cwd: Path) -> tuple[bool, str]:
    if not script.exists():
        return False, f"Missing script: {script}"

    result = subprocess.run(
        [sys.executable, str(script)],
        cwd=str(cwd),
        capture_output=True,
        text=True,
        check=False,
    )
    message = result.stdout.strip()
    if result.stderr.strip():
        message = f"{message}\nSTDERR:\n{result.stderr.strip()}".strip()
    return result.returncode == 0, message


def locate_external_dataset(root: Path) -> Path | None:
    candidates = [
        root / "Influencer marketing dataset.xlsx",
        root / "data" / "Influencer marketing dataset.xlsx",
        root / "data" / "external" / "Influencer marketing dataset.xlsx",
        root / "data" / "external_dataset" / "Influencer marketing dataset.xlsx",
    ]
    for path in candidates:
        if path.exists():
            return path
    return None


def prepare_external_dataset_for_script(root: Path) -> tuple[bool, str]:
    """Place a copy of the external dataset in root if needed by the script."""
    target = root / "Influencer marketing dataset.xlsx"
    if target.exists():
        return True, "External dataset found in repository root."

    source = locate_external_dataset(root)
    if source is None:
        return False, "External dataset not found. External validation step skipped."

    shutil.copy2(source, target)
    return True, f"Copied external dataset from {source.relative_to(root)} to repository root for script execution."


def move_external_output(root: Path) -> str:
    outputs_dir = root / "outputs"
    outputs_dir.mkdir(exist_ok=True)
    source = root / "External_Validation_Option_A_Results.xlsx"
    destination = outputs_dir / "External_Validation_Option_A_Results.xlsx"
    if source.exists():
        shutil.move(str(source), str(destination))
        return f"Moved external validation output to {destination.relative_to(root)}."
    if destination.exists():
        return f"External validation output already exists at {destination.relative_to(root)}."
    return "External validation output was not created."


def create_expected_external_summary(root: Path) -> Path:
    outputs_dir = root / "outputs"
    outputs_dir.mkdir(exist_ok=True)
    output_path = outputs_dir / "External_Validation_Reported_Summary.xlsx"
    with pd.ExcelWriter(output_path, engine="openpyxl") as writer:
        EXPECTED_EXTERNAL_PERFORMANCE.to_excel(writer, sheet_name="Reported_Performance", index=False)
        EXPECTED_EXTERNAL_IMPORTANCE.to_excel(writer, sheet_name="Reported_Feature_Importance", index=False)
    return output_path


def create_workflow_summary(root: Path, records: list[dict[str, str]]) -> Path:
    outputs_dir = root / "outputs"
    outputs_dir.mkdir(exist_ok=True)
    summary_path = outputs_dir / "Reproducibility_Workflow_Summary.xlsx"
    pd.DataFrame(records).to_excel(summary_path, index=False)
    return summary_path


def main() -> None:
    root = repo_root()
    code_dir = root / "code"
    if not code_dir.exists():
        code_dir = root
    outputs_dir = root / "outputs"
    outputs_dir.mkdir(exist_ok=True)

    records: list[dict[str, str]] = []

    main_script = code_dir / "main_sem_ml_analysis.py"
    ok, message = run_python(main_script, cwd=root)
    records.append({"Step": "Main SEM-ML output", "Status": "Completed" if ok else "Not completed", "Details": message})

    dataset_ok, dataset_msg = prepare_external_dataset_for_script(root)
    records.append({"Step": "External dataset preparation", "Status": "Completed" if dataset_ok else "Skipped", "Details": dataset_msg})

    external_script = code_dir / "external_validation_option_A.py"
    if dataset_ok and external_script.exists():
        ok, message = run_python(external_script, cwd=root)
        records.append({"Step": "External validation Option A", "Status": "Completed" if ok else "Not completed", "Details": message})
        move_msg = move_external_output(root)
        records.append({"Step": "Move external validation output", "Status": "Completed", "Details": move_msg})
    else:
        details = "External validation script or dataset missing. Reported summary workbook generated instead."
        records.append({"Step": "External validation Option A", "Status": "Skipped", "Details": details})

    expected_summary_path = create_expected_external_summary(root)
    records.append(
        {
            "Step": "Reported external validation summary",
            "Status": "Completed",
            "Details": f"Saved {expected_summary_path.relative_to(root)}",
        }
    )

    summary_path = create_workflow_summary(root, records)
    print(f"Workflow completed. Summary saved to: {summary_path}")
    print(pd.DataFrame(records).to_string(index=False))


if __name__ == "__main__":
    main()
