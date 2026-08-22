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


def seed_expert_data():
    if db.session.scalar(db.select(Symptom).limit(1)):
        return

    # Categories
    cat_resp = _get_or_create(Category, name="\u179a\u1794\u1794\u178a\u1784\u17d2\u17a0\u17be\u1798",
                              defaults={"description": "\u179a\u17c4\u1782\u179f\u1789\u17d2\u1789\u17b6\u178f\u17b6\u1780\u17cb\u178f\u1784\u1793\u17b9\u1784\u1794\u17d2\u179a\u1796\u17d0\u1793\u17d2\u1792\u178a\u1784\u17d2\u17a0\u17be\u1798"})
    cat_digest = _get_or_create(Category, name="\u179a\u17c6\u179b\u17b6\u1799\u17a2\u17b6\u17a0\u17b6\u179a",
                                defaults={"description": "\u179a\u17c4\u1782\u179f\u1789\u17d2\u1789\u17b6\u1796\u17c4\u17a0\u179c\u17c0\u1793 \u1793\u17b7\u1784\u1794\u17d2\u179a\u1796\u17d0\u1793\u17d2\u1792\u179a\u17c6\u179b\u17b6\u1799\u17a2\u17b6\u17a0\u17b6\u179a"})
    cat_neuro = _get_or_create(Category, name="\u179f\u179a\u179f\u17c3\u1794\u17d2\u179a\u179f\u17b6\u1791",
                               defaults={"description": "\u179a\u17c4\u1782\u179f\u1789\u17d2\u1789\u17b6\u1795\u17d2\u1793\u17c2\u1780\u179f\u179a\u179f\u17c3\u1794\u17d2\u179a\u179f\u17b6\u1791 \u1793\u17b7\u1784\u1785\u179b\u1793\u17b6"})
    cat_bact = _get_or_create(Category, name="\u1794\u17b6\u1780\u17cb\u178f\u17c1\u179a\u17b8",
                              defaults={"description": "\u179a\u17c4\u1782\u179f\u1789\u17d2\u1789\u17b6\u1780\u17b6\u179a\u1786\u17d2\u179b\u1784\u178a\u17c4\u1799\u1794\u17b6\u1780\u17cb\u178f\u17c1\u179a\u17b8"})
    cat_general = _get_or_create(Category, name="\u1791\u17bc\u1791\u17c5",
                                 defaults={"description": "\u179a\u17c4\u1782\u179f\u1789\u17d2\u1789\u17b6\u1791\u17bc\u1791\u17c5"})
    cat_skin = _get_or_create(Category, name="\u179f\u17d2\u1794\u17c2\u1780",
                              defaults={"description": "\u179a\u17c4\u1782\u179f\u1789\u17d2\u1789\u17b6\u179b\u17be\u179f\u17d2\u1794\u17c2\u1780 \u179a\u17c4\u1798 \u1793\u17b7\u1784\u1780\u17c6\u1794\u17d2\u17b7\u178f"})
    cat_repro = _get_or_create(Category, name="\u1794\u1793\u17d2\u178f\u1796\u17bc\u1787",
                               defaults={"description": "\u179a\u17c4\u1782\u179f\u1789\u17d2\u1789\u17b6\u178f\u17b6\u1780\u17cb\u178f\u1784\u1793\u17b9\u1784\u1796\u1784 \u1793\u17b7\u1784\u1794\u1793\u17d2\u178f\u1796\u17bc\u1787"})

    # Symptoms (30)
    symptoms = {
        # Respiratory
        "coughing": Symptom(name="\u1780\u17d2\u17a2\u1780", description="\u1780\u17d2\u17a2\u1780\u1789\u17b9\u1780\u1789\u17b6\u1794\u17cb \u17ac\u1796\u17b7\u1794\u17b6\u1780\u178a\u1780\u178a\u1784\u17d2\u17a0\u17be\u1798", category=cat_resp),
        "sneezing": Symptom(name="\u1780\u178e\u17d2\u178f\u17b6\u179f\u17cb", description="\u1780\u178e\u17d2\u178f\u17b6\u179f\u17cb\u1789\u17b9\u1780\u1789\u17b6\u1794\u17cb", category=cat_resp),
        "nasal_discharge": Symptom(name="\u17a0\u17bc\u179a\u1785\u17d2\u179a\u1798\u17bb\u17a0", description="\u1798\u17b6\u1793\u179f\u17d2\u179b\u17c1\u1780\u1785\u17c1\u1789\u1796\u17b8\u179a\u1793\u17d2\u1792\u1785\u17d2\u179a\u1798\u17bb\u17a0", category=cat_resp),
        "watery_eyes": Symptom(name="\u1797\u17d2\u1793\u17c2\u1780\u17a0\u17bc\u179a\u1791\u17b9\u1780", description="\u1797\u17d2\u1793\u17c2\u1780\u17a0\u17bc\u179a\u1791\u17b9\u1780 \u17ac\u1794\u17b7\u1791", category=cat_resp),
        "gasping": Symptom(name="\u178a\u1780\u178a\u1784\u17d2\u17a0\u17be\u1798\u1796\u17b7\u1794\u17b6\u1780", description="\u17a0\u17ba\u178f \u17ac\u178a\u1780\u178a\u1784\u17d2\u17a0\u17be\u1798\u1799\u17c9\u17b6\u1784\u1781\u17d2\u179b\u17b6\u17c6\u1784", category=cat_resp),
        "swollen_sinus": Symptom(name="\u179a\u179b\u17be\u1780 sinus", description="\u179a\u179b\u17be\u1780\u1780\u17d2\u1794\u17c2\u179a\u1797\u17d2\u1793\u17c2\u1780 \u17ac\u179a\u1793\u17d2\u1792\u1785\u17d2\u179a\u1798\u17bb\u17a0", category=cat_resp),
        "tracheal_rales": Symptom(name="\u179f\u17c6\u179b\u17c1\u1784\u1781\u17d2\u1799\u179b\u17cb\u1786\u17d2\u17a2\u17be\u179a", description="\u179f\u17c6\u179b\u17c1\u1784\u1781\u17d2\u1799\u179b\u17cb\u1798\u17b7\u1793\u1794\u17d2\u179a\u1780\u17d2\u179a\u178f\u17b8\u1793\u17c5\u1780\u17d2\u1793\u17bb\u1784\u1794\u17c6\u1796\u1784\u17cb\u1780", category=cat_resp),
        # Digestive
        "diarrhea": Symptom(name="\u179a\u17b6\u1780\u179a\u17bc\u179f", description="\u179a\u17b6\u1780\u179f\u17d2\u179a\u17b6\u179b \u17ac\u1791\u17b9\u1780", category=cat_digest),
        "bloody_diarrhea": Symptom(name="\u179a\u17b6\u1780\u1798\u17b6\u1793\u1788\u17b6\u1798", description="\u1798\u17b6\u1793\u1788\u17b6\u1798\u1780\u17d2\u1793\u17bb\u1784\u179a\u17b6\u1780", category=cat_digest),
        "green_diarrhea": Symptom(name="\u179a\u17b6\u1780\u1796\u178e\u17cc\u1794\u17c3\u178f\u1784", description="\u179b\u17b6\u1798\u1780\u1796\u178e\u17cc\u1794\u17c3\u178f\u1784 \u17ac\u179b\u17be\u1784", category=cat_digest),
        "white_diarrhea": Symptom(name="\u179a\u17b6\u1780\u1796\u178e\u17cc\u179f", description="\u179b\u17b6\u1798\u1780\u1796\u178e\u17cc\u179f \u17ac\u1794\u17d2\u179a\u1795\u17c1\u17a0", category=cat_digest),
        "crop_distension": Symptom(name="\u1794\u1794\u17bc\u179a\u1780\u17a0\u17be\u1798", description="\u1794\u1794\u17bc\u179a\u1780\u1795\u17d2\u17a2\u17be\u1798 \u17ac\u1796\u17c4\u179a\u1796\u17c1\u1789", category=cat_digest),
        # Neurological
        "lameness": Symptom(name="\u1796\u17b7\u1780\u179b\u1797\u17d2\u1793\u17c2\u1793", description="\u1796\u17b7\u1794\u17b6\u1780\u178a\u17be\u179a \u17ac\u1787\u17be\u1784\u1781\u17d2\u179f\u17c4\u1799", category=cat_neuro),
        "head_tilt": Symptom(name="\u1780\u17d2\u1794\u17b6\u179b\u179c\u17c1\u179a", description="\u1780\u17d2\u1794\u17b6\u179b\u1791\u17c1\u179a \u17ac\u1780\u17d2\u1794\u17b6\u179b\u1794\u178f\u17cb\u1798\u17bb\u1781\u1785\u17bb\u17a0", category=cat_neuro),
        "tremors": Symptom(name="\u1789\u17b6\u1780\u17cb", description="\u179a\u17b6\u1784\u1780\u17b6\u1799\u1789\u17b6\u1780\u17cb \u17ac\u1789\u17d0\u179a", category=cat_neuro),
        "paralysis": Symptom(name="\u179f\u17d2\u179b\u17b6\u1794\u17cb\u178a org \u1787\u17be\u1784", description="\u1798\u17b7\u1793\u17a2\u17b6\u1785\u178a\u17be\u179a\u1794\u17b6\u1793 \u17ac\u1787\u17be\u1784\u179f\u1796\u17d2\u179c\u1797\u17d2\u1793\u17c2\u1793", category=cat_neuro),
        "twisted_neck": Symptom(name="\u1780\u1794\u178f\u17cb\u1798\u17bb\u1781", description="\u1780\u1794\u178f\u17cb\u1798\u17bb\u1781 \u17ac\u1794\u1784\u17d2\u179c\u17b7\u179b\u1780\u17d2\u1794\u17b6\u179b (torticollis)", category=cat_neuro),
        # General
        "lethargy": Symptom(name="\u17a2\u179f\u1780\u1798\u17d2\u1798", description="\u1790\u1799\u1785\u17bb\u17a0\u1790\u17b6\u1798\u1796\u179b \u17ac\u179f\u17d2\u1784\u17b6\u178f\u17cb\u179f\u17d2\u1784\u17c0\u1798", category=cat_general),
        "ruffled": Symptom(name="\u179a\u17c4\u1798\u179a\u17bd\u1789", description="\u179a\u17c4\u1798\u1798\u17b7\u1793\u179f\u17d2\u17a2\u17b6\u178f \u17ac\u179a\u17bd\u1789", category=cat_general),
        "loss_appetite": Symptom(name="\u1794\u17b6\u178f\u17cb\u1794\u1784\u17cb\u1785\u17c6\u178e\u1784\u17cb\u17a2\u17b6\u17a0\u17b6\u179a", description="\u1798\u17b7\u1793\u1789\u17c9\u17b6\u17c6\u1785\u17c6\u178e\u17b8", category=cat_general),
        "weight_loss": Symptom(name="\u179f\u17d2\u1782\u1798", description="\u179f\u17d2\u179a\u1780\u1791\u17c6\u1784\u1793\u17cb \u17ac\u179f\u17d2\u1782\u1798\u1781\u17d2\u179b\u17b6\u17c6\u1784", category=cat_general),
        "sudden_death": Symptom(name="\u179f\u17d2\u179b\u17b6\u1794\u17cb\u1797\u17d2\u179b\u17b6\u1798\u17d7", description="\u179f\u17d2\u179b\u17b6\u1794\u17cb\u178a\u17c4\u1799\u1798\u17b7\u1793\u1798\u17b6\u1793\u179a\u17c4\u1782\u179f\u1789\u17d2\u1789\u17b6\u1785\u17d2\u1794\u17b6\u179f\u17cb", category=cat_general),
        "fever": Symptom(name="\u1782\u17d2\u179a\u17bb\u1793", description="\u179f\u17b8\u178f\u17bb\u178e\u17d2\u17a0\u1797\u17b6\u1796\u179a\u17b6\u1784\u1780\u17b6\u1799\u1781\u17d2\u1796\u179f\u17cb", category=cat_general),
        "dehydration": Symptom(name="\u1781\u17d2\u179c\u17a0\u1791\u17b9\u1780", description="\u179f\u17d2\u1794\u17c2\u1780\u179f\u17d2\u1784\u17bd\u178f \u179a\u17c4\u1798\u1789\u17c9\u17c1\u1784 \u1797\u17d2\u1793\u17c2\u1780\u1787\u17d2\u179a\u17bb\u179b", category=cat_general),
        # Skin
        "swollen_face": Symptom(name="\u1798\u17bb\u1781\u179a\u179b\u17be\u1780", description="\u1798\u17bb\u1781 \u17ac\u1780\u17d2\u1794\u17b6\u179b\u179a\u179b\u17be\u1780", category=cat_bact),
        "skin_lesions": Symptom(name="\u179a\u1794\u17bd\u179f\u179f\u17d2\u1794\u17c2\u1780", description="\u179a\u1794\u17bd\u179f \u17ac\u178a\u17c6\u1794\u17c5\u179b\u17be\u179f\u17d2\u1794\u17c2\u1780", category=cat_skin),
        "scabs": Symptom(name="\u1780\u1793\u17d2\u1791\u1780\u17cb\u179f\u17d2\u1794\u17c2\u1780", description="\u1780\u1793\u17d2\u1791\u1780\u17cb \u17ac\u179f\u17d2\u179a\u17b6\u1799\u179b\u17be\u179f\u17d2\u1794\u17c2\u1780 \u1780\u17d2\u179a\u1785\u1780\u17cb", category=cat_skin),
        "bluish_comb": Symptom(name="\u1780\u17c6\u1794\u17d2\u17b7\u178f\u179f\u17d2\u179a\u17a2\u17b6\u1794\u17cb", description="\u1780\u17c6\u1794\u17d2\u17b7\u178f \u1793\u17b7\u1784\u1780\u17c2\u1784\u1798\u17b6\u1793\u17cb\u1796\u178e\u17cc\u1781\u17c0\u179c \u17ac\u179f\u17d2\u179a\u17a2\u17b6\u1794\u17cb", category=cat_skin),
        # Reproductive
        "drop_egg": Symptom(name="\u1796\u1784\u1792\u17d2\u179b\u17b6\u1780\u17cb", description="\u1780\u17b6\u179a\u1794\u1789\u17d2\u1785\u17c1\u1789\u1796\u1784\u1790\u1799\u1785\u17bb\u17a0 \u17ac\u1788\u1794\u17cb", category=cat_repro),
        "soft_shell_eggs": Symptom(name="\u179f\u17c6\u1794\u1780\u1796\u1784\u1791\u1793\u17cb", description="\u1796\u1784\u179f\u17c6\u1794\u1780\u1791\u1793\u17cb \u17ac\u1782\u17d2\u1798\u17b6\u1793\u179f\u17c6\u1794\u1780", category=cat_repro),
        "misshapen_eggs": Symptom(name="\u1796\u1784\u1798\u17b7\u1793\u1792\u1798\u17d2\u1798\u178f\u17b6", description="\u1796\u1784\u179a\u17b6\u1784\u1794\u17d2\u179a\u17c2\u1794\u17d2\u179a\u17bd\u179b \u17ac\u178f\u17bc\u1785", category=cat_repro),
    }
    db.session.add_all(symptoms.values())

    # Diseases (11)
    diseases = {
        "infectious_bronchitis": Disease(
            name="\u1787\u17c6\u1784\u17ba\u1794\u17d2\u179a\u1796\u17d0\u1793\u17d2\u1792\u178a\u1784\u17d2\u17a0\u17be\u1798\u1786\u17d2\u179b\u1784",
            description="\u1787\u17c6\u1784\u17ba\u1786\u17d2\u179b\u1784\u1781\u17d2\u179b\u17b6\u17c6\u1784 \u1794\u17c9\u17a0\u17a0\u1796\u17b6\u179b\u17cb\u1794\u17d2\u179a\u1796\u17d0\u1793\u17d2\u1792\u178a\u1784\u17d2\u17a0\u17be\u1798 \u1793\u17b7\u1784\u17a2\u17b6\u1785\u1794\u17c9\u17a0\u17a0\u1796\u17b6\u179b\u17cb\u1780\u17b6\u179a\u1794\u1789\u17d2\u1785\u17c1\u1789\u1796\u1784\u17d4",
            treatment="\u178a\u17b6\u1780\u17cb\u17a1\u17c4\u1799\u178a\u17c4\u1799\u17a1\u17c2\u1780 \u1790\u17c2\u1791\u17b6\u17c6\u1782\u17b6\u17c6\u1791\u17d2\u179a \u1793\u17b7\u1784\u1794\u17d2\u179a\u17b9\u1780\u17d2\u179f\u17b6\u1787\u17b6\u1798\u17bd\u1799\u179c\u17c1\u1787\u17d2\u1787\u1794\u178e\u17d2\u178c\u17b7\u178f\u17d4",
            prevention="\u1785\u17b6\u1780\u17cb\u179c\u17c9\u17b6\u1780\u17cb\u179f\u17b6\u17c6\u1784 \u179a\u1780\u17d2\u179f\u17b6\u1780\u17b6\u179a\u1794\u179a\u17b7\u179f\u17bb\u1791\u17d2\u1792 \u1793\u17b7\u1784\u1780\u17b6\u179a\u1796\u17b6\u179a\u1780\u17b6\u179a\u1786\u17d2\u179b\u1784\u17d4",
            severity="\u1798\u1792\u17d2\u1799\u1798",
            is_contagious=True,
            category=cat_resp,
        ),
        "newcastle": Disease(
            name="\u1787\u17c6\u1784\u17ba Newcastle",
            description="\u1787\u17c6\u1784\u17ba virus \u1794\u17c9\u17a0\u17a0\u1796\u17b6\u179b\u17cb\u1794\u17d2\u179a\u1796\u17d0\u1793\u17d2\u1792\u178a\u1784\u17d2\u17a0\u17be\u1798 \u1793\u17b7\u1784\u179f\u179a\u179f\u17c3\u1794\u17d2\u179a\u179f\u17b6\u1791\u17d4",
            treatment="\u178a\u17b6\u1780\u17cb\u17a1\u17c4\u1799\u178a\u17c4\u1799\u17a1\u17c2\u1780 \u1787\u17bc\u1793\u178a\u17c6\u178e\u17b9\u1784\u179c\u17c1\u1787\u17d2\u1787\u1794\u178e\u17d2\u178c\u17b7\u178f \u1793\u17b7\u1784\u17a2\u1793\u17bb\u179c\u178f\u17d2\u178f\u1780\u17b6\u179a\u1785\u17b6\u1780\u17cb\u179c\u17c9\u17b6\u1780\u17cb\u179f\u17b6\u17c6\u1784\u17d4",
            prevention="\u1785\u17b6\u1780\u17cb\u179c\u17c9\u17b6\u1780\u17cb\u179f\u17b6\u17c6\u1784 Newcastle \u1787\u17b6\u1794\u17d2\u179a\u1785\u17b6\u17c6 \u1793\u17b7\u1784\u179a\u17b9\u178f\u1794\u1793\u17d2\u178f\u17b9\u1784\u1780\u17b6\u179a\u1794\u179a\u17b7\u179f\u17bb\u1791\u17d2\u1792\u17d4",
            severity="\u1781\u17d2\u1796\u179f\u17cb",
            is_contagious=True,
            category=cat_neuro,
        ),
        "coccidiosis": Disease(
            name="\u1787\u17c6\u1784\u17ba Coccidiosis",
            description="\u1787\u17c6\u1784\u17ba\u1794\u179a\u17b6\u179f\u17b8\u178f\u1780\u17d2\u1793\u17bb\u1784\u1796\u17c4\u17a0\u179c\u17c0\u1793 \u1794\u1784\u17d2\u1780\u179a\u17b6\u1780\u1798\u17b6\u1793\u1788\u17b6\u1798\u17d4",
            treatment="\u1794\u17d2\u179a\u17be\u1790\u17d2\u1793\u17b6\u17c6 anticoccidial \u1793\u17b7\u1784\u179a\u1780\u17d2\u179f\u17b6\u1780\u1793\u17d2\u179b\u17c2\u1784\u17b1\u17d2\u1799\u179f\u17d2\u17a2\u17b6\u178f\u17d4",
            prevention="\u179a\u1780\u17d2\u179f\u17b6\u1780\u1793\u17d2\u179b\u17c2\u1784\u179f\u17d2\u17a2\u17b6\u178f \u1794\u1784\u17d2\u179c\u17b7\u179b\u178a\u17b8 \u1793\u17b7\u1784\u1794\u17d2\u179a\u17be\u1790\u17d2\u1793\u17b6\u17c6\u1780\u17b6\u179a\u1796\u17b6\u179a\u17d4",
            severity="\u1798\u1792\u17d2\u1799\u1798",
            is_contagious=False,
            category=cat_digest,
        ),
        "fowl_cholera": Disease(
            name="\u1787\u17c6\u1784\u17ba Fowl Cholera",
            description="\u1780\u17b6\u179a\u1786\u17d2\u179b\u1784\u1794\u17b6\u1780\u17cb\u178f\u17c1\u179a\u17b8 \u1794\u1784\u17d2\u1780\u17a2\u17b6\u1780\u17b6\u179a\u1797\u17d2\u179b\u17b6\u1798\u17d7 \u1793\u17b7\u1784\u179f\u17d2\u179b\u17b6\u1794\u17cb\u17d4",
            treatment="\u1794\u17d2\u179a\u17be\u1790\u17d2\u1793\u17b6\u17c6 antibiotic \u1780\u17d2\u179a\u17c4\u1798\u1780\u17b6\u179a\u178e\u17c2\u1793\u17b6\u17c6\u179c\u17c1\u1787\u17d2\u1787\u1794\u178e\u17d2\u178c\u17b7\u178f \u1793\u17b7\u1784\u1780\u17c2\u179b\u17c6\u17a2\u1780\u17b6\u179a\u1794\u179a\u17b7\u179f\u17bb\u1791\u17d2\u1792\u17d4",
            prevention="\u179a\u1780\u17d2\u179f\u17b6\u1780\u17b6\u179a\u1794\u179a\u17b7\u179f\u17bb\u1791\u17d2\u1792 \u1793\u17b7\u1784\u1785\u17b6\u1780\u17cb\u179c\u17c9\u17b6\u1780\u17cb\u179f\u17b6\u17c6\u1784\u17d4",
            severity="\u1781\u17d2\u1796\u179f\u17cb",
            is_contagious=True,
            category=cat_bact,
        ),
        "marek": Disease(
            name="\u1787\u17c6\u1784\u17ba Marek",
            description="\u1787\u17c6\u1784\u17ba virus \u1794\u1784\u17d2\u1780\u1796\u17b7\u1780\u179b\u1797\u17d2\u1793\u17c2\u1793 \u1793\u17b7\u1784 tumor\u17d4",
            treatment="\u1782\u17d2\u1798\u17b6\u1793\u1790\u17d2\u1793\u17b6\u17c6\u1796\u17d2\u1799\u17b6\u1794\u17b6\u179b \u1785\u17b6\u1780\u17cb\u179c\u17c9\u17b6\u1780\u17cb\u179f\u17b6\u17c6\u1784\u1780\u17bc\u1793\u1798\u17b6\u1793\u17cb \u1793\u17b7\u1784\u178a\u17b6\u1780\u17cb\u17a1\u17c4\u1799\u178a\u17c4\u1799\u17a1\u17c2\u1780\u17d4",
            prevention="\u1785\u17b6\u1780\u17cb\u179c\u17c9\u17b6\u1780\u17cb\u179f\u17b6\u17c6\u1784 Marek \u17b1\u17d2\u1799\u1780\u17bc\u1793\u1798\u17b6\u1793\u17cb\u1790\u17d2\u1784\u17c3\u178a\u17c6\u1794\u17bc\u1784\u17d4",
            severity="\u1781\u17d2\u1796\u179f\u17cb",
            is_contagious=True,
            category=cat_neuro,
        ),
        "avian_influenza": Disease(
            name="\u1787\u17c6\u1784\u17ba\u1782\u17d2\u179a\u17bb\u1793\u1785\u17c6\u1796\u17b6\u1780\u17cb\u1798\u17b6\u1793\u17cb",
            description="\u1787\u17c6\u1784\u17ba virus \u1786\u17d2\u179b\u1784\u1781\u17d2\u179b\u17b6\u17c6\u1784 \u1794\u1784\u17d2\u1780\u179a\u17c4\u1782\u179f\u1789\u17d2\u1789\u17b6\u178a\u1784\u17d2\u17a0\u17be\u1798 \u1793\u17b7\u1784\u179f\u17d2\u179b\u17b6\u1794\u17cb\u1781\u17d2\u1796\u179f\u17cb\u17d4",
            treatment="\u178a\u17b6\u1780\u17cb\u17a1\u17c4\u1799\u178a\u17c4\u1799\u17a1\u17c2\u1780 \u1787\u17bc\u1793\u178a\u17c6\u178e\u17b9\u1784\u17a2\u17b6\u1787\u17d2\u1789\u17b6\u1792\u179a \u1793\u17b7\u1784\u179c\u17c1\u1787\u17d2\u1787\u1794\u178e\u17d2\u178c\u17b7\u178f\u1797\u17d2\u179b\u17b6\u1798\u17d7\u17d4",
            prevention="\u179a\u17b9\u178f\u1794\u1793\u17d2\u178f\u17b9\u1784 biosecurity \u1793\u17b7\u1784\u1787\u17c0\u179f\u179c\u17b6\u1784 contact \u1787\u17b6\u1798\u17bd\u1799\u179f\u178f\u17d2\u179c\u1785\u17c3\u178a\u1793\u17d2\u1799\u17d4",
            severity="\u1781\u17d2\u1796\u179f\u17cb",
            is_contagious=True,
            category=cat_resp,
        ),
        "infectious_bursal": Disease(
            name="\u1787\u17c6\u1784\u17ba Gumboro (IBD)",
            description="\u1787\u17c6\u1784\u17ba virus \u1794\u17c9\u17a0\u17a0\u1796\u17b6\u179b\u17cb\u1794\u17d2\u179a\u1796\u17d0\u1793\u17d2\u1792\u178a org \u17a2\u17ca\u17b8\u1798\u17bc\u1793 (bursa Fabricius) \u1780\u17d2\u1793\u17bb\u1784\u1798\u17b6\u1793\u17cb\u1780\u17bc\u1793\u17d4",
            treatment="\u1790\u17c2\u1791\u17b6\u17c6\u1782\u17b6\u17c6\u1791\u17d2\u179a \u17b1\u17d2\u1799\u1791\u17b9\u1780\u1782\u17d2\u179a\u1794\u17cb\u1782\u17d2\u179a\u17b6\u1793\u17cb \u1793\u17b7\u1784 electrolyte\u17d4",
            prevention="\u1785\u17b6\u1780\u17cb\u179c\u17c9\u17b6\u1780\u17cb\u179f\u17b6\u17c6\u1784 IBD \u178f\u17b6\u1798\u1780\u1798\u17d2\u1798\u179c\u17b7\u1792\u17b8\u17d4",
            severity="\u1798\u1792\u17d2\u1799\u1798-\u1781\u17d2\u1796\u179f\u17cb",
            is_contagious=True,
            category=cat_general,
        ),
        "fowl_pox": Disease(
            name="\u1787\u17c6\u1784\u17ba Fowl Pox",
            description="\u1787\u17c6\u1784\u17ba virus \u1794\u1784\u17d2\u1780\u178a\u17c6\u1794\u17c5 \u1793\u17b7\u1784\u1780\u1793\u17d2\u1791\u1780\u17cb\u179b\u17be\u179f\u17d2\u1794\u17c2\u1780 \u1780\u17c6\u1794\u17d2\u17b7\u178f \u1793\u17b7\u1784\u1798\u17b6\u178f\u17cb\u17d4",
            treatment="\u1790\u17c2\u1791\u17b6\u17c6\u179a\u1794\u17bd\u179f\u178a\u17c4\u1799 antiseptic \u1793\u17b7\u1784\u1780\u17b6\u179a\u1796\u17b6\u179a\u1794\u17d2\u179a\u1780\u17cb\u17a2org \u178f\u17b7\u1794org \u1799\u17c4\u178f\u17b7\u1780\u17d4",
            prevention="\u1785\u17b6\u1780\u17cb\u179c\u17c9\u17b6\u1780\u17cb\u179f\u17b6\u17c6\u1784 Fowl Pox \u1793\u17b7\u1784\u1780\u17c6\u1785\u17b6\u178f\u17cb\u179f org \u178f\u17d2\u179c\u1785org org org \u17d4",
            severity="\u1791\u17b6\u1794-\u1798\u1792\u17d2\u1799\u1798",
            is_contagious=True,
            category=cat_skin,
        ),
        "ecoli": Disease(
            name="\u1787\u17c6\u1784\u17ba E. coli (Colibacillosis)",
            description="\u1780\u17b6\u179a\u1786\u17d2\u179b\u1784\u1794\u17b6\u1780\u17cb\u178f\u17c1\u179a\u17b8 E. coli \u1794\u1784\u17d2\u1780\u179a\u179b\u17be\u1780\u179f org \u1793\u17d2\u179b\u17b6\u1780\u17cb \u1793\u17b7\u1784\u179a org \u17c4\u1782\u1797\u17b6\u1796\u1795\u17d2\u179f\u17c1\u1784\u17d7\u17d4",
            treatment="\u1794\u17d2\u179a\u17be\u1790\u17d2\u1793\u17b6\u17c6 antibiotic \u178f\u17b6\u1798\u179b\u1791\u17d2\u1792\u1795\u179b\u1796\u17b7\u179f\u17c4\u1792\u1793\u17cd \u1793\u17b7\u1784\u1780\u17c2\u179b\u17c6\u17a2\u1780org \u179a\u1794org \u179a\u17b7\u179f org \u1791\u17d2\u1792\u17d4",
            prevention="\u179a\u1780\u17d2\u179f\u17b6 biosecurity \u1793\u17b7\u1784\u1791\u17b9\u1780\u179f\u17d2\u17a2\u17b6\u178f\u17d4",
            severity="\u1798\u1792\u17d2\u1799\u1798-\u1781\u17d2\u1796\u179f\u17cb",
            is_contagious=False,
            category=cat_bact,
        ),
        "mycoplasmosis": Disease(
            name="\u1787\u17c6\u1784\u17ba Mycoplasmosis (CRD)",
            description="\u1787\u17c6\u1784\u17ba\u178a\u1784\u17d2\u17a0\u17be\u1798\u179a org \u17c6\u17a0org \u17be\u1784 (Mycoplasma gallisepticum) \u1794\u1784\u17d2\u1780\u1780\u17d2\u17a2\u1780\u179a org \u17c6\u17a0org \u17be\u1784\u17d4",
            treatment="\u1794\u17d2\u179a\u17be\u1790\u17d2\u1793\u17b6\u17c6 antibiotic (tylosin, enrofloxacin) \u1793\u17b7\u1784\u179a\u1780\u17d2\u179f\u17b6\u1780org \u1793\u17d2\u179b org \u17c2\u1784\u17d4",
            prevention="\u1791\u17b7\u1789\u1798\u17b6\u1793\u17cb\u1796\u17b8\u1794org \u179a\u17b7org \u178forg  \u179f\u17bb\u1791org \u17d2\u1792 \u1793\u17b7\u1784\u179a\u1780org \u179f\u17b6org  biosecurity\u17d4",
            severity="\u1798\u1792\u17d2\u1799\u1798",
            is_contagious=True,
            category=cat_resp,
        ),
        "aspergillosis": Disease(
            name="\u1787\u17c6\u1784\u17ba Aspergillosis",
            description="\u1787\u17c6\u1784\u17ba\u1795\u17b8\u178f (Aspergillus) \u1794\u17c9\u17a0\u17a0\u1796\u17b6\u179b\u17cb\u179f org \u17bd\u178f \u1793\u17b7\u1784\u1794\u17d2\u179a\u1796org \u17d0\u1793\u17d2\u1792\u178a\u1784\u17d2\u17a0\u17be\u1798\u17d4",
            treatment="\u1780\u17c2\u179b org \u17c6\u17a2\u179c org \u1793\u17d2\u178f\u17b6org  \u178a org \u1780org \u17cb\u17a1org \u17c4\u1799\u178a org \u17c4\u1799\u17a1\u17c2\u1780 \u1793\u17b7\u1784\u1794org \u17d2\u179a\u17be antifungal\u17d4",
            prevention="\u179a\u1780\u17d2\u179f\u17b6\u1780\u1793\u17d2\u179b\u17c2\u1784\u179f\u17d2\u17a2\u17b6\u178f \u1787\u17c0\u179f\u179c\u17b6\u1784\u178a org \u17b8\u179f org \u17d2\u179a org \u17b6\u17c6 \u1793\u17b7\u1784\u179c org \u1793\u17d2org \u178f\u17b7\u179b\u17b6\u178f\u17d4",
            severity="\u1798\u1792\u17d2\u1799\u1798",
            is_contagious=False,
            category=cat_resp,
        ),
    }
    db.session.add_all(diseases.values())
    db.session.flush()

    # Rules (12)
    rules = [
        Rule(
            title="Infectious Bronchitis",
            description="\u1780\u17d2\u17a2\u1780 + \u1780\u178e\u17d2\u178f\u17b6\u179f\u17cb + \u17a0\u17bc\u179a\u1785\u17d2\u179a\u1798\u17bb\u17a0 + \u1796\u1784\u1792\u17d2\u179b\u17b6\u1780\u17cb",
            priority=1,
            confidence=85.0,
            disease=diseases["infectious_bronchitis"],
            symptoms=[symptoms["coughing"], symptoms["sneezing"], symptoms["nasal_discharge"], symptoms["drop_egg"]],
        ),
        Rule(
            title="Newcastle Disease",
            description="\u1780\u17d2\u17a2\u1780 + \u17a0\u17bc\u179a\u1785\u17d2\u179a\u1798\u17bb\u17a0 + \u17a2\u179f\u1780\u1798\u17d2\u1798 + \u1780\u1794\u178f\u17cb\u1798\u17bb\u1781",
            priority=1,
            confidence=82.0,
            disease=diseases["newcastle"],
            symptoms=[symptoms["coughing"], symptoms["nasal_discharge"], symptoms["lethargy"], symptoms["twisted_neck"]],
        ),
        Rule(
            title="Coccidiosis",
            description="\u179a\u17b6\u1780\u1798\u17b6\u1793\u1788\u17b6\u1798 + \u17a2\u179f\u1780\u1798\u17d2\u1798 + \u1781\u17d2\u179c\u17a0\u1791\u17b9\u1780",
            priority=1,
            confidence=90.0,
            disease=diseases["coccidiosis"],
            symptoms=[symptoms["bloody_diarrhea"], symptoms["lethargy"], symptoms["dehydration"]],
        ),
        Rule(
            title="Fowl Cholera",
            description="\u1798\u17bb\u1781\u179a\u179b\u17be\u1780 + \u17a2\u179f\u1780\u1798\u17d2\u1798 + \u179a\u17c4\u1798\u179a\u17bd\u1789 + \u179f\u17d2\u179b\u17b6\u1794\u17cb\u1797\u17d2\u179b\u17b6\u1798\u17d7",
            priority=1,
            confidence=80.0,
            disease=diseases["fowl_cholera"],
            symptoms=[symptoms["swollen_face"], symptoms["lethargy"], symptoms["ruffled"], symptoms["sudden_death"]],
        ),
        Rule(
            title="Marek Disease",
            description="\u1796\u17b7\u1780\u179b\u1797\u17d2\u1793\u17c2\u1793 + \u17a2\u179f\u1780\u1798\u17d2\u1798 + \u179f\u17d2\u1782\u1798",
            priority=2,
            confidence=76.0,
            disease=diseases["marek"],
            symptoms=[symptoms["lameness"], symptoms["lethargy"], symptoms["weight_loss"]],
        ),
        Rule(
            title="Avian Influenza",
            description="\u1780\u17d2\u17a2\u1780 + \u17a2\u179f\u1780\u1798\u17d2\u1798 + \u1794\u17b6\u178f\u17cb\u1794\u1784\u17cb\u1785\u17c6\u178e\u1784\u17cb\u17a2\u17b6\u17a0\u17b6\u179a + \u1797\u17d2\u1793\u17c2\u1780\u17a0\u17bc\u179a\u1791\u17b9\u1780 + \u1780\u17c6\u1794\u17d2\u17b7\u178f\u179f\u17d2\u179a\u17a2\u17b6\u1794\u17cb",
            priority=1,
            confidence=88.0,
            disease=diseases["avian_influenza"],
            symptoms=[symptoms["coughing"], symptoms["lethargy"], symptoms["loss_appetite"], symptoms["watery_eyes"], symptoms["bluish_comb"]],
        ),
        Rule(
            title="Gumboro (IBD)",
            description="\u179a\u17b6\u1780\u1796\u178e\u17cc\u179f + \u17a2\u179f\u1780\u1798\u17d2\u1798 + \u1781\u17d2\u179c\u17a0\u1791\u17b9\u1780 + \u179a\u17c4\u1798\u179a\u17bd\u1789",
            priority=1,
            confidence=83.0,
            disease=diseases["infectious_bursal"],
            symptoms=[symptoms["white_diarrhea"], symptoms["lethargy"], symptoms["dehydration"], symptoms["ruffled"]],
        ),
        Rule(
            title="Fowl Pox",
            description="\u179a\u1794\u17bd\u179f\u179f\u17d2\u1794\u17c2\u1780 + \u1780\u1793\u17d2\u1791\u1780\u17cb\u179f\u17d2\u1794\u17c2\u1780 + \u1794\u17b6\u178f\u17cb\u1794\u1784\u17cb\u1785\u17c6\u178e\u1784\u17cb\u17a2\u17b6\u17a0\u17b6\u179a",
            priority=2,
            confidence=82.0,
            disease=diseases["fowl_pox"],
            symptoms=[symptoms["skin_lesions"], symptoms["scabs"], symptoms["loss_appetite"]],
        ),
        Rule(
            title="E. coli Infection",
            description="\u179a\u17b6\u1780\u1796\u178e\u17cc\u1794\u17c3\u178f\u1784 + \u17a2\u179f\u1780\u1798\u17d2\u1798 + \u179a\u17c4\u1798\u179a\u17bd\u1789 + \u1798\u17bb\u1781\u179a\u179b\u17be\u1780",
            priority=2,
            confidence=75.0,
            disease=diseases["ecoli"],
            symptoms=[symptoms["green_diarrhea"], symptoms["lethargy"], symptoms["ruffled"], symptoms["swollen_face"]],
        ),
        Rule(
            title="Mycoplasmosis (CRD)",
            description="\u1780\u17d2\u17a2\u1780 + \u1780\u178e\u17d2\u178f\u17b6\u179f\u17cb + \u179a\u179b\u17be\u1780 sinus + \u1797\u17d2\u1793\u17c2\u1780\u17a0\u17bc\u179a\u1791\u17b9\u1780",
            priority=2,
            confidence=80.0,
            disease=diseases["mycoplasmosis"],
            symptoms=[symptoms["coughing"], symptoms["sneezing"], symptoms["swollen_sinus"], symptoms["watery_eyes"]],
        ),
        Rule(
            title="Aspergillosis",
            description="\u178a\u1780\u178a\u1784\u17d2\u17a0\u17be\u1798\u1796\u17b7\u1794\u17b6\u1780 + \u17a2\u179f\u1780\u1798\u17d2\u1798 + \u179f\u17d2\u1782\u1798",
            priority=3,
            confidence=72.0,
            disease=diseases["aspergillosis"],
            symptoms=[symptoms["gasping"], symptoms["lethargy"], symptoms["weight_loss"]],
        ),
        Rule(
            title="Newcastle (Neurological)",
            description="\u1780\u17d2\u1794\u17b6\u179b\u179c\u17c1\u179a + \u1789\u17b6\u1780\u17cb + \u1796\u17b7\u1780\u179b\u1797\u17d2\u1793\u17c2\u1793 + \u179a\u17b6\u1780\u1796\u178e\u17cc\u1794\u17c3\u178f\u1784",
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


def seed_all():
    seed_permissions_and_roles()
    seed_admin_user()
    seed_expert_data()
