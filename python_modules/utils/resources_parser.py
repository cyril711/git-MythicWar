from PyQt5.Qt import QXmlStreamWriter




if __name__ == '__main__':
    xmlReader = QXmlStreamWriter("resources.qrc")
    xmlReader.setAutoFormatting(True);
    xmlReader.writeStartDocument();
     ...
     stream.writeStartElement("bookmark");
     stream.writeAttribute("href", "http://qt.nokia.com/");
     stream.writeTextElement("title", "Qt Home");
     stream.writeEndElement(); // bookmark
     ...
     stream.writeEndDocument();