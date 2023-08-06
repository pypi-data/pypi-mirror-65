"""This module defines xml-data that can be used to test the List data type"""

#: Define a list of Basic data types
DATA_BASIC = """
<root><List>
    <DataType>
        <Basic>Boolean</Basic>
    </DataType>
</List></root>
"""

#: Define a nested list xml-tree. This is actually not allowed in the standard
DATA_LIST = """
<root><List>
    <DataType>
        <List>
            <DataType>
                <Basic>Boolean</Basic>
            </DataType>
        </List>
    </DataType>
</List></root>
"""

#: Define a list of structures
DATA_STRUCTURE = """
<root><List>
    <DataType>
        <Structure>
            <Element>
                <Identifier>ListStructureElement</Identifier>
                <DisplayName>List-Structure Element</DisplayName>
                <Description>This parameter defines an element of a structure that is inside a list.</Description>
                <DataType>
                    <Basic>Boolean</Basic>
                </DataType>
            </Element>
        </Structure>
    </DataType>
</List></root>
"""

#: Define a list of constrained elements
DATA_CONSTRAINED = """
<root><List>
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
</List></root>
"""

#: Define a list of (previously) defined data types
DATA_DATA_TYPE_IDENTIFIER = """
<root><List>
    <DataType>
        <DataTypeIdentifier>TestDataType</DataTypeIdentifier>
    </DataType>
</List></root>
"""