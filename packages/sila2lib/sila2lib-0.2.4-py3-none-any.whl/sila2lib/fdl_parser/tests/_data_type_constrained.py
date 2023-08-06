"""This module defines xml-data that can be used to test the Constrained data type"""

#: Define a template of a constrained on a basic data type
DATA_BASIC_TEMPLATE = """
<root><Constrained>
    <DataType>
        <Basic>{basic_data_type}</Basic>
    </DataType>
    <Constraints>
        {constraint}
    </Constraints>
</Constrained></root>"""

#: Define a template of a constrained on a list data type
DATA_LIST_TEMPLATE = """
<root><Constrained>
    <DataType>
        <List>
            <DataType>
                <Basic>Boolean</Basic>
            </DataType>
        </List>
    </DataType>
    <Constraints>
        {constraint}
    </Constraints>
</Constrained></root>"""

#: Define a template for a constrained constrained (not allowed -> Exception SubDataTypeError)
DATA_CONSTRAINED_TEMPLATE = """
<root><Constrained>
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
    <Constraints>
        {constraint}
    </Constraints>
</Constrained></root>"""

#: Define a template for a constrained structure (not allowed -> Exception SubDataTypeError)
DATA_STRUCTURE_TEMPLATE = """
<root><Constrained>
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
    <Constraints>
        {constraint}
    </Constraints>
</Constrained></root>"""

#: Define a template for a constrained data type identifier (is this allowed?)
DATA_DATA_TYPE_IDENTIFIER_TEMPLATE = """
<root><Constrained>
    <DataType>
        <DataTypeIdentifier>TestDataType</DataTypeIdentifier>
    </DataType>
    <Constraints>
        {constraint}
    </Constraints>
</Constrained></root>"""

#: Simple basic constrained type without any constraints
DATA_BASIC = DATA_BASIC_TEMPLATE.format(
    constraint="<!-- we do not define any constraints here -->",
    basic_data_type="Boolean"
)

#: Simple list constrained type without any constraints
DATA_LIST = DATA_LIST_TEMPLATE.format(constraint="<!-- we do not define any constraints here -->")

#: Simple constrained constrained type without any constraints (invalid)
DATA_CONSTRAINED = DATA_CONSTRAINED_TEMPLATE.format(constraint="<!-- we do not define any constraints here -->")

#: Simple constrained structure type without any constraints (invalid)
DATA_STRUCTURE = DATA_STRUCTURE_TEMPLATE.format(constraint="<!-- we do not define any constraints here -->")

#: Simple constrained structure type without any constraints (invalid)
DATA_DATA_TYPE_IDENTIFIER = DATA_DATA_TYPE_IDENTIFIER_TEMPLATE.format(
    constraint="<!-- we do not define any constraints here -->"
)

#: Template for length constraints
DATA_CONSTRAINT_LENGTH_TEMPLATE = """
<Length>{length}</Length>
"""

#: Length constraint
DATA_CONSTRAINT_LENGTH = DATA_CONSTRAINT_LENGTH_TEMPLATE.format(length=42)

#: Template for minimal length constraint
DATA_CONSTRAINT_LENGTH_MINIMAL_TEMPLATE = """
<MinimalLength>{length}</MinimalLength>
"""

#: Minimal length constraint
DATA_CONSTRAINT_LENGTH_MINIMAL = DATA_CONSTRAINT_LENGTH_MINIMAL_TEMPLATE.format(length=42)

#: Template for maximal length constraint
DATA_CONSTRAINT_LENGTH_MAXIMAL_TEMPLATE = """
<MaximalLength>{length}</MaximalLength>
"""

#: Maximal length constraint
DATA_CONSTRAINT_LENGTH_MAXIMAL = DATA_CONSTRAINT_LENGTH_MAXIMAL_TEMPLATE.format(length=42)

#: Enumeration constraint
DATA_CONSTRAINT_SET = """
<Set>
    <Value>A</Value>
    <Value>B</Value>
    <Value>C</Value>
</Set>
"""

#: Pattern constraint
DATA_CONSTRAINT_PATTERN = """
<Pattern>[a-zA-Z0-9_]</Pattern>
"""

#: Maximal value constraint (exclusive)
DATA_CONSTRAINT_VALUE_MAXIMAL_EXCLUSIVE = """
<MaximalExclusive>42</MaximalExclusive>
"""

#: Maximal value constraint (inclusive)
DATA_CONSTRAINT_VALUE_MAXIMAL_INCLUSIVE = """
<MaximalInclusive>42</MaximalInclusive>
"""

#: Minimal value constraint (exclusive)
DATA_CONSTRAINT_VALUE_MINIMAL_EXCLUSIVE = """
<MinimalExclusive>42</MinimalExclusive>
"""

#: Minimal value constraint (inclusive)
DATA_CONSTRAINT_VALUE_MINIMAL_INCLUSIVE = """
<MinimalInclusive>42</MinimalInclusive>
"""

#: Unit constraint
DATA_CONSTRAINT_UNIT = """
<Unit>
    <Label>Unit-Label</Label>
    <UnitComponent>
        <SIUnit>Dimensionless</SIUnit>
        <Exponent>1</Exponent>
        <Factor>1</Factor>
        <Offset>0</Offset>
    </UnitComponent>
</Unit>
"""

#: Content type constraint (supported type/subtype)
DATA_CONSTRAINT_CONTENT_TYPE = """
<ContentType>
    <Type>application</Type>
    <Subtype>xml</Subtype>
    <Parameters>
        <Parameter>
            <Attribute>charset</Attribute>
            <Value>utf-8</Value>
        </Parameter>
        <Parameter>
            <Attribute>parameter</Attribute>
            <Value>value</Value>
        </Parameter>
    </Parameters>
</ContentType>
"""

#: Content type constraint (unsupported)
DATA_CONSTRAINT_CONTENT_TYPE_UNSUPPORTED = """
<ContentType>
    <Type>type</Type>
    <Subtype>subtype</Subtype>
    <!-- no parameters for simplification -->
</ContentType>
"""

#: Template for number of elements constraint
DATA_CONSTRAINT_ELEMENTS_COUNT_TEMPLATE = """
<ElementCount>{number}</ElementCount>
"""

#: Number of elements constraint
DATA_CONSTRAINT_ELEMENTS_COUNT = DATA_CONSTRAINT_ELEMENTS_COUNT_TEMPLATE.format(number=42)

#: Template for minimal number of elements constraint
DATA_CONSTRAINT_ELEMENTS_MINIMAL_TEMPLATE = """
<MinimalElementCount>{number}</MinimalElementCount>
"""

#: Minimal number of elements constraint
DATA_CONSTRAINT_ELEMENTS_MINIMAL = DATA_CONSTRAINT_ELEMENTS_MINIMAL_TEMPLATE.format(number=42)

#: Template for maximal number of elements constraint
DATA_CONSTRAINT_ELEMENTS_MAXIMAL_TEMPLATE = """
<MaximalElementCount>{number}</MaximalElementCount>
"""

#: Maximal number of elements constraint
DATA_CONSTRAINT_ELEMENTS_MAXIMAL = DATA_CONSTRAINT_ELEMENTS_MAXIMAL_TEMPLATE.format(number=42)

#: Template for the identifier constraint
DATA_CONSTRAINT_IDENTIFIER_TEMPLATE = """
<FullyQualifiedIdentifier>{identifier}</FullyQualifiedIdentifier>
"""

#: Identifier constraint
DATA_CONSTRAINT_IDENTIFIER = DATA_CONSTRAINT_IDENTIFIER_TEMPLATE.format(identifier='FeatureIdentifier')

#: Template for the schema constraint
DATA_CONSTRAINT_SCHEMA_TEMPLATE = """
<Schema>
    <Type>{type}</Type>
    {data}
</Schema>
"""

#: Schema constraint
DATA_CONSTRAINT_SCHEMA = DATA_CONSTRAINT_SCHEMA_TEMPLATE.format(
    type='Xml',
    data='<Url>http://www.w3.org/2001/XMLSchema</Url>'
)