from flask import request
import uuid

from domain.nrank_record_category.repository.NRankRecordCategoryRepository import NRankRecordCategoryRepository
from domain.nrank_record_category.dto.NRankRecordCategoryDto import NRankRecordCategoryDto
from domain.nrank_record_category.model.NRankRecordCategoryModel import NRankRecordCategoryModel

from decorators import *
from utils import *
from exception.types.CustomException import *

class NRankRecordCategoryService():

    @transactional(read_only=True)
    def check_duplication(self, model):
        nrankRecordCategoryRepository = NRankRecordCategoryRepository()
        saved_model = nrankRecordCategoryRepository.search_one_by_name(model.name, model.workspace_id)
        if(saved_model):
            raise CustomDuplicationException("이미 등록된 데이터입니다.")
    
    @transactional()
    def create_one(self):
        nrankRecordCategoryRepository = NRankRecordCategoryRepository()
        memberPermissionUtils = MemberPermissionUtils()

        body = request.get_json()
        workspace_info = memberPermissionUtils.get_workspace_info()
        category_name = body.get('name', '').strip()

        dto = NRankRecordCategoryDto()
        dto.id = uuid.uuid4()
        dto.name = category_name
        dto.created_at = DateTimeUtils.get_current_datetime()
        dto.created_by_member_id = workspace_info.workspaceMemberId
        dto.deleted_flag = False
        dto.workspace_id = workspace_info.workspaceId

        new_model = NRankRecordCategoryModel.to_model(dto)
        self.check_format(new_model)
        self.check_duplication(new_model)
        nrankRecordCategoryRepository.save(new_model)

    def check_format(self, model):
        if(model.name == ''):
            raise CustomNotMatchedFormatException("카테고리명은 공백이 불가능합니다.")
    
        if(len(model.name) > 20):
            raise CustomNotMatchedFormatException("카테고리명은 20글자 이하로 입력해주세요.")
        
    @transactional(read_only=True)
    def search_list(self):
        nRankRecordCategoryRepository = NRankRecordCategoryRepository()
        memberPermissionUtils = MemberPermissionUtils()

        workspace_info = memberPermissionUtils.get_workspace_info()
        models = nRankRecordCategoryRepository.search_list_by_workspace_id(workspace_info.workspaceId)
        dtos = list(map(lambda model: NRankRecordCategoryDto.to_dto(model), models))
        return dtos
    
    @transactional()
    def update_one(self, id):
        nRankRecordCategoryRepository = NRankRecordCategoryRepository()
        
        model = nRankRecordCategoryRepository.search_one(id)
        if(model is None): raise CustomNotFoundException("데이터가 존재하지 않습니다.")

        body = request.get_json()
        model.name = body['name']
        model.updated_at = DateTimeUtils.get_current_datetime()
   
        self.check_format(model)
        self.check_duplication(model)

    @transactional()
    def delete_one(self, id):
        """delete nrank record category
        
        - delete nrank record category
        - update related nrank record (nrank_record_category_id)
        """
        nRankRecordCategoryRepository = NRankRecordCategoryRepository()
        nRankRecordCategoryRepository.soft_delete_one_and_related_all(id)
    