import os
from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtWidgets import QAction
from qgis.core import QgsMessageLog, Qgis
from .interface import CalcularComprimentoDialog

class CalcularComprimentoViasAvancado:
    def __init__(self, iface):
        self.iface = iface
        self.action = None
        self.dialog = None

    def initGui(self):
        icon_path = os.path.join(os.path.dirname(__file__), 'icons', 'icon.png')
        self.action = QAction(QIcon(icon_path), "Calcular Comprimento das Vias - Avançado", self.iface.mainWindow())
        self.action.triggered.connect(self.run)
        self.iface.addPluginToMenu("Calcular Comprimento das Vias - Avançado", self.action)
        QgsMessageLog.logMessage("Plugin carregado.", "CalcularComprimento", Qgis.Info)

    def unload(self):
        self.iface.removePluginMenu("Calcular Comprimento das Vias - Avançado", self.action)
        QgsMessageLog.logMessage("Plugin descarregado.", "CalcularComprimento", Qgis.Info)

    def run(self):
        if not self.dialog:
            self.dialog = CalcularComprimentoDialog(self.iface)
        self.dialog.show()
