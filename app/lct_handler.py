import re
from xml.dom import minidom
from xml.dom.minidom import Document


class LCTHandler:
    doc: Document

    def __init__(self, dimension: str, labels: list[str], valid_values: list[str]):
        self.doc = minidom.Document()
        self.dimension = dimension

        self.labels = labels
        self.valid_values = valid_values

        self.pattern = "[" + "".join(set("".join(self.valid_values))) + "]+"
        self.from_file = False

        self.is_valid = False

    def unmount(self):
        self.doc.unlink()

    def set_labels(self, labels: list[str]):
        self.labels = labels
        self.unmount()

    def upload_from_data(self, data: list[tuple[list[tuple[str, str]], str]]):
        self.is_valid = self._upload_from_data_valid_not_checked(data)
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

            # Root data element
            analysis = self.doc.createElement('analysis')
            lct.appendChild(analysis)
            analysis.setAttribute("target", "".join(re.split(self.pattern, data[0][1])))

            for super_clause in data:
                super_clause_node = self.doc.createElement("superClause")
                analysis.appendChild(super_clause_node)

                sc_matches = re.findall(self.pattern, super_clause[1])

                if len(sc_matches) != len(self.labels):
                    self.unmount()
                    return False

                sc_attr = ""
                for i in sc_matches:
                    sc_attr += str(self.valid_values.index(i) + 1)
                super_clause_node.setAttribute('value', sc_attr)

                for clause in super_clause[0]:
                    clause_node = self.doc.createElement("clause")
                    super_clause_node.appendChild(clause_node)

                    c_matches = re.findall(self.pattern, clause[1])

                    if len(c_matches) != len(self.labels):
                        self.unmount()
                        return False

                    c_attr = ""
                    for i in c_matches:
                        c_attr += str(self.valid_values.index(i) + 1)
                    clause_node.setAttribute('value', c_attr)

                    clause_node.appendChild(self.doc.createTextNode(clause[0].replace("\n", "\\n")))
        except ValueError:
            self.unmount()
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

            if aux[1].tagName != "analysis":
                return False

            if aux[1].getAttribute("target") == "":
                return False

            aux = [item for item in aux[1].childNodes if item.nodeType == minidom.Node.ELEMENT_NODE]

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

    def get_clause_labels(self) -> list[list[str]]:
        if self.is_valid:
            result = []
            for label in self.labels:
                aux = []
                for value in self.valid_values:
                    aux.append(label + value)
                result.append(aux)

            return result
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
