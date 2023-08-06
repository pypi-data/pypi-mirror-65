from handler.flow_data import FlowData
from handler.model import Model


class Handler:
    def __init__(self):
        self.flow_data = FlowData()
        self.model = Model()


if __name__ == "__main__":
    print(Handler().flow_data.obj_name)
