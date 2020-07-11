import os
from flask_admin import Admin, BaseView, expose
from models import db, Enterprise, Schedule, Space, Equipment, Spacetype, Brand
from flask_admin.contrib.sqla import ModelView


class MyModelView(ModelView):
    column_display_pk = True

class MyModelViewActive(MyModelView):
    def get_query(self):
        return self.session.query(self.model).filter(self.model.is_active==True)

    def delete_model(self, model):
        try:
            self.on_model_delete(model)            
            model.is_active = False
            #brands = Brand.query.filter_by(enterprise_id=model.id)
            #brands = list(map(lambda x: x.serialize(), brands))
            #for x in brands:
            #    x['is_active']=False            
            db.session.commit()
        except Exception as ex:
            if not self.handle_view_exception(ex):
                flash(gettext('Failed to delete record. %(error)s', error=str(ex)), 'error')
                log.exception('Failed to delete record.')
            self.session.rollback()
            return False
        else:
            self.after_model_delete(model)
        return True

class MyModelViewNotActive(MyModelView):
    def get_query(self):        
        return self.session.query(self.model).filter(self.model.is_active==False)

class MyModelViewBrands(MyModelView):
    def get_query(self):
        brand = self.session.query(self.model)
        brand = list(map(lambda x: x.serialize(), brand))
        enterprise = Enterprise.query.get(brand[0]['enterpriseID'])               
        return self.session.query(self.model).filter(enterprise.is_active==True)
        
def setup_admin(app):
    app.secret_key = os.environ.get('FLASK_APP_KEY', 'sample key')
    app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'
    admin = Admin(app, name='Admin', template_mode='bootstrap3')


    admin.add_view(MyModelViewActive(Enterprise, db.session, endpoint='Active_Enterprise', menu_icon_type='glyph', menu_icon_value='glyphicon-user'))
    admin.add_view(MyModelViewBrands(Brand, db.session, menu_icon_type='glyph', menu_icon_value='glyphicon-briefcase'))
    admin.add_view(MyModelView(Schedule, db.session, menu_icon_type='glyph', menu_icon_value='glyphicon-list-alt'))
    admin.add_view(MyModelView(Equipment, db.session, menu_icon_type='glyph', menu_icon_value='glyphicon-wrench'))
    admin.add_view(MyModelView(Space, db.session))       
    admin.add_view(MyModelView(Spacetype, db.session))    
    admin.add_view(MyModelViewNotActive(Enterprise, db.session, "Inactive Enterprise", endpoint='Enterprise_not_active', menu_icon_type='glyph', menu_icon_value='glyphicon-alert'))
