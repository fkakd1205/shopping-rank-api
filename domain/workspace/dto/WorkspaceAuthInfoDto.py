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

    def __init__(self, res):
        self.workspaceMemberId = res['workspaceMemberId']
        self.templateUseYn = res['templateUseYn']
        self.isMaster = res['master']
        self.workspaceAuthItems = list(map(lambda item: WorkspaceAuthInfoDto.WorkspaceAuthItem(item), res['workspaceAuthItems']))
        self.workspaceId = res['workspaceId']
        self.subscriptionPlan = res['subscriptionPlan']
        self.subscriptionExpiryDate = res['subscriptionExpiryDate']

    class WorkspaceAuthItem():
        def __init__(self, item):
            self.code = item['code']
            self.essential_yn = item['essentialYn']
