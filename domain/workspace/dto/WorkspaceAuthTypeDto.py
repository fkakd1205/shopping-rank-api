class WorkspaceAuthTypeDto():
    def __init__(self, type):
        self.check_master_permission_flag = type.get('check_master_permission_flag', False)
        self.check_access_type_flag = type.get('check_access_type_flag', False)
        self.check_subscription_plan_flag = type.get('check_subscription_plan_flag', False)
        self.required_access_types = type.get('required_access_types', [])
        self.required_subscription_plans = type.get('required_subscription_plans', [])

    class CamelCase():
        def __init__(self):
            self.checkMasterPermissionFlag = False
            self.checkAccessTypeFlag = False
            self.checkSubscriptionPlanFlag = False
            self.requiredAccessTypes = []
            self.requiredSubscriptionPlans = []
