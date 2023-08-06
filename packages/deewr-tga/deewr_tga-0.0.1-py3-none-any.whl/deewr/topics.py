from lxml import etree


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


def extract_topics(namespaces, document_tree):
    topics = []
    for topic in document_tree.xpath('//authorit:Topic', namespaces=namespaces):
        topics.append(extract_topic(namespaces, topic))

    return topics


def extract_topic(namespaces, topic_element):
    text = topic_element.xpath('.//authorit:Text', namespaces=namespaces)[0]

    d = elem2dict(topic_element)
    return {
        "PrintHeading": d['Headings']['PrintHeading'],
        "FolderID": d['Object']['FolderID'],
        "GUID": d['Object']['GUID'],
        "ID": d['Object']['ID'],
        "Text": etree.tostring(text, pretty_print=True, method='html').decode("utf-8"),
    }