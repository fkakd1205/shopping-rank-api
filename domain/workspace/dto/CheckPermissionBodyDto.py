class CheckPermissionBodyDto():
    def __init__(self, type):
        self.checkMasterPermissionFlag = type.get('checkMasterPermissionFlag', False)
        self.checkAccessTypeFlag = type.get('checkAccessTypeFlag', False)
        self.checkSubscriptionPlanFlag = type.get('checkSubscriptionPlanFlag', False)
        self.requiredAccessTypes = list(map(lambda type: type.value, type['requiredAccessTypes'])) if 'requiredAccessTypes' in type else []
        self.requiredSubscriptionPlans = list(map(lambda plan: plan.value, type['requiredSubscriptionPlans'])) if 'requiredSubscriptionPlans' in type else []
