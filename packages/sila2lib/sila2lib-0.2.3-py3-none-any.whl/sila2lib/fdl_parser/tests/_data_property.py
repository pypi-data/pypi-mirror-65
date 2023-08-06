"""This module defines xml-data that can be used to test the Property class"""

#: A simple, unobservable property
DATA_SIMPLE = """
<root><Property>
    <Identifier>PropertyIdentifier</Identifier>
    <DisplayName>Property Name</DisplayName>
    <Description>Simple, unobservable property</Description>
    <Observable>No</Observable>
    <DataType>
        <Basic>Boolean</Basic>
    </DataType>
</Property></root>"""

#: A simple observable property
DATA_OBSERVABLE = """
<root><Property>
    <Identifier>PropertyIdentifier</Identifier>
    <DisplayName>Property Name</DisplayName>
    <Description>Simple, observable property</Description>
    <Observable>Yes</Observable>
    <DataType>
        <Basic>Boolean</Basic>
    </DataType>
</Property></root>"""

#: A simple property that can issue defined execution errors during reading
DATA_DEFINED_EXECUTION_ERRORS = """
<root><Property>
    <Identifier>PropertyIdentifier</Identifier>
    <DisplayName>Property Name</DisplayName>
    <Description>Simple, unobservable property with defined execution errors defined</Description>
    <Observable>No</Observable>
    <DataType>
        <Basic>Boolean</Basic>
    </DataType>
    <DefinedExecutionErrors>
        <Identifier>ReadError1</Identifier>
        <Identifier>ReadError2</Identifier>
        <Identifier>ReadError3</Identifier>
    </DefinedExecutionErrors>
</Property></root>"""