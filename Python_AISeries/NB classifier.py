from collections import Counter

# Training data: (shoot?, distanceToTargetDiscrete, weaponType)
data = [
    ("Y", "Close", "pistol"),
    ("Y", "Close", "rifle"),
    ("N", "Far", "rifle"),
    ("Y", "Far", "rifle"),
    ("N", "Close", "pistol"),
    ("N", "Far", "pistol"),
    ("Y", "Close", "rifle"),
]

# Count occurrences for prior probabilities
total_count = len(data)
shoot_count = sum(1 for d in data if d[0] == "Y")
no_shoot_count = total_count - shoot_count

prior_shoot = shoot_count / total_count
prior_no_shoot = no_shoot_count / total_count

# Count occurrences of (distance, weapon) for each class
counts_shoot = Counter((d[1], d[2]) for d in data if d[0] == "Y")
counts_no_shoot = Counter((d[1], d[2]) for d in data if d[0] == "N")

# Compute likelihood with Laplace smoothing
def likelihood(feature, label, counts, total):
    return (counts[feature] + 1) / (total + len(counts))  # Laplace smoothing

# Function to classify new input
def classify(distance, weapon):
    p_shoot = likelihood((distance, weapon), "Y", counts_shoot, shoot_count) * prior_shoot
    p_no_shoot = likelihood((distance, weapon), "N", counts_no_shoot, no_shoot_count) * prior_no_shoot

    print(f"\nP(Y | {distance}, {weapon}) = {p_shoot:.4f}")
    print(f"P(N | {distance}, {weapon}) = {p_no_shoot:.4f}")

    return "Shoot!" if p_shoot > p_no_shoot else "Don't Shoot."

# User input loop
while True:
    print("\nEnter details (or type 'exit' to quit):")
    distance = input("Distance to target (Close/Far): ").strip().capitalize()
    if distance.lower() == "exit":
        break
    
    weapon = input("Weapon Type (pistol/rifle): ").strip().lower()
    if weapon.lower() == "exit":
        break

    if distance not in ["Close", "Far"] or weapon not in ["pistol", "rifle"]:
        print("Invalid input! Enter 'Close' or 'Far' for distance and 'pistol' or 'rifle' for weapon.")
        continue

    # Get classification result
    decision = classify(distance, weapon)
    print(f"Decision: {decision}")
