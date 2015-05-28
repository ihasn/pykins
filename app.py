#!flask/bin/python
from flask import Flask, jsonify, abort, make_response, request, url_for
import psutil, platform

app = Flask(__name__)

@app.route('/pykins/api/v1.0/status', methods=['GET'])
def get_status():
    return jsonify({'status': True})

@app.route('/pykins/api/v1.0/health', methods=['GET'])
def get_health():
    if platform.system() == 'Linux':
        health = jsonify({ 'cpu_percent': psutil.cpu_percent(),
                        'memory_percent': psutil.virtual_memory().percent,
                        'disk_usage': psutil.disk_usage('/').percent })
    else:
        health = jsonify({ 'cpu_percent': psutil.cpu_percent(),
                        'memory_percent': psutil.virtual_memory().percent})
    return health

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

@app.route('/pykins/api/v1.0/tasks', methods=['POST'])
def create_task():
    if not request.json or not 'title' in request.json:
        abort(400)
    task = {
        'id': tasks[-1]['id'] + 1,
        'title': request.json['title'],
        'description': request.json.get('description', ""),
        'status': False
    }
    tasks.append(task)
    return jsonify({'task': task}), 201

@app.route('/pykins/api/v1.0/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    task = [task for task in tasks if task['id'] == task_id]
    if len(task) == 0:
        abort(404)
    if not request.json:
        abort(400)
    if 'title' in request.json and type(request.json['title']) != unicode:
        abort(400)
    if 'description' in request.json and type(request.json['description']) is not unicode:
        abort(400)
    if 'status' in request.json and type(request.json['status']) is not bool:
        abort(400)
    task[0]['title'] = request.json.get('title', task[0]['title'])
    task[0]['description'] = request.json.get('description', task[0]['description'])
    task[0]['status'] = request.json.get('status', task[0]['status'])
    return jsonify({'task': task[0]})

@app.route('/pykins/api/v1.0/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    task = [task for task in tasks if task['id'] == task_id]
    if len(task) == 0:
        abort(404)
    tasks.remove(task[0])
    return jsonify({'result': True})

if __name__ == '__main__':
    app.run(debug=True)