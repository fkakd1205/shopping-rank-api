from enum import Enum

class WorkspaceAccessTypeEnum(Enum):
    MARGIN_CALC_SEARCH = "MARGIN_CALC_SEARCH"
    MARGIN_CALC_CREATE = "MARGIN_CALC_CREATE"
    MARGIN_CALC_UPDATE = "MARGIN_CALC_UPDATE"
    MARGIN_CALC_DELETE = "MARGIN_CALC_DELETE"
    EXCEL_TRANS_SEARCH = "EXCEL_TRANS_SEARCH"
    EXCEL_TRANS_CREATE = "EXCEL_TRANS_CREATE"
    EXCEL_TRANS_UPDATE = "EXCEL_TRANS_UPDATE"
    EXCEL_TRANS_DELETE = "EXCEL_TRANS_DELETE"
    PRODUCT_MANAGE_SEARCH = "PRODUCT_MANAGE_SEARCH"
    PRODUCT_MANAGE_CREATE = "PRODUCT_MANAGE_CREATE"
    PRODUCT_MANAGE_UPDATE = "PRODUCT_MANAGE_UPDATE"
    PRODUCT_MANAGE_DELETE = "PRODUCT_MANAGE_DELETE"
    INVENTORY_MANAGE_SEARCH = "INVENTORY_MANAGE_SEARCH"
    INVENTORY_MANAGE_CREATE = "INVENTORY_MANAGE_CREATE"
    INVENTORY_MANAGE_UPDATE = "INVENTORY_MANAGE_UPDATE"
    INVENTORY_MANAGE_DELETE = "INVENTORY_MANAGE_DELETE"
    OMS_SEARCH = "OMS_SEARCH"
    OMS_CREATE = "OMS_CREATE"
    OMS_UPDATE = "OMS_UPDATE"
    OMS_DELETE = "OMS_DELETE"
    SALES_ANALYSIS_SEARCH = "SALES_ANALYSIS_SEARCH"

    STORE_RANK_SEARCH = "STORE_RANK_SEARCH"
    STORE_RANK_CREATE = "STORE_RANK_CREATE"
    STORE_RANK_UPDATE = "STORE_RANK_UPDATE"
    STORE_RANK_DELETE = "STORE_RANK_DELETE"
