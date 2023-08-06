"""This module defines xml-data that can be used to test the Structured data type"""

# First let us define the elements a structure can consist of.
#   We do not add a <root>-Tag since, we expect them to be inserted into <Structure> elements later.
#   All strings have the '{count}' element which can be used by .format to add a counter

#: An element of BasicType
DATA_BASIC_ELEMENT = """
<Element>
    <Identifier>StructureElement_{count}</Identifier>
    <DisplayName>Structure Element #{count}</DisplayName>
    <Description>This parameter defines the {count}. element of a structure.</Description>
    <DataType>
        <Basic>Boolean</Basic>
    </DataType>
</Element>
"""

#: An element of ListTyp
DATA_LIST_ELEMENT = """
<Element>
    <Identifier>StructureElement_{count}</Identifier>
    <DisplayName>Structure Element #{count}</DisplayName>
    <Description>This parameter defines the {count}. element of a structure.</Description>
    <DataType>
        <List>
            <DataType>
                <Basic>Boolean</Basic>
            </DataType>
        </List>
    </DataType>
</Element>
"""

#: An element of ListTyp
DATA_STRUCTURE_ELEMENT = """
<Element>
    <Identifier>StructureElement_{count}</Identifier>
    <DisplayName>Structure Element #{count}</DisplayName>
    <Description>This parameter defines the {count}. element of a structure.</Description>
    <DataType>
        <Structure>
            <Element>
                <Identifier>StructureStructureElement</Identifier>
                <DisplayName>Structure-Structure Element</DisplayName>
                <Description>This parameter defines an element of a structure that is inside a structure.</Description>
                <DataType>
                    <Basic>Boolean</Basic>
                </DataType>
            </Element>
        </Structure>
    </DataType>
</Element>
"""

#: An element of ListTyp
DATA_CONSTRAINED_ELEMENT = """
<Element>
    <Identifier>StructureElement_{count}</Identifier>
    <DisplayName>Structure Element #{count}</DisplayName>
    <Description>This parameter defines the {count}. element of a structure.</Description>
    <DataType>
        <Constrained>
            <DataType>
                <Basic>Boolean</Basic>
            </DataType>
            <Constraints>
                <!-- we do not define any constraints here -->
            </Constraints>
        </Constrained>
    </DataType>
</Element>
"""

#: An element of ListTyp
DATA_DATA_TYPE_IDENTIFIER_ELEMENT = """
<Element>
    <Identifier>StructureElement_{count}</Identifier>
    <DisplayName>Structure Element #{count}</DisplayName>
    <Description>This parameter defines the {count}. element of a structure.</Description>
    <DataType>
        <DataTypeIdentifier>TestDataType</DataTypeIdentifier>
    </DataType>
</Element>
"""

# Define a general structure xml tree, in which {elements} can be replaced with the element composition desired
DATA_STRUCTURE_GENERAL = """
<root><Structure>
    {elements}
</Structure></root>
"""


def data_structure_arbitrary(*args):
    """
    Allows to generate an arbitrary StructureType xml string.

    :param args: The xml strings for the sub-elements to use, see definitions above.

    :returns: the xml-tree for a StructureType with the given elements.
    """
    # combine all those elements
    elements = [item.format(count=item_index) for item_index, item in enumerate(args, 1)]

    return DATA_STRUCTURE_GENERAL.format(elements=elements)
