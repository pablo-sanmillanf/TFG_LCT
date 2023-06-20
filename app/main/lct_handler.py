import re
import xmlschema
from PyQt5.QtCore import QXmlStreamReader, QXmlStreamWriter, QByteArray, QTextStream

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

    def __init__(self, dimension: str, labels: list[list[str]], default_value: str, xml_schema: str) -> None:
        """
        LCTHandler object creator.
        :param dimension: A string that indicates the LCT dimension analyzed. In the first version should be "Semantics"
        :param labels: A list of lists. Each element is a list with all the allowed values for each tag. If SD and SG
        are been analyzed, this should be [["SD--", "SD-", "SD+", "SD++"],["SG++", "SG+", "SG-", "SG--"]]
        :param default_value: This value will be the one that a non-valid label should have
        :param xml_schema: The XML Schema to compare th XML files with.
        """
        self._dimension = dimension

        self._def_value = default_value

        self._clause_groups = []  # Store the super clause limits saving the clause limit index
        self._clause_tags = []  # List with all the tags (Sd and/or SG) for all the clauses
        self._clause_texts = []  # List with all the texts for all the clauses
        self._super_clause_tags = []  # List with all the tags (Sd and/or SG) for all the super clauses
        self._super_clause_texts = []  # List with all the texts for all the clauses

        self._labels = labels  # List of available tags.
        self._set_pattern(labels)

        self._is_valid = False
        self._is_completed = False

        self._schema = xmlschema.XMLSchema(xml_schema)

    def _set_pattern(self, labels: list[list[str]]) -> None:
        """
        Sets the structure self.pattern with the specific regex pattern to match the desired labels.
        :param labels: A list of lists. Each element is a list with all the allowed values for each tag. If SD and SG
        are been analyzed, this should be [["SD--", "SD-", "SD+", "SD++"],["SG++", "SG+", "SG-", "SG--"]]
        """
        pattern_groups = []
        for label in labels:
            pattern_groups.append(obtain_pattern(label.copy()))
        self._pattern = ".*".join(pattern_groups)

        raw_labels = self._get_raw_labels()
        self._extended_pattern = ".*".join(
            [pattern_groups[i][:-1] + "|" + raw_labels[i] + self._def_value + ")" for i in range(len(pattern_groups))]
        )

    def set_labels(self, labels: list[list[str]]) -> None:
        """
        Set the available labels for the clauses.
        :param labels: A list of lists. Each element is a list with all the allowed values for each tag. If SD and SG
        are been analyzed, this should be [["SD--", "SD-", "SD+", "SD++"],["SG++", "SG+", "SG-", "SG--"]]
        """
        self._labels = labels
        self._set_pattern(labels)

    def upload_from_data(self, data: list[tuple[list[tuple[str, str]], str]]) -> tuple[bool, bool]:
        """
        Upload the data obtained from the ClassifierView object into the XML Document. If the data is not valid, False
        will be returned.
        :param data: The structure obtained from the ClassifierView object.
        :return: True if the input data was a valid one, False otherwise.
        """
        self._clause_groups.clear()
        self._clause_tags.clear()
        self._clause_texts.clear()
        self._super_clause_tags.clear()
        self._super_clause_texts.clear()

        clause_nbr = 0
        self._clause_groups.append(clause_nbr)

        self._is_valid = False
        self._is_completed = True

        for super_clause in data:
            sc_text_item = ""

            sc_matches = re.findall(self._pattern, super_clause[1])
            if len(self._labels) > 1 and len(sc_matches) != 0:
                sc_matches = sc_matches[0]
            if len(sc_matches) != len(self._labels):
                self._is_completed = False
                sc_matches = re.findall(self._extended_pattern, super_clause[1])
                if len(self._labels) > 1 and len(sc_matches) != 0:
                    sc_matches = sc_matches[0]
                if len(sc_matches) != len(self._labels):
                    return False, False

            self._super_clause_tags.append(list(sc_matches))

            for clause in super_clause[0]:
                sc_text_item += (clause[0] + " ")

                c_matches = re.findall(self._pattern, clause[1])
                if len(self._labels) > 1 and len(c_matches) != 0:
                    c_matches = c_matches[0]
                if len(c_matches) != len(self._labels):
                    self._is_completed = False
                    c_matches = re.findall(self._extended_pattern, clause[1])
                    if len(self._labels) > 1 and len(c_matches) != 0:
                        c_matches = c_matches[0]
                    if len(c_matches) != len(self._labels):
                        return False, False

                self._clause_tags.append(list(c_matches))
                self._clause_texts.append(clause[0])
                clause_nbr += 1

            self._clause_groups.append(clause_nbr)
            self._super_clause_texts.append(sc_text_item[:-1])

        self._is_valid = True
        return self._is_valid, self._is_completed

    def upload_from_xml_string(self, xml_string: str, check: bool) -> bool:
        """
        Upload the data obtained from a .lct file into the XML Document. If the data is not valid, False will be
        returned.
        :param xml_string: The data from a .lct file.
        :param check: Indicates if the function has to check the validity of the data.
        :return: True if the input data was a valid one, False otherwise.
        """
        self._is_valid, self._is_completed = self._upload_from_xml_string_valid_not_checked(xml_string, check)
        return self._is_valid

    def _upload_from_xml_string_valid_not_checked(self, xml_string: str, check: bool) -> tuple[bool, bool]:
        """
        Upload the data obtained from a .lct file into the XML Document. If the data is not valid, False will be
        returned.
        :param xml_string: The data from a .lct file.
        :param check: Indicates if the function has to check the validity of the data.
        :return: True if the input data was a valid one, False otherwise.
        """
        if check and not self._schema.is_valid(xml_string):
            return False, False

        reader = QXmlStreamReader(xml_string)

        # Start of document
        reader.readNext()

        # Start of element "lct"
        reader.readNext()
        if reader.attributes().value("version") != "1.0":
            return False, False

        # Start of element "dimension"
        reader.readNextStartElement()
        self._dimension = reader.readElementText()

        # Start of element "targets"
        reader.readNextStartElement()

        self._labels.clear()
        while reader.readNextStartElement() or reader.name() != "targets":
            self._labels.append(reader.readElementText().split())

        self._set_pattern(self._labels)

        # Start of element "analysis"
        reader.readNextStartElement()

        self._clause_groups.clear()
        self._clause_tags.clear()
        self._clause_texts.clear()
        self._super_clause_tags.clear()
        self._super_clause_texts.clear()

        clause_nbr = 0
        self._clause_groups.append(clause_nbr)
        raw_labels = self._get_raw_labels()

        is_completed = True

        while reader.readNextStartElement() or reader.name() != "analysis":
            attr = reader.attributes()
            sc_tag_values = [((i + attr.value(i)) if attr.value(i) != "" else "") for i in raw_labels]
            if check and (reader.name() != "superClause" or "" in sc_tag_values):
                return False, False

            if self._def_value in "".join(sc_tag_values):
                is_completed = False

            self._super_clause_tags.append(sc_tag_values)

            sc_text_item = ""
            while reader.readNextStartElement() or reader.name() != "superClause":
                attr = reader.attributes()
                c_tag_values = [((i + attr.value(i)) if attr.value(i) != "" else "") for i in raw_labels]
                if check and (reader.name() != "clause" or "" in c_tag_values):
                    return False, False

                if self._def_value in "".join(c_tag_values):
                    is_completed = False

                self._clause_tags.append(c_tag_values)

                self._clause_texts.append(reader.readElementText())
                sc_text_item += (self._clause_texts[-1] + " ")
                clause_nbr += 1

            self._clause_groups.append(clause_nbr)
            self._super_clause_texts.append(sc_text_item[:-1])

        return True, is_completed

    def to_string(self) -> str:
        """
        Returns the XML Document as a pretty XML.
        :return: The string with the format of a valid .lct file or an empty string if there was no valid XML Document.
        """
        if self._is_valid:
            result = QByteArray()
            writer = QXmlStreamWriter(result)
            writer.setAutoFormatting(True)
            writer.writeStartDocument()

            writer.writeStartElement("lct")
            writer.writeAttribute("version", "1.0")
            writer.writeAttribute("xmlns", "http://www.example.org/semanticsLCT")
            writer.writeAttribute("xmlns:xsi", "http://www.w3.org/2001/XMLSchema-instance")
            writer.writeAttribute("xsi:schemaLocation", "http://www.example.org/semanticsLCT lct.xsd")
            writer.writeTextElement("dimension", "Semantics")

            raw_labels = self.get_raw_labels()

            writer.writeStartElement("targets")
            for label in self._labels:
                writer.writeTextElement("target", " ".join(label))
            writer.writeEndElement()  # Close "targets" element

            writer.writeStartElement("analysis")
            clause_group_index = 1
            simplified_clause_tags = self.get_clause_tags()

            for super_clause_tag in self.get_super_clause_tags():
                writer.writeStartElement("superClause")
                for i in range(len(super_clause_tag)):
                    writer.writeAttribute(raw_labels[i], super_clause_tag[i])

                for i in range(self._clause_groups[clause_group_index - 1], self._clause_groups[clause_group_index]):
                    writer.writeStartElement("clause")
                    for e in range(len(simplified_clause_tags[i])):
                        writer.writeAttribute(raw_labels[e], simplified_clause_tags[i][e])
                    writer.writeCharacters(self._clause_texts[i])
                    writer.writeEndElement()  # Close "clause" element
                clause_group_index += 1

                writer.writeEndElement()  # Close "superClause" element

            writer.writeEndElement()  # Close "analysis" element

            writer.writeEndElement()  # Close "lct" element

            writer.writeEndDocument()  # Close document

            stream = QTextStream(result)
            stream.setCodec(writer.codec())

            return stream.readAll()
        return ""

    def get_dimension(self) -> str:
        """
        Obtain the dimension of the .lct file. In the first version of the class, it should be "Semantics".
        :return:The dimension as a string.
        """
        if self._is_valid:
            return self._dimension
        return None

    def get_raw_labels(self) -> list[str]:
        """
        Obtain a list with the raw labels if the data is valid. If the target is SD and SG, the resulting list will be
        ["SD", "SG"]
        :return: The list with the raw labels, None if is not valid
        """
        if self._is_valid:
            return self._get_raw_labels()
        return None

    def _get_raw_labels(self) -> list[str]:
        """
        Obtain a list with the raw labels. If the target is SD and SG, the resulting list will be ["SD", "SG"]
        :return: The list with the raw labels.
        """
        result = []
        index = 1
        for label in self._labels:
            first = label[0][:index]
            while all(first == x[:index] for x in label):
                index += 1
                first = label[0][:index]
            result.append(first[:-1])

        return result

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
        if self._is_valid and self._is_completed:
            result = [[self._labels[i].index(tag[i]) + 1 for i in range(len(tag))] for tag in self._super_clause_tags]
            return result
        return None

    def get_clause_values(self) -> list[list[int]]:
        """
        Return a list with the numerical values of each clause. Each element is a list of values for each label.
        :return: The list of clause values.
        """
        if self._is_valid and self._is_completed:
            result = [[self._labels[i].index(tag[i]) + 1 for i in range(len(tag))] for tag in self._clause_tags]
            return result
        return None

    def get_super_clause_tags(self) -> list[list[str]]:
        """
        Return a list with the string value of each super clause. Each element is a list of values for each label.
        :return: The list of super clause tags.
        """
        if self._is_valid:
            simplified_labels = self.get_raw_labels()
            return [[tag[i][len(simplified_labels[i]):] for i in range(len(tag))] for tag in self._super_clause_tags]

        return None

    def get_clause_tags(self) -> list[list[str]]:
        """
        Return a list with the string value of each clause. Each element is a list of values for each label.
        :return: The list of clause tags.
        """
        if self._is_valid:
            simplified_labels = self.get_raw_labels()
            a = [[tag[i][len(simplified_labels[i]):] for i in range(len(tag))] for tag in self._clause_tags]
            return [[tag[i][len(simplified_labels[i]):] for i in range(len(tag))] for tag in self._clause_tags]
        return None

    def get_super_clause_texts(self) -> list[str]:
        """
        Return a list with the super clauses.
        :return: The list with the super clauses.
        """
        if self._is_valid:
            return self._super_clause_texts
        return None

    def get_clause_texts(self) -> list[str]:
        """
        Return a list with the clauses.
        :return: The list with the clauses.
        """
        if self._is_valid:
            return self._clause_texts
        return None
