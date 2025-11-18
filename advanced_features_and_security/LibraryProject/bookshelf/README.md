PERMISSIONS & GROUP SETUP
-------------------------

Custom permissions defined in Book model:
- can_view
- can_create
- can_edit
- can_delete

Groups:
- Viewers → can_view
- Editors → can_view, can_create, can_edit
- Admins → full permissions

Setup command:
python manage.py setup_groups

In views:
Use @permission_required('bookshelf.permission_codename', raise_exception=True)
