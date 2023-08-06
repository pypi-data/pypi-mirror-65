"""This module defines xml-data that can be used to test the Property class"""

#: A simple metadata element
DATA_SIMPLE = """
<root><Metadata>
    <Identifier>MetadataIdentifier</Identifier>
    <DisplayName>Metadata Name</DisplayName>
    <Description>Simple metadata element</Description>
    <DataType>
        <Basic>Boolean</Basic>
    </DataType>
</Metadata></root>"""

#: Metadata that contains execution errors
DATA_DEFINED_EXECUTION_ERRORS = """
<root><Metadata>
    <Identifier>MetadataIdentifier</Identifier>
    <DisplayName>Metadata Name</DisplayName>
    <Description>Simple metadata element with execution errors defined</Description>
    <DataType>
        <Basic>Boolean</Basic>
    </DataType>
    <DefinedExecutionErrors>
        <Identifier>ExecutionError1</Identifier>
        <Identifier>ExecutionError2</Identifier>
        <Identifier>ExecutionError3</Identifier>
    </DefinedExecutionErrors>
</Metadata></root>"""