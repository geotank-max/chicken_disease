# app/services/vet_seed_service.py
"""
Seeds sample veterinary clinics across Cambodian provinces.
Called once during initial DB setup.
"""
from extensions import db
from app.models.vet_clinic import VetClinic


SAMPLE_VET_CLINICS = [
    {
        "name": "Phnom Penh Poultry Veterinary Clinic",
        "phone": "023 987 654",
        "address": "Street 271, Sangkat Toul Tompong, Khan Chamkarmon",
        "province": "Phnom Penh",
        "district": "Chamkarmon",
        "latitude": 11.5564,
        "longitude": 104.9282,
        "specialization": "poultry, livestock",
    },
    {
        "name": "Battambang Animal Health Center",
        "phone": "053 952 111",
        "address": "National Road 5, Svay Pao, Battambang",
        "province": "Battambang",
        "district": "Battambang",
        "latitude": 13.1023,
        "longitude": 103.1986,
        "specialization": "poultry, general livestock",
    },
    {
        "name": "Siem Reap Vet Services",
        "phone": "063 966 321",
        "address": "Sivatha Blvd, Siem Reap",
        "province": "Siem Reap",
        "district": "Siem Reap",
        "latitude": 13.3633,
        "longitude": 103.8600,
        "specialization": "poultry, cattle",
    },
    {
        "name": "Kampong Cham Livestock Clinic",
        "phone": "042 941 202",
        "address": "Preah Bat Monivong Blvd, Kampong Cham",
        "province": "Kampong Cham",
        "district": "Kampong Cham",
        "latitude": 11.9942,
        "longitude": 105.4636,
        "specialization": "poultry, swine",
    },
    {
        "name": "Takeo Provincial Veterinary Office",
        "phone": "032 931 456",
        "address": "Doun Kaev, Takeo",
        "province": "Takeo",
        "district": "Doun Kaev",
        "latitude": 10.9908,
        "longitude": 104.7850,
        "specialization": "poultry, general",
    },
    {
        "name": "Prey Veng Animal Health Station",
        "phone": "043 944 789",
        "address": "National Road 1, Prey Veng",
        "province": "Prey Veng",
        "district": "Prey Veng",
        "latitude": 11.4847,
        "longitude": 105.3239,
        "specialization": "poultry, aquaculture",
    },
    {
        "name": "Kandal Poultry Doctor",
        "phone": "024 890 112",
        "address": "Ta Khmau, Kandal",
        "province": "Kandal",
        "district": "Ta Khmau",
        "latitude": 11.4818,
        "longitude": 104.9468,
        "specialization": "poultry",
    },
    {
        "name": "Kampong Speu Vet Center",
        "phone": "025 987 333",
        "address": "Chbar Mon, Kampong Speu",
        "province": "Kampong Speu",
        "district": "Chbar Mon",
        "latitude": 11.4519,
        "longitude": 104.5228,
        "specialization": "poultry, livestock",
    },
    {
        "name": "Banteay Meanchey Animal Clinic",
        "phone": "054 958 444",
        "address": "Sisophon, Banteay Meanchey",
        "province": "Banteay Meanchey",
        "district": "Sisophon",
        "latitude": 13.5859,
        "longitude": 102.9730,
        "specialization": "general livestock, poultry",
    },
    {
        "name": "Svay Rieng Poultry Health",
        "phone": "044 715 567",
        "address": "Svay Rieng Town, Svay Rieng",
        "province": "Svay Rieng",
        "district": "Svay Rieng",
        "latitude": 11.0879,
        "longitude": 105.7993,
        "specialization": "poultry",
    },
]


def seed_vet_clinics():
    """Insert sample vet clinics if none exist."""
    if VetClinic.query.first():
        return
    for data in SAMPLE_VET_CLINICS:
        clinic = VetClinic(**data)
        db.session.add(clinic)
    db.session.commit()
