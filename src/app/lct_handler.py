import re
from xml.dom import minidom
from xml.dom.minidom import Document

# The chars "[" and "]" were not added to avoid problems in pattern conversion. Thus, those characters are not permitted
# as a part of labels
SPECIAL_REGEX_CHARS = ["\\", ".", "+", "*", "?", "^", "$", "(", ")", "{", "}", "|"]


def obtain_pattern(labels: list[str]) -> str:
    """
    Create a pattern that matches all the possible labels.
    :param labels: All the possible labels
    :return: The string pattern
    """
    for i in range(len(labels)):
        for special_char in SPECIAL_REGEX_CHARS:
            labels[i] = labels[i].replace(special_char, "[" + special_char + "]")
    return "(" + "|".join(sorted(labels, key=len, reverse=True)) + ")"


class LCTHandler:
    """
    This class is in charge of translate to/from the format of the .lct files that is base in an XML format from/to a
    format that the ClassifierView class can understand.
    """
    _doc: Document

    def __init__(self, dimension: str, labels: list[list[str]]) -> None:
        """
        LCTHandler object creator.
        :param dimension: A string that indicates the LCT dimension analyzed. In the first version should be "Semantics"
        :param labels: A list of lists. Each element is a list with all the allowed values for each tag. If SD and SG
        are been analyzed, this should be [["SD--", "SD-", "SD+", "SD++"],["SG++", "SG+", "SG-", "SG--"]]
        """
        self._doc = minidom.Document()
        self._dimension = dimension

        self._labels = labels
        self._set_pattern(labels)
        self._from_file = False

        self._is_valid = False

    def unmount(self) -> None:
        """
        Remove all the information from the internal XML Document.
        """
        self._doc.unlink()

    def _set_pattern(self, labels: list[list[str]]) -> None:
        """
        Sets the structure self.pattern with the specific regex pattern to match the desired labels.
        :param labels: A list of lists. Each element is a list with all the allowed values for each tag. If SD and SG
        are been analyzed, this should be [["SD--", "SD-", "SD+", "SD++"],["SG++", "SG+", "SG-", "SG--"]]
        """
        self.pattern = ""
        for label in labels:
            self.pattern += (obtain_pattern(label.copy()) + ".*")
        self.pattern = self.pattern[:-2]

    def set_labels(self, labels: list[list[str]]) -> None:
        """
        Set the available labels for the clauses. This function also unmount all the previous XML Documents.
        :param labels: A list of lists. Each element is a list with all the allowed values for each tag. If SD and SG
        are been analyzed, this should be [["SD--", "SD-", "SD+", "SD++"],["SG++", "SG+", "SG-", "SG--"]]
        """
        self._labels = labels
        self._set_pattern(labels)
        self.unmount()

    def upload_from_data(self, data: list[tuple[list[tuple[str, str]], str]]) -> bool:
        """
        Upload the data obtained from the ClassifierView object into the XML Document. If the data is not valid, the
        internal XML Document will be unmounted and False will be returned.
        :param data: The structure obtained from the ClassifierView object.
        :return: True if the input data was a valid one, False otherwise.
        """
        self._is_valid = self._upload_from_data_valid_not_checked(data)
        if not self._is_valid:
            self.unmount()
        return self._is_valid

    def _upload_from_data_valid_not_checked(self, data: list[tuple[list[tuple[str, str]], str]]) -> bool:
        """
        Upload the data obtained from the ClassifierView object into the XML Document. If the data is not valid, False
        will be returned.
        :param data: The structure obtained from the ClassifierView object.
        :return: True if the input data was a valid one, False otherwise.
        """
        # Clear previous elements
        self.unmount()

        self._from_file = False

        try:
            # Root element
            lct = self._doc.createElement("lct")
            lct.setAttribute("version", "1.0")
            self._doc.appendChild(lct)

            # Add dimension. Non-critical information, won't be checked
            dim_node = self._doc.createElement("dimension")
            lct.appendChild(dim_node)
            dim_node.appendChild(self._doc.createTextNode(self._dimension))

            # Add targets.
            targets = self._doc.createElement("targets")
            lct.appendChild(targets)
            for label in self._labels:
                target = self._doc.createElement('target')
                targets.appendChild(target)
                target.appendChild(self._doc.createTextNode(" ".join(label)))

            # Root data element
            analysis = self._doc.createElement('analysis')
            lct.appendChild(analysis)

            for super_clause in data:
                super_clause_node = self._doc.createElement("superClause")
                analysis.appendChild(super_clause_node)

                sc_matches = re.findall(self.pattern, super_clause[1])

                if len(sc_matches) == 0:
                    return False

                if len(self._labels) > 1:
                    sc_matches = sc_matches[0]

                if len(sc_matches) != len(self._labels):
                    return False

                sc_attr = ""
                for i in range(len(sc_matches)):
                    sc_attr += str(self._labels[i].index(sc_matches[i]) + 1)
                super_clause_node.setAttribute('value', sc_attr)

                for clause in super_clause[0]:
                    clause_node = self._doc.createElement("clause")
                    super_clause_node.appendChild(clause_node)

                    c_matches = re.findall(self.pattern, clause[1])

                    if len(c_matches) == 0:
                        return False

                    if len(self._labels) > 1:
                        c_matches = c_matches[0]

                    if len(c_matches) != len(self._labels):
                        return False

                    c_attr = ""
                    for i in range(len(c_matches)):
                        c_attr += str(self._labels[i].index(c_matches[i]) + 1)
                    clause_node.setAttribute('value', c_attr)

                    clause_node.appendChild(self._doc.createTextNode(clause[0]))
        except ValueError:
            return False
        return True

    def upload_from_xml_string(self, xml_string: str, check: bool) -> bool:
        """
        Upload the data obtained from a .lct file into the XML Document. If the data is not valid, the internal XML
        Document will be unmounted and False will be returned.
        :param xml_string: The data from a .lct file.
        :param check: Indicates if the function has to check the validity of the data.
        :return: True if the input data was a valid one, False otherwise.
        """
        self._is_valid = self._upload_from_xml_string_valid_not_checked(xml_string, check)
        if not self._is_valid:
            self.unmount()
        return self._is_valid

    def _upload_from_xml_string_valid_not_checked(self, xml_string: str, check: bool) -> bool:
        """
        Upload the data obtained from a .lct file into the XML Document. If the data is not valid, False will be
        returned.
        :param xml_string: The data from a .lct file.
        :param check: Indicates if the function has to check the validity of the data.
        :return: True if the input data was a valid one, False otherwise.
        """
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
        self._labels.clear()
        for target in [item for item in target_list if item.nodeType == minidom.Node.ELEMENT_NODE]:
            self._labels.append(target.firstChild.nodeValue.split())

        self._set_pattern(self._labels)

        self._from_file = True
        self.unmount()
        self._doc = new_doc
        return True

    def to_string(self) -> str:
        """
        Returns the XML Document as a pretty XML.
        :return: The string with the format of a valid .lct file or an empty string if there was no valid XML Document.
        """
        if self._is_valid:
            if self._from_file:
                return self._doc.toxml()
            return self._doc.toprettyxml(indent='   ')
        return ""

    def get_dimension(self) -> str:
        """
        Obtain the dimension of the .lct file. In the first version of the class, it should be "Semantics".
        :return:The dimension as a string.
        """
        try:
            return self._doc.firstChild.getElementsByTagName("dimension")[0].firstChild.nodeValue
        except AttributeError:
            return ""

    def get_raw_labels(self) -> list[str]:
        """
        Obtain a list with the raw labels. If the target is SD and SG, the resulting list will be ["SD", "SG"]
        :return: The list with the raw labels.
        """
        if self._is_valid:
            result = []
            index = 1
            for label in self._labels:
                first = label[0][:index]
                while all(first == x[:index] for x in label):
                    index += 1
                    first = label[0][:index]
                result.append(first[:-1])

            return result
        return None

    def get_clause_labels(self) -> list[list[str]]:
        """
        A list with all the possibilities for each label. If the target is SD and SG, the resulting list will be
        [["SD--", "SD-", "SD+", "SD++"],["SG++", "SG+", "SG-", "SG--"]]
        :return:
        """
        if self._is_valid:
            return self._labels.copy()
        return None

    def get_super_clause_values(self) -> list[list[int]]:
        """
        Return a list with the numerical values of each super clause. Each element is a list of values for each label.
        :return: The list of super clause values.
        """
        if self._is_valid:
            result = []
            data_list = self._doc.firstChild.getElementsByTagName("analysis")[0]
            data_list = [item for item in data_list.childNodes if item.nodeType == minidom.Node.ELEMENT_NODE]
            for super_clause in data_list:
                result.append([int(i) for i in super_clause.getAttribute("value")])

            return result
        return None

    def get_clause_values(self) -> list[list[int]]:
        """
        Return a list with the numerical values of each clause. Each element is a list of values for each label.
        :return: The list of clause values.
        """
        if self._is_valid:
            result = []
            data_list = self._doc.firstChild.getElementsByTagName("analysis")[0]
            data_list = [item for item in data_list.childNodes if item.nodeType == minidom.Node.ELEMENT_NODE]
            for super_clause in data_list:
                clauses = [item for item in super_clause.childNodes if item.nodeType == minidom.Node.ELEMENT_NODE]

                for clause in clauses:
                    result.append([int(i) for i in clause.getAttribute("value")])

            return result
        return None

    def get_super_clause_tags(self) -> list[list[str]]:
        """
        Return a list with the string value of each super clause. Each element is a list of values for each label.
        :return: The list of super clause tags.
        """
        if self._is_valid:
            simplified_labels = self.get_raw_labels()
            result = []
            data_list = self._doc.firstChild.getElementsByTagName("analysis")[0]
            data_list = [item for item in data_list.childNodes if item.nodeType == minidom.Node.ELEMENT_NODE]
            for super_clause in data_list:
                val = super_clause.getAttribute("value")
                result.append([self._labels[i][int(val[i]) - 1][len(simplified_labels[i]):] for i in range(len(val))])

            return result
        return None

    def get_clause_tags(self) -> list[list[str]]:
        """
        Return a list with the string value of each clause. Each element is a list of values for each label.
        :return: The list of clause tags.
        """
        if self._is_valid:
            simp_labels = self.get_raw_labels()
            result = []
            data_list = self._doc.firstChild.getElementsByTagName("analysis")[0]
            data_list = [item for item in data_list.childNodes if item.nodeType == minidom.Node.ELEMENT_NODE]
            for super_clause in data_list:
                clauses = [item for item in super_clause.childNodes if item.nodeType == minidom.Node.ELEMENT_NODE]

                for clause in clauses:
                    val = clause.getAttribute("value")
                    result.append([self._labels[i][int(val[i]) - 1][len(simp_labels[i]):] for i in range(len(val))])

            return result
        return None

    def get_super_clause_texts(self) -> list[str]:
        """
        Return a list with the super clauses.
        :return: The list with the super clauses.
        """
        if self._is_valid:
            result = []
            data_list = self._doc.firstChild.getElementsByTagName("analysis")[0]
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
        """
        Return a list with the clauses.
        :return: The list with the clauses.
        """
        if self._is_valid:
            result = []
            data_list = self._doc.firstChild.getElementsByTagName("analysis")[0]
            data_list = [item for item in data_list.childNodes if item.nodeType == minidom.Node.ELEMENT_NODE]
            for super_clause in data_list:
                clauses = [item for item in super_clause.childNodes if item.nodeType == minidom.Node.ELEMENT_NODE]

                for clause in clauses:
                    result.append(clause.firstChild.nodeValue)

            return result
        return None
