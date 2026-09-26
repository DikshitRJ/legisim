import json
import os
import random
import re

# Set random seed for reproducibility
random.seed(42)

REGIONS = {
    "Uttar Pradesh": 28, "Maharashtra": 28, "Bihar": 28, "West Bengal": 28, "Madhya Pradesh": 28, "Tamil Nadu": 28,
    "Rajasthan": 20, "Karnataka": 20, "Gujarat": 20, "Andhra Pradesh": 20, "Odisha": 20, "Telangana": 20, "Kerala": 20,
    "Jharkhand": 16, "Assam": 16, "Punjab": 16, "Chhattisgarh": 16, "Haryana": 16, "Delhi (NCT)": 16,
    "Jammu & Kashmir": 10, "Uttarakhand": 10, "Himachal Pradesh": 10, "Tripura": 10, "Meghalaya": 10, "Manipur": 10, "Goa": 10, "Puducherry": 10,
    "Nagaland": 7, "Arunachal Pradesh": 7, "Mizoram": 7, "Sikkim": 7, "Chandigarh": 7, "Ladakh": 7, "Andaman & Nicobar Islands": 7, "Lakshadweep": 7, "Dadra & Nagar Haveli and Daman & Diu": 7
}

AGE_BANDS = ["18-25", "26-40", "41-60", "60+"]
AGE_WEIGHTS = [0.30, 0.35, 0.25, 0.10]

GENDERS = ["Male", "Female", "Other", "Mixed"]
GENDER_WEIGHTS = [0.45, 0.45, 0.05, 0.05]

INCOME_BANDS = ["BPL", "Low", "Lower-Middle", "Middle", "Upper-Middle", "High"]
INCOME_WEIGHTS = [0.20, 0.25, 0.25, 0.20, 0.07, 0.03]

URBAN_RURAL = ["Urban", "Rural", "Semi-Urban"]
URBAN_RURAL_WEIGHTS = [0.32, 0.53, 0.15]

EDUCATIONS = ["None", "Primary", "Secondary", "Higher-Secondary", "Vocational/Diploma", "Graduate", "Post-Graduate", "Professional"]

# Occupations mapped roughly to urban/rural
OCCUPATIONS = {
    "Rural": [
        "Marginal farmer", "Cash-crop farmer", "Horticulture farmer", "Landless agricultural laborer", 
        "Dairy farmer", "Poultry farmer", "Marine fisherfolk", "Inland fisherfolk", "Tea garden worker", 
        "Coffee/rubber plantation worker", "Spice plantation farmer", "Sericulture farmer", "Beekeeper", 
        "Forest-produce gatherer", "Shifting cultivator", "Nomadic pastoralist", "Salt-pan worker", 
        "Handloom weaver", "Handicraft artisan", "Boat builder", "Migrant brick-kiln laborer",
        "Panchayat functionary", "Rural kirana shop owner", "Traditional healer"
    ],
    "Semi-Urban": [
        "Kirana shop owner", "Wholesale trader", "Cloth merchant", "Dhaba/restaurant owner", 
        "Small hotel owner", "Auto-rickshaw driver", "Construction daily-wage laborer", "Mason", 
        "Tailor", "Two-wheeler mechanic", "Barber/salon worker", "Government-school teacher", 
        "Police constable", "ASHA/community health worker", "Anganwadi worker", "MSME manufacturing worker",
        "Small online seller"
    ],
    "Urban": [
        "Street vendor", "E-rickshaw driver", "App-based cab driver", "Food-delivery gig worker", 
        "Domestic worker", "Security guard", "Sanitation worker", "Rag picker/waste worker", 
        "Long-haul truck driver", "Railway/market porter", "Laundry worker", "Textile mill worker", 
        "Garment export factory worker", "IT software professional", "BPO/call-center employee", 
        "Bank employee", "Government clerk", "Private-school teacher", "College lecturer", 
        "Government-hospital doctor", "Private-practice doctor", "Nurse", "Pharmacist", "Lawyer", 
        "Chartered accountant", "Journalist", "Corporate mid-manager", "Corporate senior executive", 
        "Startup founder", "Civil engineer/architect", "NGO/social worker", "Municipal employee",
        "Job-seeking unemployed youth"
    ]
}

def generate_id(region, occupation, age, gender, income):
    # Create a slug from region
    region_slug = re.sub(r'[^a-z0-9]', '', region.lower())[:5]
    occ_slug = re.sub(r'[^a-z0-9_]', '_', occupation.lower().replace(" ", "_").replace("/", "_"))[:15].strip('_')
    age_slug = "y" if age == "18-25" else "m" if age in ["26-40", "41-60"] else "o"
    gender_slug = gender[0].lower()
    inc_slug = income.lower().split('-')[0][:3]
    return f"{region_slug}_{occ_slug}_{inc_slug}_{age_slug}{gender_slug}"

def get_education_literacy(income, age, urban_rural):
    # Basic heuristic
    if income in ["BPL", "Low"] and urban_rural == "Rural" and age in ["41-60", "60+"]:
        edu = random.choices(["None", "Primary"], weights=[0.7, 0.3])[0]
        lit = "Illiterate" if edu == "None" and random.random() < 0.8 else "Literate"
    elif income in ["Upper-Middle", "High"]:
        edu = random.choices(["Graduate", "Post-Graduate", "Professional"], weights=[0.4, 0.4, 0.2])[0]
        lit = "Literate"
    else:
        # middle ground
        edu = random.choices(["Primary", "Secondary", "Higher-Secondary", "Vocational/Diploma", "Graduate"], weights=[0.1, 0.3, 0.3, 0.1, 0.2])[0]
        lit = "Literate"
    return edu, lit

def get_spend_mix(income):
    if income == "BPL":
        base = [random.uniform(0.50, 0.55), random.uniform(0.08, 0.12), random.uniform(0.04, 0.06), random.uniform(0.10, 0.15), random.uniform(0.02, 0.05), random.uniform(0.08, 0.12)]
    elif income == "Low":
        base = [random.uniform(0.40, 0.45), random.uniform(0.12, 0.15), random.uniform(0.06, 0.08), random.uniform(0.10, 0.12), random.uniform(0.04, 0.06), random.uniform(0.12, 0.15)]
    elif income == "Lower-Middle":
        base = [random.uniform(0.32, 0.38), random.uniform(0.15, 0.18), random.uniform(0.08, 0.10), random.uniform(0.08, 0.10), random.uniform(0.07, 0.10), random.uniform(0.15, 0.18)]
    elif income == "Middle":
        base = [random.uniform(0.22, 0.28), random.uniform(0.18, 0.22), random.uniform(0.10, 0.13), random.uniform(0.07, 0.09), random.uniform(0.10, 0.14), random.uniform(0.20, 0.25)]
    elif income == "Upper-Middle":
        base = [random.uniform(0.15, 0.20), random.uniform(0.20, 0.25), random.uniform(0.10, 0.12), random.uniform(0.06, 0.08), random.uniform(0.10, 0.15), random.uniform(0.25, 0.30)]
    else: # High
        base = [random.uniform(0.10, 0.15), random.uniform(0.22, 0.28), random.uniform(0.08, 0.10), random.uniform(0.05, 0.08), random.uniform(0.08, 0.12), random.uniform(0.32, 0.38)]
    
    # Normalize to exactly 1.0 (with 2 decimal places to be safe)
    total = sum(base)
    base = [b / total for b in base]
    # Round to 3 decimal places
    base = [round(b, 3) for b in base]
    # Adjust last one to ensure sum is exactly 1
    base[-1] = round(1.0 - sum(base[:-1]), 3)
    
    return {
        "food": max(0, min(1, base[0])),
        "housing": max(0, min(1, base[1])),
        "transport": max(0, min(1, base[2])),
        "healthcare": max(0, min(1, base[3])),
        "education": max(0, min(1, base[4])),
        "other": max(0, min(1, base[5]))
    }

def generate_cohorts():
    os.makedirs('personas', exist_ok=True)
    generated_ids = set()
    total_generated = 0
    
    for region, target in REGIONS.items():
        for _ in range(target):
            # Sample demographic attributes
            age = random.choices(AGE_BANDS, weights=AGE_WEIGHTS)[0]
            gender = random.choices(GENDERS, weights=GENDER_WEIGHTS)[0]
            income = random.choices(INCOME_BANDS, weights=INCOME_WEIGHTS)[0]
            ur = random.choices(URBAN_RURAL, weights=URBAN_RURAL_WEIGHTS)[0]
            
            occupation = random.choice(OCCUPATIONS[ur])
            
            # Specific occupation overrides for plausibility
            if income in ["Upper-Middle", "High"] and ur == "Rural":
                occupation = random.choice(["Cash-crop farmer", "Dairy farmer", "Horticulture farmer", "Kirana shop owner"])
            if income in ["BPL", "Low"] and occupation in ["IT software professional", "Corporate senior executive", "Startup founder"]:
                income = random.choice(["Lower-Middle", "Middle"])
            
            edu, lit = get_education_literacy(income, age, ur)
            
            base_id = generate_id(region, occupation, age, gender, income)
            pid = base_id
            counter = 1
            while pid in generated_ids:
                pid = f"{base_id}_{counter}"
                counter += 1
            generated_ids.add(pid)
            
            # Heuristics for numeric values
            # trust_in_govt
            trust = random.uniform(0.4, 0.6)
            if income in ["BPL", "Low"] or occupation in ["Landless agricultural laborer", "Street vendor", "Migrant brick-kiln laborer"]:
                trust -= random.uniform(0.1, 0.3)
            if income in ["Upper-Middle", "High"] or "Government" in occupation or "officer" in occupation:
                trust += random.uniform(0.1, 0.3)
            trust = max(0.0, min(1.0, round(trust, 3)))
            
            # agreeableness
            agree = random.uniform(0.4, 0.7)
            if occupation in ["Marginal farmer", "Factory worker", "Student"]:
                agree -= random.uniform(0.1, 0.2) # More likely to mobilize
            if income in ["Middle", "Upper-Middle", "High"]:
                agree += random.uniform(0.1, 0.2) # Generally prefer status quo/smooth
            agree = max(0.0, min(1.0, round(agree, 3)))
            
            # ideological_lean
            lean = random.uniform(-0.6, 0.6)
            if ur == "Urban" and income in ["Middle", "Upper-Middle", "High"]:
                lean += random.uniform(0.1, 0.4)
            if ur == "Rural" and income in ["BPL", "Low"]:
                lean -= random.uniform(0.1, 0.4)
            lean = max(-1.0, min(1.0, round(lean, 3)))
            
            # size & weight
            # rough scale: BPL/Low/Rural is huge, High/Urban is smaller
            size = random.randint(100_000, 5_000_000)
            if income in ["High"]:
                size = random.randint(10_000, 500_000)
            if region in ["Lakshadweep", "Ladakh", "Sikkim"]:
                size = random.randint(1_000, 50_000)
                
            weight = round(size / 1_400_000_000, 7)
            
            persona = {
                "$schema": "https://json-schema.org/draft/2020-12/schema",
                "title": "LegiSim Persona",
                "description": "Schema for a population cohort persona in the LegiSim engine.",
                "id": pid,
                "demographics": {
                    "region": region,
                    "age_band": age,
                    "gender": gender,
                    "income_band": income,
                    "occupation": occupation,
                    "urban_rural": ur,
                    "education": edu,
                    "literacy": lit
                },
                "spend_mix": get_spend_mix(income),
                "trust_in_govt": trust,
                "ideological_lean": lean,
                "agreeableness": agree,
                "size": size,
                "weight": weight
            }
            
            with open(f"personas/{pid}.json", "w") as f:
                json.dump(persona, f, indent=2)
            total_generated += 1
            
    # Also ensure the worked examples from prompt are added, or enough are generated
    # (We are generating 547 here, we can add some examples to reach ~555)

if __name__ == '__main__':
    generate_cohorts()
    print("Done generating personas.")
