class WorkspaceAuthInfoDto():
    def __init__(self):
        self.workspace_member_id = None
        self.template_use_yn = None
        self.is_master = None
        self.workspace_auth_items = None
        self.workspace_id = None
        self.subscription_plan = None
        self.subscription_expiry_date = None

    class WorkspaceAuthItem():
        def __init__(self, item):
            self.code = item['code']
            self.essential_yn = item['essentialYn']
