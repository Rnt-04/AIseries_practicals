import math
import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn import tree
import graphviz

# Step 1: Create the dataset
data = [
    ["Healthy", "Exposed", "With Ammo", "In Group", "Close", "Attack"],
    ["Healthy", "In Cover", "With Ammo", "In Group", "Close", "Attack"],
    ["Healthy", "In Cover", "With Ammo", "Alone", "Far Away", "Attack"],
    ["Healthy", "In Cover", "With Ammo", "Alone", "Close", "Defend"],
    ["Healthy", "In Cover", "Empty", "Alone", "Close", "Defend"],
    ["Healthy", "Exposed", "With Ammo", "Alone", "Close", "Defend"],
]

# Step 2: Convert data into a pandas DataFrame
columns = ["Health", "Cover", "Ammo", "Grouping", "Distance", "Decision"]
df = pd.DataFrame(data, columns=columns)

# Convert categorical variables to numerical values
for col in df.columns:
    df[col] = df[col].astype("category").cat.codes  # Convert categories to numbers

# Step 3: Split data into features (X) and target (y)
X = df.drop(columns=["Decision"])  # Features
y = df["Decision"]  # Target variable

# Step 4: Train Decision Tree Model
clf = DecisionTreeClassifier(criterion="entropy")  # Using entropy for Information Gain
clf.fit(X, y)

# Step 5: Visualize the Decision Tree in a separate window
dot_data = tree.export_graphviz(
    clf,
    out_file=None,
    feature_names=X.columns,
    class_names=["Attack", "Defend"],
    filled=True,
    rounded=True,
    special_characters=True,
)

# Create and display the decision tree using graphviz
graph = graphviz.Source(dot_data)
graph.view()  # Opens the decision tree in a new window
