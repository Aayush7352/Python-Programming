"""
Scikit-learn machine learning demonstration.

Requires: pip install scikit-learn numpy
"""
import sys


def main():
    try:
        from sklearn.datasets import load_iris, make_classification
        from sklearn.model_selection import train_test_split, cross_val_score
        from sklearn.preprocessing import StandardScaler, LabelEncoder
        from sklearn.linear_model import LogisticRegression
        from sklearn.tree import DecisionTreeClassifier
        from sklearn.ensemble import RandomForestClassifier
        from sklearn.svm import SVC
        from sklearn.metrics import (
            accuracy_score, confusion_matrix, classification_report,
            mean_squared_error, r2_score
        )
        from sklearn.pipeline import Pipeline
        import numpy as np
    except ImportError:
        print("scikit-learn not installed (pip install scikit-learn)")
        sys.exit(1)

    print("=== Scikit-learn ML Pipeline ===\n")

    # Load dataset
    iris = load_iris()
    X, y = iris.data, iris.target
    feature_names = iris.feature_names
    target_names = iris.target_names

    print(f"  Dataset: Iris")
    print(f"  Samples: {X.shape[0]}, Features: {X.shape[1]}")
    print(f"  Classes: {target_names}")

    # Train/test split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.3, random_state=42, stratify=y
    )
    print(f"\n  Train size: {X_train.shape[0]}, Test size: {X_test.shape[0]}")

    # Preprocessing
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    # Model training & evaluation
    models = {
        "Logistic Regression": LogisticRegression(max_iter=200),
        "Decision Tree": DecisionTreeClassifier(max_depth=3),
        "Random Forest": RandomForestClassifier(n_estimators=100),
        "SVM": SVC(kernel="rbf"),
    }

    print("\n=== Model Comparison ===")
    results = {}
    for name, model in models.items():
        model.fit(X_train_scaled, y_train)
        y_pred = model.predict(X_test_scaled)
        accuracy = accuracy_score(y_test, y_pred)
        results[name] = accuracy
        print(f"  {name:25} Accuracy: {accuracy:.4f}")

    # Cross-validation
    print("\n=== Cross-Validation (5-fold) ===")
    for name, model in models.items():
        scores = cross_val_score(model, X, y, cv=5)
        print(f"  {name:25} Mean: {scores.mean():.4f} (+/- {scores.std() * 2:.4f})")

    # Pipeline example
    print("\n=== Pipeline ===")
    pipeline = Pipeline([
        ("scaler", StandardScaler()),
        ("classifier", RandomForestClassifier(n_estimators=50, random_state=42)),
    ])
    pipeline.fit(X_train, y_train)
    y_pred = pipeline.predict(X_test)
    print(f"  Pipeline accuracy: {accuracy_score(y_test, y_pred):.4f}")

    # Detailed metrics
    print("\n=== Classification Report (Random Forest) ===")
    best_model = RandomForestClassifier(n_estimators=100, random_state=42)
    best_model.fit(X_train_scaled, y_train)
    y_pred = best_model.predict(X_test_scaled)

    print(f"\n  Confusion Matrix:")
    print(f"  {confusion_matrix(y_test, y_pred)}")
    print(f"\n  Classification Report:")
    print(f"  {classification_report(y_test, y_pred, target_names=target_names)}")

    # Feature importance
    print("\n=== Feature Importance (Random Forest) ===")
    for name, importance in zip(feature_names, best_model.feature_importances_):
        print(f"  {name:25} {importance:.4f}")

    # Regression example
    print("\n=== Regression ===")
    from sklearn.datasets import make_regression
    from sklearn.linear_model import LinearRegression
    from sklearn.ensemble import GradientBoostingRegressor

    X_reg, y_reg = make_regression(n_samples=200, n_features=5, noise=0.1, random_state=42)
    Xr_train, Xr_test, yr_train, yr_test = train_test_split(
        X_reg, y_reg, test_size=0.3, random_state=42
    )

    reg_models = {
        "Linear Regression": LinearRegression(),
        "Gradient Boosting": GradientBoostingRegressor(n_estimators=100),
    }

    print(f"\n  Regression dataset: {X_reg.shape}")
    for name, model in reg_models.items():
        model.fit(Xr_train, yr_train)
        yr_pred = model.predict(Xr_test)
        mse = mean_squared_error(yr_test, yr_pred)
        r2 = r2_score(yr_test, yr_pred)
        print(f"  {name:25} MSE: {mse:.4f}, R2: {r2:.4f}")


if __name__ == "__main__":
    main()
