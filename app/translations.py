# app/translations.py
"""
Localization and Translation Service for Chicken Disease Diagnosis System.
Supports Khmer ('km') as default, and English ('en').
"""
from typing import Any
from flask import session

DEFAULT_LANGUAGE = "km"

LANGUAGES = {
    "km": {
        "code": "km",
        "name": "ភាសាខ្មែរ",
        "english_name": "Khmer",
        "flag": "🇰🇭",
        "short": "ខ្មែរ",
    },
    "en": {
        "code": "en",
        "name": "English",
        "english_name": "English",
        "flag": "🇬🇧",
        "short": "EN",
    },
}

TRANSLATIONS: dict[str, dict[str, str]] = {
    # ── Brand & Navigation ──────────────────────────────────────────
    "brand.title": {
        "km": "IDNS",
        "en": "IDNS",
    },
    "brand.subtitle": {
        "km": "ប្រព័ន្ធវិភាគជំងឺមាន់",
        "en": "Chicken Diagnosis System",
    },
    "theme.switch_dark": {
        "km": "ប្តូរទៅទម្រង់ងងឹត (Dark Mode)",
        "en": "Switch to Dark Mode",
    },
    "theme.switch_light": {
        "km": "ប្តូរទៅទម្រង់ភ្លឺ (Light Mode)",
        "en": "Switch to Light Mode",
    },
    "theme.toggle": {
        "km": "ប្តូរទម្រង់ពន្លឺ/ងងឹត",
        "en": "Toggle Dark/Light Mode",
    },
    "nav.overview": {
        "km": "ទិដ្ឋភាពទូទៅ",
        "en": "Overview",
    },
    "nav.dashboard": {
        "km": "ផ្ទាំងគ្រប់គ្រង",
        "en": "Dashboard",
    },
    "nav.home": {
        "km": "ទំព័រដើម",
        "en": "Home",
    },
    "nav.diagnosis_section": {
        "km": "ការធ្វើរោគវិនិច្ឆ័យ",
        "en": "Diagnosis",
    },
    "nav.run_diagnosis": {
        "km": "វិភាគជំងឺថ្មី",
        "en": "Run Diagnosis",
    },
    "nav.case_history": {
        "km": "ប្រវត្តិករណី",
        "en": "Case History",
    },
    "nav.disease_library": {
        "km": "បណ្ណាល័យជំងឺ",
        "en": "Disease Library",
    },
    "nav.knowledge_base": {
        "km": "មូលដ្ឋានចំណេះដឹង",
        "en": "Knowledge Base",
    },
    "nav.rules": {
        "km": "ច្បាប់វិភាគ (Rules)",
        "en": "Rules",
    },
    "nav.symptoms": {
        "km": "រោគសញ្ញា",
        "en": "Symptoms",
    },
    "nav.diseases": {
        "km": "ជំងឺមាន់",
        "en": "Diseases",
    },
    "nav.categories": {
        "km": "ប្រភេទរោគសញ្ញា",
        "en": "Categories",
    },
    "nav.system": {
        "km": "ប្រព័ន្ធគ្រប់គ្រង",
        "en": "System",
    },
    "nav.users": {
        "km": "អ្នកប្រើប្រាស់",
        "en": "Users",
    },
    "nav.roles": {
        "km": "តួនាទី",
        "en": "Roles",
    },
    "nav.permissions": {
        "km": "សិទ្ធិអនុញ្ញាត",
        "en": "Permissions",
    },
    "nav.audit_logs": {
        "km": "កំណត់ត្រាសកម្មភាព",
        "en": "Audit Logs",
    },
    "nav.doctor_applications": {
        "km": "ពាក្យស្នើសុំវេជ្ជបណ្ឌិត",
        "en": "Doctor Applications",
    },
    "nav.account": {
        "km": "គណនី",
        "en": "Account",
    },
    "nav.apply_doctor": {
        "km": "ស្នើសុំជាវេជ្ជបណ្ឌិត",
        "en": "Apply as Doctor",
    },
    "nav.login": {
        "km": "ចូលប្រើប្រាស់",
        "en": "Login",
    },
    "nav.register": {
        "km": "ចុះឈ្មោះ",
        "en": "Register",
    },
    "nav.logout": {
        "km": "ចាកចេញ",
        "en": "Logout",
    },
    "nav.profile": {
        "km": "គណនីរបស់ខ្ញុំ",
        "en": "My Profile",
    },
    "nav.notifications": {
        "km": "ការជូនដំណឹង",
        "en": "Notifications",
    },
    "nav.language": {
        "km": "ភាសា",
        "en": "Language",
    },

    # ── Common Buttons & Actions ─────────────────────────────────────
    "btn.save": {
        "km": "រក្សាទុក",
        "en": "Save",
    },
    "btn.cancel": {
        "km": "បោះបង់",
        "en": "Cancel",
    },
    "btn.edit": {
        "km": "កែប្រែ",
        "en": "Edit",
    },
    "btn.delete": {
        "km": "លុប",
        "en": "Delete",
    },
    "btn.view": {
        "km": "មើល",
        "en": "View",
    },
    "btn.view_all": {
        "km": "មើលទាំងអស់",
        "en": "View All",
    },
    "btn.detail": {
        "km": "លម្អិត",
        "en": "Details",
    },
    "btn.print": {
        "km": "បោះពុម្ព",
        "en": "Print",
    },
    "btn.download": {
        "km": "ទាញយក",
        "en": "Download",
    },
    "btn.back": {
        "km": "ថយក្រោយ",
        "en": "Back",
    },
    "btn.next": {
        "km": "បន្ទាប់",
        "en": "Next",
    },
    "btn.submit": {
        "km": "ដាក់ស្នើ",
        "en": "Submit",
    },
    "btn.confirm": {
        "km": "បញ្ជាក់",
        "en": "Confirm",
    },
    "btn.close": {
        "km": "បិទ",
        "en": "Close",
    },
    "btn.search": {
        "km": "ស្វែងរក",
        "en": "Search",
    },
    "btn.filter": {
        "km": "ចម្រាញ់",
        "en": "Filter",
    },
    "btn.reset": {
        "km": "កំណត់ឡើងវិញ",
        "en": "Reset",
    },
    "btn.clear_filters": {
        "km": "សម្អាតការចម្រាញ់",
        "en": "Clear Filters",
    },
    "btn.restart_diagnosis": {
        "km": "វិភាគជាថ្មី",
        "en": "Start New Diagnosis",
    },
    "btn.apply_now": {
        "km": "ដាក់ពាក្យឥឡូវនេះ",
        "en": "Apply Now",
    },
    "btn.send": {
        "km": "ផ្ញើ",
        "en": "Send",
    },
    "btn.add": {
        "km": "បន្ថែម",
        "en": "Add",
    },
    "btn.create": {
        "km": "បង្កើតថ្មី",
        "en": "Create New",
    },

    # ── Common Statuses ──────────────────────────────────────────────
    "status.all": {
        "km": "ទាំងអស់",
        "en": "All",
    },
    "status.pending": {
        "km": "រង់ចាំពិនិត្យ",
        "en": "Pending",
    },
    "status.confirmed": {
        "km": "បានបញ្ជាក់",
        "en": "Confirmed",
    },
    "status.rejected": {
        "km": "បានបដិសេធ",
        "en": "Rejected",
    },
    "status.active": {
        "km": "សកម្ម",
        "en": "Active",
    },
    "status.inactive": {
        "km": "អសកម្ម",
        "en": "Inactive",
    },
    "status.good": {
        "km": "ស្ថានភាពល្អ",
        "en": "Good Condition",
    },
    "status.monitoring": {
        "km": "កំពុងតាមដាន",
        "en": "Under Monitoring",
    },

    # ── Follow-up Statuses ───────────────────────────────────────────
    "followup.none": {
        "km": "មិនទាន់មាន",
        "en": "None",
    },
    "followup.improving": {
        "km": "កំពុងធូរស្រាល",
        "en": "Improving",
    },
    "followup.not_improved": {
        "km": "មិនធូរស្រាល",
        "en": "Not Improved",
    },
    "followup.recovered": {
        "km": "ជាសះស្បើយ",
        "en": "Recovered",
    },
    "followup.dead": {
        "km": "ស្លាប់",
        "en": "Mortality/Dead",
    },
    "followup.needs_revisit": {
        "km": "ត្រូវពិនិត្យឡើងវិញ",
        "en": "Needs Revisit",
    },

    # ── Severity Levels ──────────────────────────────────────────────
    "severity.low": {
        "km": "កម្រិតស្រាល",
        "en": "Low",
    },
    "severity.medium": {
        "km": "កម្រិតមធ្យម",
        "en": "Medium",
    },
    "severity.high": {
        "km": "កម្រិតធ្ងន់ធ្ងរ",
        "en": "High",
    },
    "severity.critical": {
        "km": "កម្រិតអាសន្ន",
        "en": "Critical",
    },

    # ── Common Yes / No / Options ────────────────────────────────────
    "opt.yes": {
        "km": "បាទ/ចាស",
        "en": "Yes",
    },
    "opt.no": {
        "km": "ទេ",
        "en": "No",
    },
    "opt.unknown": {
        "km": "មិនដឹង",
        "en": "Unknown",
    },
    "opt.none": {
        "km": "គ្មាន / មិនមាន",
        "en": "None",
    },
    "opt.vax_none": {
        "km": "មិនបានចាក់",
        "en": "Not Vaccinated",
    },
    "opt.vax_partial": {
        "km": "ចាក់មិនគ្រប់",
        "en": "Partially Vaccinated",
    },
    "opt.vax_full": {
        "km": "ចាក់គ្រប់កម្រិត",
        "en": "Fully Vaccinated",
    },
    "opt.vax_completed": {
        "km": "បានចាក់គ្រប់",
        "en": "Fully Vaccinated",
    },
    "opt.coop_good": {
        "km": "ល្អ/ស្អាត",
        "en": "Good / Clean",
    },
    "opt.coop_fair": {
        "km": "មធ្យម",
        "en": "Fair",
    },
    "opt.coop_poor": {
        "km": "មិនល្អ/កខ្វក់",
        "en": "Poor / Dirty",
    },
    "opt.coop_clean": {
        "km": "ស្អាត",
        "en": "Clean",
    },
    "opt.coop_damp": {
        "km": "សើម",
        "en": "Damp / Humid",
    },
    "opt.coop_dirty": {
        "km": "កខ្វក់",
        "en": "Dirty / Unhygienic",
    },
    "opt.coop_crowded": {
        "km": "ណែនណាន់ / ចង្អៀត",
        "en": "Overcrowded",
    },
    "opt.intake_normal": {
        "km": "ធម្មតា",
        "en": "Normal",
    },
    "opt.intake_reduced": {
        "km": "ថយចុះ",
        "en": "Reduced",
    },
    "opt.intake_none": {
        "km": "ឈប់ស៊ី/ផឹក",
        "en": "None / Refused",
    },
    "opt.intake_increased": {
        "km": "កើនឡើង",
        "en": "Increased",
    },

    # ── User Home & Dashboard ────────────────────────────────────────
    "home.welcome_prefix": {
        "km": "សួស្តី",
        "en": "Welcome back",
    },
    "home.assistant_badge": {
        "km": "ជំនួយការសុខភាពហ្វូងមាន់",
        "en": "Flock Health Assistant",
    },
    "home.hero_subtitle": {
        "km": "ការពារ និងថែទាំហ្វូងមាន់របស់អ្នក ជាមួយនឹងប្រព័ន្ធវិភាគឆ្លាតវៃ និងការបញ្ជាក់ពីវេជ្ជបណ្ឌិត។",
        "en": "Protect and care for your poultry flock with intelligent rule-based diagnosis and veterinary verification.",
    },
    "home.start_diagnosis": {
        "km": "វិភាគជំងឺថ្មី",
        "en": "Start Diagnosis",
    },
    "home.duration_hint": {
        "km": "ចំណាយពេល ~១ នាទី",
        "en": "Takes ~1 minute",
    },
    "home.flock_status_title": {
        "km": "ស្ថានភាពទូទៅ",
        "en": "Flock Status",
    },
    "home.total_cases": {
        "km": "ករណីសរុប",
        "en": "Total Cases",
    },
    "home.pending_review": {
        "km": "រង់ចាំពិនិត្យ",
        "en": "Pending Review",
    },
    "home.confirmed_count": {
        "km": "បានបញ្ជាក់",
        "en": "Confirmed",
    },
    "home.this_week": {
        "km": "សប្តាហ៍នេះ",
        "en": "This Week",
    },
    "home.recent_cases_title": {
        "km": "ករណីថ្មីៗ",
        "en": "Recent Diagnoses",
    },
    "home.empty_cases_title": {
        "km": "អ្នកមិនទាន់មានករណីវិភាគទេ",
        "en": "No diagnosis cases yet",
    },
    "home.empty_cases_desc": {
        "km": "ចាប់ផ្តើមការធ្វើរោគវិនិច្ឆ័យដំបូងរបស់អ្នក ដើម្បីពិនិត្យសុខភាពហ្វូងមាន់។",
        "en": "Run your first diagnosis now to check the health status of your flock.",
    },
    "home.disease_spotlight": {
        "km": "ចំណេះដឹងជំងឺ",
        "en": "Disease Spotlight",
    },
    "home.read_full_guide": {
        "km": "អានមគ្គុទ្ទេសក៍ពេញលេញ",
        "en": "Read Full Guide",
    },
    "home.biosecurity_tips_title": {
        "km": "គន្លឹះថែទាំ និងសុវត្ថិភាពជីវសាស្រ្ត",
        "en": "Biosecurity & Flock Tips",
    },
    "home.tip_1": {
        "km": "ជ្រើសរើសរោគសញ្ញាច្រើនជាងមួយ ដើម្បីទទួលបានលទ្ធផលវិភាគកាន់តែច្បាស់។",
        "en": "Select multiple symptoms to achieve higher diagnosis confidence and accuracy.",
    },
    "home.tip_2": {
        "km": "ករណីដែលបានបញ្ជាក់ដោយវេជ្ជបណ្ឌិតមានភាពជឿជាក់ និងមានជំហានព្យាបាលច្បាស់លាស់។",
        "en": "Doctor-confirmed cases provide verified clinical diagnosis and structured treatment steps.",
    },
    "home.tip_3": {
        "km": "បើមាន់មានរោគសញ្ញាធ្ងន់ធ្ងរ សូមបំបែកមាន់ឈឺជាបន្ទាន់ និងទាក់ទងពេទ្យសត្វ។",
        "en": "Isolate severely sick birds immediately and contact local veterinary services.",
    },
    "home.doctor_cta_title": {
        "km": "តើអ្នកជាវេជ្ជបណ្ឌិតសត្វ?",
        "en": "Are you a Veterinarian?",
    },
    "home.doctor_cta_desc": {
        "km": "ដាក់ពាក្យដើម្បីទទួលបានសិទ្ធិពិនិត្យករណី។",
        "en": "Apply to gain reviewer access and assist local farmers.",
    },
    "home.confidence": {
        "km": "ភាពជឿជាក់",
        "en": "Confidence",
    },
    "home.flock_birds": {
        "km": "ក្បាល",
        "en": "birds",
    },
    "home.inconclusive": {
        "km": "មិនទាន់បញ្ជាក់",
        "en": "Inconclusive / Unverified",
    },

    # ── Admin Dashboard ──────────────────────────────────────────────
    "dashboard.title": {
        "km": "ផ្ទាំងគ្រប់គ្រងប្រព័ន្ធ",
        "en": "Dashboard",
    },
    "dashboard.subtitle": {
        "km": "ទិដ្ឋភាពទូទៅ និងស្ថិតិវិភាគជំងឺ",
        "en": "System overview and clinical analytics",
    },
    "dashboard.welcome_banner": {
        "km": "សូមស្វាគមន៍ការត្រឡប់មកវិញ, {name}!",
        "en": "Welcome back, {name}!",
    },
    "dashboard.banner_desc": {
        "km": "នេះជាស្ថានភាព និងស្ថិតិថ្មីៗនៃប្រព័ន្ធវិភាគជំងឺមាន់នៅថ្ងៃនេះ។",
        "en": "Here's what's happening with your chicken diagnosis system today.",
    },
    "dashboard.date_from": {
        "km": "ចាប់ពី",
        "en": "From Date",
    },
    "dashboard.date_to": {
        "km": "ដល់",
        "en": "To Date",
    },
    "dashboard.filter_disease": {
        "km": "ជំងឺ",
        "en": "Disease",
    },
    "dashboard.filter_all_diseases": {
        "km": "ជំងឺទាំងអស់",
        "en": "All Diseases",
    },
    "dashboard.filter_status": {
        "km": "ស្ថានភាព",
        "en": "Status",
    },
    "dashboard.stat_total_cases": {
        "km": "ករណីសរុប",
        "en": "Total Cases",
    },
    "dashboard.stat_pending_cases": {
        "km": "រង់ចាំពិនិត្យ",
        "en": "Pending Review",
    },
    "dashboard.stat_confirmed_cases": {
        "km": "បានបញ្ជាក់",
        "en": "Confirmed",
    },
    "dashboard.stat_rejected_cases": {
        "km": "បានបដិសេធ",
        "en": "Rejected",
    },
    "dashboard.stat_accuracy": {
        "km": "អត្រាបញ្ជាក់",
        "en": "Confirmation Rate",
    },
    "dashboard.resolution_rate": {
        "km": "អត្រាសម្រេចករណី",
        "en": "Resolution Rate",
    },
    "dashboard.triage_queue": {
        "km": "ជួររង់ចាំពិនិត្យ",
        "en": "Live Triage Queue",
    },
    "dashboard.review_needed": {
        "km": "ត្រូវការពិនិត្យ",
        "en": "Needs Review",
    },
    "dashboard.verified_cases": {
        "km": "ផ្ទៀងផ្ទាត់ដោយពេទ្យ",
        "en": "Clinically Verified",
    },
    "dashboard.dismissed_cases": {
        "km": "បានបដិសេធ",
        "en": "Dismissed Cases",
    },
    "dashboard.status_health": {
        "km": "ស្ថានភាពករណី និងការវិភាគ",
        "en": "Case Status & Triage Center",
    },
    "dashboard.view_filtered": {
        "km": "មើលបញ្ជីករណី",
        "en": "View Cases",
    },
    "dashboard.efficiency_title": {
        "km": "ប្រសិទ្ធភាពនៃការដោះស្រាយករណី",
        "en": "Resolution Efficiency",
    },
    "dashboard.disease_distribution": {
        "km": "ការចែកចាយជំងឺដែលបានរកឃើញ",
        "en": "Disease Distribution",
    },
    "dashboard.cases_over_time": {
        "km": "និន្នាការករណីតាមពេលវេលា",
        "en": "Cases Trend Over Time",
    },
    "dashboard.recent_diagnoses_table": {
        "km": "ករណីវិភាគចុងក្រោយ",
        "en": "Recent Diagnosis Records",
    },
    "dashboard.sick_vs_dead_title": {
        "km": "មាន់ឈឺ ធៀបនឹង មាន់ងាប់",
        "en": "Sick vs Dead Birds",
    },
    "dashboard.sick_vs_dead_subtitle": {
        "km": "កំណត់រដូវកាលដែលមានអត្រាងាប់ខ្ពស់ និងការផ្ទុះជំងឺ",
        "en": "Identifies peak seasonal mortality & outbreaks",
    },
    "dashboard.sick_birds": {
        "km": "មាន់ឈឺ",
        "en": "Sick Birds",
    },
    "dashboard.dead_birds": {
        "km": "មាន់ងាប់",
        "en": "Dead Birds",
    },
    "dashboard.peak_mortality": {
        "km": "ខែផ្ទុះខ្លាំងបំផុត",
        "en": "Peak Outbreak",
    },
    "dashboard.mortality_rate": {
        "km": "អត្រាងាប់",
        "en": "Mortality Rate",
    },
    "dashboard.birds_impacted": {
        "km": "មាន់រងផលប៉ះពាល់",
        "en": "Birds Impacted",
    },
    "dashboard.period_this_year": {
        "km": "ឆ្នាំនេះ",
        "en": "This Year",
    },
    "dashboard.provincial_hotspots": {
        "km": "ការផ្ទុះជំងឺតាមតំបន់ និងខេត្ត",
        "en": "Regional Outbreak Hotspots",
    },
    "dashboard.provincial_hotspots_sub": {
        "km": "ការចែកចាយករណីតាមខេត្ត ជំងឺចម្បង និងអត្រាងាប់ទូទាំងប្រទេសកម្ពុជា",
        "en": "Geographic case distribution, dominant diseases & mortality across Cambodia",
    },
    "dashboard.dominant_disease": {
        "km": "ជំងឺចម្បង",
        "en": "Dominant Disease",
    },
    "dashboard.risk_level": {
        "km": "កម្រិតហានិភ័យ",
        "en": "Risk Level",
    },
    "dashboard.provincial_chart": {
        "km": "ការចែកចាយតាមខេត្ត",
        "en": "Provincial Outbreak Distribution",
    },
    "diag.province": {
        "km": "ខេត្ត/រាជធានី",
        "en": "Province",
    },
    "diag.select_province": {
        "km": "ជ្រើសរើសខេត្ត/រាជធានី",
        "en": "Select Province",
    },
    "diag.district": {
        "km": "ស្រុក/ខណ្ឌ/ក្រុង",
        "en": "District",
    },
    "diag.select_district": {
        "km": "ជ្រើសរើសស្រុក/ខណ្ឌ/ក្រុង",
        "en": "Select District",
    },
    "diag.commune": {
        "km": "ឃុំ/សង្កាត់/ភូមិ",
        "en": "Commune / Village",
    },
    "diag.commune_ph": {
        "km": "ឧ. សង្កាត់ស្ទឹងមានជ័យ ឬ ភូមិ១",
        "en": "e.g. Sangkat Steung Meanchey or Village 1",
    },
    "diag.farm_type": {
        "km": "ប្រភេទកសិដ្ឋាន",
        "en": "Farm Type",
    },
    "diag.select_farm_type": {
        "km": "ជ្រើសរើសប្រភេទកសិដ្ឋាន",
        "en": "Select Farm Type",
    },
    "diag.farm_scale": {
        "km": "ទំហំកសិដ្ឋាន",
        "en": "Farm Scale",
    },
    "diag.select_farm_scale": {
        "km": "ជ្រើសរើសទំហំកសិដ្ឋាន",
        "en": "Select Farm Scale",
    },
    "diag.use_gps": {
        "km": "ប្រើ GPS",
        "en": "Use GPS",
    },
    "diag.use_gps_title": {
        "km": "កំណត់ទីតាំងបច្ចុប្បន្នតាមរយៈ GPS",
        "en": "Detect current location via device GPS",
    },
    "diag.gps_error": {
        "km": "មិនអាចទាញយកទីតាំង GPS បានទេ",
        "en": "Unable to retrieve GPS location",
    },

    # ── Diagnosis Wizard: Common & Stepper ────────────────────────────
    "diag.page_title": {
        "km": "ការធ្វើរោគវិនិច្ឆ័យជំងឺមាន់",
        "en": "Chicken Disease Diagnosis",
    },
    "diag.step1_nav": {
        "km": "ព័ត៌មានហ្វូងមាន់",
        "en": "Flock Info",
    },
    "diag.step2_nav": {
        "km": "រោគសញ្ញា",
        "en": "Symptoms",
    },
    "diag.step3_nav": {
        "km": "លទ្ធផលវិភាគ",
        "en": "Results",
    },

    # ── Diagnosis Step 1: Substep Progress & Pills ───────────────────
    "diag.step1_progress_sub1": {
        "km": "ជំហានទី 1 នៃ 4: ព័ត៌មានមូលដ្ឋាន",
        "en": "Step 1 of 4: Basic Flock Info",
    },
    "diag.step1_progress_sub2": {
        "km": "ជំហានទី 2 នៃ 4: សុខភាព & ការស្លាប់",
        "en": "Step 2 of 4: Health & Mortality",
    },
    "diag.step1_progress_sub3": {
        "km": "ជំហានទី 3 នៃ 4: បរិស្ថាន & ទ្រុង",
        "en": "Step 3 of 4: Environment & Coop",
    },
    "diag.step1_progress_sub4": {
        "km": "ជំហានទី 4 នៃ 4: រូបភាព (ស្រេចចិត្ត)",
        "en": "Step 4 of 4: Photos (Optional)",
    },
    "diag.substep1_name": {
        "km": "1. ព័ត៌មានមូលដ្ឋាន",
        "en": "1. Basic Info",
    },
    "diag.substep1_sub": {
        "km": "ទំហំ អាយុ និងពូជ",
        "en": "Size, age & breed",
    },
    "diag.substep2_name": {
        "km": "2. សុខភាព & ការស្លាប់",
        "en": "2. Health & Mortality",
    },
    "diag.substep2_sub": {
        "km": "មាន់ឈឺ ស្លាប់ ការស៊ីផឹក",
        "en": "Sick/dead & intake",
    },
    "diag.substep3_name": {
        "km": "3. បរិស្ថាន & ទ្រុង",
        "en": "3. Environment & Coop",
    },
    "diag.substep3_sub": {
        "km": "ទ្រុង វ៉ាក់សាំង និងអនាម័យ",
        "en": "Housing & biosecurity",
    },
    "diag.substep4_name": {
        "km": "4. រូបភាព (ស្រេចចិត្ត)",
        "en": "4. Photos (Optional)",
    },
    "diag.substep4_sub": {
        "km": "រូបភាពរោគសញ្ញាជាក់ស្តែង",
        "en": "Symptom photos",
    },

    # ── Diagnosis Step 1 Sub-step 1: Basic Info ──────────────────────
    "diag.substep1_header_title": {
        "km": "ព័ត៌មានមូលដ្ឋាននៃហ្វូងមាន់",
        "en": "Basic Flock Information",
    },
    "diag.substep1_header_sub": {
        "km": "ព័ត៌មានទូទៅអំពីកសិដ្ឋាន និងហ្វូងមាន់",
        "en": "General farm and flock details",
    },
    "diag.flock_size": {
        "km": "ចំនួនមាន់ក្នុងហ្វូង (ក្បាល)",
        "en": "Flock Size (Birds)",
    },
    "diag.flock_size_ph": {
        "km": "ឧ. 100",
        "en": "e.g. 100",
    },
    "diag.flock_size_help": {
        "km": "ចំនួនមាន់សរុបទាំងអស់នៅក្នុងទ្រុង ឬចំការ",
        "en": "Total number of chickens in the coop or farm",
    },
    "diag.bird_age": {
        "km": "អាយុមាន់",
        "en": "Bird Age",
    },
    "diag.bird_age_ph": {
        "km": "ឧ. ៧-៩ សប្ដាហ៍ ឬ ៤៥ ថ្ងៃ",
        "en": "e.g. 7-9 weeks or 45 days",
    },
    "diag.bird_age_help": {
        "km": "អាយុកាលគិតជាថ្ងៃ ឬសប្តាហ៍",
        "en": "Age in days or weeks",
    },
    "diag.breed": {
        "km": "ពូជ/ប្រភេទមាន់",
        "en": "Breed / Type",
    },
    "diag.breed_ph": {
        "km": "ឧ. មាន់ស្រែ, មាន់សាច់, មាន់ពង",
        "en": "e.g. Broiler, Layer, Native/Local",
    },
    "diag.location": {
        "km": "ទីតាំង/ខេត្ត",
        "en": "Location / Province",
    },
    "diag.location_ph": {
        "km": "ឧ. ខេត្តកំពង់ចាម",
        "en": "e.g. Kampong Cham",
    },
    "diag.btn_to_substep2": {
        "km": "បន្តទៅសុខភាព & ការស្លាប់",
        "en": "Continue to Health & Mortality",
    },

    # ── Diagnosis Step 1 Sub-step 2: Health & Mortality ──────────────
    "diag.substep2_header_title": {
        "km": "ស្ថានភាពសុខភាព និងមរណភាព",
        "en": "Health & Mortality Data",
    },
    "diag.substep2_header_sub": {
        "km": "ចំនួនមាន់ឈឺ ស្លាប់ និងការប្រែប្រួលរាងកាយ",
        "en": "Sick count, mortality and daily intake changes",
    },
    "diag.sick_count": {
        "km": "ចំនួនមាន់ឈឺ (ក្បាល)",
        "en": "Number of Sick Birds",
    },
    "diag.sick_count_ph": {
        "km": "ឧ. 5",
        "en": "e.g. 5",
    },
    "diag.dead_count": {
        "km": "ចំនួនមាន់ស្លាប់ (ក្បាល)",
        "en": "Number of Dead Birds",
    },
    "diag.dead_count_ph": {
        "km": "ឧ. 2",
        "en": "e.g. 2",
    },
    "diag.duration": {
        "km": "រយៈពេលចាប់ផ្តើមឈឺ",
        "en": "Symptom Duration",
    },
    "diag.duration_ph": {
        "km": "ឧ. ៣ ថ្ងៃ",
        "en": "e.g. 3 days",
    },
    "diag.appetite": {
        "km": "កម្រិតការស៊ីចំណី",
        "en": "Feed Intake / Appetite",
    },
    "diag.water_intake": {
        "km": "កម្រិតការផឹកទឹក",
        "en": "Water Intake Level",
    },
    "diag.select_level": {
        "km": "ជ្រើសរើសកម្រិត",
        "en": "Select intake level",
    },
    "diag.egg_drop": {
        "km": "ការធ្លាក់ចុះនៃការផលិតពង (ប្រសិនបើមាន់ពង)",
        "en": "Egg Production Drop (if layers)",
    },
    "diag.egg_drop_ph": {
        "km": "ឧ. 30%",
        "en": "e.g. 30%",
    },
    "diag.btn_to_substep3": {
        "km": "បន្តទៅបរិស្ថាន & ទ្រុង",
        "en": "Continue to Environment & Coop",
    },

    # ── Diagnosis Step 1 Sub-step 3: Environment & Coop ──────────────
    "diag.substep3_header_title": {
        "km": "លក្ខខណ្ឌបរិស្ថាន និងការគ្រប់គ្រង",
        "en": "Environment & Housing Conditions",
    },
    "diag.substep3_header_sub": {
        "km": "ស្ថានភាពទ្រុង ការចាក់វ៉ាក់សាំង និងជីវសុវត្ថិភាព",
        "en": "Coop conditions, vaccination and biosecurity",
    },
    "diag.coop_condition": {
        "km": "លក្ខខណ្ឌទ្រុង",
        "en": "Coop / Housing Condition",
    },
    "diag.select_coop": {
        "km": "ជ្រើសរើសស្ថានភាពទ្រុង",
        "en": "Select coop condition",
    },
    "diag.vaccination": {
        "km": "ស្ថានភាពចាក់វ៉ាក់សាំង",
        "en": "Vaccination Status",
    },
    "diag.select_vaccination": {
        "km": "ជ្រើសរើស",
        "en": "Select vaccination",
    },
    "diag.feed_changed": {
        "km": "ប្តូរចំណី/ទឹកថ្មីៗ",
        "en": "Recent Feed / Water Change?",
    },
    "diag.new_birds": {
        "km": "បន្ថែមមាន់ថ្មីៗ",
        "en": "New Birds Added Recently?",
    },
    "diag.nearby_sick": {
        "km": "ចំការជិតខាងមានមាន់ឈឺ",
        "en": "Nearby Farms Experiencing Outbreak?",
    },
    "diag.notes": {
        "km": "កំណត់ចំណាំបន្ថែម",
        "en": "Additional Notes / Observations",
    },
    "diag.notes_ph": {
        "km": "ឧ. ចាប់ផ្តើមឈឺក្រោយភ្លៀង ឬបន្ទាប់ពីប្តូរចំណី",
        "en": "e.g. Started after heavy rain or feed change...",
    },
    "diag.btn_to_substep4": {
        "km": "បន្តទៅរូបភាព",
        "en": "Continue to Photos",
    },

    # ── Diagnosis Step 1 Sub-step 4: Photos (Optional) ───────────────
    "diag.substep4_header_title": {
        "km": "រូបភាពសញ្ញានៃជំងឺ",
        "en": "Symptom Photos",
    },
    "diag.optional_badge": {
        "km": "ស្រេចចិត្ត",
        "en": "Optional",
    },
    "diag.substep4_header_sub": {
        "km": "ការភ្ជាប់រូបភាពជួយឱ្យពេទ្យសត្វវាយតម្លៃបានលឿន និងច្បាស់។",
        "en": "Uploading photos helps veterinarians review and confirm cases accurately.",
    },
    "diag.max_photos_badge": {
        "km": "អតិបរមា 5 រូប / ប្រភេទ",
        "en": "Max 5 photos / category",
    },
    "diag.photos_guide": {
        "km": "ជ្រើសប្រភេទរូបភាព រួចចុចប្រអប់ខាងក្រោមដើម្បីបន្ថែមរូបដែលច្បាស់។",
        "en": "Select a photo category chip, then click below to add clear photos.",
    },
    "diag.add_photo_for": {
        "km": "បន្ថែមរូបភាព:",
        "en": "Add photos:",
    },
    "diag.choose_photo_btn": {
        "km": "ជ្រើសរើសរូប",
        "en": "Choose Files",
    },
    "diag.selected_photos_title": {
        "km": "រូបភាពដែលបានជ្រើស",
        "en": "Selected Photos",
    },
    "diag.no_photos_yet": {
        "km": "មិនទាន់មានរូបភាពទេ (មិនចាំបាច់ក៏អាចបន្តបាន)",
        "en": "No photos selected yet (optional to proceed)",
    },
    "diag.btn_to_symptoms": {
        "km": "បន្តទៅជ្រើសរើសរោគសញ្ញា (Step 2)",
        "en": "Continue to Symptoms Selection (Step 2)",
    },
    "diag.photo_droppings_name": {
        "km": "លាមក",
        "en": "Droppings / Feces",
    },
    "diag.photo_droppings_hint": {
        "km": "ថតរូបលាមក ពណ៌ ឬសភាព",
        "en": "Photos showing color or texture of droppings",
    },
    "diag.photo_eyes_name": {
        "km": "ភ្នែក / ក្បាល",
        "en": "Eyes & Head",
    },
    "diag.photo_eyes_hint": {
        "km": "ភ្នែកហើម ហូរទឹក ឬបិទ",
        "en": "Swollen eyes, discharge, head lesions",
    },
    "diag.photo_comb_name": {
        "km": "មកុដ / ពុកចង្កា",
        "en": "Comb & Wattles",
    },
    "diag.photo_comb_hint": {
        "km": "មកុដខ្មៅ ស្លេក ឬប្រែពណ៌",
        "en": "Cyanotic, pale, or discolored comb",
    },
    "diag.photo_skin_name": {
        "km": "ស្បែក / របួស",
        "en": "Skin / Lesions",
    },
    "diag.photo_skin_hint": {
        "km": "របួស ដំបៅ ឬកន្ទួលស្បែក",
        "en": "Wounds, blisters, feather loss",
    },
    "diag.photo_dead_name": {
        "km": "មាន់ស្លាប់",
        "en": "Dead Birds",
    },
    "diag.photo_dead_hint": {
        "km": "ចំនួន ឬសភាពមាន់ស្លាប់",
        "en": "Dead bird count or posture",
    },
    "diag.photo_coop_name": {
        "km": "ទ្រុង / បរិស្ថាន",
        "en": "Coop / Housing",
    },
    "diag.photo_coop_hint": {
        "km": "លក្ខខណ្ឌទ្រុង ឬជុំវិញ",
        "en": "Housing ventilation and coop condition",
    },
    "diag.photo_other_name": {
        "km": "ផ្សេងៗ",
        "en": "Other Photos",
    },
    "diag.photo_other_hint": {
        "km": "រូបភាពផ្សេងពីខាងលើ",
        "en": "Any other supporting photos",
    },
    "diag.photos_size_exceeded": {
        "km": "ទំហំសរុប {size} MB — លើសពី {max} MB។ សូមដកចេញរូបភាពខ្លះ។",
        "en": "Total size {size} MB exceeds {max} MB limit. Please remove some photos.",
    },
    "diag.photos_total_size": {
        "km": "ទំហំសរុប: {size} MB",
        "en": "Total size: {size} MB",
    },

    # ── Diagnosis Step 2: Symptoms Selection ──────────────────────────
    "diag.entered_info": {
        "km": "ព័ត៌មានដែលបានបញ្ចូល",
        "en": "Entered Flock Information",
    },
    "diag.edit_info": {
        "km": "កែប្រែ",
        "en": "Edit",
    },
    "diag.summary_flock": {
        "km": "ចំនួនមាន់",
        "en": "Flock Size",
    },
    "diag.summary_age": {
        "km": "អាយុ",
        "en": "Age",
    },
    "diag.summary_breed": {
        "km": "ប្រភេទមាន់",
        "en": "Breed",
    },
    "diag.summary_sick": {
        "km": "មាន់ឈឺ",
        "en": "Sick Birds",
    },
    "diag.summary_dead": {
        "km": "មាន់ស្លាប់",
        "en": "Dead Birds",
    },
    "diag.birds_unit": {
        "km": "ក្បាល",
        "en": "birds",
    },
    "diag.live_prediction_title": {
        "km": "ជំងឺដែលអាចទំនង",
        "en": "Likely Suspected Diseases",
    },
    "diag.live_prediction_subtitle": {
        "km": "ការទស្សន៍ទាយតាមពេលវេលាជាក់ស្តែង",
        "en": "Real-time AI Match Suggestions",
    },
    "diag.live_empty_hint": {
        "km": "ជ្រើសរើសរោគសញ្ញា ដើម្បីមើលការទស្សន៍ទាយជំងឺ",
        "en": "Select symptoms to view live disease predictions",
    },
    "diag.no_matching_disease": {
        "km": "មិនទាន់មានជំងឺដែលត្រូវនឹងរោគសញ្ញាទេ",
        "en": "No matching disease found for selected symptoms",
    },
    "diag.matched_symptoms_count": {
        "km": "{count} រោគសញ្ញាត្រូវគ្នា",
        "en": "{count} matched symptom(s)",
    },
    "diag.select_symptoms_title": {
        "km": "ជ្រើសរើសរោគសញ្ញាដែលកើតមាន",
        "en": "Select Observed Symptoms",
    },
    "diag.select_symptoms_desc": {
        "km": "សូមជ្រើសរើសរោគសញ្ញាទាំងអស់ដែលបានសង្កេតឃើញ",
        "en": "Select all symptoms observed in your flock",
    },
    "diag.clear_all": {
        "km": "លុបការជ្រើសទាំងអស់",
        "en": "Clear All",
    },
    "diag.search_placeholder": {
        "km": "វាយ ដើម្បីស្វែងរករោគសញ្ញាភ្លាមៗ...",
        "en": "Type to search symptoms instantly...",
    },
    "diag.all_categories_tab": {
        "km": "ទាំងអស់",
        "en": "All Symptoms",
    },
    "diag.symptoms_count_badge": {
        "km": "{count} រោគសញ្ញា",
        "en": "{count} symptoms",
    },
    "diag.no_symptoms_found": {
        "km": "រកមិនឃើញរោគសញ្ញាដែលត្រូវនឹងពាក្យស្វែងរកទេ។",
        "en": "No symptoms matched your search query.",
    },
    "diag.btn_prev_category": {
        "km": "ប្រភេទមុន",
        "en": "Previous Category",
    },
    "diag.btn_next_category": {
        "km": "ប្រភេទបន្ទាប់",
        "en": "Next Category",
    },
    "diag.btn_analyze_symptoms": {
        "km": "វិភាគរោគសញ្ញា",
        "en": "Analyze Symptoms (Step 3)",
    },

    # ── Diagnosis Step 3: Results & Unlock ────────────────────────────
    "diag.match_found_title": {
        "km": "ការវិភាគបានរកឃើញការផ្គូផ្គង!",
        "en": "Diagnostic Match Found!",
    },
    "diag.match_found_desc": {
        "km": "ផ្អែកលើព័ត៌មាន និងរោគសញ្ញាដែលអ្នកបានបញ្ចូល ប្រព័ន្ធបានរកឃើញ {count} ជំងឺដែលអាចកើតមាន។",
        "en": "Based on your reported data, the system identified {count} suspected disease(s).",
    },
    "diag.highest_confidence_label": {
        "km": "កម្រិតទំនុកចិត្តខ្ពស់បំផុត",
        "en": "Highest Confidence",
    },
    "diag.likely_match_badge": {
        "km": "លទ្ធផលដែលអាចទំនង",
        "en": "Likely Primary Match",
    },
    "diag.infectious_badge": {
        "km": "ជំងឺឆ្លង",
        "en": "Infectious Disease",
    },
    "diag.disease_desc_title": {
        "km": "ការពិពណ៌នាជំងឺ",
        "en": "Disease Description",
    },
    "diag.treatment_and_meds": {
        "km": "វិធីព្យាបាល និងថ្នាំ",
        "en": "Treatment & Medications",
    },
    "diag.biosecurity_protocol": {
        "km": "វិធានការការពារជីវសុវត្ថិភាព",
        "en": "Biosecurity & Prevention Protocol",
    },
    "diag.verified_on_symptoms": {
        "km": "ផ្ទៀងផ្ទាត់លើ {count} រោគសញ្ញា",
        "en": "Verified on {count} symptoms",
    },
    "diag.unlock_title": {
        "km": "ចូលគណនីដើម្បីមើលលទ្ធផលពេញលេញ",
        "en": "Sign In to Unlock Full Diagnostic Report",
    },
    "diag.unlock_desc": {
        "km": "បង្កើតគណនីឥតគិតថ្លៃ ឬចូលគណនីដើម្បីមើលឈ្មោះជំងឺ វិធីព្យាបាល ការណែនាំថ្នាំ និងរក្សាទុកប្រវត្តិនៃករណីនេះ។",
        "en": "Create a free account or sign in to view the disease name, clinical treatment protocol, medication guide, and save this case history.",
    },
    "diag.continue_with_google": {
        "km": "បន្តជាមួយ Google",
        "en": "Continue with Google",
    },
    "diag.create_free_account": {
        "km": "បង្កើតគណនីថ្មី (ឥតគិតថ្លៃ)",
        "en": "Create Free Account",
    },
    "diag.already_have_account": {
        "km": "មានគណនីរួចហើយ? ចូលគណនី",
        "en": "Already have an account? Sign In",
    },
    "diag.edit_symptoms_link": {
        "km": "កែប្រែរោគសញ្ញា",
        "en": "Edit Symptoms",
    },
    "diag.results_detailed_title": {
        "km": "លទ្ធផលនៃការវិភាគលម្អិត",
        "en": "Detailed Diagnostic Results",
    },
    "diag.found_count_badge": {
        "km": "រកឃើញ {count}",
        "en": "Found {count}",
    },
    "diag.save_case_btn": {
        "km": "រក្សាទុកករណី",
        "en": "Save Case Report",
    },
    "diag.no_match_title": {
        "km": "រកមិនឃើញការផ្គូផ្គង",
        "en": "No Matching Diagnosis Found",
    },
    "diag.no_match_desc": {
        "km": "សូមជ្រើសរើសរោគសញ្ញាផ្សេង ឬបន្ថែមរោគសញ្ញា។",
        "en": "Please select different symptoms or add more observed signs.",
    },
    "diag.back_to_symptoms_btn": {
        "km": "ត្រឡប់ទៅជ្រើសរើសរោគសញ្ញា",
        "en": "Return to Symptom Selection",
    },

    # ── Cases & History ──────────────────────────────────────────────
    "cases.title": {
        "km": "ប្រវត្តិករណីវិភាគ",
        "en": "Diagnosis Case History",
    },
    "cases.subtitle": {
        "km": "ពិនិត្យមើលរបាយការណ៍រោគវិនិច្ឆ័យកន្លងមក និងលទ្ធផលតាមដានសុខភាពហ្វូងមាន់។",
        "en": "Review past diagnostic reports and flock treatment progress.",
    },
    "cases.filter_by_status": {
        "km": "ស្ថានភាព",
        "en": "Status",
    },
    "cases.col_id": {
        "km": "លេខកូដ",
        "en": "Case ID",
    },
    "cases.col_date": {
        "km": "កាលបរិច្ឆេទ",
        "en": "Date",
    },
    "cases.col_disease": {
        "km": "ជំងឺដែលបានរកឃើញ",
        "en": "Diagnosed Disease",
    },
    "cases.col_confidence": {
        "km": "ភាពជឿជាក់",
        "en": "Confidence",
    },
    "cases.col_flock": {
        "km": "ព័ត៌មានហ្វូង",
        "en": "Flock Info",
    },
    "cases.col_status": {
        "km": "ស្ថានភាព",
        "en": "Status",
    },
    "cases.col_actions": {
        "km": "សកម្មភាព",
        "en": "Actions",
    },
    "cases.no_cases_found": {
        "km": "រកមិនឃើញករណីណាត្រូវនឹងការស្វែងរកទេ។",
        "en": "No diagnosis cases matched your filter criteria.",
    },

    # ── Case Detail Page ─────────────────────────────────────────────
    "case_detail.title": {
        "km": "របាយការណ៍ករណី #{id}",
        "en": "Case Report #{id}",
    },
    "case_detail.overview_card": {
        "km": "ព័ត៌មានទូទៅនៃករណី",
        "en": "Case Overview",
    },
    "case_detail.flock_profile": {
        "km": "ទម្រង់ហ្វូងមាន់ និងបរិស្ថាន",
        "en": "Flock Profile & Environment",
    },
    "case_detail.symptoms_presented": {
        "km": "រោគសញ្ញាដែលបានរាយការណ៍",
        "en": "Reported Symptoms",
    },
    "case_detail.photos_gallery": {
        "km": "រូបភាពរោគសញ្ញា",
        "en": "Case Symptom Photos",
    },
    "case_detail.treatment_checklist": {
        "km": "តារាងតាមដានជំហានព្យាបាល",
        "en": "Treatment Steps Checklist",
    },
    "case_detail.doctor_review_card": {
        "km": "ការវាយតម្លៃរបស់វេជ្ជបណ្ឌិត",
        "en": "Doctor Review & Verification",
    },
    "case_detail.review_status": {
        "km": "ស្ថានភាពការពិនិត្យ",
        "en": "Review Status",
    },
    "case_detail.doctor_notes": {
        "km": "មតិយោបល់ និងការណែនាំរបស់វេជ្ជបណ្ឌិត",
        "en": "Doctor Notes & Instructions",
    },
    "case_detail.messages_title": {
        "km": "ការសន្ទនា / សំណួរចម្លើយជាមួយវេជ្ជបណ្ឌិត",
        "en": "Consultation Messages",
    },
    "case_detail.send_message_ph": {
        "km": "សរសេរសារ ឬសួរសំណួរបន្ថែមនៅទីនេះ...",
        "en": "Type your message or clinical inquiry here...",
    },
    "case_detail.followup_status": {
        "km": "ស្ថានភាពតាមដានក្រោយព្យាបាល",
        "en": "Follow-up Health Status",
    },
    "case_detail.back_to_history": {
        "km": "ត្រឡប់ទៅប្រវត្តិ",
        "en": "Back to History",
    },
    "case_detail.print": {
        "km": "បោះពុម្ព",
        "en": "Print",
    },
    "case_detail.diagnosis_for": {
        "km": "ការធ្វើរោគវិនិច្ឆ័យសម្រាប់",
        "en": "Diagnosis For",
    },
    "case_detail.date": {
        "km": "កាលបរិច្ឆេទ",
        "en": "Date",
    },
    "case_detail.ai_confidence": {
        "km": "កម្រិតទំនុកចិត្ត (AI Match Confidence)",
        "en": "AI Match Confidence",
    },
    "case_detail.farm_info": {
        "km": "ព័ត៌មានចំការ",
        "en": "Farm Information",
    },
    "case_detail.flock_size": {
        "km": "ចំនួន",
        "en": "Size",
    },
    "case_detail.bird_age": {
        "km": "អាយុ",
        "en": "Age",
    },
    "case_detail.breed": {
        "km": "ប្រភេទ",
        "en": "Breed",
    },
    "case_detail.location": {
        "km": "ទីតាំង",
        "en": "Location",
    },
    "case_detail.health_risk_info": {
        "km": "ព័ត៌មានសុខភាព និងហានិភ័យ",
        "en": "Health & Risk Factors",
    },
    "case_detail.sick_count": {
        "km": "មាន់ឈឺ",
        "en": "Sick Birds",
    },
    "case_detail.dead_count": {
        "km": "មាន់ស្លាប់",
        "en": "Dead Birds",
    },
    "case_detail.symptom_duration": {
        "km": "រយៈពេលរោគសញ្ញា",
        "en": "Symptom Duration",
    },
    "case_detail.vaccination": {
        "km": "វ៉ាក់សាំង",
        "en": "Vaccination",
    },
    "case_detail.egg_drop": {
        "km": "ពងធ្លាក់ចុះ",
        "en": "Egg Drop",
    },
    "case_detail.coop_condition": {
        "km": "លក្ខខណ្ឌទ្រុង",
        "en": "Coop Condition",
    },
    "case_detail.feed_intake": {
        "km": "ការស៊ី",
        "en": "Feed Intake",
    },
    "case_detail.water_intake": {
        "km": "ការផឹកទឹក",
        "en": "Water Intake",
    },
    "case_detail.feed_water_changed": {
        "km": "ប្តូរចំណី/ទឹក",
        "en": "Feed/Water Changed",
    },
    "case_detail.new_birds_added": {
        "km": "បន្ថែមមាន់ថ្មី",
        "en": "New Birds Added",
    },
    "case_detail.nearby_farms_sick": {
        "km": "ចំការជិតខាងឈឺ",
        "en": "Nearby Outbreak",
    },
    "case_detail.possible_diagnoses": {
        "km": "លទ្ធផលវិនិច្ឆ័យដែលអាចកើតមាន",
        "en": "Possible Diagnoses",
    },
    "case_detail.found_possible_diseases": {
        "km": "រកឃើញ {count} ជំងឺដែលអាចកើតមានផ្អែកលើការវិភាគរោគសញ្ញា",
        "en": "Found {count} suspected disease(s) based on symptom analysis",
    },
    "case_detail.primary_diagnosis_result": {
        "km": "លទ្ធផលរោគវិនិច្ឆ័យចម្បង",
        "en": "Primary Diagnosis Result",
    },
    "case_detail.results_count": {
        "km": "{count} លទ្ធផល",
        "en": "{count} Results",
    },
    "case_detail.most_likely": {
        "km": "ទំនងបំផុត",
        "en": "Most likely",
    },
    "case_detail.option_rank": {
        "km": "ជម្រើសទី {rank}",
        "en": "Option {rank}",
    },
    "case_detail.confidence": {
        "km": "កម្រិតទំនុកចិត្ត",
        "en": "Confidence",
    },
    "case_detail.verified_on_symptoms": {
        "km": "ផ្ទៀងផ្ទាត់លើ {matched}/{total} រោគសញ្ញា",
        "en": "Verified on {matched}/{total} symptoms",
    },
    "case_detail.info_and_treatment": {
        "km": "ព័ត៌មាន & វិធីព្យាបាល",
        "en": "Info & Treatment",
    },
    "case_detail.description": {
        "km": "ការពិពណ៌នា",
        "en": "Description",
    },
    "case_detail.treatment": {
        "km": "វិធីព្យាបាល",
        "en": "Treatment",
    },
    "case_detail.prevention": {
        "km": "ការការពារ",
        "en": "Prevention",
    },
    "case_detail.treatment_plan": {
        "km": "ការព្យាបាល",
        "en": "Treatment Plan",
    },
    "case_detail.steps": {
        "km": "ជំហាន",
        "en": "steps",
    },
    "case_detail.all_steps_completed": {
        "km": "អបអរសាទរ! ជំហានព្យាបាលទាំងអស់ត្រូវបានអនុវត្តរួចរាល់។",
        "en": "Congratulations! All treatment steps completed.",
    },
    "case_detail.step_done": {
        "km": "បានអនុវត្ត",
        "en": "Done",
    },
    "case_detail.step_num": {
        "km": "ជំហានទី {num}",
        "en": "Step {num}",
    },
    "case_detail.owner_only_record": {
        "km": "មានតែម្ចាស់ករណីទេដែលអាចកត់ត្រាការអនុវត្ត",
        "en": "Only the case owner can track implementation progress.",
    },
    "case_detail.observed_symptoms": {
        "km": "រោគសញ្ញាដែលបានសង្កេត",
        "en": "Observed Symptoms",
    },
    "case_detail.reviewed_by_doctor": {
        "km": "ការពិនិត្យដោយវេជ្ជបណ្ឌិត",
        "en": "Veterinary Doctor Review",
    },
    "case_detail.symptom_photos_title": {
        "km": "រូបភាពសញ្ញានៃជំងឺ",
        "en": "Symptom Photos",
    },
    "case_detail.photos_summary": {
        "km": "{photo_count} រូបភាព · {cat_count} ប្រភេទ",
        "en": "{photo_count} photos · {cat_count} categories",
    },
    "case_detail.all_photos": {
        "km": "ទាំងអស់",
        "en": "All",
    },
    "case_detail.review_case": {
        "km": "ពិនិត្យករណី",
        "en": "Review Case",
    },
    "case_detail.follow_up_status_title": {
        "km": "ស្ថានភាពតាមដាន",
        "en": "Follow-up Status",
    },
    "case_detail.last_updated": {
        "km": "ធ្វើបច្ចុប្បន្នភាពចុងក្រោយ៖",
        "en": "Last updated:",
    },
    "case_detail.how_flock_changing": {
        "km": "តើសុខភាពមាន់ប្រែប្រួលយ៉ាងណា?",
        "en": "How is the flock condition changing?",
    },
    "case_detail.follow_up_conversation": {
        "km": "ការសន្ទនាតាមដាន",
        "en": "Follow-up Conversation",
    },
    "case_detail.doctor_badge": {
        "km": "វេជ្ជបណ្ឌិត",
        "en": "Veterinarian",
    },
    "case_detail.user_default_name": {
        "km": "អ្នកប្រើ",
        "en": "User",
    },
    "case_detail.no_messages_yet": {
        "km": "មិនទាន់មានសារនៅឡើយទេ។ ចាប់ផ្តើមការសន្ទនា។",
        "en": "No messages yet. Start the conversation.",
    },
    "case_detail.doctor_placeholder": {
        "km": "សរសេរមតិ ឬសំណួរបន្ថែម...",
        "en": "Write clinical notes or questions...",
    },
    "case_detail.farmer_placeholder": {
        "km": "សួរសំណួរបន្ថែមទៅវេជ្ជបណ្ឌិត...",
        "en": "Ask follow-up questions to the veterinarian...",
    },
    "case_detail.send": {
        "km": "ផ្ញើ",
        "en": "Send",
    },
    "case_detail.sending": {
        "km": "ផ្ញើ...",
        "en": "Sending...",
    },
    "case_detail.send_failed": {
        "km": "មិនអាចផ្ញើសារបានទេ។ សូមព្យាយាមម្តងទៀត។",
        "en": "Could not send message. Please try again.",
    },
    "case_detail.feedback_title": {
        "km": "មតិប្រតិកម្ម",
        "en": "Feedback",
    },
    "case_detail.user_feedback_title": {
        "km": "មតិប្រតិកម្មអ្នកប្រើ",
        "en": "User Feedback",
    },
    "case_detail.you_rated": {
        "km": "អ្នកបានវាយតម្លៃ: {rating}/5",
        "en": "Your rating: {rating}/5",
    },
    "case_detail.was_diagnosis_helpful": {
        "km": "តើការវិនិច្ឆ័យនេះមានប្រយោជន៍សម្រាប់អ្នកដែរឬទេ?",
        "en": "Was this diagnosis helpful to you?",
    },
    "case_detail.additional_feedback_ph": {
        "km": "មតិបន្ថែម (ស្រេចចិត្ត)...",
        "en": "Additional feedback (optional)...",
    },
    "case_detail.send_feedback": {
        "km": "ផ្ញើមតិប្រតិកម្ម",
        "en": "Submit Feedback",
    },
    "case_detail.contagious": {
        "km": "ឆ្លង",
        "en": "Contagious",
    },
    "case_detail.non_contagious": {
        "km": "មិនឆ្លង",
        "en": "Non-contagious",
    },
    "case_detail.unknown": {
        "km": "មិនស្គាល់",
        "en": "Unknown",
    },

    # ── Disease Library ──────────────────────────────────────────────
    "lib.title": {
        "km": "បណ្ណាល័យជំងឺមាន់",
        "en": "Chicken Disease Library",
    },
    "lib.subtitle": {
        "km": "មគ្គុទ្ទេសក៍ជំងឺ រោគសញ្ញា វិធីព្យាបាល និងការការពារ",
        "en": "Comprehensive guide on poultry diseases, symptoms, treatment and biosecurity",
    },
    "lib.search_ph": {
        "km": "ស្វែងរកឈ្មោះជំងឺ (ឧ. ញូកាសល, ក្អកមាន់, អាសន្នរោគ...)",
        "en": "Search diseases by name, pathogen, or symptoms...",
    },
    "lib.all_categories": {
        "km": "គ្រប់ប្រភេទ",
        "en": "All Categories",
    },
    "lib.total_diseases": {
        "km": "ជំងឺសរុប",
        "en": "Total Diseases",
    },
    "lib.symptoms_count": {
        "km": "{count} រោគសញ្ញា",
        "en": "{count} symptoms",
    },
    "lib.read_guide": {
        "km": "អានព័ត៌មានលម្អិត",
        "en": "View Disease Guide",
    },
    "lib.tab_overview": {
        "km": "ទិដ្ឋភាពទូទៅ",
        "en": "Overview",
    },
    "lib.tab_symptoms": {
        "km": "រោគសញ្ញាគ្លីនិក",
        "en": "Clinical Symptoms",
    },
    "lib.tab_treatment": {
        "km": "វិធីសាស្ត្រព្យាបាល",
        "en": "Treatment Guidelines",
    },
    "lib.tab_prevention": {
        "km": "វិធានការបង្ការ",
        "en": "Prevention & Biosecurity",
    },
    "lib.contagious_badge": {
        "km": "ជំងឺឆ្លង",
        "en": "Contagious",
    },
    "lib.non_contagious_badge": {
        "km": "មិនឆ្លង",
        "en": "Non-contagious",
    },
    "diag.treatment_guide": {
        "km": "ជំហានព្យាបាល",
        "en": "Treatment Guide",
    },
    "lib.description": {
        "km": "ការពិពណ៌នា",
        "en": "Description",
    },
    "lib.cause_type": {
        "km": "មូលហេតុ និងប្រភេទ",
        "en": "Cause & Type",
    },
    "lib.category_label": {
        "km": "ក្រុមជំងឺ",
        "en": "Category",
    },
    "lib.symptoms_title": {
        "km": "រោគសញ្ញា",
        "en": "Symptoms",
    },
    "lib.no_linked_symptoms": {
        "km": "មិនទាន់មានរោគសញ្ញាភ្ជាប់នៅឡើយទេ។",
        "en": "No linked symptoms yet.",
    },
    "lib.treatment_title": {
        "km": "ការព្យាបាល",
        "en": "Treatment",
    },
    "lib.treatment_hint": {
        "km": "នៅពេលអ្នកបង្កើតករណី អ្នកអាចធីកជំហានទាំងនេះម្តងមួយៗ។",
        "en": "When creating a diagnosis case, you can track these steps individually.",
    },
    "lib.prevention_title": {
        "km": "ការការពារ",
        "en": "Prevention",
    },
    "lib.quick_facts": {
        "km": "ព័ត៌មានសង្ខេប",
        "en": "Quick Summary",
    },
    "lib.severity": {
        "km": "កម្រិត",
        "en": "Severity",
    },
    "lib.contagious": {
        "km": "ការឆ្លង",
        "en": "Contagious",
    },
    "lib.rules": {
        "km": "វិធានវិនិច្ឆ័យ",
        "en": "Rules",
    },
    "lib.related_rules": {
        "km": "វិធានវិនិច្ឆ័យពាក់ព័ន្ធ",
        "en": "Related Rules",
    },
    "lib.rule_meta": {
        "km": "{symptom_count} រោគសញ្ញា · អាទិភាព {priority}",
        "en": "{symptom_count} symptoms · Priority {priority}",
    },
    "lib.edit_rule": {
        "km": "កែប្រែវិធាន",
        "en": "Edit Rule",
    },
    "lib.no_rules": {
        "km": "មិនទាន់មានវិធានវិនិច្ឆ័យនៅឡើយទេ។",
        "en": "No diagnostic rules yet.",
    },
    "lib.cta_suspect": {
        "km": "សង្ស័យថាមាន់របស់អ្នកមានជំងឺនេះមែនទេ?",
        "en": "Suspect your flock has this disease?",
    },
    "lib.cta_start": {
        "km": "ចាប់ផ្តើមវិភាគ",
        "en": "Start Diagnosis",
    },
    "steps.title": {
        "km": "ជំហានព្យាបាល (បញ្ជីត្រួតពិនិត្យ)",
        "en": "Treatment Steps (Checklist)",
    },
    "steps.count": {
        "km": "{count} ជំហាន",
        "en": "{count} steps",
    },
    "steps.desc": {
        "km": "បង្កើតជំហានព្យាបាលច្បាស់លាស់ដែលកសិករអាចធីកម្តងមួយៗ។ បើមិនមានជំហានទេ ប្រព័ន្ធនឹងបំបែកអត្ថបទ \"ការព្យាបាល\" ខាងលើដោយស្វ័យប្រវត្តិ។",
        "en": "Author structured treatment steps farmers can check off. If omitted, the system falls back to auto-parsing the raw treatment text.",
    },
    "steps.new_step": {
        "km": "ជំហានថ្មី",
        "en": "New Step",
    },
    "steps.new_step_ph": {
        "km": "ឧ. ដាក់ឱ្យដោយឡែក...",
        "en": "e.g. Isolate affected birds...",
    },
    "steps.notes_optional": {
        "km": "កំណត់ចំណាំ (ស្រេចចិត្ត)",
        "en": "Notes (optional)",
    },
    "steps.notes_ph": {
        "km": "ដូស / ព័ត៌មានបន្ថែម",
        "en": "Dosage / extra instructions",
    },
    "steps.note_placeholder": {
        "km": "កំណត់ចំណាំ / ដូស (ស្រេចចិត្ត)",
        "en": "Notes / dosage (optional)",
    },
    "steps.move_up": {
        "km": "ឡើងលើ",
        "en": "Move up",
    },
    "steps.move_down": {
        "km": "ចុះក្រោម",
        "en": "Move down",
    },
    "steps.no_steps": {
        "km": "មិនទាន់មានជំហានព្យាបាលដែលបានកំណត់ទេ។",
        "en": "No treatment steps configured yet.",
    },
    "steps.enter_text": {
        "km": "សូមបញ្ចូលអត្ថបទជំហាន។",
        "en": "Please enter step text.",
    },
    "diseases.create_title": {
        "km": "បង្កើតជំងឺថ្មី",
        "en": "Create Disease",
    },
    "diseases.edit_title": {
        "km": "កែប្រែជំងឺ",
        "en": "Edit Disease",
    },
    "diseases.manage_title": {
        "km": "គ្រប់គ្រងជំងឺ",
        "en": "Manage Diseases",
    },
    "diseases.manage_desc": {
        "km": "គ្រប់គ្រងប្រវត្តិរូបជំងឺ និងការព្យាបាល",
        "en": "Manage poultry disease profiles, symptoms and treatment guidelines",
    },
    "diseases.no_diseases": {
        "km": "មិនទាន់មានទិន្នន័យជំងឺនៅឡើយទេ។",
        "en": "No disease records yet.",
    },
    "diseases.no_match": {
        "km": "រកមិនឃើញជំងឺដែលត្រូវនឹងលក្ខខណ្ឌស្វែងរកទេ។",
        "en": "No diseases match your search criteria.",
    },
    "diseases.delete_title": {
        "km": "លុបជំងឺ",
        "en": "Delete Disease",
    },
    "diseases.delete_confirm": {
        "km": "តើអ្នកប្រាកដថាចង់លុប {name} ទេ?",
        "en": "Are you sure you want to delete {name}?",
    },
    "btn.add_disease": {
        "km": "បន្ថែមជំងឺ",
        "en": "Add Disease",
    },

    # ── Rules Management ─────────────────────────────────────────────
    "rules.title": {
        "km": "វិធាន",
        "en": "Rules",
    },
    "rules.subtitle": {
        "km": "ផ្គូផ្គងរោគសញ្ញាទៅនឹងជំងឺ",
        "en": "Map symptoms to diseases",
    },
    "rules.create_title": {
        "km": "បង្កើតវិធាន",
        "en": "Create Rule",
    },
    "rules.edit_title": {
        "km": "កែប្រែវិធាន",
        "en": "Edit Rule",
    },
    "rules.delete_title": {
        "km": "លុបវិធាន",
        "en": "Delete Rule",
    },
    "rules.delete_confirm": {
        "km": "តើអ្នកប្រាកដថាចង់លុប {title} ទេ?",
        "en": "Are you sure you want to delete {title}?",
    },
    "rules.confirm_delete_btn": {
        "km": "បញ្ជាក់ការលុប",
        "en": "Confirm Delete",
    },
    "rules.col_title": {
        "km": "ចំណងជើង",
        "en": "Title",
    },
    "rules.col_symptoms": {
        "km": "រោគសញ្ញា",
        "en": "Symptoms",
    },
    "rules.col_disease": {
        "km": "ជំងឺ",
        "en": "Disease",
    },
    "rules.col_confidence": {
        "km": "ទំនុកចិត្ត",
        "en": "Confidence",
    },
    "btn.add_rule": {
        "km": "បន្ថែមវិធាន",
        "en": "Add Rule",
    },

    # ── Symptoms Management ──────────────────────────────────────────
    "symptoms.manage_title": {
        "km": "ការគ្រប់គ្រងរោគសញ្ញា",
        "en": "Manage Symptoms",
    },
    "symptoms.library_title": {
        "km": "បណ្ណាល័យរោគសញ្ញា",
        "en": "Symptom Library",
    },
    "symptoms.manage_desc": {
        "km": "គ្រប់គ្រងរោគសញ្ញាដែលប្រើសម្រាប់ការធ្វើរោគវិនិច្ឆ័យ។",
        "en": "Manage symptoms used for diagnosis inference.",
    },
    "symptoms.all_symptoms": {
        "km": "រោគសញ្ញាទាំងអស់",
        "en": "All Symptoms",
    },
    "symptoms.new_symptom": {
        "km": "រោគសញ្ញាថ្មី",
        "en": "New Symptom",
    },
    "symptoms.create_title": {
        "km": "បង្កើតរោគសញ្ញាថ្មី",
        "en": "Create Symptom",
    },
    "symptoms.edit_title": {
        "km": "កែប្រែរោគសញ្ញា",
        "en": "Edit Symptom",
    },
    "symptoms.delete_title": {
        "km": "លុបរោគសញ្ញា",
        "en": "Delete Symptom",
    },
    "symptoms.delete_confirm": {
        "km": "តើអ្នកប្រាកដថាចង់លុប {name} ទេ?",
        "en": "Are you sure you want to delete {name}?",
    },
    "symptoms.no_symptoms": {
        "km": "មិនទាន់មានរោគសញ្ញាត្រូវបានបន្ថែមទេ។",
        "en": "No symptoms added yet.",
    },
    "symptoms.add_first": {
        "km": "បន្ថែមរោគសញ្ញាដំបូង",
        "en": "Add First Symptom",
    },
    "symptoms.detail_title": {
        "km": "ព័ត៌មានលម្អិតរោគសញ្ញា",
        "en": "Symptom Details",
    },
    "symptoms.name_label": {
        "km": "ឈ្មោះរោគសញ្ញា",
        "en": "Symptom Name",
    },
    "symptoms.name_ph": {
        "km": "ឧ. ក្អក",
        "en": "e.g. Coughing",
    },
    "symptoms.desc_ph": {
        "km": "ការពន្យល់សង្ខេបអំពីរោគសញ្ញា",
        "en": "Brief description of the symptom",
    },
    "symptoms.preview": {
        "km": "មើលជាមុន",
        "en": "Live Preview",
    },
    "symptoms.preview_default_desc": {
        "km": "ការពិពណ៌នារោគសញ្ញានឹងបង្ហាញនៅទីនេះ។",
        "en": "Symptom description will appear here.",
    },
    "symptoms.save_btn": {
        "km": "រក្សាទុករោគសញ្ញា",
        "en": "Save Symptom",
    },
    "symptoms.back_to_library": {
        "km": "ត្រឡប់ទៅបណ្ណាល័យ",
        "en": "Back to Library",
    },
    "symptoms.update_title": {
        "km": "ធ្វើបច្ចុប្បន្នភាពព័ត៌មានលម្អិត",
        "en": "Update Symptom Details",
    },
    "symptoms.update_btn": {
        "km": "ធ្វើបច្ចុប្បន្នភាពរោគសញ្ញា",
        "en": "Update Symptom",
    },

    # ── Categories Management ────────────────────────────────────────
    "categories.manage_title": {
        "km": "គ្រប់គ្រងប្រភេទ",
        "en": "Manage Categories",
    },
    "categories.manage_desc": {
        "km": "ដាក់ក្រុមជំងឺតាមការផ្តោតអារម្មណ៍គ្លីនិក",
        "en": "Group diseases by clinical focus",
    },
    "categories.create_title": {
        "km": "បង្កើតប្រភេទថ្មី",
        "en": "Create Category",
    },
    "categories.edit_title": {
        "km": "កែប្រែប្រភេទ",
        "en": "Edit Category",
    },
    "categories.delete_title": {
        "km": "លុបប្រភេទ",
        "en": "Delete Category",
    },
    "categories.delete_confirm": {
        "km": "តើអ្នកប្រាកដថាចង់លុប {name} ទេ?",
        "en": "Are you sure you want to delete {name}?",
    },
    "categories.col_name": {
        "km": "ឈ្មោះ",
        "en": "Name",
    },
    "categories.col_description": {
        "km": "ការពិពណ៌នា",
        "en": "Description",
    },
    "btn.add_category": {
        "km": "បន្ថែមប្រភេទ",
        "en": "Add Category",
    },

    # ── Notifications ────────────────────────────────────────────────
    "notif.title": {
        "km": "ការជូនដំណឹង",
        "en": "Notifications",
    },
    "notif.subtitle": {
        "km": "តាមដានរាល់បច្ចុប្បន្នភាព និងសកម្មភាពក្នុងប្រព័ន្ធ។",
        "en": "Stay updated on system activity.",
    },
    "notif.unread_count": {
        "km": "មិនទាន់អាន {count}",
        "en": "{count} unread",
    },
    "notif.mark_all_read": {
        "km": "សម្គាល់ថាបានអានទាំងអស់",
        "en": "Mark all as read",
    },
    "notif.mark_read": {
        "km": "សម្គាល់ថាបានអាន",
        "en": "Mark as read",
    },
    "notif.new_badge": {
        "km": "ថ្មី",
        "en": "New",
    },
    "notif.no_notifications": {
        "km": "មិនមានការជូនដំណឹងទេ",
        "en": "No notifications",
    },
    "notif.all_caught_up": {
        "km": "អ្នកបានពិនិត្យមើលគ្រប់ការជូនដំណឹងអស់ហើយ!",
        "en": "You're all caught up!",
    },

    # ── Auth & Account ───────────────────────────────────────────────
    "auth.login_title": {
        "km": "ចូលប្រើប្រាស់គណនី",
        "en": "Log In to Your Account",
    },
    "auth.login_subtitle": {
        "km": "បញ្ចូលព័ត៌មានគណនីរបស់អ្នកដើម្បីបន្ត",
        "en": "Enter your credentials to access the diagnosis system",
    },
    "auth.username_or_email": {
        "km": "ឈ្មោះអ្នកប្រើប្រាស់ ឬ អ៊ីមែល",
        "en": "Username or Email",
    },
    "auth.password": {
        "km": "ពាក្យសម្ងាត់",
        "en": "Password",
    },
    "auth.remember_me": {
        "km": "ចងចាំខ្ញុំ",
        "en": "Remember Me",
    },
    "auth.forgot_password": {
        "km": "ភ្លេចពាក្យសម្ងាត់?",
        "en": "Forgot Password?",
    },
    "auth.btn_login": {
        "km": "ចូលប្រើប្រាស់",
        "en": "Log In",
    },
    "auth.google_login": {
        "km": "ចូលដោយប្រើ Google",
        "en": "Continue with Google",
    },
    "auth.no_account": {
        "km": "មិនទាន់មានគណនី?",
        "en": "Don't have an account?",
    },
    "auth.register_now": {
        "km": "ចុះឈ្មោះឥឡូវនេះ",
        "en": "Register Now",
    },
    "auth.register_title": {
        "km": "បង្កើតគណនីថ្មី",
        "en": "Create an Account",
    },
    "auth.register_subtitle": {
        "km": "ចុះឈ្មោះដើម្បីតាមដាន និងរក្សាទុកប្រវត្តិជំងឺមាន់របស់អ្នក",
        "en": "Sign up to track and manage your chicken flock health",
    },
    "auth.full_name": {
        "km": "ឈ្មោះពេញ",
        "en": "Full Name",
    },
    "auth.username": {
        "km": "ឈ្មោះអ្នកប្រើប្រាស់",
        "en": "Username",
    },
    "auth.email": {
        "km": "អ៊ីមែល",
        "en": "Email Address",
    },
    "auth.confirm_password": {
        "km": "បញ្ជាក់ពាក្យសម្ងាត់",
        "en": "Confirm Password",
    },
    "auth.btn_register": {
        "km": "ចុះឈ្មោះគណនី",
        "en": "Register Account",
    },
    "auth.has_account": {
        "km": "មានគណនីរួចហើយ?",
        "en": "Already have an account?",
    },
    "auth.login_now": {
        "km": "ចូលប្រើប្រាស់នៅទីនេះ",
        "en": "Log In Here",
    },
    "auth.logout_confirm_title": {
        "km": "ចាកចេញពីប្រព័ន្ធ",
        "en": "Log Out Confirmation",
    },
    "auth.logout_confirm_msg": {
        "km": "តើអ្នកពិតជាចង់ចាកចេញពីគណនីមែនទេ?",
        "en": "Are you sure you want to log out of your session?",
    },

    # ── User Management ──────────────────────────────────────────────
    "users.list_title": {
        "km": "ការគ្រប់គ្រងអ្នកប្រើប្រាស់",
        "en": "User Management",
    },
    "users.list_subtitle": {
        "km": "បញ្ជីអ្នកប្រើប្រាស់ទាំងអស់ដែលបានចុះឈ្មោះក្នុងប្រព័ន្ធ",
        "en": "List of all registered users in the system",
    },
    "users.create_title": {
        "km": "បង្កើតអ្នកប្រើប្រាស់",
        "en": "Create User",
    },
    "users.create_subtitle": {
        "km": "បង្កើតគណនីអ្នកប្រើប្រាស់ថ្មី និងកំណត់តួនាទីក្នុងប្រព័ន្ធ",
        "en": "Create a new user account and assign system role",
    },
    "users.edit_title": {
        "km": "កែប្រែអ្នកប្រើប្រាស់",
        "en": "Edit User",
    },
    "users.edit_subtitle": {
        "km": "កែប្រែព័ត៌មានគណនី និងសិទ្ធិប្រើប្រាស់",
        "en": "Update user account details and permissions",
    },
    "users.account_info": {
        "km": "ព័ត៌មានគណនី",
        "en": "Account Information",
    },
    "users.account_info_desc": {
        "km": "បញ្ចូលព័ត៌មានសម្គាល់ផ្ទាល់ខ្លួន និងឈ្មោះគណនី",
        "en": "Enter personal identification and login username",
    },
    "users.username": {
        "km": "ឈ្មោះអ្នកប្រើប្រាស់ (Username)",
        "en": "Username",
    },
    "users.username_placeholder": {
        "km": "បញ្ចូលឈ្មោះអ្នកប្រើប្រាស់",
        "en": "Enter username",
    },
    "users.username_hint": {
        "km": "ឈ្មោះគណនីសម្រាប់ចូលប្រព័ន្ធ (យ៉ាងតិច ៣ តួអក្សរ)",
        "en": "Unique account identifier for login (min 3 characters)",
    },
    "users.email": {
        "km": "អ៊ីមែល (Email)",
        "en": "Email Address",
    },
    "users.email_placeholder": {
        "km": "user@example.com",
        "en": "user@example.com",
    },
    "users.email_hint": {
        "km": "ប្រើសម្រាប់ទទួលការជូនដំណឹង និងស្តារពាក្យសម្ងាត់",
        "en": "Used for notifications and password recovery",
    },
    "users.full_name": {
        "km": "ឈ្មោះពេញ (Full Name)",
        "en": "Full Name",
    },
    "users.full_name_placeholder": {
        "km": "បញ្ចូលឈ្មោះពេញរបស់អ្នកប្រើប្រាស់",
        "en": "Enter user full name",
    },
    "users.role_status": {
        "km": "តួនាទី និងស្ថានភាពគណនី",
        "en": "Role & Account Status",
    },
    "users.role_status_desc": {
        "km": "កំណត់កម្រិតសិទ្ធិ និងភាពសកម្មនៃគណនី",
        "en": "Configure permission level and account active status",
    },
    "users.role": {
        "km": "តួនាទី (Role)",
        "en": "Role",
    },
    "users.select_role": {
        "km": "ជ្រើសរើសតួនាទី...",
        "en": "Select a role...",
    },
    "users.role_admin": {
        "km": "អ្នកគ្រប់គ្រង (Admin)",
        "en": "Admin",
    },
    "users.role_doctor": {
        "km": "វេជ្ជបណ្ឌិត / ពេទ្យសត្វ (Doctor)",
        "en": "Doctor / Veterinarian",
    },
    "users.role_user": {
        "km": "អ្នកប្រើប្រាស់ទូទៅ (User)",
        "en": "Standard User",
    },
    "users.status": {
        "km": "ស្ថានភាពគណនី",
        "en": "Account Status",
    },
    "users.active": {
        "km": "គណនីសកម្ម (Active)",
        "en": "Active Account",
    },
    "users.active_desc": {
        "km": "អនុញ្ញាតឱ្យអ្នកប្រើប្រាស់អាចចូលប្រើប្រាស់ប្រព័ន្ធបាន",
        "en": "Allow user to log in and access system features",
    },
    "users.inactive_desc": {
        "km": "គណនីអសកម្មមិនអាចចូលប្រើប្រាស់ប្រព័ន្ធបានទេ",
        "en": "Inactive accounts cannot log in to the system",
    },
    "users.password_section": {
        "km": "កំណត់ពាក្យសម្ងាត់",
        "en": "Password & Security",
    },
    "users.password_section_desc": {
        "km": "កំណត់ពាក្យសម្ងាត់សម្រាប់ការពារសុវត្ថិភាពគណនី",
        "en": "Set security credentials for this user",
    },
    "users.password": {
        "km": "ពាក្យសម្ងាត់ (Password)",
        "en": "Password",
    },
    "users.password_placeholder": {
        "km": "បញ្ចូលពាក្យសម្ងាត់រឹងមាំ",
        "en": "Enter strong password",
    },
    "users.confirm_password": {
        "km": "បញ្ជាក់ពាក្យសម្ងាត់ (Confirm Password)",
        "en": "Confirm Password",
    },
    "users.confirm_password_placeholder": {
        "km": "បញ្ចូលពាក្យសម្ងាត់ម្តងទៀត",
        "en": "Confirm password again",
    },
    "users.password_hint": {
        "km": "ពាក្យសម្ងាត់ត្រូវមានយ៉ាងតិច ៨ តួអក្សរ ដោយរួមបញ្ចូលអក្សរធំ (A-Z) អក្សរតូច (a-z) លេខ (0-9) និងនិមិត្តសញ្ញាពិសេស (@$!%*#?&)",
        "en": "Must be at least 8 characters with uppercase, lowercase, number, and special character",
    },
    "users.password_edit_hint": {
        "km": "ទុកនៅទំនេរ ប្រសិនបើមិនចង់ប្តូរពាក្យសម្ងាត់បច្ចុប្បន្ន។",
        "en": "Leave blank to keep the current password.",
    },
    "users.btn_create": {
        "km": "រក្សាទុកអ្នកប្រើប្រាស់",
        "en": "Create User",
    },
    "users.btn_save": {
        "km": "រក្សាទុកការកែប្រែ",
        "en": "Save Changes",
    },
    "users.btn_cancel": {
        "km": "បោះបង់",
        "en": "Cancel",
    },
    "users.btn_back": {
        "km": "ត្រឡប់ទៅបញ្ជី",
        "en": "Back to Users",
    },
    "users.preview_title": {
        "km": "ទិដ្ឋភាពគណនីសង្ខេប",
        "en": "User Preview",
    },
    "users.preview_desc": {
        "km": "ព័ត៌មានដែលនឹងបង្ហាញក្នុងប្រព័ន្ធ",
        "en": "Live preview of account badge",
    },
    "users.quick_tips": {
        "km": "ការណែនាំ និងសុវត្ថិភាព",
        "en": "Guidelines & Security",
    },
    "users.tip_role": {
        "km": "តួនាទី Admin មានសិទ្ធិពេញលេញលើប្រព័ន្ធ។ Doctor មានសិទ្ធិវិភាគ និងពិនិត្យករណីជំងឺ។",
        "en": "Admin role grants full system control. Doctor role allows diagnosis review and validation.",
    },
    "users.tip_security": {
        "km": "សូមប្រាកដថាបានផ្តល់ពាក្យសម្ងាត់ដែលបានបង្កើតដល់អ្នកប្រើប្រាស់ដោយសុវត្ថិភាព។",
        "en": "Ensure you securely deliver the initial login credentials to the user.",
    },
    "users.fix_errors": {
        "km": "សូមពិនិត្យ និងកែតម្រូវទិន្នន័យដែលខុសឆ្គងខាងក្រោម៖",
        "en": "Please check and fix the following form errors:",
    },

    # ── Printable Diagnostic Report ──────────────────────────────────
    "print.report_header": {
        "km": "របាយការណ៍រោគវិនិច្ឆ័យជំងឺមាន់",
        "en": "Poultry Clinical Diagnosis Report",
    },
    "print.system_name": {
        "km": "ប្រព័ន្ធជំនាញវិភាគជំងឺមាន់ (IDNS)",
        "en": "Intelligent Disease Diagnosis & Notification System (IDNS)",
    },
    "print.case_id": {
        "km": "លេខកូដករណី",
        "en": "Case ID",
    },
    "print.date_generated": {
        "km": "កាលបរិច្ឆេទចេញរបាយការណ៍",
        "en": "Date Generated",
    },
    "print.farmer_info": {
        "km": "ព័ត៌មានកសិករ / ម្ចាស់កសិដ្ឋាន",
        "en": "Farmer / Owner Information",
    },
    "print.flock_details": {
        "km": "ទិន្នន័យហ្វូងមាន់",
        "en": "Flock Information",
    },
    "print.clinical_findings": {
        "km": "រោគវិនិច្ឆ័យ និងរោគសញ្ញាដែលបានរកឃើញ",
        "en": "Clinical Findings & Diagnosis",
    },
    "print.treatment_plan": {
        "km": "ផែនការថែទាំ និងការព្យាបាល",
        "en": "Treatment & Management Plan",
    },
    "print.doctor_signature": {
        "km": "ហត្ថលេខា / ត្រាពេទ្យសត្វ",
        "en": "Veterinary Signature & Stamp",
    },
    "print.disclaimer": {
        "km": "របាយការណ៍នេះបង្កើតឡើងដោយប្រព័ន្ធជំនាញ IDNS។ សម្រាប់ជំងឺឆ្លងកម្រិតធ្ងន់ធ្ងរ សូមពិគ្រោះជាមួយពេទ្យសត្វក្នុងតំបន់។",
        "en": "This report is generated by IDNS Expert System. For severe or notifiable outbreaks, please notify local agricultural authorities.",
    },
}


def get_current_language() -> str:
    """Return the active language code stored in session, defaulting to 'km'."""
    try:
        lang = session.get("lang")
        if lang in LANGUAGES:
            return lang
    except Exception:
        pass
    return DEFAULT_LANGUAGE


def t(key: str, default: str | None = None, **kwargs: Any) -> str:
    """
    Translate a key for the current active language.

    Usage:
        t("nav.dashboard")
        t("home.welcome_prefix")
        t("dashboard.welcome_banner", name="Sokha")
    """
    lang = get_current_language()
    entry = TRANSLATIONS.get(key)
    
    if entry and lang in entry:
        text = entry[lang]
    elif entry and DEFAULT_LANGUAGE in entry:
        text = entry[DEFAULT_LANGUAGE]
    elif entry and "en" in entry:
        text = entry["en"]
    else:
        text = default if default is not None else key

    if kwargs and isinstance(text, str):
        try:
            return text.format(**kwargs)
        except Exception:
            return text
            
    return text


def get_translated_option(label_type: str, value: str | None) -> str:
    """Translate specific option choices (e.g. yes/no, vaccination, etc.)."""
    if not value:
        return ""
    
    val_str = str(value).lower()
    key_map = {
        "yes_no": f"opt.{val_str}",
        "vaccination": f"opt.vax_{val_str}",
        "coop": f"opt.coop_{val_str}",
        "intake": f"opt.intake_{val_str}",
        "status": f"status.{val_str}",
        "followup": f"followup.{val_str}",
        "follow_up": f"followup.{val_str}",
        "severity": f"severity.{val_str}",
        "contagious": "case_detail.contagious" if val_str in ("true", "1", "yes", "contagious") else "case_detail.non_contagious",
    }
    
    key = key_map.get(label_type, f"opt.{val_str}")
    return t(key, default=str(value))


def get_translated_role(role_name: str | None) -> str:
    """Translate system role names."""
    if not role_name:
        return ""
    val_str = str(role_name).lower()
    if val_str == "admin":
        return t("users.role_admin", default="Admin")
    elif val_str in ("doctor", "veterinarian"):
        return t("users.role_doctor", default="Doctor")
    elif val_str in ("user", "farmer"):
        return t("users.role_user", default="User")
    return str(role_name)
