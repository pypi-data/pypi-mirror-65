"""This module defines xml-data that can be used to test the DataTypeDefinition data type"""

#: (Re-)define a basic data type
DATA_BASIC = """
<root><DataTypeDefinition>
    <Identifier>BasicIdentifier</Identifier>
    <DisplayName>Basic Identifier</DisplayName>
    <Description>Definition of an identifier for a basic data type</Description>
    <DataType>
        <Basic>Boolean</Basic>
    </DataType>
</DataTypeDefinition></root>
"""

#: (Re-)define a list type
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

#: (Re-)define a structure data type
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

#: (Re-)define a constrained data type
DATA_CONSTRAINED = """
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

#: (Re-)define another data type definition
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