from app.problematicCase import bp

@bp.route('/')
def get():
    pass

@bp.route('/<id>')
def get_id():
    pass

@bp.route('/add')
def add():
    pass

@bp.route('/edit')
def edit():
    pass

@bp.route('/correctToNotPaid')
def correctToNotPaid():
    pass

@bp.route('/correctToNotVerified')
def correctToNotVerified():
    pass