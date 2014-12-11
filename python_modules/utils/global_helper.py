# -*- coding: ISO-8859-1 -*-
from PyQt5 import QtGui, QtWidgets
import re
import json


class Singleton( type ):
    """ Singleton metaclass """
    def __init__( cls, name, bases, cls_dict ):
        super( Singleton, cls ).__init__( name, bases, cls_dict )
        cls.instance = None

    def __call__( cls, *args, **kwargs ):
        if cls.instance is None:
            cls.instance = super( Singleton, cls ).__call__( *args, **kwargs )
        return cls.instance

def invert_color( qcolor ):
    ( r, g, b, a ) = qcolor.getRgb()
    return QtGui.QColor( 255 - r, 255 - g, 255 - b, a )

def dd2dm( dd ):
    'Convert decimal degrees to degrees,minutes'
    is_positive = dd >= 0
    dd = abs( dd )
    degrees, minutes = divmod( dd * 60, 60 )
    degrees = degrees if is_positive else -degrees
    return ( degrees, minutes )

def dd2dms( dd ):
    'Convert decimal degrees to degrees,minutes,seconds'
    is_positive = dd >= 0
    dd = abs( dd )
    minutes, seconds = divmod( dd * 3600, 60 )
    degrees, minutes = divmod( minutes, 60 )
    degrees = degrees if is_positive else -degrees
    return ( degrees, minutes, seconds )

def metres2feets( metres ):
    return metres * 3.2808

def metres2nautical_miles( metres ):
    return metres / 1852.0

def pointNearSegment( p1, p2, p, distance_threshold ):
    ' Retourne True si la distance entre le point p et le segment [p1,p2] est < à distance_threshold '
    v1 = QtGui.QVector2D( p1 )
    v2 = QtGui.QVector2D( p2 )
    v = QtGui.QVector2D( p )
    l2 = ( v2 - v1 ).lengthSquared()
    t = QtGui.QVector2D.dotProduct( v - v1, v2 - v1 ) / l2
    if t > 0.0 and t < 1.0:
        # la projection tombe sur le segment
        proj = v1 + t * ( v2 - v1 )
        return ( proj - v ).length() <= distance_threshold
    return False

def camelcase2underscore( s ):
    ss = re.sub( '(.)([A-Z][a-z]+)', r'\1_\2', s )
    return re.sub( '([a-z0-9])([A-Z])', r'\1_\2', ss ).lower()

def underscore2camelcase( s ):
    s = s[0].upper() + s[1:]
    return re.compile( r'_([a-z])' ).sub( lambda x: x.group( 1 ).upper(), s )

def writePrettyXml( element_tree_root, filename ):
    'Take a xml.etree.ElementTree.Element in input and write its tree with a pretty xml formatting'
    import xml.dom.minidom
    import xml.etree.ElementTree
    # remove all the 'tail' elements (represents the leading and trailing spaces from the original file, if applicable)
    for child in element_tree_root.iter():
        child.tail = None
    # parse the xml with minidom and use the prettyxml function
    xml_str = xml.etree.ElementTree.tostring( element_tree_root, encoding="UTF-8" )
    dom = xml.dom.minidom.parseString( xml_str )
    pretty_xml = dom.toprettyxml( encoding="UTF-8" )
    with open( filename, 'w' ) as f:
        f.write( pretty_xml )

def meter2feet( meters ):
    return 3.2808399 * meters


