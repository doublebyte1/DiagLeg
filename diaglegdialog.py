# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DiagLegDialog
                                 A QGIS plugin
 Diagram Legend Plugin
                             -------------------
        begin                : 2013-06-18
        copyright            : (C) 2013 by Joana Simoes/FAO
        email                : info@doublebyte.net
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtXml import *
from qgis.core import *
from qgis.utils import iface
from qgis.gui import *

import tempfile
# initialize Qt resource
import resources
from ui_diagleg import Ui_DiagLeg
#from ui_about import Ui_aboutDlg

from __init__ import *


# create the dialog for zoom to point
class DiagLegDialog(QDialog):

    def __init__(self):
        QDialog.__init__(self)
        # Set up the user interface from Designer.
        self.ui = Ui_DiagLeg()
        self.ui.setupUi(self)
        self.ui.textEdit.clear()
        self.ui.frame.setVisible(False)
                
        scene=QGraphicsScene()
        scene.setBackgroundBrush(QBrush(QColor(255,255,255)));
	self.ui.view.setScene(scene)
  
    def saveDoc(self, strFileName):                
      doc=self.ui.textEdit.document()
      writer=QTextDocumentWriter()	
      
      if strFileName == "":
       return
      
      fi=QFileInfo(strFileName)   
      if fi.suffix() == "html":      
	writer.setFormat("html")	
	writer.setFileName(strFileName)	
	writer.write(doc)	
      elif fi.suffix() == "png":
	img=QImage(self.ui.view.scene().width(),self.ui.view.scene().height(),6);
	p=QPainter(img);
	self.ui.view.scene().render(p);
	p.end(); 
	img.save(strFileName);
      else:
	QMessageBox.critical(self, QString("DiagLeg"),
				  QString("Sorry: Unsupported format!"),
				  QMessageBox.Ok
				  );
	return      
        
    def readBrush(self, node, str):      
	child = node.firstChild()      
	r=0
	g=0
	b=0
	while not child.isNull():
	  ok=True
	  if child.toElement().tagName() == "brush":
	    if (child.attributes().contains("red")):
	      r=child.attributes().namedItem("red").toAttr().value()
	    else:
	      ok=False
	    if (child.attributes().contains("green")):
	      g=child.attributes().namedItem("green").toAttr().value()
	    else:
	      ok=False
	    if (child.attributes().contains("blue")):
	      b=child.attributes().namedItem("blue").toAttr().value()
	    else:
	      ok=False
	      
	    str+="<td style=\"background-color:rgb("
	    str+=QString(QVariant(r).toString() + "," + QVariant(g).toString() + "," + QVariant(b).toString())
	    str+=");color:white;font-style:bold;\">"#col
	    #if (ok):
	      #str+= QString("rgb(" + QVariant(r).toString() + ", " + QVariant(g).toString() + ", " + QVariant(b).toString() +")")#col
	    #else:
	       #str+="error" #n.b.: it should never come here!
	    str+="</td>"#col

	  child = child.nextSibling()
	  	  
	  
    def readFactory(self, node, listFields):
	child = node.firstChild()

	str=QString()
	str+="<table border=\"0\" cellpadding=\"5\" cellspacing=\"0\" width=\"80%\">"
	
	str+="<tr width=5%><th></th><th align=\"left\">Class</th></tr>"
	
	while not child.isNull():
	  if child.toElement().tagName() == "category":      
	    if (child.attributes().contains("attribute")):
	      str+="<tr>"#line	      

	      self.readBrush(child,str)	      	      	      
	      str+="<td>"#col	     
	      index=child.attributes().namedItem("attribute").toAttr().value()
	      idx = int(index)
	      strField=listFields.__getitem__ (idx)
	      str+=strField
	      str+="</td>"#col	      	      
	      
	      str+="</tr>"#line	      
	  child = child.nextSibling()

	str+="</table>"
	self.ui.textEdit.insertHtml(str)
	
	graphics=QGraphicsTextItem();
	graphics.setHtml(str);
	self.ui.view.scene().addItem(graphics)
	graphics.adjustSize()

	
    def readOverlay(self, node, listFields):
	child = node.firstChild()      
	while not child.isNull():
	  if child.toElement().tagName() == "factory":
	    self.readFactory(child, listFields)
	  child = child.nextSibling()    	    
	      
	return

    def populateFromDOM(self, dom, listFields):
      root = dom.documentElement()
      if root.tagName() != "qgis":
	raise ValueError, "not a style XML file"
      
#      clear(False)
	
      node = root.firstChild()
      while not node.isNull():
	if node.toElement().tagName() == "overlay":
	  self.readOverlay(node,listFields)
	node = node.nextSibling()    
	    
      return
	  
    def importDOM(self, fname, listFields):
      dom = QDomDocument() 
      error = None
      fh = None
      try:
	fh = QFile(fname)
	if not fh.open(QIODevice.ReadOnly):
	  raise IOError, unicode(fh.errorString())
	if not dom.setContent(fh):
	  raise ValueError, "could not parse XML"
	
      except (IOError, OSError, ValueError),e:
	error = "Failed to import: %s" % e 	
      finally:
	if fh is not None:
	  fh.close()
	  if error is not None:
	    return False, error
      try:
	self.populateFromDOM(dom,listFields)
		
      except ValueError, e:
	return False, "Failed to import: %s" % e
	self._fname = QString()
	self._dirty = True

      #self.ui.textEdit.insertHtml(QFileInfo(fname).fileName())	  		
      return True, QFileInfo(fname).fileName()
  
    def onOk(self):
      self.ui.textEdit.clear()
      self.ui.view.scene().clear()

            
      aLayer = iface.activeLayer()   
      
      if aLayer is None:
	QMessageBox.warning(self, QString("DiagLeg"),
				  QString("Please select a Layer and try again!"),
				  QMessageBox.Ok
				  );
	return
      
      provider = aLayer.dataProvider()
      	
      listFields=QStringList()
      fields = aLayer.pendingFields()
      i=0 #imagine they come always in alphabetical order
      for field in fields.itervalues():            
	#self.ui.textEdit.insertHtml(QVariant(i).toString() + ", " )      
	#self.ui.textEdit.insertHtml(field.name() + "<br>")
	listFields.append( field.name())
	i=i+1

      #First we create the system temp to get the name, and then a .qml created by Qgis when it saved the style
      f = tempfile.NamedTemporaryFile(delete=True)      
      aLayer.saveNamedStyle(f.name);
                  
      strTmp=f.name+".qml"      
      #self.ui.textEdit.insertHtml(strTmp + "<br>")      
      #self.ui.textEdit.insertHtml(f.name + "<br>")      
      
      self.importDOM(strTmp,listFields)      
      #self.importDOM("/home/joana/git/GISforEAF/scenarios/vms/test/sales_fishground.qml",listFields)
      
      #Remember to delete both files!
      f.close()
      b=QFile(strTmp).remove()
      
      #self.saveDoc()

    def onExport(self):  
    
      if self.ui.textEdit.toPlainText().isEmpty():
	QMessageBox.warning(self, QString("DiagLeg"),
				  QString("There is nothing to export! Please generate a legend, first"),
				  QMessageBox.Ok
				  );
	return
      
      filename = QFileDialog.getSaveFileName(self, "Save file", QDir.tempPath(), "Images (*.png);;Webpages (*.html)")      
      self.saveDoc(filename)
      
    def onAbout(self):     
	QMessageBox.about(self, "About DiagLeg %2.1f..." % appVers , "This plugin was developed in the context of the EAF-Nansen project.<p> The EAF-Nansen Project \"Strengthening the Knowledge Base for and Implementing an Ecosystem Approach to Marine Fisheries in Developing Countries\" (GCP/INT/003/NOR) is an initiative to support the implementation of the ecosystem approach in the management of marine fisheries. The aim is to promote sustainable utilization of marine living resources and improved protection of the marine environment.<p> <a href=\"http://www.eaf-nansen.org/nansen/en\">http://www.eaf-nansen.org/nansen/en</a>");

