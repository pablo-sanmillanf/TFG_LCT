import re
from xml.dom import minidom
from xml.dom.minidom import Document

# The chars "[" and "]" were no added to avoid problems in pattern conversion. Thus, those characters are not permitted
# as a part of labels
SPECIAL_REGEX_CHARS = ["\\", ".", "+", "*", "?", "^", "$", "(", ")", "{", "}", "|"]


def get_pattern(labels: list[str]):
    for i in range(len(labels)):
        for special_char in SPECIAL_REGEX_CHARS:
            labels[i] = labels[i].replace(special_char, "[" + special_char + "]")
    return "(" + "|".join(sorted(labels, key=len, reverse=True)) + ")"


class LCTHandler:
    doc: Document

    def __init__(self, dimension: str, labels: list[list[str]]):
        self.doc = minidom.Document()
        self.dimension = dimension

        self.labels = labels
        self.pattern = ""
        for label in labels:
            self.pattern += (get_pattern(label.copy()) + ".*")
        self.pattern = self.pattern[:-2]
        self.from_file = False

        self.is_valid = False

    def unmount(self):
        self.doc.unlink()

    def set_labels(self, labels: list[list[str]]):
        self.labels = labels
        self.unmount()

    def upload_from_data(self, data: list[tuple[list[tuple[str, str]], str]]):
        self.is_valid = self._upload_from_data_valid_not_checked(data)
        if not self.is_valid:
            self.unmount()
        return self.is_valid

    def _upload_from_data_valid_not_checked(self, data: list[tuple[list[tuple[str, str]], str]]):
        # Clear previous elements
        self.unmount()

        self.from_file = False

        try:
            # Root element
            lct = self.doc.createElement("lct")
            lct.setAttribute("version", "1.0")
            self.doc.appendChild(lct)

            # Add dimension. Non-critical information, won't be checked
            dim_node = self.doc.createElement("dimension")
            lct.appendChild(dim_node)
            dim_node.appendChild(self.doc.createTextNode(self.dimension))

            # Add targets.
            targets = self.doc.createElement("targets")
            lct.appendChild(targets)
            for label in self.labels:
                target = self.doc.createElement('target')
                targets.appendChild(target)
                target.appendChild(self.doc.createTextNode(" ".join(label)))

            # Root data element
            analysis = self.doc.createElement('analysis')
            lct.appendChild(analysis)

            for super_clause in data:
                super_clause_node = self.doc.createElement("superClause")
                analysis.appendChild(super_clause_node)

                sc_matches = re.findall(self.pattern, super_clause[1])

                if len(sc_matches) == 0:
                    return False
                sc_matches = sc_matches[0]

                if len(sc_matches) != len(self.labels):
                    return False

                sc_attr = ""
                for i in range(len(sc_matches)):
                    sc_attr += str(self.labels[i].index(sc_matches[i]) + 1)
                super_clause_node.setAttribute('value', sc_attr)

                for clause in super_clause[0]:
                    clause_node = self.doc.createElement("clause")
                    super_clause_node.appendChild(clause_node)

                    c_matches = re.findall(self.pattern, clause[1])

                    if len(c_matches) == 0:
                        return False
                    c_matches = c_matches[0]

                    if len(c_matches) != len(self.labels):
                        return False

                    c_attr = ""
                    for i in range(len(c_matches)):
                        c_attr += str(self.labels[i].index(c_matches[i]) + 1)
                    clause_node.setAttribute('value', c_attr)

                    clause_node.appendChild(self.doc.createTextNode(clause[0]))
        except ValueError:
            return False
        return True

    def upload_from_xml_string(self, xml_string: str, check: bool):
        self.is_valid = self._upload_from_xml_string_valid_not_checked(xml_string, check)
        return self.is_valid

    def _upload_from_xml_string_valid_not_checked(self, xml_string: str, check: bool):

        new_doc = minidom.parseString(xml_string)

        if check:
            aux = new_doc.childNodes

            if len(aux) != 1:
                return False
            if aux[0].tagName != "lct":
                return False

            aux = [item for item in aux[0].childNodes if item.nodeType == minidom.Node.ELEMENT_NODE]

            if aux[0].tagName != "dimension":
                return False

            if aux[1].tagName != "targets":
                return False

            targets = [item for item in aux[1].childNodes if item.nodeType == minidom.Node.ELEMENT_NODE]

            if not all(item.tagName == "target" for item in targets):
                return False

            if aux[2].tagName != "analysis":
                return False

            aux = [item for item in aux[2].childNodes if item.nodeType == minidom.Node.ELEMENT_NODE]

            if not all(item.tagName == "superClause" for item in aux):
                return False

            for super_clause in aux:
                if super_clause.tagName != "superClause":
                    return False
                if not super_clause.getAttribute("value").isnumeric():
                    return False
                for clause in [item for item in super_clause.childNodes if item.nodeType == minidom.Node.ELEMENT_NODE]:
                    if clause.tagName != "clause":
                        return False
                    if not clause.getAttribute("value").isnumeric():
                        return False
                    if len([item for item in clause.childNodes if item.nodeType == minidom.Node.ELEMENT_NODE]) != 0:
                        return False

        target_list = [item for item in new_doc.firstChild.childNodes
                       if item.nodeType == minidom.Node.ELEMENT_NODE][1].childNodes
        self.labels.clear()
        for target in [item for item in target_list if item.nodeType == minidom.Node.ELEMENT_NODE]:
            self.labels.append(target.firstChild.nodeValue.split())

        self.from_file = True
        self.unmount()
        self.doc = new_doc
        return True

    def to_string(self) -> str:
        if self.is_valid:
            if self.from_file:
                return self.doc.toxml()
            return self.doc.toprettyxml(indent='   ')
        return ""

    def get_dimension(self) -> str:
        try:
            return self.doc.firstChild.getElementsByTagName("dimension")[0].firstChild.nodeValue
        except AttributeError:
            return ""

    def get_raw_labels(self) -> list[str]:
        if self.is_valid:
            result = []
            index = 1
            for label in self.labels:
                first = label[0][:index]
                while all(first == x[:index] for x in label):
                    index += 1
                    first = label[0][:index]
                result.append(first[:-1])

            return result
        return None

    def get_clause_labels(self) -> list[list[str]]:
        if self.is_valid:
            return self.labels.copy()
        return None

    def get_super_clause_values(self) -> list[list[int]]:
        if self.is_valid:
            result = []
            data_list = self.doc.firstChild.getElementsByTagName("analysis")[0]
            data_list = [item for item in data_list.childNodes if item.nodeType == minidom.Node.ELEMENT_NODE]
            for super_clause in data_list:
                result.append([int(i) for i in super_clause.getAttribute("value")])

            return result
        return None

    def get_clause_values(self) -> list[list[int]]:
        if self.is_valid:
            result = []
            data_list = self.doc.firstChild.getElementsByTagName("analysis")[0]
            data_list = [item for item in data_list.childNodes if item.nodeType == minidom.Node.ELEMENT_NODE]
            for super_clause in data_list:
                clauses = [item for item in super_clause.childNodes if item.nodeType == minidom.Node.ELEMENT_NODE]

                for clause in clauses:
                    result.append([int(i) for i in clause.getAttribute("value")])

            return result
        return None

    def get_super_clause_texts(self) -> list[str]:
        if self.is_valid:
            result = []
            data_list = self.doc.firstChild.getElementsByTagName("analysis")[0]
            data_list = [item for item in data_list.childNodes if item.nodeType == minidom.Node.ELEMENT_NODE]
            for super_clause in data_list:
                clauses = [item for item in super_clause.childNodes if item.nodeType == minidom.Node.ELEMENT_NODE]
                aux = ""
                for clause in clauses:
                    aux += (clause.firstChild.nodeValue + " ")
                result.append(aux[:-1])

            return result
        return None

    def get_clause_texts(self) -> list[str]:
        if self.is_valid:
            result = []
            data_list = self.doc.firstChild.getElementsByTagName("analysis")[0]
            data_list = [item for item in data_list.childNodes if item.nodeType == minidom.Node.ELEMENT_NODE]
            for super_clause in data_list:
                clauses = [item for item in super_clause.childNodes if item.nodeType == minidom.Node.ELEMENT_NODE]

                for clause in clauses:
                    result.append(clause.firstChild.nodeValue)

            return result
        return None
