"""
Feature engineering techniques.

Requires: pip install scikit-learn numpy pandas
"""
import sys


def main():
    try:
        import numpy as np
        import pandas as pd
        from sklearn.preprocessing import (
            StandardScaler, MinMaxScaler, LabelEncoder,
            OneHotEncoder, PolynomialFeatures, KBinsDiscretizer,
            FunctionTransformer
        )
        from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
        from sklearn.feature_selection import SelectKBest, mutual_info_classif
        from sklearn.decomposition import PCA
    except ImportError:
        print("Required packages not installed.")
        print("pip install scikit-learn numpy pandas")
        sys.exit(1)

    print("=== Feature Engineering Techniques ===\n")

    # 1. Numerical feature scaling
    print("1. Feature Scaling")
    data = np.array([[100, 0.001], [200, 0.01], [300, 0.1], [400, 1.0], [500, 10.0]])

    standard_scaler = StandardScaler()
    minmax_scaler = MinMaxScaler()

    standardized = standard_scaler.fit_transform(data)
    normalized = minmax_scaler.fit_transform(data)

    print(f"  Original:\n{data}")
    print(f"  Standardized:\n{standardized.round(3)}")
    print(f"  MinMax Normalized:\n{normalized.round(3)}")

    # 2. Encoding categorical variables
    print("\n2. Encoding Categorical Variables")
    categories = ["red", "blue", "green", "blue", "red"]

    label_enc = LabelEncoder()
    encoded = label_enc.fit_transform(categories)
    print(f"  Label Encoded: {encoded}")

    onehot_enc = OneHotEncoder(sparse_output=False)
    onehot = onehot_enc.fit_transform(np.array(categories).reshape(-1, 1))
    print(f"  One-Hot Encoded:\n{onehot}")

    # 3. Polynomial features
    print("\n3. Polynomial Features")
    X = np.array([[1, 2], [3, 4], [5, 6]])
    poly = PolynomialFeatures(degree=2, include_bias=False)
    X_poly = poly.fit_transform(X)
    print(f"  Original:\n{X}")
    print(f"  Polynomial (degree=2):\n{X_poly}")
    print(f"  Feature names: {poly.get_feature_names_out()}")

    # 4. Binning
    print("\n4. Binning / Discretization")
    ages = np.array([18, 25, 34, 45, 52, 67, 81]).reshape(-1, 1)
    binner = KBinsDiscretizer(n_bins=3, encode="ordinal", strategy="uniform")
    binned = binner.fit_transform(ages)
    print(f"  Ages: {ages.ravel()}")
    print(f"  Binned: {binned.ravel()}")

    # 5. Text feature extraction
    print("\n5. Text Feature Extraction")
    documents = [
        "The quick brown fox jumps over the lazy dog",
        "Python is a great programming language",
        "Machine learning is transforming technology",
        "Python for data science and machine learning",
    ]

    vectorizer = CountVectorizer(stop_words="english")
    bow = vectorizer.fit_transform(documents)
    print(f"  Bag of Words shape: {bow.shape}")
    print(f"  Vocabulary: {list(vectorizer.get_feature_names_out()[:10])}...")

    tfidf = TfidfVectorizer(stop_words="english")
    tfidf_matrix = tfidf.fit_transform(documents)
    print(f"  TF-IDF shape: {tfidf_matrix.shape}")

    # 6. Feature selection
    print("\n6. Feature Selection")
    from sklearn.datasets import load_iris
    iris = load_iris()
    X, y = iris.data, iris.target

    selector = SelectKBest(score_func=mutual_info_classif, k=2)
    X_selected = selector.fit_transform(X, y)
    print(f"  Original features: {X.shape[1]}")
    print(f"  Selected features: {X_selected.shape[1]}")
    print(f"  Scores: {selector.scores_.round(3)}")
    print(f"  Selected indices: {selector.get_support(indices=True)}")

    # 7. Dimensionality reduction
    print("\n7. PCA (Dimensionality Reduction)")
    pca = PCA(n_components=2)
    X_pca = pca.fit_transform(X)
    print(f"  Original shape: {X.shape}")
    print(f"  PCA shape: {X_pca.shape}")
    print(f"  Explained variance ratio: {pca.explained_variance_ratio_.round(3)}")
    print(f"  Total variance explained: {pca.explained_variance_ratio_.sum():.3f}")

    # 8. Custom feature engineering
    print("\n8. Custom Feature Transformations")
    df = pd.DataFrame({
        "transaction_date": pd.date_range("2024-01-01", periods=5, freq="D"),
        "amount": [100, 250, 150, 300, 200],
        "category": ["food", "transport", "food", "entertainment", "transport"],
    })

    # Feature extraction from dates
    df["day_of_week"] = df["transaction_date"].dt.dayofweek
    df["is_weekend"] = df["day_of_week"].isin([5, 6]).astype(int)
    df["hour"] = 14  # placeholder

    print(f"  Engineered features:\n{df}")

    # 9. Interaction features
    print("\n9. Interaction Features")
    X = np.array([[1, 2], [3, 4], [5, 6]])
    interaction = PolynomialFeatures(degree=2, interaction_only=True, include_bias=False)
    X_inter = interaction.fit_transform(X)
    print(f"  Original:\n{X}")
    print(f"  Interaction features:\n{X_inter}")

    print("\n=== Feature Engineering Summary ===")
    print("  1. Scaling: StandardScaler, MinMaxScaler")
    print("  2. Encoding: LabelEncoder, OneHotEncoder")
    print("  3. Polynomial: PolynomialFeatures")
    print("  4. Binning: KBinsDiscretizer")
    print("  5. Text: CountVectorizer, TF-IDF")
    print("  6. Selection: SelectKBest, mutual_info")
    print("  7. Reduction: PCA, t-SNE")
    print("  8. Date features, aggregations")
    print("  9. Interaction features")


if __name__ == "__main__":
    main()
