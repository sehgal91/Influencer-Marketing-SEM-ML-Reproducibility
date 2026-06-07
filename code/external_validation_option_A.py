# ============================================================
# External Robustness Validation - Option A (Likert Regression)
# Dataset: Influencer marketing dataset.xlsx
# Purpose: Predict continuous purchase-intention score (1-5 Likert)
# ============================================================

import pandas as pd
import numpy as np

from sklearn.model_selection import RepeatedKFold, cross_validate
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LinearRegression, Ridge
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.svm import SVR
from sklearn.inspection import permutation_importance

# -----------------------------
# 1. Load dataset
# -----------------------------
file_path = "Influencer marketing dataset.xlsx"
df = pd.read_excel(file_path, sheet_name="Form responses 1")

# Remove empty rows/columns
df = df.dropna(how="all").dropna(axis=1, how="all")
df.columns = df.columns.astype(str).str.strip()

# -----------------------------
# 2. Define key columns
# -----------------------------
follow_col = "Do you follow any influencers on the social media sites?"
target_col = "Keeping in mind the influencer whose name you wrote in the above answer, rate the level of your agreement or disagreement to the following statements: [I would purchase brands endorsed by influencers.]"

# Keep respondents who follow influencers
analysis_df = df[df[follow_col].astype(str).str.strip().str.lower().eq("yes")].copy()

# -----------------------------
# 3. Likert coding
# -----------------------------
likert_map = {
    "Strongly Disagree": 1,
    "Disagree": 2,
    "Neither Agree nor Disagree": 3,
    "Agree": 4,
    "Strongly Agree": 5,
}

# Item labels used to build constructs
items = {
    "expert": "Keeping in mind the influencer whose name you wrote in the above answer, rate the level of your agreement or disagreement to the following statements: [I feel that the influencer is an expert.]",
    "experienced": "Keeping in mind the influencer whose name you wrote in the above answer, rate the level of your agreement or disagreement to the following statements: [I feel that the influencer is experienced.]",
    "qualified": "Keeping in mind the influencer whose name you wrote in the above answer, rate the level of your agreement or disagreement to the following statements: [I feel that the influencer is qualiﬁed.]",
    "skilled": "Keeping in mind the influencer whose name you wrote in the above answer, rate the level of your agreement or disagreement to the following statements: [I feel that the influencer is skilled.]",
    "dependable": "Keeping in mind the influencer whose name you wrote in the above answer, rate the level of your agreement or disagreement to the following statements: [I feel that the influencer is dependable.]",
    "honest": "Keeping in mind the influencer whose name you wrote in the above answer, rate the level of your agreement or disagreement to the following statements: [I feel that the influencer is honest.]",
    "reliable": "Keeping in mind the influencer whose name you wrote in the above answer, rate the level of your agreement or disagreement to the following statements: [I feel that the influencer is reliable.]",
    "friendly": "Keeping in mind the influencer whose name you wrote in the above answer, rate the level of your agreement or disagreement to the following statements: [I feel that the influencer is friendly.]",
    "likeable": "Keeping in mind the influencer whose name you wrote in the above answer, rate the level of your agreement or disagreement to the following statements: [I feel that the influencer is likeable.]",
    "convincing": "Keeping in mind the influencer whose name you wrote in the above answer, rate the level of your agreement or disagreement to the following statements: [I feel that his/her information is convincing.]",
    "strong_arguments": "Keeping in mind the influencer whose name you wrote in the above answer, rate the level of your agreement or disagreement to the following statements: [I feel that his/her information is supported by strong arguments.]",
    "believable": "Keeping in mind the influencer whose name you wrote in the above answer, rate the level of your agreement or disagreement to the following statements: [The influencer’s posts/videos provide believable information.]",
    "reliable_info": "Keeping in mind the influencer whose name you wrote in the above answer, rate the level of your agreement or disagreement to the following statements: [The influencer’s posts/videos provide reliable information.]",
    "exciting": "Keeping in mind the influencer whose name you wrote in the above answer, rate the level of your agreement or disagreement to the following statements: [The influencer’s posts/videos are exciting.]",
    "delightful": "Keeping in mind the influencer whose name you wrote in the above answer, rate the level of your agreement or disagreement to the following statements: [The influencer’s posts/videos are delightful.]",
    "thrilling": "Keeping in mind the influencer whose name you wrote in the above answer, rate the level of your agreement or disagreement to the following statements: [The influencer’s posts/videos are thrilling.]",
    "enjoyable": "Keeping in mind the influencer whose name you wrote in the above answer, rate the level of your agreement or disagreement to the following statements: [The influencer’s posts/videos are enjoyable.]",
}

for short_name, full_col in items.items():
    analysis_df[short_name] = analysis_df[full_col].map(likert_map)

analysis_df["Purchase_Intention_Target"] = analysis_df[target_col].map(likert_map)

# -----------------------------
# 4. Create composite predictors
# -----------------------------
analysis_df["Expertise"] = analysis_df[["expert", "experienced", "qualified", "skilled"]].mean(axis=1)
analysis_df["Trustworthiness"] = analysis_df[["dependable", "honest", "reliable"]].mean(axis=1)
analysis_df["Attractiveness_Likeability"] = analysis_df[["friendly", "likeable"]].mean(axis=1)
analysis_df["Argument_Quality"] = analysis_df[["convincing", "strong_arguments"]].mean(axis=1)
analysis_df["Information_Credibility"] = analysis_df[["believable", "reliable_info"]].mean(axis=1)
analysis_df["Entertainment_Value"] = analysis_df[["exciting", "delightful", "thrilling", "enjoyable"]].mean(axis=1)

predictors = [
    "Gender",
    "Age",
    "Educational Qualification",
    "How frequently do you use the above selected social media sites?",
    "Expertise",
    "Trustworthiness",
    "Attractiveness_Likeability",
    "Argument_Quality",
    "Information_Credibility",
    "Entertainment_Value",
]

model_df = analysis_df[predictors + ["Purchase_Intention_Target"]].dropna().copy()

X = model_df[predictors]
y = model_df["Purchase_Intention_Target"].astype(float)

# -----------------------------
# 5. Preprocessing
# -----------------------------
numeric_features = [
    "Expertise",
    "Trustworthiness",
    "Attractiveness_Likeability",
    "Argument_Quality",
    "Information_Credibility",
    "Entertainment_Value",
]

categorical_features = [col for col in predictors if col not in numeric_features]

preprocess = ColumnTransformer(
    transformers=[
        ("num", Pipeline([
            ("imputer", SimpleImputer(strategy="median")),
            ("scaler", StandardScaler())
        ]), numeric_features),
        ("cat", Pipeline([
            ("imputer", SimpleImputer(strategy="most_frequent")),
            ("onehot", OneHotEncoder(handle_unknown="ignore", sparse_output=False))
        ]), categorical_features),
    ]
)

# -----------------------------
# 6. Models and repeated CV
# -----------------------------
models = {
    "Linear Regression": LinearRegression(),
    "Ridge Regression": Ridge(alpha=1.0),
    "Random Forest": RandomForestRegressor(n_estimators=80, random_state=42, min_samples_leaf=3),
    "Gradient Boosting": GradientBoostingRegressor(random_state=42, max_depth=2, learning_rate=0.05, n_estimators=60),
    "SVR": SVR(kernel="rbf", C=1.0, epsilon=0.1),
}

cv = RepeatedKFold(n_splits=5, n_repeats=3, random_state=42)
scoring = {
    "MAE": "neg_mean_absolute_error",
    "RMSE": "neg_root_mean_squared_error",
    "R2": "r2",
}

results = []

for model_name, model in models.items():
    pipe = Pipeline([
        ("preprocess", preprocess),
        ("model", model)
    ])
    scores = cross_validate(pipe, X, y, cv=cv, scoring=scoring, n_jobs=1)
    results.append({
        "Model": model_name,
        "MAE": -scores["test_MAE"].mean(),
        "RMSE": -scores["test_RMSE"].mean(),
        "R2": scores["test_R2"].mean(),
        "MAE_SD": scores["test_MAE"].std(),
        "RMSE_SD": scores["test_RMSE"].std(),
        "R2_SD": scores["test_R2"].std(),
    })

results_df = pd.DataFrame(results).sort_values("RMSE")
print("\nExternal validation performance:")
print(results_df.round(3))

# -----------------------------
# 7. Feature importance for best model
# -----------------------------
best_model_name = results_df.iloc[0]["Model"]
best_model = models[best_model_name]
best_pipe = Pipeline([
    ("preprocess", preprocess),
    ("model", best_model)
])
best_pipe.fit(X, y)

perm = permutation_importance(
    best_pipe,
    X,
    y,
    n_repeats=30,
    random_state=42,
    scoring="neg_root_mean_squared_error"
)

importance_df = pd.DataFrame({
    "Feature": X.columns,
    "Permutation_importance_RMSE_increase": perm.importances_mean
}).sort_values("Permutation_importance_RMSE_increase", ascending=False)

summary_df = pd.DataFrame({
    "Item": [
        "Original rows",
        "Rows after influencer-following filter",
        "Final rows used for Option A regression",
        "Target variable",
        "Best model",
        "Validation method"
    ],
    "Value": [
        df.shape[0],
        analysis_df.shape[0],
        model_df.shape[0],
        "I would purchase brands endorsed by influencers (Likert 1-5)",
        best_model_name,
        "Repeated 5-fold cross-validation, 3 repeats"
    ]
})

construct_summary = model_df[numeric_features + ["Purchase_Intention_Target"]].describe().T

# -----------------------------
# 8. Save outputs
# -----------------------------
with pd.ExcelWriter("External_Validation_Option_A_Results.xlsx") as writer:
    summary_df.to_excel(writer, sheet_name="Validation_Summary", index=False)
    results_df.to_excel(writer, sheet_name="Model_Performance", index=False)
    importance_df.to_excel(writer, sheet_name="Feature_Importance", index=False)
    construct_summary.to_excel(writer, sheet_name="Construct_Summary")
    model_df.to_excel(writer, sheet_name="Processed_Model_Data", index=False)

print("\nBest model:", best_model_name)
print("\nTop predictors:")
print(importance_df.head(10).round(4))
print("\nSaved: External_Validation_Option_A_Results.xlsx")
