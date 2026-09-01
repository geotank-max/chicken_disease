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

    # ── Diagnosis Step 1: Flock Information ───────────────────────────
    "diag.step1_title": {
        "km": "ជំហានទី ១: បញ្ចូលព័ត៌មានហ្វូងមាន់",
        "en": "Step 1: Flock Information & Clinical Context",
    },
    "diag.step1_desc": {
        "km": "ព័ត៌មានលម្អិតជួយឱ្យប្រព័ន្ធ និងវេជ្ជបណ្ឌិតវិភាគស្ថានភាពបានកាន់តែត្រឹមត្រូវ។",
        "en": "Detailed context improves diagnostic accuracy and helps veterinarian verification.",
    },
    "diag.flock_size": {
        "km": "ទំហំហ្វូងមាន់ (ក្បាល)",
        "en": "Flock Size (Birds)",
    },
    "diag.flock_size_ph": {
        "km": "ឧ. 500",
        "en": "e.g. 500",
    },
    "diag.bird_age": {
        "km": "អាយុមាន់",
        "en": "Bird Age",
    },
    "diag.bird_age_ph": {
        "km": "ឧ. ៤ សប្តាហ៍ ឬ ៤៥ ថ្ងៃ",
        "en": "e.g. 4 weeks or 45 days",
    },
    "diag.breed": {
        "km": "ពូជមាន់",
        "en": "Breed / Type",
    },
    "diag.breed_ph": {
        "km": "ឧ. មាន់ស្រែ, មាន់សាច់ (Broiler), មាន់ពង",
        "en": "e.g. Broiler, Layer, Native/Local",
    },
    "diag.location": {
        "km": "ទីតាំងកសិដ្ឋាន / ខេត្ត",
        "en": "Farm Location / Province",
    },
    "diag.location_ph": {
        "km": "ឧ. ខេត្តកំពង់ចាម",
        "en": "e.g. Kampong Cham",
    },
    "diag.sick_count": {
        "km": "ចំនួនមាន់ឈឺ",
        "en": "Number of Sick Birds",
    },
    "diag.dead_count": {
        "km": "ចំនួនមាន់ងាប់",
        "en": "Number of Dead Birds",
    },
    "diag.duration": {
        "km": "រយៈពេលចេញរោគសញ្ញា",
        "en": "Symptom Duration",
    },
    "diag.duration_ph": {
        "km": "ឧ. ២ ថ្ងៃ, ១ សប្តាហ៍",
        "en": "e.g. 2 days, 1 week",
    },
    "diag.vaccination": {
        "km": "ស្ថានភាពចាក់វ៉ាក់សាំង",
        "en": "Vaccination Status",
    },
    "diag.egg_drop": {
        "km": "ការថយចុះពង (%)",
        "en": "Egg Production Drop (%)",
    },
    "diag.feed_changed": {
        "km": "ទើបប្តូរចំណី ឬប្រភពទឹក?",
        "en": "Recent Feed / Water Change?",
    },
    "diag.new_birds": {
        "km": "ទើបនាំចូលមាន់ថ្មី?",
        "en": "New Birds Introduced Recently?",
    },
    "diag.nearby_sick": {
        "km": "កសិដ្ឋានក្បែរខាងមានជំងឺ?",
        "en": "Nearby Farms Experiencing Outbreak?",
    },
    "diag.coop_condition": {
        "km": "ស្ថានភាពទ្រុងមាន់",
        "en": "Coop / Housing Condition",
    },
    "diag.appetite": {
        "km": "ការស៊ីចំណី",
        "en": "Appetite / Feed Intake",
    },
    "diag.water_intake": {
        "km": "ការផឹកទឹក",
        "en": "Water Intake",
    },
    "diag.notes": {
        "km": "កំណត់សម្គាល់បន្ថែមពីម្ចាស់កសិដ្ឋាន",
        "en": "Additional Notes / Observations",
    },
    "diag.notes_ph": {
        "km": "រៀបរាប់ពីការសង្កេតបន្ថែម ដូចជាការផ្តល់ថ្នាំកន្លងមក...",
        "en": "Describe any additional observations, past treatments, or unusual symptoms...",
    },
    "diag.photos_title": {
        "km": "រូបភាពរោគសញ្ញា (ជាជម្រើស)",
        "en": "Symptom Photos (Optional)",
    },
    "diag.photos_desc": {
        "km": "ការភ្ជាប់រូបភាពលាមក ភ្នែក ឬសរីរាង្គមាន់ ជួយឱ្យពេទ្យសត្វវាយតម្លៃបានលឿន និងច្បាស់។",
        "en": "Uploading photos of droppings, head/eyes, or affected birds helps veterinarians review accurately.",
    },
    "diag.photo_droppings": {
        "km": "រូបភាពលាមក (Droppings)",
        "en": "Droppings / Feces",
    },
    "diag.photo_eyes": {
        "km": "រូបភាពភ្នែក/ក្បាល (Head & Eyes)",
        "en": "Eyes & Head",
    },
    "diag.photo_body": {
        "km": "រូបភាពទូទៅ/ដងខ្លួន (General Body)",
        "en": "General Body / Feathers",
    },
    "diag.photo_legs": {
        "km": "រូបភាពជើង/សន្លាក់ (Legs & Joints)",
        "en": "Legs & Joints",
    },
    "diag.photo_organs": {
        "km": "រូបភាពកោសល្យវិច័យ/សរីរាង្គ (Organs)",
        "en": "Autopsy / Internal Organs",
    },
    "diag.btn_to_symptoms": {
        "km": "បន្តទៅជ្រើសរើសរោគសញ្ញា",
        "en": "Continue to Select Symptoms",
    },

    # ── Diagnosis Step 2: Symptoms Selection ──────────────────────────
    "diag.step2_title": {
        "km": "ជំហានទី ២: ជ្រើសរើសរោគសញ្ញាដែលបានសង្កេតឃើញ",
        "en": "Step 2: Select Observed Symptoms",
    },
    "diag.step2_desc": {
        "km": "សូមគូសធីកលើរោគសញ្ញាទាំងអស់ដែលមាននៅក្នុងហ្វូងមាន់របស់អ្នក។",
        "en": "Check all symptoms observed in your chicken flock to run the inference engine.",
    },
    "diag.search_symptoms_ph": {
        "km": "ស្វែងរករោគសញ្ញា (ឧ. ក្អក, លាមកស, ហើមភ្នែក...)",
        "en": "Search symptoms (e.g. coughing, white diarrhea, swollen eyes...)",
    },
    "diag.all_categories": {
        "km": "ទាំងអស់",
        "en": "All Categories",
    },
    "diag.selected_count": {
        "km": "បានជ្រើសរើស {count} រោគសញ្ញា",
        "en": "{count} symptom(s) selected",
    },
    "diag.min_symptoms_warning": {
        "km": "សូមជ្រើសរើសយ៉ាងហោចណាស់ ១ រោគសញ្ញាដើម្បីបន្ត។",
        "en": "Please select at least 1 symptom to proceed with diagnosis.",
    },
    "diag.btn_run_diagnosis": {
        "km": "ដំណើរការវិភាគជំងឺ",
        "en": "Run Diagnosis Now",
    },

    # ── Diagnosis Step 3: Results ─────────────────────────────────────
    "diag.step3_title": {
        "km": "ជំហានទី ៣: លទ្ធផលវិភាគ និងការណែនាំព្យាបាល",
        "en": "Step 3: Diagnosis Results & Treatment Guide",
    },
    "diag.step3_desc": {
        "km": "ផ្អែកលើច្បាប់វិភាគ និងរោគសញ្ញាដែលអ្នកបានជ្រើសរើស។",
        "en": "Generated by expert system inference engine based on your reported clinical symptoms.",
    },
    "diag.primary_disease": {
        "km": "រោគវិនិច្ឆ័យចម្បង",
        "en": "Primary Suspected Disease",
    },
    "diag.confidence_score": {
        "km": "កម្រិតភាពជឿជាក់",
        "en": "Confidence Score",
    },
    "diag.matched_symptoms": {
        "km": "រោគសញ្ញាដែលត្រូវគ្នា",
        "en": "Matched Symptoms",
    },
    "diag.other_differentials": {
        "km": "ជំងឺផ្សេងទៀតដែលអាចកើតមាន",
        "en": "Other Differential Diagnoses",
    },
    "diag.treatment_guide": {
        "km": "ផែនការ និងជំហានព្យាបាល",
        "en": "Treatment Protocol & Step-by-Step Guide",
    },
    "diag.prevention_guide": {
        "km": "វិធានការបង្ការ និងជីវសុវត្ថិភាព",
        "en": "Prevention & Biosecurity Measures",
    },
    "diag.disclaimer_title": {
        "km": "សេចក្តីជូនដំណឹង និងការប្រុងប្រយ័ត្ន",
        "en": "Veterinary Disclaimer & Urgent Notice",
    },
    "diag.disclaimer_text": {
        "km": "លទ្ធផលនេះជាការវិភាគបឋមដោយប្រព័ន្ធជំនាញ។ ករណីធ្ងន់ធ្ងរ សូមទាក់ទងពេទ្យសត្វជំនាញ ឬរង់ចាំការពិនិត្យបញ្ជាក់ពីវេជ្ជបណ្ឌិតក្នុងប្រព័ន្ធ។",
        "en": "This is an automated preliminary expert diagnosis. In acute outbreaks, consult an accredited veterinarian or submit for online doctor review.",
    },
    "diag.case_saved_notice": {
        "km": "ករណីនេះត្រូវបានរក្សាទុកជាស្វ័យប្រវត្តិក្នងប្រវត្តិករណីរបស់អ្នក (លេខកូដ #{case_id})។",
        "en": "This diagnosis has been saved to your case history (Case #{case_id}).",
    },
    "diag.view_case_detail": {
        "km": "មើលរបាយការណ៍ពេញលេញ",
        "en": "View Full Case Report",
    },
    "diag.print_report": {
        "km": "បោះពុម្ពរបាយការណ៍",
        "en": "Print Diagnosis Report",
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
    
    key_map = {
        "yes_no": f"opt.{value}",
        "vaccination": f"opt.vax_{value}",
        "coop": f"opt.coop_{value}",
        "intake": f"opt.intake_{value}",
        "status": f"status.{value}",
        "followup": f"followup.{value}",
    }
    
    key = key_map.get(label_type, f"opt.{value}")
    return t(key, default=value)
