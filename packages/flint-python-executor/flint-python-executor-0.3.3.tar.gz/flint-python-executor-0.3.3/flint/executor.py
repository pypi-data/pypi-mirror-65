from flask import Flask, request, jsonify
from handler.handler_helper import Handler
from handler.flow_data import FlowDataException
import socket

application = Flask(__name__)
global_workflows = {}


class App:

    def __init__(self):
        pass

    def register_workflows(self, workflows):
        global global_workflows
        global_workflows = workflows

    @staticmethod
    @application.route('/execute')
    def execute():
        missing_args = []
        step = request.args.get('step', default=None)
        workflow = request.args.get('workflow', default=None)
        obj_name = request.args.get('obj_name', default=None)
        group = request.args.get('group', default=None)
        version = request.args.get('version', default=None)
        resource = request.args.get('resource', default=None)
        namespace = request.args.get('namespace', default=None)
        if step is None:
            missing_args.append("step")
        if workflow is None:
            missing_args.append("workflow")
        if obj_name is None:
            missing_args.append("workflow")
        if group is None:
            missing_args.append("group")
        if version is None:
            missing_args.append("version")
        if resource is None:
            missing_args.append("resource")
        if namespace is None:
            missing_args.append("namespace")
        if len(missing_args) > 0:
            message = "Flint Python Executor API Missing params: {}".format(', '.join(missing_args))
            response = {
                "message": message,
                "status": "failure"
            }
        else:
            handler_instance = Handler()
            handler_instance.flow_data.obj_name = obj_name
            handler_instance.flow_data.group = group
            handler_instance.flow_data.version = version
            handler_instance.flow_data.namespace = namespace
            handler_instance.flow_data.plural = resource
            try:
                global_workflows[workflow][step](handler_instance)
                response = {
                    "message": "",
                    "status": "success"
                }
            except FlowDataException as e:
                response = {
                    "message": e.reason,
                    "status": "failure"
                }
            except Exception as err:
                response = {
                    "message": repr(err),
                    "status": "failure"
                }
        return jsonify(response)

    @staticmethod
    def start():
        try:
            port = select_port()
            write_port_to_file(port)
            application.run(host='0.0.0.0', port=port)
        except ExecutorException as e:
            raise ExecutorException(status=e.status, reason=e.reason)
        except Exception as e:
            print(e)
            raise ExecutorException(status=0, reason="Failed to start python executor api service")


def create_app():
    return App()


def is_port_in_use(port):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            return s.connect_ex(('localhost', port)) == 0
    except Exception as e:
        print(e)
        raise ExecutorException(status=0, reason="Failed to check available Port")


def select_port():
    port = 8080
    while True:
        if is_port_in_use(port):
            port += 1
            if port > 8180:
                raise ExecutorException(status=0, reason="Failed to find available Port between 8080 and 8180")
        else:
            break
    return port


# todo change to working dir when deploy
def write_port_to_file(port):
    file_path = '/tmp/flint_python_executor_port'
    try:
        with open(file_path,  'w') as writer:
            writer.write(str(port))
    except Exception as e:
        print(e)
        raise ExecutorException(status=0, reason="Failed to write port to file {0}".format(file_path))


class ExecutorException(Exception):

    def __init__(self, status=None, reason=None):
        self.status = status
        self.reason = reason

    def __str__(self):
        error_message = "Reason: {0}\n".format(self.reason)
        return error_message
