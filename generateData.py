# Genarate dummy patient-condition data (Similar to PCCIU)

import random
import csv

# Save the data to a CSV file
patientFilename = "./data/patients_random_1K.csv"
weightFilename = "./data/patientsWeights_random_1K.csv"

# Number of patients and health conditions
num_patients = 1000
num_conditions = 40
min_sparse_factor = 0.025 # To control min #conditions for patients
max_sparse_factor = 0.2 # To control max #conditions for patients

# List of health conditions
health_conditions = [
    'Hypertension', 'CHD', 'StrokeTIA', 'CKD', 'PeripheralVascularDisease',
    'AtrialFibrillation', 'HeartFailure', 'Diabetes', 'COPD', 'Asthma',
    'Bronchiectasis', 'PainfulCondition', 'Depression', 'Anxiety',
    'SchizophreniaBipolar', 'Dementia', 'EatingDisorders', 'LearningDisability',
    'AlcoholProblems', 'SubstanceProblems', 'ThyroidDisorders',
    'InflammatoryArthritis', 'HearingImpairment', 'VisualImpairment',
    'RecentCancer', 'Dyspepsia', 'IrritableBowelSyndrome', 'Constipation',
    'DiverticularDisease', 'InflammatoryBowelDisease', 'ChronicSinusitis',
    'ViralHepatitis', 'ChronicLiverDisease', 'ProstateDisorders', 'Glaucoma',
    'Epilepsy', 'Migraine', 'ParkinsonsDisease', 'MultipleSclerosis',
    'PsoriasisEczema'
]

# List of cities in the UK
uk_cities = [
    'London', 'Birmingham', 'Glasgow', 'Liverpool', 'Bristol',
    'Manchester', 'Sheffield', 'Leeds', 'Edinburgh', 'Leicester',
    'Coventry', 'Bradford', 'Cardiff', 'Belfast', 'Nottingham',
    'Kingston upon Hull', 'Newcastle upon Tyne', 'Stoke-on-Trent',
    'Southampton', 'Derby'
]

# Generate random matrix for health conditions
patient_matrix = []
for _ in range(num_patients):
    sparse_factor = random.uniform(min_sparse_factor, max_sparse_factor)
    patient_conditions = [0] * num_conditions
    num_ones = max(1, int(num_conditions * sparse_factor))
    ones_indices = random.sample(range(num_conditions), num_ones)
    for index in ones_indices:
        patient_conditions[index] = 1
    patient_matrix.append(patient_conditions)

# Generate random attributes for each patient
patients_data = []
for i in range(1, num_patients + 1):
    age = random.randint(40, 99)
    sex = random.choice([1, 2])
    carstairs_score = round(random.uniform(0, 10), 2)
    bmi = round(random.uniform(18.5, 40), 2)
    location = random.choice(uk_cities)
    patients_data.append([i, age, sex, carstairs_score, bmi, location])

with open(patientFilename, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['PatientID', 'Age', 'Sex', 'CarstairsScore', 'BMI', 'Location'] + health_conditions)  # Write header row
    for patient, health_conditions in zip(patients_data, patient_matrix):
        writer.writerow(patient + health_conditions)  # Write patient attributes and health conditions
        
# Generate weights data
weights_data = [random.randint(1, 10) for _ in range(num_patients)] # (randomly between 1 and 10)
# weights_data = [1] * num_patients # (all 1, i.e., equal weights)

# Save the weights data to a TXT file
with open(weightFilename, 'w') as txtfile:
    for weight in weights_data:
        txtfile.write(f"{weight}\n")

print(f"Patient data saved to {patientFilename}")
print(f"Patients' weights saved to {weightFilename}")
