from flask_admin.contrib.sqla import ModelView


class UserView(ModelView):
    """
    This class is responsible for managing the settings for create, update, and delete of user Profiles admin view.
    """
    can_create = True
    can_edit = True
    can_delete = True
    can_export = True
    create_modal = True
    edit_modal = True
    column_hide_backrefs = False
