"""This module defines xml-data that can be used to test Parameter data type"""

#: A basic parameter
DATA_BASIC = """
<root><Parameter>
    <Identifier>BasicParameter</Identifier>
    <DisplayName>Basic Parameter</DisplayName>
    <Description>This parameter defines a basic parameter.</Description>
    <DataType>
        <Basic>Boolean</Basic>
    </DataType>
</Parameter></root>
"""

#: A parameter that is a list
DATA_LIST = """
<root><Parameter>
    <Identifier>ListParameter</Identifier>
    <DisplayName>List Parameter</DisplayName>
    <Description>This parameter defines a list parameter.</Description>
    <DataType>
        <List>
            <DataType>
                <Basic>Boolean</Basic>
            </DataType>
        </List>
    </DataType>
</Parameter></root>
"""

#: A structured parameter with sub-elements
DATA_STRUCTURE = """
<root><Parameter>
    <Identifier>StructureParameter</Identifier>
    <DisplayName>Structure Parameter</DisplayName>
    <Description>This parameter defines a structure parameter.</Description>
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
</Parameter></root>
"""

#: A constrained parameter
DATA_CONSTRAINED = """
<root><Parameter>
    <Identifier>ConstrainedParameter</Identifier>
    <DisplayName>Constrained Parameter</DisplayName>
    <Description>This parameter defines a constrained parameter.</Description>
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
</Parameter></root>
"""

#: A parameter that uses a data type identifier to define its type
DATA_DATA_TYPE_IDENTIFIER = """
<root><Parameter>
    <Identifier>DefinedDataType</Identifier>
    <DisplayName>DefinedDataType Parameter</DisplayName>
    <Description>This parameter defines a parameter that has been defined previously.</Description>
    <DataType>
        <DataTypeIdentifier>TestDataType</DataTypeIdentifier>
    </DataType>
</Parameter></root>
"""