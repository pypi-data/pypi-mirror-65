"""This module defines xml-data that can be used to test the Command class"""

#: A simple command that contains only a parameter and a response
DATA_SIMPLE = """
<root><Command>
    <Identifier>CommandIdentifier</Identifier>
    <DisplayName>Command Name</DisplayName>
    <Description>Simple, unobservable command without any complex elements</Description>
    <Observable>No</Observable>
    <Parameter>
        <Identifier>ParameterIdentifier</Identifier>
        <DisplayName>Parameter Identifier</DisplayName>
        <Description>A random parameter definition.</Description>
        <DataType>
            <Basic>Boolean</Basic>
        </DataType>
    </Parameter>
    <Response>
        <Identifier>ResponseIdentifier</Identifier>
        <DisplayName>Response Identifier</DisplayName>
        <Description>A random response definition.</Description>
        <DataType>
            <Basic>Boolean</Basic>
        </DataType>
    </Response>
</Command></root>"""

#: A command that does not require a parameter
DATA_EMPTY_PARAMETER = """
<root><Command>
    <Identifier>CommandIdentifier</Identifier>
    <DisplayName>Command Name</DisplayName>
    <Description>Simple, unobservable command without any parameters</Description>
    <Observable>No</Observable>
    <Response>
        <Identifier>ResponseIdentifier</Identifier>
        <DisplayName>Response Identifier</DisplayName>
        <Description>A random response definition.</Description>
        <DataType>
            <Basic>Boolean</Basic>
        </DataType>
    </Response>
</Command></root>"""

#: A command that does not issue any response
DATA_EMPTY_RESPONSE = """
<root><Command>
    <Identifier>CommandIdentifier</Identifier>
    <DisplayName>Command Name</DisplayName>
    <Description>Simple, unobservable command without any responses</Description>
    <Observable>No</Observable>
    <Parameter>
        <Identifier>ParameterIdentifier</Identifier>
        <DisplayName>Parameter Identifier</DisplayName>
        <Description>A random parameter definition.</Description>
        <DataType>
            <Basic>Boolean</Basic>
        </DataType>
    </Parameter>
</Command></root>"""

#: A command that issues neither a response nor requires a parameter
DATA_EMPTY_BOTH = """
<root><Command>
    <Identifier>CommandIdentifier</Identifier>
    <DisplayName>Command Name</DisplayName>
    <Description>Simple, unobservable command without parameters and responses</Description>
    <Observable>No</Observable>
</Command></root>"""

#: A simple command that is defined as observable
DATA_OBSERVABLE = """
<root><Command>
    <Identifier>CommandIdentifier</Identifier>
    <DisplayName>Command Name</DisplayName>
    <Description>Simple, observable command without any complex elements</Description>
    <Observable>Yes</Observable>
    <Parameter>
        <Identifier>ParameterIdentifier</Identifier>
        <DisplayName>Parameter Identifier</DisplayName>
        <Description>A random parameter definition.</Description>
        <DataType>
            <Basic>Boolean</Basic>
        </DataType>
    </Parameter>
    <Response>
        <Identifier>ResponseIdentifier</Identifier>
        <DisplayName>Response Identifier</DisplayName>
        <Description>A random response definition.</Description>
        <DataType>
            <Basic>Boolean</Basic>
        </DataType>
    </Response>
</Command></root>"""

#: Data to check on intermediate responses
DATA_OBSERVABLE_INTERMEDIATE = """
<root><Command>
    <Identifier>CommandIdentifier</Identifier>
    <DisplayName>Command Name</DisplayName>
    <Description>Simple, observable command without any complex elements</Description>
    <Description>Simple, observable command without any complex elements</Description>
    <Observable>Yes</Observable>
    <IntermediateResponse>
        <Identifier>IntermediateIdentifier</Identifier>
        <DisplayName>Intermediate Identifier</DisplayName>
        <Description>A random intermediate response definition.</Description>
        <DataType>
            <Basic>Boolean</Basic>
        </DataType>
    </IntermediateResponse>
</Command></root>"""

#: A command containing an intermediate response while being not observable, this is not allowed
DATA_UNOBSERVABLE_INTERMEDIATE = """
<root><Command>
    <Identifier>CommandIdentifier</Identifier>
    <DisplayName>Command Name</DisplayName>
    <Description>Simple, observable command without any complex elements</Description>
    <Observable>No</Observable>
    <IntermediateResponse>
        <Identifier>IntermediateIdentifier</Identifier>
        <DisplayName>Intermediate Identifier</DisplayName>
        <Description>A random intermediate response definition.</Description>
        <DataType>
            <Basic>Boolean</Basic>
        </DataType>
    </IntermediateResponse>
</Command></root>"""

#: Defines an input for a command that contains three parameter
DATA_MULTIPLE_PARAMETER = """
<root><Command>
    <Identifier>CommandIdentifier</Identifier>
    <DisplayName>Command Name</DisplayName>
    <Description>Simple, unobservable command with multiple parameters</Description>
    <Observable>No</Observable>
    <Parameter>
        <Identifier>ParameterIdentifier1</Identifier>
        <DisplayName>1. Parameter Identifier</DisplayName>
        <Description>A random parameter definition (Parameter 1).</Description>
        <DataType>
            <Basic>Boolean</Basic>
        </DataType>
    </Parameter>
    <Parameter>
        <Identifier>ParameterIdentifier2</Identifier>
        <DisplayName>2. Parameter Identifier</DisplayName>
        <Description>A random parameter definition (Parameter 2).</Description>
        <DataType>
            <Basic>Boolean</Basic>
        </DataType>
    </Parameter>
    <Parameter>
        <Identifier>ParameterIdentifier3</Identifier>
        <DisplayName>3. Parameter Identifier</DisplayName>
        <Description>A random parameter definition (Parameter 3).</Description>
        <DataType>
            <Basic>Boolean</Basic>
        </DataType>
    </Parameter>
    <Response>
        <Identifier>ResponseIdentifier</Identifier>
        <DisplayName>Response Identifier</DisplayName>
        <Description>A random response definition.</Description>
        <DataType>
            <Basic>Boolean</Basic>
        </DataType>
    </Response>
</Command></root>"""

#: Defines an input for a command that contains three responses
DATA_MULTIPLE_RESPONSES = """
<root><Command>
    <Identifier>CommandIdentifier</Identifier>
    <DisplayName>Command Name</DisplayName>
    <Description>Simple, unobservable command with multiple responses</Description>
    <Observable>Yes</Observable>
    <Parameter>
        <Identifier>ParameterIdentifier</Identifier>
        <DisplayName>Parameter Identifier</DisplayName>
        <Description>A random parameter definition.</Description>
        <DataType>
            <Basic>Boolean</Basic>
        </DataType>
    </Parameter>
    <Response>
        <Identifier>ResponseIdentifier1</Identifier>
        <DisplayName>1. Response Identifier</DisplayName>
        <Description>A random response definition (Response 1).</Description>
        <DataType>
            <Basic>Boolean</Basic>
        </DataType>
    </Response>
    <Response>
        <Identifier>ResponseIdentifier2</Identifier>
        <DisplayName>2. Response Identifier</DisplayName>
        <Description>A random response definition (Response 2).</Description>
        <DataType>
            <Basic>Boolean</Basic>
        </DataType>
    </Response>
    <Response>
        <Identifier>ResponseIdentifier3</Identifier>
        <DisplayName>3. Response Identifier</DisplayName>
        <Description>A random response definition (Response 3).</Description>
        <DataType>
            <Basic>Boolean</Basic>
        </DataType>
    </Response>
</Command></root>"""

#: Have some defined execution errors that can occur while executing the command
DATA_DEFINED_EXECUTION_ERRORS = """
<root><Command>
    <Identifier>CommandIdentifier</Identifier>
    <DisplayName>Command Name</DisplayName>
    <Description>Simple, unobservable command with defined execution errors defined</Description>
    <Observable>No</Observable>
    <Parameter>
        <Identifier>ParameterIdentifier</Identifier>
        <DisplayName>Parameter Identifier</DisplayName>
        <Description>A random parameter definition.</Description>
        <DataType>
            <Basic>Boolean</Basic>
        </DataType>
    </Parameter>
    <Response>
        <Identifier>ResponseIdentifier</Identifier>
        <DisplayName>Response Identifier</DisplayName>
        <Description>A random response definition.</Description>
        <DataType>
            <Basic>Boolean</Basic>
        </DataType>
    </Response>
    <DefinedExecutionErrors>
        <Identifier>ExecutionError1</Identifier>
        <Identifier>ExecutionError2</Identifier>
        <Identifier>ExecutionError3</Identifier>
    </DefinedExecutionErrors>
</Command></root>"""