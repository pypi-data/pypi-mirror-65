from kubernetes import client, config
import json
from kubernetes.client.rest import ApiException

config.load_kube_config()
api = client.CustomObjectsApi()


class FlowData:
    def __init__(self):
        self.obj_name = ""
        self.group = ""
        self.version = ""
        self.namespace = ""
        self.plural = ""

    def get(self, path):
        parsed_path = parse_path(path)
        try:
            obj = api.get_namespaced_custom_object(self.group, self.version, self.namespace, self.plural, self.obj_name)
            flow_data = json.loads(obj["spec"]["flowData"])
            if not parsed_path:
                return flow_data
            return flow_data[parsed_path]
        except ApiException as e:
            status = e.status
            reason = e.reason
            reason = "Failed to get value of path {0} from flow data.\n Reason: ".format(path, reason)
            raise FlowDataException(status=status, reason=reason)
        except Exception as e:
            reason = "Failed to get value of path {0} from flow data.\n Reason: ".format(path, e)
            raise FlowDataException(status=0, reason=reason)

    def set(self, path, value):
        try:
            obj = api.get_namespaced_custom_object(self.group, self.version, self.namespace, self.plural, self.obj_name)
            parsed_path = parse_path(path)
            flow_data = json.loads(obj["spec"]["flowData"])
            if not parsed_path:
                obj["spec"]["flowData"] = json.dumps(value)
            else:
                flow_data[parsed_path] = value
                obj["spec"]["flowData"] = json.dumps(flow_data)
            api_response = api.patch_namespaced_custom_object(self.group, self.version, self.namespace, self.plural, self.obj_name, obj)
        except ApiException as e:
            status = e.status
            reason = e.reason
            reason = "Failed to set value {0} of path {1} from flow data.\n Reason: ".format(path, reason)
            raise FlowDataException(status=status, reason=reason)
        except Exception as e:
            reason = "Failed to set value {0} of path {1} from flow data.\n Reason: ".format(path, e)
            raise FlowDataException(status=0, reason=reason)


def parse_path(path):
    path = path.split(".")
    if path[0] == "$":
        path = path[1:]
    return ".".join(path)


class FlowDataException(Exception):

    def __init__(self, status=None, reason=None):
        self.status = status
        self.reason = reason

    def __str__(self):
        error_message = "Reason: {0}\n".format(self.reason)
        return error_message
