# app/services/seed_service.py
from extensions import db
from app.models import PermissionTable, RoleTable, UserTable
from app.models.expert_system import Category, Symptom, Disease, Rule


def _get_or_create(model, defaults=None, **kwargs):
    instance = db.session.scalar(db.select(model).filter_by(**kwargs))
    if instance:
        return instance
    params = dict(defaults or {})
    params.update(kwargs)
    instance = model(**params)
    db.session.add(instance)
    return instance


def seed_permissions_and_roles():
    permissions = [
        ("USER_CREATE", "Create Users", "Users"),
        ("USER_EDIT", "Edit Users", "Users"),
        ("USER_DELETE", "Delete Users", "Users"),
        ("ROLE_MANAGE", "Manage Roles", "Roles"),
        ("PERMISSION_MANAGE", "Manage Permissions", "Permissions"),
        ("view_dashboard", "View Dashboard", "Dashboard"),
        ("author_rules", "Author Expert Rules", "Expert System"),
        ("manage_symptoms", "Manage Symptoms", "Expert System"),
        ("manage_diseases", "Manage Diseases", "Expert System"),
        ("manage_rules", "Manage Rules", "Expert System"),
        ("manage_categories", "Manage Categories", "Expert System"),
        ("run_diagnosis", "Run Diagnosis", "Expert System"),
        ("view_cases", "View Case History", "Expert System"),
        ("review_cases", "Review Diagnosis Cases", "Expert System"),
    ]

    perm_objs = []
    for code, name, module in permissions:
        perm = _get_or_create(
            PermissionTable,
            code=code,
            defaults={"name": name, "module": module},
        )
        perm.name = name
        perm.module = module
        perm_objs.append(perm)

    admin_role = _get_or_create(RoleTable, name="Admin", defaults={"description": "System administrator"})
    doctor_role = _get_or_create(RoleTable, name="Doctor", defaults={"description": "Knowledge author"})
    user_role = _get_or_create(RoleTable, name="User", defaults={"description": "Diagnosis user"})

    db.session.flush()

    admin_role.permissions = perm_objs
    doctor_role.permissions = [
        p for p in perm_objs
        if p.code in {
            "view_dashboard",
            "author_rules",
            "manage_symptoms",
            "manage_diseases",
            "manage_rules",
            "manage_categories",
            "view_cases",
            "run_diagnosis",
            "review_cases",
        }
    ]
    user_role.permissions = [p for p in perm_objs if p.code in {"run_diagnosis", "view_cases"}]

    db.session.commit()


def seed_admin_user():
    admin = db.session.scalar(db.select(UserTable).filter_by(username="admin"))
    if admin:
        return
    admin_role = db.session.scalar(db.select(RoleTable).filter_by(name="Admin"))
    if not admin_role:
        return
    admin = UserTable(
        username="admin",
        email="admin@example.com",
        full_name="System Administrator",
        is_active=True,
    )
    admin.set_password("Admin@123")
    admin.roles = [admin_role]
    db.session.add(admin)
    db.session.commit()


# ── Clean, Professional Khmer Veterinary Knowledge Base (11 Diseases) ────────

DISEASE_KNOWLEDGE = {
    "infectious_bronchitis": {
        "name": "ជំងឺរលាកទងសួតឆ្លង (Infectious Bronchitis - IB)",
        "category_key": "cat_resp",
        "severity": "ខ្ពស់",
        "is_contagious": True,
        "description": (
            "ជាជំងឺឆ្លងផ្លូវដង្ហើមស្រួចស្រាវលើមាន់គ្រប់វ័យ បង្កឡើងដោយវីរុសកូរ៉ូណា (Avian Coronavirus)។ "
            "ជំងឺនេះធ្វើឱ្យមាន់ក្អក កណ្តាស់ ហៀរសំបោរ ដកដង្ហើមឮសំឡេងខ្យល់ស្អក និងហើមប្រហោងមុខ។ "
            "ចំពោះមាន់យកពង ជំងឺនេះបណ្តាលឱ្យទិន្នផលពងធ្លាក់ចុះយ៉ាងគំហុក ព្រមទាំងពងមានសំបកស្តើង រលក ឬខូចទ្រង់ទ្រាយ។"
        ),
        "treatment": (
            "• ញែកមាន់ដែលចេញរោគសញ្ញាឈឺចេញពីហ្វូងជាបន្ទាន់ ដើម្បីទប់ស្កាត់ការឆ្លងរាលដាលតាមផ្លូវដង្ហើម។\n"
            "• ជំងឺបង្កដោយវីរុសគ្មានឱសថសម្លាប់មេរោគដោយផ្ទាល់ឡើយ ត្រូវផ្តោតសំខាន់លើការថែទាំទ្រទ្រង់សុខភាពសត្វ។\n"
            "• ផ្តល់ថ្នាំផ្សះអង់ទីប៊ីយ៉ូទិកដូចជា Tylosin, Doxycycline ឬ Enrofloxacin រយៈពេល ៣ ទៅ ៥ ថ្ងៃ ដើម្បីការពារការឆ្លងបាក់តេរីបន្ទាប់បន្សំ។\n"
            "• បន្ថែមវីតាមីនចម្រុះ (Vitamin A, C, E) និងអេឡិចត្រូលីតក្នុងទឹកផឹក ដើម្បីជួយពង្រឹងប្រព័ន្ធការពាររាងកាយ និងកាត់បន្ថយភាពតានតឹង។\n"
            "• បង្កើនកម្ដៅ និងខ្យល់ចេញចូលឱ្យបានល្អក្នុងរោងចិញ្ចឹម ជៀសវាងសំណើមខ្ពស់ និងក្លិនឧស្ម័នអាម៉ូញាក់។\n"
            "• តាមដានសុខភាពមាន់ជារៀងរាល់ថ្ងៃ ប្រសិនបើរោគសញ្ញាមិនធូរស្រាល ត្រូវពិគ្រោះជាមួយពេទ្យសត្វជំនាញ។"
        ),
        "prevention": (
            "• ចាក់វ៉ាក់សាំងការពារជំងឺរលាកទងសួតឆ្លង (IB Vaccine) តាមកាលវិភាគឱ្យបានទៀងទាត់តាំងពីកូនមាន់អាយុ ១ ថ្ងៃ។\n"
            "• អនុវត្តវិធានការជីវសុវត្ថិភាពតឹងរ៉ឹង ដោយបាញ់ថ្នាំសម្លាប់មេរោគក្នុងទ្រុង និងឧបករណ៍ចិញ្ចឹមជាប្រចាំ។\n"
            "• ចៀសវាងការចិញ្ចឹមមាន់ចម្រុះអាយុក្នុងរោងតែមួយ និងរក្សាគម្លាតសុវត្ថិភាពពីកសិដ្ឋានដទៃ។"
        ),
    },
    "newcastle": {
        "name": "ជំងឺញូកាសល (Newcastle Disease - ND)",
        "category_key": "cat_resp",
        "severity": "ធ្ងន់ធ្ងរបំផុត",
        "is_contagious": True,
        "description": (
            "ជាជំងឺឆ្លងកាចសាហាវបំផុតលើបក្សី បង្កឡើងដោយវីរុស Paramyxovirus ដែលធ្វើឱ្យមាន់ងាប់យ៉ាងឆាប់រហ័ស និងមានអត្រាងាប់ខ្ពស់រហូតដល់ ១០០%។ "
            "រោគសញ្ញាសំខាន់ៗលេចឡើងទាំងផ្លូវដង្ហើម (ពិបាកដកដង្ហើម ក្អក ហៀរសំបោរ) ប្រព័ន្ធរំលាយអាហារ (រាគលាមកពណ៌បៃតងស្រស់លាយស) "
            "និងប្រព័ន្ធសរសៃប្រសាទ (ក្បាលវៀច រមួលក ដើរបង្វិលជុំវិញខ្លួន ឬខ្វិនជើងស្លាប)។"
        ),
        "treatment": (
            "• ជំងឺញូកាសលគ្មានឱសថព្យាបាលឱ្យជាសះស្បើយឡើយ ត្រូវញែកមាន់ឈឺដាច់ដោយឡែកភ្លាមៗ។\n"
            "• ចំពោះមាន់ដែលងាប់ ត្រូវប្រមូលយកទៅដុត ឬកប់ក្នុងរណ្តៅជម្រៅយ៉ាងតិច ១ ម៉ែត្រជាមួយកំបោរស ដើម្បីទប់ស្កាត់ការរាលដាល។\n"
            "• ផ្តល់វីតាមីនចម្រុះ អេឡិចត្រូលីត និងស្ករគ្លុយកូសក្នុងទឹកផឹកដល់មាន់ដែលនៅសេសសល់ ដើម្បីបង្កើនកម្លាំងទប់ទល់។\n"
            "• ប្រើប្រាស់ថ្នាំផ្សះអង់ទីប៊ីយ៉ូទិកកម្រិតស្រាលរយៈពេល ៣ ទៅ ៥ ថ្ងៃ ដើម្បីការពារការឆ្លងមេរោគបាក់តេរីបន្ទាប់បន្សំ។\n"
            "• បាញ់ថ្នាំសម្លាប់មេរោគជុំវិញបរិវេណទ្រុងជារៀងរាល់ថ្ងៃ និងរាយការណ៍ជូនមន្ត្រីបសុពេទ្យមូលដ្ឋានជាបន្ទាន់។"
        ),
        "prevention": (
            "• អនុវត្តកម្មវិធីចាក់ និងបន្តក់វ៉ាក់សាំងការពារជំងឺញូកាសល (ND-Lasota / Clone 30) ឱ្យបានម៉ឺងម៉ាត់តាមអាយុកាលកំណត់។\n"
            "• ទប់ស្កាត់ការប៉ះពាល់ជាមួយបក្សីព្រៃ និងដាក់សត្វមាន់ថ្មីឱ្យនៅដាច់ដោយឡែកយ៉ាងតិច ២ សប្តាហ៍មុនបញ្ចូលហ្វូង។\n"
            "• បាញ់សម្លាប់មេរោគរាល់យានយន្ត និងមនុស្សមុនអនុញ្ញាតឱ្យចូលក្នុងបរិវេណកសិដ្ឋាន។"
        ),
    },
    "coccidiosis": {
        "name": "ជំងឺកុកស៊ីឌីយ៉ូស ឬ រាគឈាម (Coccidiosis)",
        "category_key": "cat_digest",
        "severity": "ខ្ពស់",
        "is_contagious": True,
        "description": (
            "ជាជំងឺប៉ារ៉ាស៊ីតបង្កឡើងដោយពពួកឯកកោសិកា Eimeria ដែលបំផ្លាញកោសិកាស្រទាប់ភ្នាសពោះវៀនរបស់មាន់ ពិសេសលើកូនមាន់អាយុពី ៣ ទៅ ៨ សប្តាហ៍។ "
            "រោគសញ្ញាសំខាន់ៗរួមមាន រាគមានឈាមស្រស់ ឬលាមកពណ៌ក្រម៉ៅ ស្រពោន ញាក់ញ័រ ស្លេកស្លាំង រោមបះរញ៉េរញ៉ៃ មិនស៊ីចំណី និងខ្វះជាតិទឹកខ្លាំង។"
        ),
        "treatment": (
            "• ញែកមាន់ដែលរាគមានឈាមចេញពីហ្វូងជាបន្ទាន់ ដើម្បីងាយស្រួលថែទាំ និងការពារការឆ្លងបន្ត។\n"
            "• ផ្តល់ថ្នាំកម្ចាត់ប៉ារ៉ាស៊ីតកុកស៊ីឌីយ៉ូស ដូចជា Toltrazuril (Baycox) រយៈពេល ២ ថ្ងៃជាប់គ្នា ឬប្រើ Amprolium / Sulfaclozine រយៈពេល ៣ ទៅ ៥ ថ្ងៃ តាមកម្រិតណែនាំ។\n"
            "• លាយវីតាមីន K ក្នុងទឹកផឹកជាបន្ទាន់ ដើម្បីជួយកកឈាម និងទប់ស្កាត់ការធ្លាក់ឈាមក្នុងពោះវៀន។\n"
            "• ផ្តល់អេឡិចត្រូលីត និងវីតាមីន A ដើម្បីបំពេញជាតិទឹកដែលបាត់បង់ និងជួយជួសជុលភ្នាសពោះវៀនដែលខូចខាត។\n"
            "• កោសប្រមូលអង្កាមទ្រនាប់រោងដែលសើមចេញភ្លាមៗ រួចរោយម្សៅកំបោរស និងដាក់អង្កាមថ្មីដែលស្ងួតស្អាត។\n"
            "• លាងសម្អាត និងសម្លាប់មេរោគលើស្នូកចំណី និងស្នូកទឹកឱ្យបានស្អាតជារៀងរាល់ថ្ងៃ។"
        ),
        "prevention": (
            "• ថែរក្សាទ្រនាប់រោងឱ្យស្ងួតជានិច្ច ជៀសវាងការលេចធ្លាយ ឬកំពប់ទឹកពីស្នូកទឹកផឹក។\n"
            "• ប្រើប្រាស់ចំណីដែលមានលាយថ្នាំការពារកុកស៊ីឌីយ៉ូស (Coccidiostat) សម្រាប់កូនមាន់តូច ឬផ្តល់វ៉ាក់សាំងការពារជំងឺកុកស៊ីឌីយ៉ូស។\n"
            "• រក្សាកម្ដៅ និងខ្យល់ចេញចូលក្នុងរោងឱ្យបានត្រឹមត្រូវ ដើម្បីកាត់បន្ថយសំណើម។"
        ),
    },
    "fowl_cholera": {
        "name": "ជំងឺអាសន្នរោគបក្សី (Fowl Cholera)",
        "category_key": "cat_bact",
        "severity": "ខ្ពស់",
        "is_contagious": True,
        "description": (
            "ជាជំងឺឆ្លងបាក់តេរីស្រួចស្រាវបង្កឡើងដោយ Pasteurella multocida។ ក្នុងទម្រង់ធ្ងន់ធ្ងរ មាន់អាចងាប់ភ្លាមៗដោយគ្មានបង្ហាញរោគសញ្ញាអ្វីឡើយ។ "
            "ក្នុងទម្រង់ទូទៅ មាន់ក្តៅខ្លួនខ្លាំង ស្រពោន ហើមមុខ ហើមសន្ទះកំបិត កំបិតឡើងពណ៌ស្វាយជាំ រាគលាមកពណ៌បៃតងលាយលឿង និងដកដង្ហើមពិបាកឮសូរគ្រតៗ។"
        ),
        "treatment": (
            "• ញែកមាន់ឈឺដាច់ដោយឡែកជាបន្ទាន់ ហើយប្រមូលមាន់ងាប់យកទៅកម្ទេច ឬកប់កំបោរឱ្យបានឆ្ងាយពីរោងចិញ្ចឹម។\n"
            "• ប្រើប្រាស់ថ្នាំផ្សះអង់ទីប៊ីយ៉ូទិកដូចជា Enrofloxacin, Amoxicillin, Oxytetracycline ឬ Doxycycline លាយក្នុងទឹកផឹករយៈពេល ៥ ទៅ ៧ ថ្ងៃ។\n"
            "• ចំពោះមាន់ដែលឈឺធ្ងន់មិនអាចផឹកទឹកបាន អាចចាក់ថ្នាំផ្សះតាមសាច់ដុំទ្រូងតាមការណែនាំរបស់ពេទ្យសត្វ។\n"
            "• ផ្តល់អេឡិចត្រូលីត វីតាមីន C និងថ្នាំបញ្ចុះកម្ដៅក្នុងទឹកផឹក ដើម្បីជួយកាត់បន្ថយកម្ដៅ និងទប់ទល់ការបាត់បង់ជាតិទឹក។\n"
            "• លាងសម្អាត និងបាញ់ថ្នាំសម្លាប់មេរោគលើស្នូកចំណី ស្នូកទឹក និងបរិវេណរោងជារៀងរាល់ថ្ងៃ។"
        ),
        "prevention": (
            "• ចាក់វ៉ាក់សាំងការពារជំងឺអាសន្នរោគបក្សីនៅអាយុ ៨ ទៅ ១២ សប្តាហ៍។\n"
            "• កម្ចាត់សត្វកកេរ កណ្តុរ សត្វស្លាបព្រៃ និងសត្វល្អិតចង្រៃដែលជាភ្នាក់ងារចម្បងក្នុងការចម្លងមេរោគ។\n"
            "• រក្សាអនាម័យប្រភពទឹកផឹក និងចំណីឱ្យបានស្អាតល្អជានិច្ច មិនឱ្យមានការបំពុលពីលាមកសត្វ។"
        ),
    },
    "marek": {
        "name": "ជំងឺម៉ារ៉ែក (Marek's Disease)",
        "category_key": "cat_neuro",
        "severity": "ខ្ពស់",
        "is_contagious": True,
        "description": (
            "ជាជំងឺឆ្លងបង្កឡើងដោយវីរុស Herpesvirus ដែលបំផ្លាញប្រព័ន្ធសរសៃប្រសាទ និងបង្កើតជាដុំសាច់មហារីកលើសរីរាង្គក្នុង។ "
            "សញ្ញាពិសេសគឺមាន់ខ្វិនជើង ឬស្លាប ដោយជើងម្ខាងទាញទៅមុខ និងជើងម្ខាងទៀតទាញទៅក្រោយ ភ្នែកឡើងពណ៌ប្រផេះឬខ្វាក់ និងស្គមរីងរៃ។"
        ),
        "treatment": (
            "• ជំងឺម៉ារ៉ែកបណ្តាលមកពីវីរុសបង្កដុំសាច់ គ្មានវិធីព្យាបាលឱ្យជាសះស្បើយឡើយ។\n"
            "• ត្រូវញែកមាន់ដែលខ្វិនជើងចេញពីហ្វូងជាបន្ទាន់ ដើម្បីកាត់បន្ថយការសាយភាយធូលីរោមដែលមានផ្ទុកមេរោគ។\n"
            "• បោសសម្អាតកម្ចាត់ធូលី និងកម្ទេចរោមមាន់ក្នុងរោងឱ្យបានហ្មត់ចត់ ព្រោះមេរោគរស់នៅក្នុងធូលីរោមបានយូរអង្វែង។\n"
            "• ផ្តល់វីតាមីនជំនួយសរសៃប្រសាទ (Vitamin B-Complex) និងអេឡិចត្រូលីតដល់មាន់ដែលនៅសេសសល់ ដើម្បីជួយពង្រឹងកម្លាំង។\n"
            "• បាញ់ថ្នាំសម្លាប់មេរោគដែលមានប្រសិទ្ធភាពខ្ពស់លើវីរុសជុំវិញបរិវេណរោងចិញ្ចឹម។"
        ),
        "prevention": (
            "• ចាក់វ៉ាក់សាំងការពារជំងឺម៉ារ៉ែក (Marek Vaccine) ឱ្យបានម៉ឺងម៉ាត់បំផុតលើកូនមាន់ទើបញាស់អាយុ ១ ថ្ងៃ នៅកន្លែងភ្ញាស់។\n"
            "• សម្អាត និងសម្លាប់មេរោគក្នុងទ្រុងក្រាបកូនមាន់ឱ្យបានល្អិតល្អន់មុនដាក់កូនមាន់ចូល។\n"
            "• គ្រប់គ្រងខ្យល់ចេញចូលឱ្យបានល្អ ដើម្បីកាត់បន្ថយការប្រមូលផ្តុំធូលីរោមក្នុងរោង។"
        ),
    },
    "avian_influenza": {
        "name": "ជំងឺផ្តាសាយបក្សី (Avian Influenza - Bird Flu)",
        "category_key": "cat_resp",
        "severity": "គ្រោះថ្នាក់បំផុត",
        "is_contagious": True,
        "description": (
            "ជាជំងឺឆ្លងរលាកផ្លូវដង្ហើមកាចសាហាវបំផុត បង្កឡើងដោយវីរុសគ្រុនផ្តាសាយប្រភេទ A (ពពួក H5N1, H5N6) ដែលអាចឆ្លងរាលដាលដល់មនុស្សបាន។ "
            "មាន់ងាប់លឿននិងច្រើនក្នុងពេលតែមួយ កំបិតនិងសន្ទះកំបិតឡើងពណ៌ស្វាយជាំខ្លាំង ហើមមុខ ហើមភ្នែក ហូរឈាមក្រោមស្បែកជើង ពិបាកដកដង្ហើម និងរាគ។"
        ),
        "treatment": (
            "• ជំងឺផ្តាសាយបក្សីគ្មានការព្យាបាលជាដាច់ខាត ហាមលក់ បរិភោគ ឬយកមាន់ឈឺទៅធ្វើចរាចរណ៍។\n"
            "• រាយការណ៍ជាបន្ទាន់បំផុតទៅកាន់អាជ្ញាធរមូលដ្ឋាន ឬមន្ត្រីបសុពេទ្យជំនាញប្រចាំស្រុក/ខេត្ត។\n"
            "• អនុវត្តវិធានការដាក់កម្រិតចរាចរណ៍សត្វ និងបិទច្រកចេញចូលកសិដ្ឋានជាបន្ទាន់។\n"
            "• កម្ទេចសត្វឈឺ និងសត្វងាប់ដោយដុត ឬកប់ជម្រៅយ៉ាងតិច ១.៥ ម៉ែត្រ រួមជាមួយការរោយកំបោរសយ៉ាងក្រាស់ ក្រោមការត្រួតពិនិត្យរបស់មន្ត្រីជំនាញ។\n"
            "• បាញ់ថ្នាំសម្លាប់មេរោគគ្រប់ច្រកល្ហកក្នុងរោង និងបរិវេណជុំវិញ ហើយអ្នកថែទាំត្រូវពាក់ម៉ាស់ ស្រោមដៃ និងខោអាវការពារឱ្យបានត្រឹមត្រូវ។"
        ),
        "prevention": (
            "• ពង្រឹងវិធានការជីវសុវត្ថិភាពយ៉ាងតឹងរ៉ឹង ការពារកុំឱ្យបក្សីស្រុកប៉ះពាល់ជាមួយបក្សីព្រៃ ឬប្រភពទឹកធម្មជាតិ។\n"
            "• ប្រើប្រាស់សម្លៀកបំពាក់ និងស្បែកជើងដាច់ដោយឡែកក្នុងកសិដ្ឋាន និងបាញ់សម្លាប់មេរោគរាល់យានយន្តដែលចេញចូល។\n"
            "• តាមដានសុខភាពសត្វជាប្រចាំ និងដាក់សត្វមាន់ថ្មីនៅដាច់ដោយឡែកមុនបញ្ចូលហ្វូង។"
        ),
    },
    "infectious_bursal": {
        "name": "ជំងឺហ្គាំបូរ៉ូ (Gumboro - IBD)",
        "category_key": "cat_general",
        "severity": "ខ្ពស់",
        "is_contagious": True,
        "description": (
            "ជាជំងឺឆ្លងស្រួចស្រាវបង្កឡើងដោយវីរុស Birnavirus ដែលបំផ្លាញថង់ប្រព័ន្ធការពាររាងកាយ (Bursa of Fabricius) លើកូនមាន់អាយុពី ៣ ទៅ ៦ សប្តាហ៍។ "
            "សញ្ញាសំខាន់ៗរួមមាន ស្រពោនខ្លាំង ដេកផ្អៀងផ្អែកលើដី រោមរញ៉េរញ៉ៃ រាគលាមកពណ៌សកំបោរស្អិតជុំវិញគូទ និងខ្វះជាតិទឹកធ្ងន់ធ្ងរ។"
        ),
        "treatment": (
            "• ដោយសារជាជំងឺបង្កឡើងដោយវីរុស គ្មានថ្នាំផ្សះណាអាចសម្លាប់វីរុស IBD ដោយផ្ទាល់បានឡើយ។\n"
            "• ផ្តល់ទឹកស្អាតលាយជាមួយអេឡិចត្រូលីត (Electrolytes) និងស្ករគ្លុយកូសជាបន្ទាន់ ដើម្បីជួយសង្គ្រោះមាន់ពីការខ្វះជាតិទឹក និងអស់កម្លាំង។\n"
            "• ផ្តល់វីតាមីនចម្រុះ (Vitamin A, B-complex, C, E) ដើម្បីជួយជំរុញប្រព័ន្ធការពាររាងកាយដែលកំពុងចុះខ្សោយ។\n"
            "• ប្រើថ្នាំប៉ូវថ្លើម និងតម្រងនោម ដើម្បីជួយបញ្ចេញជាតិពុលក្នុងរាងកាយសត្វ។\n"
            "• អាចប្រើថ្នាំផ្សះកម្រិតស្រាលដូចជា Amoxicillin ដើម្បីទប់ស្កាត់ការឆ្លងរោគបាក់តេរីបន្ទាប់បន្សំ។\n"
            "• រក្សាកម្ដៅក្នុងរោងឱ្យមានស្ថិរភាព និងជៀសវាងភាពតានតឹង (Stress) ផ្សេងៗដល់កូនមាន់។"
        ),
        "prevention": (
            "• អនុវត្តកម្មវិធីផ្ដល់វ៉ាក់សាំងការពារជំងឺហ្គាំបូរ៉ូ (Gumboro Vaccine) ឱ្យបានទៀងទាត់នៅអាយុប្រហែល ១០ ទៅ ១៤ ថ្ងៃ និងលើកទីពីរនៅអាយុ ២១ ថ្ងៃ។\n"
            "• សម្អាត និងសម្លាប់មេរោគក្នុងទ្រុងឱ្យបានហ្មត់ចត់មុននឹងដាក់កូនមាន់ថ្មី។\n"
            "• ទុកចន្លោះពេលសម្រាកទ្រុងយ៉ាងតិច ២ សប្តាហ៍រវាងការចិញ្ចឹមមួយវគ្គទៅមួយវគ្គ។"
        ),
    },
    "fowl_pox": {
        "name": "ជំងឺអុតបក្សី (Fowl Pox)",
        "category_key": "cat_skin",
        "severity": "មធ្យម",
        "is_contagious": True,
        "description": (
            "ជាជំងឺឆ្លងបង្កឡើងដោយវីរុស Avipoxvirus ដែលចម្លងយឺតៗតាមរយៈមូសខាំ ឬស្នាមរបួសស្បែក។ "
            "បង្ហាញចេញជាពីរទម្រង់៖ ទម្រង់ស្បែក (មានពងបែក ដំបៅ ឬក្រមរខ្មៅលើកំបិត មុខ ជុំវិញភ្នែក និងជើង) "
            "និងទម្រង់សើម (ដំបៅរលួយភ្នាសសក្នុងមាត់ បំពង់ក ធ្វើឱ្យពិបាកលេបចំណី និងពិបាកដកដង្ហើម)។"
        ),
        "treatment": (
            "• ញែកមាន់ដែលមានស្នាមដំបៅអុតចេញ ដើម្បីកាត់បន្ថយការចម្លងតាមការចឹកគ្នា។\n"
            "• សម្អាតក្រមរ ឬដំបៅខាងក្រៅដោយប្រុងប្រយ័ត្ន រួចលាបថ្នាំសម្លាប់មេរោគ Betadine (Povidone Iodine) ឬ Blue Methyl លើស្នាមដំបៅជារៀងរាល់ថ្ងៃ។\n"
            "• ករណីមានដំបៅក្នុងមាត់ ត្រូវជូតសម្អាតស្លេស្ម ឬដំបៅសដោយដុំសំឡីស្អាតជ្រលក់ទឹកថ្នាំសម្លាប់មេរោគស្រាល។\n"
            "• ផ្តល់ថ្នាំផ្សះដូចជា Oxytetracycline ឬ Amoxicillin លាយក្នុងទឹកផឹករយៈពេល ៤ ទៅ ៥ ថ្ងៃ ដើម្បីការពារការឆ្លងរោគបាក់តេរីលើដំបៅ។\n"
            "• ផ្តល់វីតាមីន A និងវីតាមីនចម្រុះក្នុងទឹកផឹក ដើម្បីជួយជំរុញការលូតលាស់នៃកោសិកាស្បែក និងភ្នាសសើម។\n"
            "• ផ្តល់ចំណីទន់ៗ និងទឹកឱ្យបានគ្រប់គ្រាន់ដើម្បីជួយសម្រួលដល់ការស៊ីចំណី។"
        ),
        "prevention": (
            "• ចាក់វ៉ាក់សាំងការពារជំងឺអុតមាន់ (Fowl Pox Vaccine) ដោយវិធីចាក់ទម្លុះភ្នាសស្លាប (Wing web) នៅអាយុ ៦ ទៅ ៨ សប្តាហ៍។\n"
            "• កម្ចាត់មូស សត្វល្អិតបឺតឈាម និងលុបបំបាត់ថ្លុកទឹកដក់ជុំវិញរោងចិញ្ចឹម។\n"
            "• ជៀសវាងការចិញ្ចឹមមាន់ណែនតឹងពេក ដែលបង្កឱ្យមានការចឹកគ្នានិងមានស្នាមរបួស។"
        ),
    },
    "ecoli": {
        "name": "ជំងឺឆ្លងបាក់តេរី អ៊ីខូឡៃ (Colibacillosis - E. coli)",
        "category_key": "cat_bact",
        "severity": "មធ្យមទៅខ្ពស់",
        "is_contagious": False,
        "description": (
            "ជាជំងឺឆ្លងបង្កឡើងដោយបាក់តេរី Escherichia coli ដែលជាធម្មតាកើតឡើងនៅពេលមាន់មានភាពតានតឹង បរិស្ថានរោងមិនស្អាត ឬឆ្លងបន្តពីជំងឺផ្លូវដង្ហើមដទៃ។ "
            "រោគសញ្ញារួមមាន រាគលាមកពណ៌លឿងឬបៃតង ស្រពោន ហើមពោះ រលាកផ្ចិតលើកូនមាន់ រលាកថង់ខ្យល់ និងងាប់រាយប៉ាយ។"
        ),
        "treatment": (
            "• ញែកមាន់ឈឺចេញពីហ្វូង ហើយកែលម្អអនាម័យក្នុងរោងជាបន្ទាន់។\n"
            "• ប្រើប្រាស់ថ្នាំផ្សះអង់ទីប៊ីយ៉ូទិកប្រឆាំងបាក់តេរី E. coli ដូចជា Enrofloxacin, Colistin, Neomycin ឬ Fosfomycin លាយក្នុងទឹកផឹករយៈពេល ៣ ទៅ ៥ ថ្ងៃ តាមកម្រិតកំណត់។\n"
            "• បន្ថែមវីតាមីនចម្រុះ និងអេឡិចត្រូលីត ដើម្បីជួយឱ្យមាន់ឆាប់ដឹងខ្លួន និងបង្កើនកម្លាំងប្រឆាំងជំងឺ។\n"
            "• លាងសម្អាត និងសម្លាប់មេរោគក្នុងស្នូកទឹក និងបំពង់បង្ហូរទឹកឱ្យបានស្អាតជានិច្ច ព្រោះបាក់តេរីច្រើនសម្បុកក្នុងទឹករងៃ។\n"
            "• កែលម្អប្រព័ន្ធខ្យល់ចេញចូល ដើម្បីកាត់បន្ថយឧស្ម័នអាម៉ូញាក់ និងសំណើមដែលបំផ្លាញផ្លូវដង្ហើមមាន់។"
        ),
        "prevention": (
            "• ធានាឱ្យបាននូវប្រភពទឹកផឹកស្អាត ដោយអាចប្រើប្រាស់ក្លរីន ឬថ្នាំសម្លាប់មេរោគក្នុងកម្រិតសុវត្ថិភាព។\n"
            "• រក្សាអនាម័យសំបុកពង មិនយកពងប្រឡាក់លាមកទៅភ្ញាស់ និងសម្អាតកន្លែងចិញ្ចឹមឱ្យស្ងួតល្អជានិច្ច។\n"
            "• កាត់បន្ថយភាពតានតឹងដល់សត្វមាន់ តាមរយៈការគ្រប់គ្រងសីតុណ្ហភាព និងដង់ស៊ីតេចិញ្ចឹមឱ្យបានសមស្រប។"
        ),
    },
    "mycoplasmosis": {
        "name": "ជំងឺរលាកផ្លូវដង្ហើមរ៉ាំរ៉ៃ ស៊ីអ័រឌី (Mycoplasmosis - CRD)",
        "category_key": "cat_resp",
        "severity": "មធ្យម",
        "is_contagious": True,
        "description": (
            "ជាជំងឺផ្លូវដង្ហើមរ៉ាំរ៉ៃបង្កឡើងដោយបាក់តេរី Mycoplasma gallisepticum។ "
            "រោគសញ្ញាសំខាន់ៗរួមមាន ក្អក កណ្តាស់ ដកដង្ហើមឮសូរគ្រតៗ ហៀរសំបោរខាប់ ហើមប៉ោងជុំវិញភ្នែកនិងប្រហោងច្រមុះ ភ្នែកស្រវាំងបិទជិត និងធ្វើឱ្យមាន់ថយចុះការស៊ីចំណី ស្គមរីងរៃ និងធ្លាក់ចុះការបញ្ចេញពង។"
        ),
        "treatment": (
            "• ញែកមាន់ដែលមានសញ្ញាហើមមុខ ឬក្អកធ្ងន់ធ្ងរចេញពីហ្វូង។\n"
            "• ប្រើថ្នាំផ្សះអង់ទីប៊ីយ៉ូទិកដែលស័ក្តិសមសម្រាប់ Mycoplasma ដូចជា Tylosin, Doxycycline, Tilmicosin ឬ Enrofloxacin លាយក្នុងទឹកផឹករយៈពេល ៥ ទៅ ៧ ថ្ងៃជាប់គ្នា។\n"
            "• លាយវីតាមីន A និងវីតាមីន C ក្នុងទឹកផឹក ដើម្បីជួយជួសជុលភ្នាសរំអិលផ្លូវដង្ហើម និងបង្កើនភាពធន់នឹងជំងឺ។\n"
            "• ជូតសម្អាតស្លេស្មសំបោរ និងទឹកភ្នែកមាន់ដោយប្រើសំឡីស្អាតជ្រលក់ទឹកអំបិលវេជ្ជសាស្ត្រ (Saline solution)។\n"
            "• បន្ថយដង់ស៊ីតេចិញ្ចឹមកុំឱ្យចង្អៀតពេក និងបើកចំហររោងឱ្យមានខ្យល់អាកាសបរិសុទ្ធចេញចូលគ្រប់គ្រាន់។"
        ),
        "prevention": (
            "• ជ្រើសរើសទិញកូនមាន់ពីកសិដ្ឋានបង្កាត់ពូជដែលគ្មានផ្ទុកមេរោគ Mycoplasma (CRD-free)។\n"
            "• អនុវត្តវិធានការជីវសុវត្ថិភាព និងចៀសវាងការផ្លាស់ប្តូរសីតុណ្ហភាពភ្លាមៗក្នុងរោង។\n"
            "• កុំចិញ្ចឹមមាន់ច្របល់ជាមួយសត្វស្លាបដទៃដូចជា ទា ក្ងាន ឬសត្វស្លាបព្រៃ។"
        ),
    },
    "aspergillosis": {
        "name": "ជំងឺផ្សិតសួតបក្សី (Aspergillosis)",
        "category_key": "cat_resp",
        "severity": "មធ្យម",
        "is_contagious": False,
        "description": (
            "ជាជំងឺបង្កឡើងដោយការដកដង្ហើមស្រូបយកស្ប៉ោ (Spores) នៃផ្សិត Aspergillus fumigatus ដែលដុះលើចំណីផ្អួរ កន្ទក់ ឬអង្កាមទ្រនាប់សើម។ "
            "សញ្ញាសំខាន់ៗរួមមាន ពិបាកដកដង្ហើមខ្លាំង ហារមាត់ដកដង្ហើមញាប់ស្អេកស្កះ ស្រពោន ស្រេកទឹកខ្លាំង ស្គមរីងរៃ ប៉ុន្តែមិនឮសំឡេងក្អកឬហៀរសំបោរដូចជំងឺឆ្លងផ្លូវដង្ហើមដទៃឡើយ។"
        ),
        "treatment": (
            "• ញែកមាន់ឈឺចេញពីប្រភពផ្សិតជាបន្ទាន់។\n"
            "• ជំងឺផ្សិតមិនអាចព្យាបាលដោយថ្នាំផ្សះអង់ទីប៊ីយ៉ូទិកបានឡើយ ហើយការប្រើថ្នាំផ្សះអាចធ្វើឱ្យផ្សិតដុះកាន់តែខ្លាំង។\n"
            "• ប្រមូលកម្ចាត់ និងដុតចោលនូវអង្កាមទ្រនាប់រោង និងចំណីដែលផ្អួរ ឬសើមដុះផ្សិតទាំងអស់។\n"
            "• អាចប្រើថ្នាំប្រឆាំងផ្សិត (Antifungal) ដូចជា Copper Sulfate (លាយក្នុងកម្រិតស្រាលតាមការណែនាំរបស់ពេទ្យសត្វ) ឬ Nystatin / Ketoconazole ក្នុងទឹកផឹក។\n"
            "• បាញ់ថ្នាំសម្លាប់មេរោគផ្សិតដែលមានជាតិអ៊ីយ៉ូត ឬ Virkon S ក្នុងរោង និងឧបករណ៍ចិញ្ចឹម។\n"
            "• ផ្តល់វីតាមីនចម្រុះ និងអេឡិចត្រូលីត ដើម្បីជំនួយកម្លាំងដល់មាន់។\n"
            "• បង្កើនការបញ្ចេញបញ្ចូលខ្យល់អាកាសក្នុងរោងឱ្យបានស្ងួតល្អ និងមានពន្លឺថ្ងៃចាំងចូលគ្រប់គ្រាន់។"
        ),
        "prevention": (
            "• ហាមប្រើប្រាស់ចំណីផ្អួរ ដុះផ្សិត ឬរក្សាទុកចំណីនៅកន្លែងសើម។\n"
            "• ប្រើប្រាស់អង្កាមទ្រនាប់រោងដែលស្ងួតស្អាត និងផ្លាស់ប្តូរភ្លាមៗនៅពេលមានការជ្រាបទឹក។\n"
            "• សម្អាត និងហាលទូភ្ញាស់ឱ្យស្ងួតមុនពេលប្រើប្រាស់។"
        ),
    },
}


def seed_expert_data():
    if db.session.scalar(db.select(Symptom).limit(1)):
        return

    # Categories
    cat_resp = _get_or_create(Category, name="ប្រព័ន្ធដង្ហើម",
                              defaults={"description": "រោគសញ្ញាទាក់ទងនឹងប្រព័ន្ធដង្ហើម"})
    cat_digest = _get_or_create(Category, name="ប្រព័ន្ធរំលាយអាហារ",
                                defaults={"description": "រោគសញ្ញាទាក់ទងនឹងពោះវៀន និងប្រព័ន្ធរំលាយអាហារ"})
    cat_neuro = _get_or_create(Category, name="ប្រព័ន្ធសរសៃប្រសាទ",
                               defaults={"description": "រោគសញ្ញាផ្នែកសរសៃប្រសាទ និងចលនាខ្វិន"})
    cat_bact = _get_or_create(Category, name="ការឆ្លងបាក់តេរី",
                              defaults={"description": "រោគសញ្ញាបង្កឡើងដោយការឆ្លងបាក់តេរី"})
    cat_general = _get_or_create(Category, name="រោគសញ្ញាទូទៅ",
                                 defaults={"description": "រោគសញ្ញាទូទៅលើសុខភាព និងកាយវិការ"})
    cat_skin = _get_or_create(Category, name="ស្បែកនិងរោម",
                              defaults={"description": "រោគសញ្ញាលើស្បែក រោម កំបិត និងភ្នែក"})
    cat_repro = _get_or_create(Category, name="ការផលិតពង",
                               defaults={"description": "រោគសញ្ញាទាក់ទងនឹងការបញ្ចេញពង និងបន្តពូជ"})

    # Symptoms (31)
    symptoms = {
        # Respiratory
        "coughing": Symptom(name="ក្អក", description="ក្អកញឹកញាប់ ឬពិបាកដកដង្ហើម", category=cat_resp),
        "sneezing": Symptom(name="កណ្តាស់", description="កណ្តាស់ញឹកញាប់", category=cat_resp),
        "nasal_discharge": Symptom(name="ហៀរសំបោរ", description="មានសំបោរ ឬស្លេស្មចេញពីរន្ធច្រមុះ", category=cat_resp),
        "watery_eyes": Symptom(name="ហៀរទឹកភ្នែក", description="ភ្នែកហៀរទឹក ហើម ឬបិទជិត", category=cat_resp),
        "gasping": Symptom(name="ពិបាកដកដង្ហើម/ហារមាត់", description="ហារមាត់ដកដង្ហើម ឬដកដង្ហើមញាប់ខ្លាំង", category=cat_resp),
        "swollen_sinus": Symptom(name="ហើមប្រហោងមុខ", description="ហើមរលាកក្បែរភ្នែក ឬប្រហោងច្រមុះ", category=cat_resp),
        "tracheal_rales": Symptom(name="សំឡេងខ្យល់ដង្ហើមស្អក", description="សំឡេងខ្យល់ដង្ហើមមិនប្រក្រតីឮសូរគ្រតៗក្នុងបំពង់ក", category=cat_resp),
        # Digestive
        "diarrhea": Symptom(name="រាគរូស", description="រាគលាមករាវ ឬជាទឹក", category=cat_digest),
        "bloody_diarrhea": Symptom(name="រាគមានឈាម", description="មានឈាមស្រស់ ឬកំទេចឈាមលាយឡំក្នុងលាមក", category=cat_digest),
        "green_diarrhea": Symptom(name="រាគពណ៌បៃតង", description="លាមករាវពណ៌បៃតងស្រស់ ឬលាយស", category=cat_digest),
        "white_diarrhea": Symptom(name="រាគពណ៌សកំបោរ", description="លាមករាវពណ៌សកំបោរស្អិតជាប់គូទ", category=cat_digest),
        "crop_distension": Symptom(name="ប៉ោងក្រពះចំណី", description="ក្រពះចំណី (ពោះវៀនក) ឡើងប៉ោងតឹងពេញដោយទឹកឬខ្យល់", category=cat_digest),
        # Neurological
        "lameness": Symptom(name="ទន់ជើង/ដើរខ្វិន", description="ពិបាកដើរ ជើងទន់ខ្សោយ ឬដើរទាក់", category=cat_neuro),
        "head_tilt": Symptom(name="ក្បាលផ្អៀង/វៀច", description="ក្បាលផ្អៀងទៅម្ខាង ឬងាកចុះក្រោម", category=cat_neuro),
        "tremors": Symptom(name="ញ័រខ្លួន/កន្ត្រាក់", description="រាងកាយញ័រ ឬកន្ត្រាក់សាច់ដុំ", category=cat_neuro),
        "paralysis": Symptom(name="ខ្វិនជើង ឬស្លាប", description="មិនអាចដើរបាន ឬជើងនិងស្លាបទន់លែងកម្រើក", category=cat_neuro),
        "twisted_neck": Symptom(name="ក្បាលរមួលបង្វិល", description="ក្បាលរមួលបង្វិលខុសធម្មជាតិ (Torticollis)", category=cat_neuro),
        # General
        "lethargy": Symptom(name="ស្រពោន/អសកម្ម", description="ថយចុះថាមពល ដេកសណ្តូកស្ងប់ស្ងៀម មិនរវើករវាយ", category=cat_general),
        "ruffled": Symptom(name="រោមរញ៉េរញ៉ៃ/បះ", description="រោមបះមិនស្អាត ឬរញ៉េរញ៉ៃ ធ្លាក់ស្លាប", category=cat_general),
        "loss_appetite": Symptom(name="បាត់បង់ចំណង់អាហារ", description="មិនស៊ីចំណី ឬស៊ីតិចតួចខុសធម្មតា", category=cat_general),
        "weight_loss": Symptom(name="ស្រកទម្ងន់/ស្គម", description="ស្រកទម្ងន់លឿន ឬស្គមរីងរៃសល់តែឆ្អឹងទ្រូង", category=cat_general),
        "sudden_death": Symptom(name="ងាប់ភ្លាមៗ", description="ងាប់យ៉ាងឆាប់រហ័សដោយគ្មានរោគសញ្ញាព្រមាន", category=cat_general),
        "fever": Symptom(name="ក្តៅខ្លួនខ្លាំង", description="សីតុណ្ហភាពរាងកាយឡើងខ្ពស់ ជើងក្តៅ", category=cat_general),
        "dehydration": Symptom(name="ខ្វះជាតិទឹក", description="ស្បែកស្ងួត ភ្នែកខូងស្រពោន ជើងស្វិតស្ងួត", category=cat_general),
        # Skin
        "swollen_face": Symptom(name="ហើមមុខ/ក្បាល", description="ផ្ទៃមុខ ក្បាល ឬកំបិតឡើងហើមធំ", category=cat_bact),
        "skin_lesions": Symptom(name="ដំបៅស្បែក/ពងបែក", description="របួស ដំបៅ ឬពងបែកលើស្បែក", category=cat_skin),
        "scabs": Symptom(name="ក្រមរខ្មៅលើស្បែក", description="ក្រមរខ្មៅ ឬកន្ទួលលើស្បែក កំបិត និងជើង", category=cat_skin),
        "bluish_comb": Symptom(name="កំបិតឡើងពណ៌ស្វាយជាំ", description="កំបិត និងសន្ទះកំបិតឡើងពណ៌ខៀវស្វាយ ឬជាំខ្មៅ", category=cat_skin),
        # Reproductive
        "drop_egg": Symptom(name="ធ្លាក់ចុះការផលិតពង", description="ការបញ្ចេញពងថយចុះយ៉ាងខ្លាំង ឬឈប់ពងទាំងស្រុង", category=cat_repro),
        "soft_shell_eggs": Symptom(name="ពងសំបកទន់", description="ពងសំបកទន់ ឬគ្មានសំបកកំបោររឹង", category=cat_repro),
        "misshapen_eggs": Symptom(name="ពងខូចទ្រង់ទ្រាយ", description="ពងមានរូបរាងប្រែប្រួល រលក ឬតូចខុសប្រក្រតី", category=cat_repro),
    }
    db.session.add_all(symptoms.values())

    categories_map = {
        "cat_resp": cat_resp,
        "cat_digest": cat_digest,
        "cat_neuro": cat_neuro,
        "cat_bact": cat_bact,
        "cat_general": cat_general,
        "cat_skin": cat_skin,
        "cat_repro": cat_repro,
    }

    # Diseases (11) with clean, professional Khmer veterinary literature
    diseases = {}
    for key, data in DISEASE_KNOWLEDGE.items():
        diseases[key] = Disease(
            name=data["name"],
            description=data["description"],
            treatment=data["treatment"],
            prevention=data["prevention"],
            severity=data["severity"],
            is_contagious=data["is_contagious"],
            category=categories_map.get(data.get("category_key", "cat_general")),
        )
    db.session.add_all(diseases.values())
    db.session.flush()

    # Rules (12)
    rules = [
        Rule(
            title="Infectious Bronchitis",
            description="ក្អក + កណ្តាស់ + ហៀរសំបោរ + ធ្លាក់ចុះការផលិតពង",
            priority=1,
            confidence=85.0,
            disease=diseases["infectious_bronchitis"],
            symptoms=[symptoms["coughing"], symptoms["sneezing"], symptoms["nasal_discharge"], symptoms["drop_egg"]],
        ),
        Rule(
            title="Newcastle Disease",
            description="ក្អក + ហៀរសំបោរ + ស្រពោន/អសកម្ម + ក្បាលរមួលបង្វិល",
            priority=1,
            confidence=82.0,
            disease=diseases["newcastle"],
            symptoms=[symptoms["coughing"], symptoms["nasal_discharge"], symptoms["lethargy"], symptoms["twisted_neck"]],
        ),
        Rule(
            title="Coccidiosis",
            description="រាគមានឈាម + ស្រពោន/អសកម្ម + ខ្វះជាតិទឹក",
            priority=1,
            confidence=90.0,
            disease=diseases["coccidiosis"],
            symptoms=[symptoms["bloody_diarrhea"], symptoms["lethargy"], symptoms["dehydration"]],
        ),
        Rule(
            title="Fowl Cholera",
            description="ហើមមុខ/ក្បាល + ស្រពោន/អសកម្ម + រោមរញ៉េរញ៉ៃ/បះ + ងាប់ភ្លាមៗ",
            priority=1,
            confidence=80.0,
            disease=diseases["fowl_cholera"],
            symptoms=[symptoms["swollen_face"], symptoms["lethargy"], symptoms["ruffled"], symptoms["sudden_death"]],
        ),
        Rule(
            title="Marek Disease",
            description="ទន់ជើង/ដើរខ្វិន + ស្រពោន/អសកម្ម + ស្រកទម្ងន់/ស្គម",
            priority=2,
            confidence=76.0,
            disease=diseases["marek"],
            symptoms=[symptoms["lameness"], symptoms["lethargy"], symptoms["weight_loss"]],
        ),
        Rule(
            title="Avian Influenza",
            description="ក្អក + ស្រពោន/អសកម្ម + បាត់បង់ចំណង់អាហារ + ហៀរទឹកភ្នែក + កំបិតឡើងពណ៌ស្វាយជាំ",
            priority=1,
            confidence=88.0,
            disease=diseases["avian_influenza"],
            symptoms=[symptoms["coughing"], symptoms["lethargy"], symptoms["loss_appetite"], symptoms["watery_eyes"], symptoms["bluish_comb"]],
        ),
        Rule(
            title="Gumboro (IBD)",
            description="រាគពណ៌សកំបោរ + ស្រពោន/អសកម្ម + ខ្វះជាតិទឹក + រោមរញ៉េរញ៉ៃ/បះ",
            priority=1,
            confidence=83.0,
            disease=diseases["infectious_bursal"],
            symptoms=[symptoms["white_diarrhea"], symptoms["lethargy"], symptoms["dehydration"], symptoms["ruffled"]],
        ),
        Rule(
            title="Fowl Pox",
            description="ដំបៅស្បែក/ពងបែក + ក្រមរខ្មៅលើស្បែក + បាត់បង់ចំណង់អាហារ",
            priority=2,
            confidence=82.0,
            disease=diseases["fowl_pox"],
            symptoms=[symptoms["skin_lesions"], symptoms["scabs"], symptoms["loss_appetite"]],
        ),
        Rule(
            title="E. coli Infection",
            description="រាគពណ៌បៃតង + ស្រពោន/អសកម្ម + រោមរញ៉េរញ៉ៃ/បះ + ហើមមុខ/ក្បាល",
            priority=2,
            confidence=75.0,
            disease=diseases["ecoli"],
            symptoms=[symptoms["green_diarrhea"], symptoms["lethargy"], symptoms["ruffled"], symptoms["swollen_face"]],
        ),
        Rule(
            title="Mycoplasmosis (CRD)",
            description="ក្អក + កណ្តាស់ + ហើមប្រហោងមុខ + ហៀរទឹកភ្នែក",
            priority=2,
            confidence=80.0,
            disease=diseases["mycoplasmosis"],
            symptoms=[symptoms["coughing"], symptoms["sneezing"], symptoms["swollen_sinus"], symptoms["watery_eyes"]],
        ),
        Rule(
            title="Aspergillosis",
            description="ពិបាកដកដង្ហើម/ហារមាត់ + ស្រពោន/អសកម្ម + ស្រកទម្ងន់/ស្គម",
            priority=3,
            confidence=72.0,
            disease=diseases["aspergillosis"],
            symptoms=[symptoms["gasping"], symptoms["lethargy"], symptoms["weight_loss"]],
        ),
        Rule(
            title="Newcastle (Neurological)",
            description="ក្បាលផ្អៀង/វៀច + ញ័រខ្លួន/កន្ត្រាក់ + ទន់ជើង/ដើរខ្វិន + រាគពណ៌បៃតង",
            priority=1,
            confidence=85.0,
            disease=diseases["newcastle"],
            symptoms=[symptoms["head_tilt"], symptoms["tremors"], symptoms["lameness"], symptoms["green_diarrhea"]],
        ),
    ]
    db.session.add_all(rules)
    db.session.commit()


def upgrade_permissions():
    """Ensure new permissions exist on existing databases.
    Only creates missing permissions — does NOT overwrite
    role-permission assignments made via the admin UI.
    """
    permissions = [
        ("USER_CREATE", "Create Users", "Users"),
        ("USER_EDIT", "Edit Users", "Users"),
        ("USER_DELETE", "Delete Users", "Users"),
        ("ROLE_MANAGE", "Manage Roles", "Roles"),
        ("PERMISSION_MANAGE", "Manage Permissions", "Permissions"),
        ("view_dashboard", "View Dashboard", "Dashboard"),
        ("author_rules", "Author Expert Rules", "Expert System"),
        ("manage_symptoms", "Manage Symptoms", "Expert System"),
        ("manage_diseases", "Manage Diseases", "Expert System"),
        ("manage_rules", "Manage Rules", "Expert System"),
        ("manage_categories", "Manage Categories", "Expert System"),
        ("run_diagnosis", "Run Diagnosis", "Expert System"),
        ("view_cases", "View Case History", "Expert System"),
        ("review_cases", "Review Diagnosis Cases", "Expert System"),
    ]

    for code, name, module in permissions:
        existing = db.session.scalar(
            db.select(PermissionTable).filter_by(code=code)
        )
        if not existing:
            perm = PermissionTable(code=code, name=name, module=module)
            db.session.add(perm)

    # Ensure the three base roles exist (but don't touch their permissions)
    for role_name, desc in [("Admin", "System administrator"), ("Doctor", "Knowledge author"), ("User", "Diagnosis user")]:
        existing = db.session.scalar(db.select(RoleTable).filter_by(name=role_name))
        if not existing:
            db.session.add(RoleTable(name=role_name, description=desc))

    db.session.commit()


def update_disease_knowledge():
    """Sync all 11 diseases, symptoms, and categories in existing databases with professional Khmer literature."""
    try:
        # 1. Update Categories
        categories_data = {
            "ប្រព័ន្ធដង្ហើម": "រោគសញ្ញាទាក់ទងនឹងប្រព័ន្ធដង្ហើម",
            "ប្រព័ន្ធរំលាយអាហារ": "រោគសញ្ញាទាក់ទងនឹងពោះវៀន និងប្រព័ន្ធរំលាយអាហារ",
            "ប្រព័ន្ធសរសៃប្រសាទ": "រោគសញ្ញាផ្នែកសរសៃប្រសាទ និងចលនាខ្វិន",
            "ការឆ្លងបាក់តេរី": "រោគសញ្ញាបង្កឡើងដោយការឆ្លងបាក់តេរី",
            "រោគសញ្ញាទូទៅ": "រោគសញ្ញាទូទៅលើសុខភាព និងកាយវិការ",
            "ស្បែកនិងរោម": "រោគសញ្ញាលើស្បែក រោម កំបិត និងភ្នែក",
            "ការផលិតពង": "រោគសញ្ញាទាក់ទងនឹងការបញ្ចេញពង និងបន្តពូជ",
        }
        legacy_cat_map = {
            "របបដង្ហើម": "ប្រព័ន្ធដង្ហើម",
            "រំលាយអាហារ": "ប្រព័ន្ធរំលាយអាហារ",
            "សរសៃប្រសាទ": "ប្រព័ន្ធសរសៃប្រសាទ",
            "បាក់តេរី": "ការឆ្លងបាក់តេរី",
            "ទូទៅ": "រោគសញ្ញាទូទៅ",
            "ស្បែក": "ស្បែកនិងរោម",
            "បន្តពូជ": "ការផលិតពង",
        }
        for old_name, new_name in legacy_cat_map.items():
            cat = db.session.scalar(db.select(Category).filter_by(name=old_name))
            if cat:
                cat.name = new_name
                cat.description = categories_data.get(new_name, cat.description)

        for cat_name, cat_desc in categories_data.items():
            cat = db.session.scalar(db.select(Category).filter_by(name=cat_name))
            if cat and not cat.description:
                cat.description = cat_desc

        # 2. Update Symptoms
        symptoms_clean = {
            "ក្អក": ("ក្អក", "ក្អកញឹកញាប់ ឬពិបាកដកដង្ហើម"),
            "កណ្តាស់": ("កណ្តាស់", "កណ្តាស់ញឹកញាប់"),
            "ហៀរសំបោរ": ("ហៀរសំបោរ", "មានសំបោរ ឬស្លេស្មចេញពីរន្ធច្រមុះ"),
            "ហៀរទឹកភ្នែក": ("ហៀរទឹកភ្នែក", "ភ្នែកហៀរទឹក ហើម ឬបិទជិត"),
            "ពិបាកដកដង្ហើម": ("ពិបាកដកដង្ហើម/ហារមាត់", "ហារមាត់ដកដង្ហើម ឬដកដង្ហើមញាប់ខ្លាំង"),
            "រលាកច្រមុះ/ប្រហោងមុខ": ("ហើមប្រហោងមុខ", "ហើមរលាកក្បែរភ្នែក ឬប្រហោងច្រមុះ"),
            "សំឡេងខ្យល់ស្អក": ("សំឡេងខ្យល់ដង្ហើមស្អក", "សំឡេងខ្យល់ដង្ហើមមិនប្រក្រតីឮសូរគ្រតៗក្នុងបំពង់ក"),
            "រាគរូស": ("រាគរូស", "រាគលាមករាវ ឬជាទឹក"),
            "រាគមានឈាម": ("រាគមានឈាម", "មានឈាមស្រស់ ឬកំទេចឈាមលាយឡំក្នុងលាមក"),
            "រាគពណ៌បៃតង": ("រាគពណ៌បៃតង", "លាមករាវពណ៌បៃតងស្រស់ ឬលាយស"),
            "រាគពណ៌ស": ("រាគពណ៌សកំបោរ", "លាមករាវពណ៌សកំបោរស្អិតជាប់គូទ"),
            "ប៉ោងក្រពះចំណី": ("ប៉ោងក្រពះចំណី", "ក្រពះចំណី (ពោះវៀនក) ឡើងប៉ោងតឹងពេញដោយទឹកឬខ្យល់"),
            "ខ្វិនជើង": ("ទន់ជើង/ដើរខ្វិន", "ពិបាកដើរ ជើងទន់ខ្សោយ ឬដើរទាក់"),
            "ក្បាលវៀច": ("ក្បាលផ្អៀង/វៀច", "ក្បាលផ្អៀងទៅម្ខាង ឬងាកចុះក្រោម"),
            "ញ័រខ្លួន": ("ញ័រខ្លួន/កន្ត្រាក់", "រាងកាយញ័រ ឬកន្ត្រាក់សាច់ដុំ"),
            "ខ្វិនជើង ឬស្លាប": ("ខ្វិនជើង ឬស្លាប", "មិនអាចដើរបាន ឬជើងនិងស្លាបទន់លែងកម្រើក"),
            "ក្បាលបង្វិល": ("ក្បាលរមួលបង្វិល", "ក្បាលរមួលបង្វិលខុសធម្មជាតិ (Torticollis)"),
            "ស្រពោន/អសកម្ម": ("ស្រពោន/អសកម្ម", "ថយចុះថាមពល ដេកសណ្តូកស្ងប់ស្ងៀម មិនរវើករវាយ"),
            "រោមរញ៉េរញ៉ៃ": ("រោមរញ៉េរញ៉ៃ/បះ", "រោមបះមិនស្អាត ឬរញ៉េរញ៉ៃ ធ្លាក់ស្លាប"),
            "បាត់បង់ចំណង់អាហារ": ("បាត់បង់ចំណង់អាហារ", "មិនស៊ីចំណី ឬស៊ីតិចតួចខុសធម្មតា"),
            "ស្រកទម្ងន់": ("ស្រកទម្ងន់/ស្គម", "ស្រកទម្ងន់លឿន ឬស្គមរីងរៃសល់តែឆ្អឹងទ្រូង"),
            "ងាប់ភ្លាមៗ": ("ងាប់ភ្លាមៗ", "ងាប់យ៉ាងឆាប់រហ័សដោយគ្មានរោគសញ្ញាព្រមាន"),
            "ក្តៅខ្លួន": ("ក្តៅខ្លួនខ្លាំង", "សីតុណ្ហភាពរាងកាយឡើងខ្ពស់ ជើងក្តៅ"),
            "ខ្វះជាតិទឹក": ("ខ្វះជាតិទឹក", "ស្បែកស្ងួត ភ្នែកខូងស្រពោន ជើងស្វិតស្ងួត"),
            "ហើមមុខ": ("ហើមមុខ/ក្បាល", "ផ្ទៃមុខ ក្បាល ឬកំបិតឡើងហើមធំ"),
            "ដំបៅស្បែក": ("ដំបៅស្បែក/ពងបែក", "របួស ដំបៅ ឬពងបែកលើស្បែក"),
            "ក្រមរស្បែក": ("ក្រមរខ្មៅលើស្បែក", "ក្រមរខ្មៅ ឬកន្ទួលលើស្បែក កំបិត និងជើង"),
            "កំបិតស្វាយ/ជាំ": ("កំបិតឡើងពណ៌ស្វាយជាំ", "កំបិត និងសន្ទះកំបិតឡើងពណ៌ខៀវស្វាយ ឬជាំខ្មៅ"),
            "ធ្លាក់ចុះការផលិតពង": ("ធ្លាក់ចុះការផលិតពង", "ការបញ្ចេញពងថយចុះយ៉ាងខ្លាំង ឬឈប់ពងទាំងស្រុង"),
            "សំបកពងទន់": ("ពងសំបកទន់", "ពងសំបកទន់ ឬគ្មានសំបកកំបោររឹង"),
            "ពងខូចទ្រង់ទ្រាយ": ("ពងខូចទ្រង់ទ្រាយ", "ពងមានរូបរាងប្រែប្រួល រលក ឬតូចខុសប្រក្រតី"),
        }
        for old_name, (new_name, new_desc) in symptoms_clean.items():
            sym = db.session.scalar(db.select(Symptom).filter_by(name=old_name))
            if sym:
                sym.name = new_name
                sym.description = new_desc

        # 3. Update Diseases
        keyword_map = {
            "infectious_bronchitis": ["bronchitis", "ទងសួត"],
            "newcastle": ["newcastle", "ញូកាសល"],
            "coccidiosis": ["coccidiosis", "រាគឈាម", "កុកស៊ីឌី"],
            "fowl_cholera": ["cholera", "អាសន្នរោគ"],
            "marek": ["marek", "ម៉ារ៉ែក"],
            "avian_influenza": ["influenza", "ផ្តាសាយ", "គ្រុនចំពាក់"],
            "infectious_bursal": ["gumboro", "ibd", "ហ្គាំបូរ៉ូ", "ប៊ូរសា"],
            "fowl_pox": ["pox", "អុត"],
            "ecoli": ["coli", "អ៊ីខូឡៃ"],
            "mycoplasmosis": ["mycoplasmosis", "crd", "រ៉ាំរ៉ៃ"],
            "aspergillosis": ["aspergillosis", "ផ្សិត"],
        }
        id_order = [
            "infectious_bronchitis",
            "newcastle",
            "coccidiosis",
            "fowl_cholera",
            "marek",
            "avian_influenza",
            "infectious_bursal",
            "fowl_pox",
            "ecoli",
            "mycoplasmosis",
            "aspergillosis",
        ]

        all_diseases = db.session.scalars(db.select(Disease)).all()
        updated_keys = set()

        for d in all_diseases:
            matched_key = None
            d_name_lower = d.name.lower()
            for key, keywords in keyword_map.items():
                if any(kw in d_name_lower for kw in keywords):
                    matched_key = key
                    break
            if not matched_key and 1 <= d.id <= len(id_order):
                matched_key = id_order[d.id - 1]

            if matched_key and matched_key in DISEASE_KNOWLEDGE:
                data = DISEASE_KNOWLEDGE[matched_key]
                d.name = data["name"]
                d.description = data["description"]
                d.treatment = data["treatment"]
                d.prevention = data["prevention"]
                d.severity = data["severity"]
                d.is_contagious = data["is_contagious"]
                updated_keys.add(matched_key)

        # If any disease was missing, create it
        for key, data in DISEASE_KNOWLEDGE.items():
            if key not in updated_keys:
                existing = db.session.scalar(db.select(Disease).filter_by(name=data["name"]))
                if not existing:
                    cat = db.session.scalar(db.select(Category).filter_by(name="ប្រព័ន្ធដង្ហើម"))
                    new_d = Disease(
                        name=data["name"],
                        description=data["description"],
                        treatment=data["treatment"],
                        prevention=data["prevention"],
                        severity=data["severity"],
                        is_contagious=data["is_contagious"],
                        category=cat,
                    )
                    db.session.add(new_d)

        db.session.commit()
    except Exception as e:
        db.session.rollback()


def seed_all():
    seed_permissions_and_roles()
    seed_admin_user()
    seed_expert_data()
    update_disease_knowledge()
