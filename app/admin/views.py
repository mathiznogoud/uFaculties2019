from flask import abort, flash, redirect, render_template, url_for, request
from flask_login import current_user, login_required
from . import admin
from .forms import DepartmentForm, RoleForm, UserAssignForm, UserEditForm, DepartmentSearchFilter
from .. import db, mysql
from ..models import Department, Role, User


from flask import abort, flash, redirect, render_template, url_for
from flask_login import current_user, login_required


def check_admin():
    """
    Prevent non-admins from accessing the page
    """
    if not current_user.is_admin:
        abort(403)

# Department Views


@admin.route('/departments', methods=['GET', 'POST'])
@login_required

def list_departments():
    """
    List all departments
    """
    check_admin()
    form = DepartmentSearchFilter()
    departments = Department.query.order_by(Department.address.asc())
    if form.validate_on_submit():
        departments = Department.query.filter_by(depType=form.depType.data)
    return render_template('admin/departments/departments.html',
                           departments=departments, form = form, title="Departments")

@admin.route('/departments/add', methods=['GET', 'POST'])
@login_required
def add_department():
    """
    Add a department to the database
    """
    check_admin()

    add_department = True

    form = DepartmentForm()
    if form.validate_on_submit():
        department = Department(name=form.name.data,
                                code=form.code.data,
                                depType=form.depType.data,
                                address=form.address.data,
                                phone=form.phone.data,
                                website=form.website.data)
        try:
            # add department to the database
            db.session.add(department)
            db.session.commit()
            flash('You have successfully added a new department.')
        except:
            # in case department name already exists
            flash('Error: department name already exists.')

        # redirect to departments page
        return redirect(url_for('admin.list_departments'))

    # load department template
    return render_template('admin/departments/department.html', action="Add",
                           add_department=add_department, form=form,
                           title="Add Department")


@admin.route('/departments/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_department(id):
    """
    Edit a department
    """
    check_admin()

    add_department = False

    department = Department.query.get_or_404(id)
    form = DepartmentForm(obj=department)
    if form.validate_on_submit():
        department.name = form.name.data
        department.code = form.code.data
        department.depType = form.depType.data
        department.address = form.address.data
        department.phone = form.phone.data
        department.website = form.website.data
        db.session.commit()
        flash('You have successfully edited the department.')

        # redirect to the departments page
        return redirect(url_for('admin.list_departments'))

    return render_template('admin/departments/department.html', action="Edit",
                           add_department=add_department, form=form,
                           department=department, title="Edit Department")


@admin.route('/departments/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_department(id):
    """
    Delete a department from the database
    """
    check_admin()

    department = Department.query.get_or_404(id)
    db.session.delete(department)
    db.session.commit()
    flash('You have successfully deleted the department.')

    # redirect to the departments page
    return redirect(url_for('admin.list_departments'))

#Role views
@admin.route('/roles')
@login_required
def list_roles():
    check_admin()
    """
    List all roles
    """
    roles = Role.query.all()
    return render_template('admin/roles/roles.html',
                           roles=roles, title='Roles')


@admin.route('/roles/add', methods=['GET', 'POST'])
@login_required
def add_role():
    """
    Add a role to the database
    """
    check_admin()

    add_role = True

    form = RoleForm()
    if form.validate_on_submit():
        role = Role(name=form.name.data)
        try:
            # add role to the database
            db.session.add(role)
            db.session.commit()
            flash('You have successfully added a new role.')
        except:
            # in case role name already exists
            flash('Error: role name already exists.')

        # redirect to the roles page
        return redirect(url_for('admin.list_roles'))

    # load role template
    return render_template('admin/roles/role.html', add_role=add_role,
                           form=form, title='Add Role')


@admin.route('/roles/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_role(id):
    """
    Edit a role
    """
    check_admin()

    add_role = False

    role = Role.query.get_or_404(id)
    form = RoleForm(obj=role)
    if form.validate_on_submit():
        role.name = form.name.data
        db.session.add(role)
        db.session.commit()
        flash('You have successfully edited the role.')

        # redirect to the roles page
        return redirect(url_for('admin.list_roles'))

    form.name.data = role.name
    return render_template('admin/roles/role.html', add_role=add_role,
                           form=form, title="Edit Role")


@admin.route('/roles/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_role(id):
    """
    Delete a role from the database
    """
    check_admin()

    role = Role.query.get_or_404(id)
    db.session.delete(role)
    db.session.commit()
    flash('You have successfully deleted the role.')

    # redirect to the roles page
    return redirect(url_for('admin.list_roles'))

    return render_template(title="Delete Role")


#user view
@admin.route('/users')
@login_required
def list_users():
    """
    List all users
    """
    check_admin()
    users = User.query.all()
    
    return render_template('admin/users/users.html',
                           users=users, title='Users')


@admin.route('/users/assign/<int:id>', methods=['GET', 'POST'])
@login_required
def assign_user(id):
    check_admin()

    user = User.query.get_or_404(id)

    # prevent admin from being assigned a department or role
    if user.is_admin:
        abort(403)

    form = UserAssignForm(obj=user)
    if form.validate_on_submit():
        user.role = form.role.data
        user.department = form.department.data
        db.session.add(user)
        db.session.commit()
        flash('You have successfully assigned a department and role.')

        # redirect to the roles page
        return redirect(url_for('admin.list_users'))

    return render_template('admin/users/user.html', user=user, form=form, title='Assign User')

@admin.route('/users/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_user(id):
    """
    Delete a role from the database
    """
    check_admin()

    user = User.query.get_or_404(id)
    db.session.delete(user)
    db.session.commit()
    flash('You have successfully deleted the user.')

    # redirect to the roles page
    return redirect(url_for('admin.list_users'))

    return render_template(title="Delete Role")

@admin.route('/users/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_user(id):
    """
    Edit a user
    """
    check_admin()

    add_user = False

    user = User.query.get_or_404(id)
    form = UserEditForm(obj=user)
    if form.validate_on_submit():
        user.first_name = form.first_name.data
        user.last_name = form.last_name.data
        user.user_code = user.department.code + str(user.id)
        user.username = form.username.data
        user.vnu_email = form.vnu_email.data
        user.degree = form.degree.data
        flash('You have successfully edited the user.')
        db.session.commit()
        # redirect to the departments page
        return redirect(url_for('admin.list_users'))

    return render_template('admin/users/edituser.html', action="Edit",
                           add_user=add_user, form=form,
                           user=user, title="Edit User")
@admin.route('/user/add', methods=['GET', 'POST'])
def add_user():    
    """
    Add a department to the database
    """
    check_admin()

    add_department = True

    form = DepartmentForm()
    if form.validate_on_submit():
        user = User(name=form.name.data,
                                code=form.code.data,
                                depType=form.depType.data,
                                address=form.address.data,
                                phone=form.phone.data,
                                website=form.website.data)
        try:
            # add department to the database
            db.session.add(department)
            db.session.commit()
            flash('You have successfully added a new department.')
        except:
            # in case department name already exists
            flash('Error: department name already exists.')

        # redirect to departments page
        return redirect(url_for('admin.list_departments'))

    # load department template
    return render_template('admin/departments/department.html', action="Add",
                           add_department=add_department, form=form,
                           title="Add Department")