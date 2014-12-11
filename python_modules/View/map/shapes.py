from PyQt5 import QtCore, QtGui



# def getSize ():
#     return {'Triangle': triangleIcon(),'Square': squareIcon(),'Circle': circleIcon()}
    
def getShape (shape,size):
    if shape == 'Triangle':
        return triangle(size*0.5)
    elif shape == 'Square':
        return square (size*0.5)
    elif shape == 'Circle':
        return circle (size*0.5)
    
def triangle (size):
    pts = []
    pts.append(QtCore.QPointF(-size,size))
    pts.append(QtCore.QPointF(0,-2*size))
    pts.append(QtCore.QPointF(size,size))
    return [QtGui.QPolygonF(pts),QtGui.QPolygonF(pts).boundingRect()]
def square (size):
    pts = []
    pts.append(QtCore.QPointF(-size,size))
    pts.append(QtCore.QPointF(0,-2*size))
    pts.append(QtCore.QPointF(size,size))
    return [QtGui.QPolygonF(pts),QtGui.QPolygonF(pts).boundingRect()]    
    
def circle (size):
    pts = []
    pts.append(QtCore.QPointF(-size,size))
    pts.append(QtCore.QPointF(0,-2*size))
    pts.append(QtCore.QPointF(size,size))
    return [QtGui.QPolygonF(pts),QtGui.QPolygonF(pts).boundingRect()]


# def getNewPixmap (size):
#     pixmap = QtGui.QPixmap(size,size)
#     pixmap.fill (QtGui.QColor(0,0,0,0))
#     
# def getNewPainter (pixmap, size):
#     
# def 