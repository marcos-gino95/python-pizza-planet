from flask import jsonify


def __response(entity, error):
    response = entity if not error else {"error": error}
    status_code = 200 if not error else 400
    return jsonify(response), status_code


def create_service(controller, request):
    entity, error = controller.create(request.json)
    return __response(entity, error)


def update_service(controller, request):
    entity, error = controller.update(request.json)
    return __response(entity, error)


def get_all(controller):
    entities, error = controller.get_all()
    return __response(entities, error)


def get_by_id(controller, _id):
    entity, error = controller.get_by_id(_id)
    return __response(entity, error)
