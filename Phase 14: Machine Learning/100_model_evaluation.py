"""
Model evaluation techniques.

Requires: pip install scikit-learn numpy pandas matplotlib
"""
import sys


def main():
    try:
        import numpy as np
        from sklearn.datasets import make_classification, make_regression
        from sklearn.model_selection import (
            train_test_split, cross_val_score, KFold,
            learning_curve, validation_curve
        )
        from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
        from sklearn.metrics import (
            accuracy_score, precision_score, recall_score, f1_score,
            roc_auc_score, roc_curve, confusion_matrix, classification_report,
            mean_squared_error, r2_score, mean_absolute_error
        )
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except ImportError:
        print("Required packages not installed.")
        sys.exit(1)

    print("=== Model Evaluation Techniques ===\n")

    # Generate classification dataset
    X, y = make_classification(
        n_samples=1000, n_features=20, n_informative=10,
        n_redundant=5, random_state=42
    )
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.3, random_state=42
    )

    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    y_proba = model.predict_proba(X_test)[:, 1]

    # 1. Basic metrics
    print("1. Classification Metrics")
    print(f"   Accuracy:  {accuracy_score(y_test, y_pred):.4f}")
    print(f"   Precision: {precision_score(y_test, y_pred):.4f}")
    print(f"   Recall:    {recall_score(y_test, y_pred):.4f}")
    print(f"   F1-Score:  {f1_score(y_test, y_pred):.4f}")
    print(f"   ROC-AUC:   {roc_auc_score(y_test, y_proba):.4f}")

    # 2. Confusion Matrix
    print(f"\n2. Confusion Matrix")
    cm = confusion_matrix(y_test, y_pred)
    print(f"   {cm}")

    # 3. Classification Report
    print(f"\n3. Classification Report")
    print(f"   {classification_report(y_test, y_pred)}")

    # 4. ROC Curve
    print("\n4. ROC Curve (saved to /tmp/roc_curve.png)")
    fpr, tpr, thresholds = roc_curve(y_test, y_proba)
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.plot(fpr, tpr, label=f"ROC Curve (AUC = {roc_auc_score(y_test, y_proba):.3f})")
    ax.plot([0, 1], [0, 1], "k--", label="Random Classifier")
    ax.set_xlabel("False Positive Rate")
    ax.set_ylabel("True Positive Rate")
    ax.set_title("ROC Curve")
    ax.legend()
    fig.savefig("/tmp/roc_curve.png", dpi=100)
    plt.close()

    # 5. Cross-validation
    print("\n5. Cross-Validation")
    kfold = KFold(n_splits=5, shuffle=True, random_state=42)
    cv_scores = cross_val_score(model, X, y, cv=kfold, scoring="accuracy")
    print(f"   Scores: {cv_scores.round(4)}")
    print(f"   Mean: {cv_scores.mean():.4f} (+/- {cv_scores.std() * 2:.4f})")

    # 6. Learning curves
    print("\n6. Learning Curves (saved to /tmp/learning_curve.png)")
    train_sizes, train_scores, test_scores = learning_curve(
        model, X, y, cv=5, n_jobs=-1,
        train_sizes=np.linspace(0.1, 1.0, 10),
        scoring="accuracy"
    )
    train_mean = np.mean(train_scores, axis=1)
    test_mean = np.mean(test_scores, axis=1)

    fig, ax = plt.subplots(figsize=(8, 6))
    ax.plot(train_sizes, train_mean, "o-", label="Training Score")
    ax.plot(train_sizes, test_mean, "o-", label="Validation Score")
    ax.set_xlabel("Training Examples")
    ax.set_ylabel("Score")
    ax.set_title("Learning Curves")
    ax.legend()
    fig.savefig("/tmp/learning_curve.png", dpi=100)
    plt.close()

    # 7. Regression metrics
    print("\n7. Regression Metrics")
    X_reg, y_reg = make_regression(
        n_samples=500, n_features=10, noise=0.1, random_state=42
    )
    Xr_train, Xr_test, yr_train, yr_test = train_test_split(
        X_reg, y_reg, test_size=0.3, random_state=42
    )
    reg_model = RandomForestRegressor(n_estimators=100, random_state=42)
    reg_model.fit(Xr_train, yr_train)
    yr_pred = reg_model.predict(Xr_test)

    mse = mean_squared_error(yr_test, yr_pred)
    rmse = np.sqrt(mse)
    mae = mean_absolute_error(yr_test, yr_pred)
    r2 = r2_score(yr_test, yr_pred)

    print(f"   MSE:  {mse:.4f}")
    print(f"   RMSE: {rmse:.4f}")
    print(f"   MAE:  {mae:.4f}")
    print(f"   R²:   {r2:.4f}")

    # 8. Overfitting detection
    print("\n8. Overfitting Detection")
    train_score = model.score(X_train, y_train)
    test_score = model.score(X_test, y_test)
    print(f"   Training accuracy: {train_score:.4f}")
    print(f"   Test accuracy: {test_score:.4f}")
    print(f"   Gap: {train_score - test_score:.4f}")
    if train_score - test_score > 0.1:
        print("   WARNING: Possible overfitting detected!")
    else:
        print("   Model generalizes well.")

    # 9. Feature importance
    print("\n9. Feature Importance")
    importances = model.feature_importances_
    top_k = 5
    top_indices = np.argsort(importances)[-top_k:][::-1]
    print(f"   Top {top_k} features:")
    for idx in top_indices:
        print(f"     Feature {idx}: {importances[idx]:.4f}")

    print("\n=== Model Evaluation Summary ===")
    print("  1. Classification: Accuracy, Precision, Recall, F1, ROC-AUC")
    print("  2. Regression: MSE, RMSE, MAE, R²")
    print("  3. Cross-validation for robust estimation")
    print("  4. Learning curves for bias/variance diagnosis")
    print("  5. Confusion matrix for detailed analysis")
    print("  6. Feature importance for interpretability")
    print("  7. Overfitting detection (train vs test gap)")


if __name__ == "__main__":
    main()
