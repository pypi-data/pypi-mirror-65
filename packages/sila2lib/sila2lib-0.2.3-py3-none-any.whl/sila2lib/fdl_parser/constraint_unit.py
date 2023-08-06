"""
__________________________________________________________________________________________________

:project: SiLA2_python

:details: Module to store ContentType constraints.

:file:    constraint_unit.py
:authors: Timm Severin

:date: (creation)          20190821
:date: (last modification) 20190821

__________________________________________________________________________________________________

**Copyright**:
  This file is provided "AS IS" with NO WARRANTY OF ANY KIND,
  INCLUDING THE WARRANTIES OF DESIGN, MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE.

  For further Information see LICENSE file that comes with this distribution.
__________________________________________________________________________________________________
"""

from typing import List

from enum import Enum


class ConstraintUnit:
    """
    Class to store Unit constraints.

    With the data given in the constraint the unit can be constructed from basic SI units using the following equation:

    :math:`\\text{Unit} = \\prod_{i=1}^n \\left[ f_i^{e_i} \\cdot \\text{SIUnit}_i^{e_i} +
    \\left( o_i \\cdot \\text{SIUnit}_i \\right)^{e_i} \\right]`

    *where for each component:*

    ============== ==========
    factor         :math:`f`
    exponent       :math:`e`
    offset         :math:`o`
    -------------- ----------
    #components    :math:`n`
    ============== ==========

    .. note:: As of writing this documentation the exact conversion equation is still being discussed. Please refer to
              the standards documentation to ensure usage of the correct conversion equation.

    .. todo:: Check conversion equation once finalised in the standard
    """

    #: Label of the unit
    label: str

    # The SI unit(s) the given unit is comprised of as well as conversion information
    unit_components: List['UnitComponent']

    def __init__(self, xml_tree_element):
        """
        Class initialiser.

        :param xml_tree_element: The content of this <Unit>-xml element that contains this constraint.
        """

        self.label = xml_tree_element.Label.text

        self.unit_components = []
        for unit_component in xml_tree_element.UnitComponent:
            self.unit_components.append(UnitComponent(xml_tree_element=unit_component))


class UnitComponent:
    """
    Class to store a single unit component and the conversion of this component to the final unit.

    For information on the conversion see :class:`ConstraintUnit`.
    """

    #: The base unit
    si_unit: 'SIUnit'

    #: Conversion information: Exponent
    exponent: float

    #: Conversion information: Factor
    factor: float

    #: Conversion information: Offset
    offset: float

    def __init__(self, xml_tree_element):
        """
        Class initialiser.

        :param xml_tree_element: The content of a <UnitComponent>-xml element.
        """

        self.si_unit = SIUnit[xml_tree_element.SIUnit.text.upper()]

        self.exponent = float(xml_tree_element.Exponent.text)
        self.factor = float(xml_tree_element.Factor.text)
        self.offset = float(xml_tree_element.Offset.text)


class SIUnit(Enum):
    """
    Enumeration to reference the SIUnits in the separate components.
    """

    DIMENSIONLESS = '-'
    METER = 'm'
    KILOGRAM = 'kg'
    SECOND = 's'
    AMPERE = 'A'
    KELVIN = 'K'
    MOLE = 'mol'
    CANDELA = 'cd'
