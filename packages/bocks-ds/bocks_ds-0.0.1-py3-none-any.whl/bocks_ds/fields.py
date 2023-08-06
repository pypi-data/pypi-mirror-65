class Fields:
    def __init__(self, content):
        self.content = self.check(content)
        self.output = self.prepare_output()

    def __str__(self):
        return self.output

    def check(self, content):
        if type(content) == list:
            return content
        raise TypeError('Fields value must be a list')

    def prepare_output(self):
        output = ''
        for entry in self.content:
            if type(entry) == str:
                output += entry + ' '
            elif type(entry) == dict: # expects dict of lists
                output += self.parse_nested_dict(entry)
            else:
                raise TypeError('Field entries must be strings, or dicts containing lists of strings')
        return output

    def parse_nested_dict(self, data):
        output = ''
        for key, value in data.items():
            suboutput = key + ' { '
            for entry in value:
                if type(entry) == dict:
                    suboutput += self.parse_nested_dict(entry)
                else:
                    suboutput += entry + ' '
            output += suboutput + '} '
        return output
