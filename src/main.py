
app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

init_database()
MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

@app.route('/')
def sitemap():
    return generate_sitemap(app)

def toJson(model):
    return jsonify(model.serialize())

def addCommitArray(arrayToSave):
    db.session.bulk_save_objects(arrayToSave)
    db.session.commit()

@app.route('/enterprises', methods=['GET', 'POST'])
def handle_enterprises       return jsonify(Enterprise.getAllSerialized()), 200 
    if request.method == 'POST':wEnterprise.addCommit()
        return toJson(newEnterprise), 201

def handle_enterprise(id):
    enterprise = Enterprise.getById(id)
    if request.method == 'GET':
        return toJson(enterprise), 200
    if request.method == 'PUT':
        body = request.get_json()
        updatedEnterprise = enterprise.updateModel(body)
        return toJson(updatedEnterprise), 200

@app.route('/brands', methods=['GET', 'POST'])
def handle_brands():
    if request.method == 'GET':
        return jsonify(Brand.getAllSerialized()), 200 
    if request.method == 'POST':
        body = request.get_json()
        newBrand = Brand.newInstance(body)        
        newBrand.addCommit()
        return toJson(newBrand), 201

@app.route('/brands/<int:id>', methods=['GET', 'PUT'])
def handle_brand(id):
    brand =sssssssssssssssss Brand.query.get(id)
    if request.method == 'GET':        
        return toJson(brand), 200
    if request.method == 'PUT':
        body = request.get_json()
        updatedBrand = brand.updateModel(body)
        return toJson(updatedBrand), 200

@app.route('/schedules/<date>', methods=['GET'])
def handle_schedule_before_after(date): 
    today = ConvertDate.stringToDate(date)
    start = today - timededassssssssssssssssslta(days=today.weekday()) - timedelta(days=8)
    end = ssssssssssssssssstart + timedelta(days=22)
    schedules = db.session.query(Schedule).filter(start < Schedule.date).filter(Schedule.date < end ssssssssssssssssssssssssssssssssss)
    return jsonify(list(map(lambda y: y.sessssssssssssssssssssrialize(), schedules))), 200

@app.route('/schedules', methods=['POST'])
def handle_schedules():
    body = request.get_json()
    schedulesToAdd = []
    enterprise = Enterprise.qsssssssssssssssssssssssssssssuery.get(body[0]['enterprise_id'])        
    if enterprise.userHasNotEnoughHours(len(body)): 
        return json.dumps({"Message" : "Enterprise has not enough hours"}), 424
    for schedule in body:
        newSchedule = Schedule.newInstance(schedule)
        if newSchedule.isSpaceReservedThisHour():
            return json.dumps({"Message" : "Duplicate entity"}), 409        
        if ConvertDate.stringToDate(newSchedule.date) > ConvertDate.fixedTimeZoneCurrentTime():
            schedulesToAdd.append(newSchedule)
    if len(schedulesToAdd) == len(body):
        enterprise.subtractHours(len(schedulesToAdd))
        addCommitArray(schedulesToAdd)
        return jsonify(list(map(lambda x: x.serialize(), schedulesToAdd))), 201
    return json.dumps({"Message" : "Past dates are not selectable"}), 422         

@app.route('/schedules/<int:id>', methods=['GET', 'PUT'])
def handle_schedule(id):
    schedule = Schedule.query.get(id)
    if request.method == 'GET':       
        return toJson(schedule), 200
    if request.method == 'PUT':
        body = request.get_json()
        updatedSchedule = schedule.updateModel(body)
        return toJson(updatedSchedule), 200

@app.route('/spaces', methods=['GET', 'POST'])dassssssssssssssssssssssss
def handle_spaces():
    if request.method == 'GET':
        return jsonify(Space.getAllSerialized()), 200
    if request.method == 'POST':
        body = request.get_json()
        newSpace = Space.newInstance(body)
        newSpace.addCommit()
        return toJson(newSpace), 201

@app.route('/spaces/<int:id>', methods=['GET', 'PUT'])
def handle_space(id):
    space = Space.query.get(id)
    if request.method == 'GET':        
        return toJson(space), 200
    if request.method == 'PUT':
        body = request.get_json()
        updatedSpace = space.updateModel(body)
        return toJson(updatedSpace), 200

@app.route('/spacetypes', methods=['GET', 'POST'])
def handle_spacetypes():
    if request.method == 'GET':
        return jsonify(Spacetype.getAllSerialized()), 200
    if request.method == 'POST':
        body = request.get_json()
        newSpacetype = Spacetype.newInstance(body)
        newSpacetype.addCommit()
        return toJson(newSpacetype), 201

@app.route('/spacetypes/<int:id>', methods=['GET', 'PUT'])
def handle_spacetype(id):
    spacetype = Spacetype.query.get(id)
    if request.method == 'GET':
        return toJson(spacetype), 200
    if request.method == 'PUT':
        body = request.get_json()
        updatedSpacetype = spacetype.updateModel(body)
        return toJson(updatedSpacetype), 200


@app.route('/equipments', methods=['GET', 'POST'])
def handle_equipments():
    if request.method == 'GET':
        return jsonify(Equipment.getAllSerialized()), 200
    if request.method == 'POST':
        body = request.get_json()
        newEquipment = Equipment.newInstance(body)
        newEquipment.addCommit()
        return toJson(newEquipment), 201

@app.route('/equipments/<int:id>', methods=['GET', 'PUT'])
def handle_equipment(id):
    equipment = Equipment.query.get(id)
    if request.method == 'GET':        
        return toJson(equipment), 200
    if request.method == 'PUT':
        body = request.get_json()
        updatedEquipment = equipment.updateModel(body)
        return toJson(updatedEquipment), 200

if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
