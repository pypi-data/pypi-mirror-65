from . import variables, topics
import urllib.request
from lxml import etree


def extract_from_url(namespaces, url):
    document = {
        'URL': url,
        'Books': [],
    }
    response = urllib.request.urlopen(url).read()

    parser = etree.XMLParser(recover=True)
    tree = etree.fromstring(response, parser=parser)

    ve = variables.VariableExtractor(tree.xpath('//authorit:Variable', namespaces=namespaces))

    extracted_topics = topics.extract_topics(namespaces, tree)
    books = tree.xpath('//authorit:Book', namespaces=namespaces)
    for book in books:

        va = variables.VariableAssignmentExtractor(book.xpath('//authorit:VariableAssignment', namespaces=namespaces))

        courseBook = {
            'PrintTitle': variables.resolve_template_variables(va, ve, book.xpath('//authorit:PrintTitle', namespaces=namespaces)[0].text),
            'PrintSubTitle': variables.resolve_template_variables(va, ve, book.xpath('//authorit:PrintSubTitle', namespaces=namespaces)[0].text),
            'PrintSuperTitle': variables.resolve_template_variables(va, ve, book.xpath('//authorit:PrintSuperTitle', namespaces=namespaces)[0].text),
            'PrintVersion': variables.resolve_template_variables(va, ve, book.xpath('//authorit:PrintVersion', namespaces=namespaces)[0].text),
            'ContentNodes': [],
        }
        nodes = book.xpath('//authorit:ContentsNodes/authorit:Node', namespaces=namespaces)
        for node in nodes:
            node_id = node.attrib['id']

            found = False
            for topic in extracted_topics:
                if topic['ID'] == node_id:
                    found = True
                    courseBook['ContentNodes'].append(topic)

            if not found:
                print(node)

        document['Books'].append(courseBook)

    return document