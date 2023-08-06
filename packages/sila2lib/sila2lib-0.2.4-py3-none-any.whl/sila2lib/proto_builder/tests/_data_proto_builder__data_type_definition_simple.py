"""This module defines xml-data that can be used to test the DataTypeDefinition data type"""

DATA_BASIC_TEMPLATE = """
<root><DataTypeDefinition>
    <Identifier>BasicIdentifier</Identifier>
    <DisplayName>Basic Identifier</DisplayName>
    <Description>Definition of an identifier for a basic data type</Description>
    <DataType>
        <Basic>{basic_type}</Basic>
    </DataType>
</DataTypeDefinition></root>
"""

DATA_BASIC = {
    'Boolean': DATA_BASIC_TEMPLATE.format(basic_type="Boolean"),
    'String': DATA_BASIC_TEMPLATE.format(basic_type="String"),
    'Integer': DATA_BASIC_TEMPLATE.format(basic_type="Integer"),
    'Real': DATA_BASIC_TEMPLATE.format(basic_type="Real"),
    'Binary': DATA_BASIC_TEMPLATE.format(basic_type="Binary"),
    'Date': DATA_BASIC_TEMPLATE.format(basic_type="Date"),
    'Time': DATA_BASIC_TEMPLATE.format(basic_type="Time"),
    'Timestamp': DATA_BASIC_TEMPLATE.format(basic_type="Timestamp")
}

DATA_BASIC_INVALID = DATA_BASIC_TEMPLATE.format(basic_type="Invalid")

DATA_LIST = """
<root><DataTypeDefinition>
    <Identifier>ListIdentifier</Identifier>
    <DisplayName>List Identifier</DisplayName>
    <Description>Definition of an identifier for a list data type</Description>
    <DataType>
        <List>
            <DataType>
                <Basic>Boolean</Basic>
            </DataType>
        </List>
    </DataType>
</DataTypeDefinition></root>
"""

DATA_STRUCTURE = """
<root><DataTypeDefinition>
    <Identifier>StructureIdentifier</Identifier>
    <DisplayName>Structure Identifier</DisplayName>
    <Description>Definition of an identifier for a structure data type</Description>
    <DataType>
        <Structure>
            <Element>
                <Identifier>BasicElement</Identifier>
                <DisplayName>Basic Element</DisplayName>
                <Description>This parameter defines a basic element.</Description>             
                <DataType>
                    <Basic>Boolean</Basic>
                </DataType>
            </Element>
        </Structure>
    </DataType>
</DataTypeDefinition></root>
"""

DATA_MULTI_STRUCTURE = """
<root><DataTypeDefinition>
    <Identifier>StructureIdentifier</Identifier>
    <DisplayName>Structure Identifier</DisplayName>
    <Description>Definition of an identifier for a structure data type</Description>
    <DataType>
        <Structure>
            <Element>
                <Identifier>BasicElement1</Identifier>
                <DisplayName>1. Basic Element</DisplayName>
                <Description>This parameter defines a 1. basic element.</Description>             
                <DataType>
                    <Basic>Boolean</Basic>
                </DataType>
            </Element>
            <Element>
                <Identifier>BasicElement2</Identifier>
                <DisplayName>2. Basic Element</DisplayName>
                <Description>This parameter defines a 2. basic element.</Description>             
                <DataType>
                    <Basic>Boolean</Basic>
                </DataType>
            </Element>
        </Structure>
    </DataType>
</DataTypeDefinition></root>
"""

DATA_CONSTRAINED_BASIC = """
<root><DataTypeDefinition>
    <Identifier>ConstrainedIdentifier</Identifier>
    <DisplayName>Constrained Identifier</DisplayName>
    <Description>Definition of an identifier for a constrained data type</Description>
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
</DataTypeDefinition></root>
"""

DATA_CONSTRAINED_LIST = """
<root><DataTypeDefinition>
    <Identifier>ConstrainedIdentifier</Identifier>
    <DisplayName>Constrained Identifier</DisplayName>
    <Description>Definition of an identifier for a constrained data type</Description>
    <DataType>
        <Constrained>
            <DataType>
                <List>
                    <DataType>
                        <Basic>Boolean</Basic>
                    </DataType>
                </List>
            </DataType>
            <Constraints>
                <!-- we do not define any constraints here -->
            </Constraints>
        </Constrained>
    </DataType>
</DataTypeDefinition></root>
"""


DATA_DATA_TYPE_IDENTIFIER = """
<root><DataTypeDefinition>
    <Identifier>DefinitionIdentifier</Identifier>
    <DisplayName>Definition Identifier</DisplayName>
    <Description>Definition of an identifier for a defined data type</Description>
    <DataType>
        <DataTypeIdentifier>TestDataType</DataTypeIdentifier>
    </DataType>
</DataTypeDefinition></root>
"""