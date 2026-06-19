"""NailCareAI Core Constants."""

CLASS_LABELS = [
    "Darier's disease", "Muehrcke's lines", "Alopecia areata", "Beau's lines",
    "Bluish nail", "Clubbing", "Eczema", "Half and half nails (Lindsay's nails)",
    "Koilonychia", "Leukonychia", "Onycholysis", "Pale nail", "Red lunula",
    "Splinter hemorrhage", "Terry's nail", "White nail", "Yellow nails",
]

NUM_CLASSES = len(CLASS_LABELS)

DISEASE_INFO = {
    "Darier's disease": {"description": "Genetic disorder causing rough, scaly patches.", "symptoms": ["Nail pitting", "Red/white streaks"], "severity": "Moderate", "next_steps": "Consult dermatologist."},
    "Muehrcke's lines": {"description": "White bands from low albumin.", "symptoms": ["Parallel white lines"], "severity": "Low", "next_steps": "Check albumin levels."},
    "Alopecia areata": {"description": "Autoimmune hair loss affecting nails.", "symptoms": ["Nail pitting", "Rough nails"], "severity": "Moderate", "next_steps": "See dermatologist."},
    "Beau's lines": {"description": "Horizontal ridges from growth interruption.", "symptoms": ["Horizontal grooves"], "severity": "Low", "next_steps": "Identify underlying cause."},
    "Bluish nail": {"description": "Cyanosis indicating poor oxygenation.", "symptoms": ["Blue nail beds"], "severity": "High", "next_steps": "Seek immediate medical attention."},
    "Clubbing": {"description": "Enlarged fingertips with curved nails.", "symptoms": ["Bulbous fingertips"], "severity": "High", "next_steps": "Urgent evaluation needed."},
    "Eczema": {"description": "Inflammatory skin condition.", "symptoms": ["Red itchy skin"], "severity": "Moderate", "next_steps": "Dermatologist consultation."},
    "Half and half nails (Lindsay's nails)": {"description": "White base, red/brown tip.", "symptoms": ["Bicolor appearance"], "severity": "Moderate", "next_steps": "Check kidney function."},
    "Koilonychia": {"description": "Spoon-shaped nails.", "symptoms": ["Concave surface"], "severity": "Low", "next_steps": "Check iron levels."},
    "Leukonychia": {"description": "White spots from minor trauma.", "symptoms": ["White spots"], "severity": "Low", "next_steps": "Usually benign."},
    "Onycholysis": {"description": "Nail plate separation.", "symptoms": ["Nail lifting"], "severity": "Moderate", "next_steps": "Treat underlying cause."},
    "Pale nail": {"description": "Pale beds indicating anemia.", "symptoms": ["Pale nail bed"], "severity": "Moderate", "next_steps": "Complete blood count."},
    "Red lunula": {"description": "Red half-moon at nail base.", "symptoms": ["Red half-moon"], "severity": "Moderate", "next_steps": "Cardiovascular evaluation."},
    "Splinter hemorrhage": {"description": "Tiny blood clots under nails.", "symptoms": ["Dark red streaks"], "severity": "Low", "next_steps": "Usually from trauma."},
    "Terry's nail": {"description": "Mostly white with pink tip.", "symptoms": ["White nail", "Pink band"], "severity": "High", "next_steps": "Liver function tests."},
    "White nail": {"description": "Complete whitening.", "symptoms": ["Total white"], "severity": "Moderate", "next_steps": "Metabolic panel."},
    "Yellow nails": {"description": "Yellow discoloration.", "symptoms": ["Yellow color", "Thickened"], "severity": "Moderate", "next_steps": "Rule out fungus."},
}

MODEL_METADATA = {
    "name": "VGG-16 Nail Disease Classifier",
    "architecture": "VGG-16 (Transfer Learning)",
    "input_shape": (224, 224, 3),
    "output_classes": NUM_CLASSES,
    "version": "1.0.0",
}

MEDICAL_DISCLAIMER = "This AI screening tool is for informational purposes only. It is not a substitute for professional medical advice, diagnosis, or treatment. Always seek the advice of a qualified healthcare provider."
