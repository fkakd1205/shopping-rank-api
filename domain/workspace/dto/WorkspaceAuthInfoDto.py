from dataclasses import dataclass

@dataclass
class WorkspaceAuthInfoDto():
    workspaceMemberId = None
    templateUseYn = None
    isMaster = None
    workspaceAuthItems = None
    workspaceId = None
    subscriptionPlan = None
    subscriptionExpiryDate = None
    accessibleSubscriptionPlans = None

    def __init__(self, res):
        self.workspaceMemberId = res.get('workspaceMemberId')
        self.templateUseYn = res.get('templateUseYn')
        self.isMaster = res.get('master')
        self.workspaceAuthItems = list(map(lambda item: WorkspaceAuthInfoDto.WorkspaceAuthItem(item), res.get('workspaceAuthItems')))
        self.workspaceId = res.get('workspaceId')
        self.subscriptionPlan = res.get('subscriptionPlan')
        self.subscriptionExpiryDate = res.get('subscriptionExpiryDate')
        self.accessibleSubscriptionPlans = res.get('accessibleSubscriptionPlans')

    class WorkspaceAuthItem():
        def __init__(self, item):
            self.code = item.get('code')
            self.essential_yn = item.get('essentialYn')
