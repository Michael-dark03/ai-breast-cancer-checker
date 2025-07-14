import pandas as pd
import numpy as np
from faker import Faker
import random
from datetime import datetime, timedelta

# Initialize faker
fake = Faker()

# Set random seed for reproducibility
np.random.seed(42)
random.seed(42)

# Generate synthetic data
data = []
for _ in range(10000):
    # Basic demographics
    age = random.randint(18, 85)
    bmi = round(random.uniform(18, 45), 1)
    family_history = random.choices([0, 1], weights=[0.7, 0.3])[0]
    menopause_status = 1 if age > 50 else random.choices([0, 1], weights=[0.9, 0.1])[0]
    
    # Self-check observations
    lump_present = random.choices([0, 1], weights=[0.85, 0.15])[0]
    if lump_present:
        lump_size = round(random.uniform(0.5, 5.0), 1)  # cm
        lump_fixed = random.choices([0, 1], weights=[0.4, 0.6])[0]
        lump_pain = random.choices([0, 1], weights=[0.7, 0.3])[0]
    else:
        lump_size = 0.0
        lump_fixed = 0
        lump_pain = random.choices([0, 1], weights=[0.9, 0.1])[0]
    
    # Other symptoms
    nipple_discharge = random.choices([0, 1], weights=[0.85, 0.15])[0]
    skin_changes = random.choices([0, 1], weights=[0.9, 0.1])[0]
    nipple_retraction = random.choices([0, 1], weights=[0.95, 0.05])[0]
    breast_pain = random.choices([0, 1], weights=[0.8, 0.2])[0]
    swelling = random.choices([0, 1], weights=[0.9, 0.1])[0]
    
    # Risk factors
    hormonal_therapy = random.choices([0, 1], weights=[0.8, 0.2])[0]
    oral_contraceptives = random.choices([0, 1], weights=[0.7, 0.3])[0] if age < 50 else 0
    alcohol_consumption = random.choices([0, 1], weights=[0.6, 0.4])[0]
    smoking = random.choices([0, 1], weights=[0.75, 0.25])[0]
    physical_activity = random.choices(['none', 'low', 'moderate', 'high'], 
                                     weights=[0.2, 0.3, 0.3, 0.2])[0]
    
    # Medical history
    previous_biopsy = random.choices([0, 1], weights=[0.85, 0.15])[0]
    mammogram_history = 1 if age > 40 else random.choices([0, 1], weights=[0.9, 0.1])[0]
    if mammogram_history:
        last_mammogram = fake.date_between(start_date='-5y', end_date='today')
    else:
        last_mammogram = None
    
    # Generate diagnosis based on symptoms and risk factors
    # Base probability of cancer
    cancer_prob = 0.01  # base rate
    
    # Increase probability based on risk factors
    cancer_prob += 0.15 if family_history else 0
    cancer_prob += 0.1 if hormonal_therapy else 0
    cancer_prob += 0.05 if smoking else 0
    cancer_prob += 0.05 if alcohol_consumption else 0
    cancer_prob += 0.02 * (age / 10)  # age factor
    cancer_prob += 0.1 if lump_present else 0
    cancer_prob += 0.05 if lump_fixed else 0
    cancer_prob += 0.03 if nipple_discharge else 0
    cancer_prob += 0.05 if skin_changes else 0
    cancer_prob += 0.04 if nipple_retraction else 0
    
    # Cap probability
    cancer_prob = min(cancer_prob, 0.95)
    
    # Generate diagnosis
    rand_val = random.random()
    if rand_val < cancer_prob * 0.7:  # 70% of high risk get cancer diagnosis
        diagnosis = 1  # cancer
    elif rand_val < cancer_prob:  # 30% of high risk get suspicious
        diagnosis = 2  # suspicious
    else:
        diagnosis = 0  # no cancer
    
    # Add some noise - sometimes cancer appears without obvious symptoms
    if random.random() < 0.02:  # 2% chance of silent cancer
        diagnosis = 1
    
    data.append({
        'age': age,
        'bmi': bmi,
        'family_history': family_history,
        'menopause_status': menopause_status,
        'lump_present': lump_present,
        'lump_size': lump_size,
        'lump_fixed': lump_fixed,
        'lump_pain': lump_pain,
        'nipple_discharge': nipple_discharge,
        'skin_changes': skin_changes,
        'nipple_retraction': nipple_retraction,
        'breast_pain': breast_pain,
        'swelling': swelling,
        'hormonal_therapy': hormonal_therapy,
        'oral_contraceptives': oral_contraceptives,
        'alcohol_consumption': alcohol_consumption,
        'smoking': smoking,
        'physical_activity': physical_activity,
        'previous_biopsy': previous_biopsy,
        'mammogram_history': mammogram_history,
        'last_mammogram': last_mammogram,
        'diagnosis': diagnosis
    })

# Create DataFrame
df = pd.DataFrame(data)

# Save to CSV
df.to_csv('breast_cancer_self_check_data.csv', index=False)