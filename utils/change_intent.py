from rasa.nlu.components import Component


class ChangeIntent(Component):
    supported_language_list = ["zh"]

    # print("enter SortIntent Component")

    def __init__(self, component_config=None):
        super(ChangeIntent, self).__init__(component_config)

    def process(self, message, **kwargs):
        if message.get('text') and message.get('intent'):
            # print(message.data)
            # print(message.get('text'))
            # print(message.get('intent'))
            intent = message.get('intent')
            # message.set('intent', {'id': intent['id'], 'name': 'goodbye', 'confidence': 1.0})
