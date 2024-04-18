from datetime import datetime
from beam_viewer import db


class Beam_Inform (db.Model):
    id=db.Column(db.String(36),primary_key=True)
    upload_filename=db.Column(db.String(36))
    revise_filename=db.Column(db.String(36))
    case_name=db.Column(db.String(140))
    user_id=db.Column(db.String(140))
    save_path=db.Column(db.String(140))
    create_time=db.Column(db.DateTime,default=datetime.now)

    
    def __repr__(self):
        return 'id={},tweet={},create time={},user_id={}'.format(
             self.id,self.body,self.create_time
        )
    def case_name_records_casename(casename):
        own=Beam_Inform.query.filter_by(case_name=casename)
        return own.order_by(Beam_Inform.create_time.desc())
    
    def case_name_records_id(id):
        own=Beam_Inform.query.filter_by(id=id).first()
        return own
    
    def case_name_records():
        own=Beam_Inform.query.all()
        return own
