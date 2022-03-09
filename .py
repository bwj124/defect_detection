import sys
import yaml


class Ref:
    yaml_tag = u'!Ref:'

    def __init__(self, value, style=None):
        self.value = value
        self.style = style

    @classmethod
    def to_yaml(cls, representer, node):
        return representer.represent_scalar(cls.yaml_tag,
                                            u'{.value}'.format(node), node.style)

    @classmethod
    def from_yaml(cls, constructor, node):
        return cls(node.value, node.style)

    def __iadd__(self, v):
        self.value += str(v)
        return self

class Sub:
    yaml_tag = u'!Sub'
    def __init__(self, value, style=None):
        self.value = value
        self.style = style

    @classmethod
    def to_yaml(cls, representer, node):
        return representer.represent_scalar(cls.yaml_tag,
                                            u'{.value}'.format(node), node.style)

    @classmethod
    def from_yaml(cls, constructor, node):
        return cls(node.value, node.style)


yaml = YAML(typ='rt')
yaml.register_class(Ref)
yaml.register_class(Sub)

data = yaml.load("""\
Outputs:
  Vpc:
    Value: !Ref: vpc    # first tag
    Export:
      Name: !Sub "${AWS::StackName}-Vpc"  # second tag
""")

data['Outputs']['Vpc']['Value'] += '123'

yaml.dump(data, sys.stdout)