from utils.db.DBUtils import db

class NRankRecordInfoModel(db.Model):
    __tablename__ = 'nrank_record_info'

    cid = db.Column("cid", db.BigInteger, primary_key=True, autoincrement=True)
    id = db.Column("id", db.String(36), unique=True, nullable=False)
    thumbnail_url = db.Column("thumbnail_url", db.String(600), nullable=True)
    created_at = db.Column("created_at", db.DateTime(timezone = True), nullable=True)
    nrank_record_id = db.Column("nrank_record_id", db.String(36), nullable=False)
    # nrank_record_id = db.Column("nrank_record_id", db.String(36), db.ForeignKey("nrank_record.id"), nullable=False)

    def __init__(self):
        self.id = None
        self.thumbnail_url = None
        self.created_at = None
        self.nrank_record_id = None

    @staticmethod
    def to_model(dto):
        model = NRankRecordInfoModel()
        model.id = dto.id
        model.thumbnail_url = dto.thumbnail_url
        model.created_at = dto.created_at
        model.nrank_record_id = dto.nrank_record_id
        return model
