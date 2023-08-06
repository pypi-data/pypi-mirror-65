import re


def elem2dict(node):
    """
    Convert an lxml.etree node tree into a dict.
    """
    d = {}
    for e in node.iterchildren():
        key = e.tag.split('}')[1] if '}' in e.tag else e.tag
        value = e.text if e.text else elem2dict(e)
        d[key] = value
    return d


class VariableExtractor:

    def __init__(self, xmlNodes):
        self.data = {}
        for xmlNode in xmlNodes:
            d = elem2dict(xmlNode)
            self.data[d['ID']] = d

    def getbyname(self, name):
        for id in self.data:
            data = self.data[id]
            if "Name" in data and isinstance(data['Name'], str):
                if data['Name'].upper() == name.upper():
                    return data


class VariableAssignmentExtractor:

    def __init__(self, xmlNodes):
        self.data = {}
        for xmlNode in xmlNodes:
            d = elem2dict(xmlNode)
            self.data[d['ID']] = d


def resolve_variable_value(variable, variable_assignment):
    if variable_assignment is None:
        return variable['Value']

    if variable['Type'] == '0':
        return variable_assignment['Value']

    print("dont know how to resolve that variable type", variable)
    exit(1)


def resolve_template_variables(variable_assignment_extractor, variable_extractor, template):
    regex = r"<.+?>"
    matches = re.finditer(regex, template, re.MULTILINE)
    for matchNum, match in enumerate(matches, start=1):
        templateMatch = match.group()
        variableName = templateMatch[1:len(templateMatch)-1]
        codeVariable = variable_extractor.getbyname(variableName)
        if codeVariable:
            codeAssignment = None
            if codeVariable['ID'] in variable_assignment_extractor.data:
                codeAssignment = variable_assignment_extractor.data[codeVariable['ID']]
            resolvedVariable = resolve_variable_value(codeVariable, codeAssignment)
            template = template.replace(templateMatch, resolvedVariable)

    return template