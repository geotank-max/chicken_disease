# app/routes/user_routes.py
from flask import Blueprint, render_template, redirect, url_for, flash, abort
from flask_login import login_required, current_user
from extensions import db
from app.forms.user_forms import(
    UserCreateForm,
    UserEditForm,
    UserConfirmDeleteForm,
)
from app.services.user_service import UserService
from app.services.audit_service import AuditService

# blueprint name define endpoint prefix: tbl_users.*
user_bp = Blueprint("tbl_users", __name__, url_prefix="/users")

@user_bp.route("/")
@login_required
def index():
    # Only users with USER_CREATE permission can view user list
    if not current_user.has_permission("USER_CREATE"):
        abort(403)
        
    users = UserService.get_user_all()
    return render_template("users/index.html", users=users)

@user_bp.route("/profile")
@login_required
def profile():
    return render_template("users/profile.html", user=current_user)

@user_bp.route("/<int:user_id>")
@login_required
def detail(user_id: int):
    # Only users with USER_EDIT permission can view other user details
    if not current_user.has_permission("USER_EDIT") and current_user.id != user_id:
        abort(403)

    user = UserService.get_user_by_id(user_id)
    if user is None:
        abort(404)
    return render_template("users/detail.html", user=user)

@user_bp.route("/create", methods=["GET", "POST"])
@login_required
def create():
    # Only users with USER_CREATE permission can create users
    if not current_user.has_permission("USER_CREATE"):
        abort(403)

    form = UserCreateForm()
    if form.validate_on_submit():
        data = {
            "username": form.username.data,
            "email": form.email.data,
            "full_name": form.full_name.data,
            "is_active": form.is_active.data,
        }
        password = form.password.data
        role_id = form.role_id.data or None
        
        user = UserService.create_user(data, password, role_id)
        AuditService.log("CREATE", "User", user.id, f"Created user: {user.username}")
        flash(f"User '{user.username}' was created successfully.", "success")
        return redirect(url_for("tbl_users.index"))
    
    return render_template("users/create.html", form=form)

@user_bp.route("/<int:user_id>/edit", methods=["GET", "POST"])
@login_required
def edit(user_id: int):
    # Only users with USER_EDIT permission can edit other users; others can only edit themselves
    if not current_user.has_permission("USER_EDIT") and current_user.id != user_id:
        abort(403)

    user = UserService.get_user_by_id(user_id)
    if user is None:
        abort(404)

    is_admin = current_user.has_permission("USER_EDIT")
    form = UserEditForm(original_user=user, obj=user)

    # Non-admins cannot change roles or active status at all
    if not is_admin:
        del form.role_id
        del form.is_active

    if form.validate_on_submit():
        data = {
            "username": form.username.data,
            "email": form.email.data,
            "full_name": form.full_name.data,
            "is_active": form.is_active.data if is_admin else user.is_active,
        }
        password = form.password.data or None

        # Only admin can change role
        role_id = None
        if is_admin:
            role_id = form.role_id.data or None

        UserService.update_user(user, data, password, role_id)
        AuditService.log("UPDATE", "User", user.id, f"Updated user: {user.username}")
        flash(f"User '{user.username}' was updated successfully.", "success")

        if is_admin:
            return redirect(url_for("tbl_users.detail", user_id=user.id))
        else:
            return redirect(url_for("tbl_users.profile"))

    return render_template("users/edit.html", form=form, user=user, is_admin=is_admin)


@user_bp.route("/<int:user_id>/delete", methods=["GET"])
@login_required
def delete_confirm(user_id: int):
    if not current_user.has_permission("USER_DELETE"):
        abort(403)

    # Prevent deleting self
    if current_user.id == user_id:
        flash("You cannot delete your own account.", "danger")
        return redirect(url_for("tbl_users.index"))

    user = UserService.get_user_by_id(user_id)
    if user is None:
        abort(404)
        
    form = UserConfirmDeleteForm()
    return render_template("users/delete_confirm.html", user=user, form=form)


@user_bp.route("/<int:user_id>/delete", methods=["POST"])
@login_required
def delete(user_id: int):
    if not current_user.has_permission("USER_DELETE"):
        abort(403)

    # Prevent deleting self
    if current_user.id == user_id:
        flash("You cannot delete your own account.", "danger")
        return redirect(url_for("tbl_users.index"))

    user = UserService.get_user_by_id(user_id)
    if user is None:
        abort(404)
        
    username = user.username
    UserService.delete_user(user)
    AuditService.log("DELETE", "User", user_id, f"Deleted user: {username}")
    flash("User was deleted successfully.", "success")
    return redirect(url_for("tbl_users.index"))
