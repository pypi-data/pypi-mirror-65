"""This module defines xml-data that can be used to test BasicType data types"""

#: define a xml tree for each basic type, use a dictionary to make it easier to access the data in the test
DATA_SILA_STANDARD_TYPES = {
    'Boolean':      """<root><Basic>Boolean</Basic></root>""",
    'Integer':      """<root><Basic>Integer</Basic></root>""",
    'Real':         """<root><Basic>Real</Basic></root>""",
    'String':       """<root><Basic>String</Basic></root>""",
    'Binary':       """<root><Basic>Binary</Basic></root>""",
    'Void':         """<root><Basic>Void</Basic></root>""",
    'Date':         """<root><Basic>Date</Basic></root>""",
    'Time':         """<root><Basic>Time</Basic></root>""",
    'Timestamp':    """<root><Basic>Timestamp</Basic></root>"""
}

#: A separate boolean expression for a simple test where we don't want the whole dictionary
DATA_BOOLEAN = DATA_SILA_STANDARD_TYPES['Boolean']
