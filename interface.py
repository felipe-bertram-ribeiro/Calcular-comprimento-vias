# -*- coding: utf-8 -*-
import os
from qgis.PyQt.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QComboBox, QPushButton, QPlainTextEdit,
    QFileDialog, QMessageBox
)
from qgis.PyQt.QtCore import Qt, QVariant
from qgis.core import (
    QgsProject, QgsWkbTypes, QgsCoordinateTransform,
    QgsCoordinateReferenceSystem, QgsField, QgsVectorFileWriter,
    QgsVectorLayer, QgsGeometry, QgsMessageLog, Qgis
)

FIELD_NAME = 'comp_km'

class CalcularComprimentoDialog(QDialog):
    def __init__(self, iface):
        super().__init__(iface.mainWindow())
        self.iface = iface
        self.setWindowTitle("Calcular Comprimento das Vias - Avançado")
        self.setFixedSize(450, 400)
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # Layer selection
        self.layout.addWidget(QLabel("Selecione a camada de linhas:"))
        self.layer_combobox = QComboBox()
        self.layout.addWidget(self.layer_combobox)
        self.populate_layers()

        # Buttons
        self.btn_total = QPushButton("Calcular Total Geral")
        self.btn_total.clicked.connect(self.calcular_total)
        self.layout.addWidget(self.btn_total)
        self.btn_cat = QPushButton("Calcular por Categoria")
        self.btn_cat.clicked.connect(self.calcular_por_categoria)
        self.layout.addWidget(self.btn_cat)

        # Results
        self.result_area = QPlainTextEdit()
        self.result_area.setReadOnly(True)
        self.layout.addWidget(self.result_area)

        # Save/Export
        self.btn_save = QPushButton("Salvar Shapefile em UTM")
        self.btn_save.setEnabled(False)
        self.btn_save.clicked.connect(self.salvar_shapefile)
        self.layout.addWidget(self.btn_save)
        self.btn_csv = QPushButton("Exportar CSV por Categoria")
        self.btn_csv.setEnabled(False)
        self.btn_csv.clicked.connect(self.exportar_csv)
        self.layout.addWidget(self.btn_csv)

        self.layer = None
        self.total_length = 0.0
        self.category_data = {}

    def populate_layers(self):
        self.layer_combobox.clear()
        for lyr in QgsProject.instance().mapLayers().values():
            if isinstance(lyr, QgsVectorLayer) and lyr.geometryType() == QgsWkbTypes.LineGeometry:
                self.layer_combobox.addItem(lyr.name(), lyr.id())

    def get_layer(self):
        layer_id = self.layer_combobox.currentData()
        return QgsProject.instance().mapLayer(layer_id) if layer_id else None

    def get_transform(self, layer):
        target = QgsCoordinateReferenceSystem("EPSG:31982")
        if layer.crs() != target:
            return QgsCoordinateTransform(layer.crs(), target, QgsProject.instance())
        return None

    def ensure_field(self):
        if self.layer.fields().indexOf(FIELD_NAME) == -1:
            self.layer.startEditing()
            self.layer.addAttribute(QgsField(FIELD_NAME, QVariant.Double))
            self.layer.commitChanges()

    def calcular_total(self):
        self.layer = self.get_layer()
        if not self.layer:
            QMessageBox.warning(self, "Erro", "Selecione uma camada de linhas.")
            return
        transform = self.get_transform(self.layer)
        self.ensure_field()
        self.layer.startEditing()
        total = 0.0
        for feat in self.layer.getFeatures():
            geom = feat.geometry()
            geom_clone = QgsGeometry(geom)
            if transform:
                geom_clone.transform(transform)
            length_m = geom_clone.length()
            length_km = length_m / 1000.0
            total += length_km
            self.layer.changeAttributeValue(feat.id(), self.layer.fields().indexOf(FIELD_NAME), length_km)
        self.layer.commitChanges()
        self.total_length = total
        msg = f"Total: {total:.3f} km"
        self.result_area.setPlainText(msg)
        self.btn_save.setEnabled(True)
        QgsMessageLog.logMessage("Cálculo total concluído.", "CalcularComprimento", Qgis.Info)

    def calcular_por_categoria(self):
        self.layer = self.get_layer()
        if not self.layer:
            QMessageBox.warning(self, "Erro", "Selecione uma camada de linhas.")
            return
        transform = self.get_transform(self.layer)
        self.ensure_field()
        self.layer.startEditing()
        total = 0.0
        cat_data = {}
        for feat in self.layer.getFeatures():
            geom = feat.geometry()
            geom_clone = QgsGeometry(geom)
            if transform:
                geom_clone.transform(transform)
            length_m = geom_clone.length()
            length_km = length_m / 1000.0
            total += length_km
            self.layer.changeAttributeValue(feat.id(), self.layer.fields().indexOf(FIELD_NAME), length_km)
            highway_cat = feat['highway'] if feat['highway'] else 'desconhecido'
            cat_data[highway_cat] = cat_data.get(highway_cat, 0.0) + length_km
        self.layer.commitChanges()
        self.total_length = total
        self.category_data = cat_data
        text = "Por categoria (highway):\n"
        for k, v in cat_data.items():
            text += f"{k}: {v:.3f} km\n"
        self.result_area.setPlainText(text)
        self.btn_save.setEnabled(True)
        self.btn_csv.setEnabled(True)
        QgsMessageLog.logMessage("Cálculo por categoria concluído.", "CalcularComprimento", Qgis.Info)

    def salvar_shapefile(self):
        save_path, _ = QFileDialog.getSaveFileName(self, "Salvar Shapefile", "", "Shapefile (*.shp)")
        if not save_path:
            return
        if not save_path.lower().endswith('.shp'):
            save_path += '.shp'
        transform = self.get_transform(self.layer)
        options = QgsVectorFileWriter.SaveVectorOptions()
        options.driverName = "ESRI Shapefile"
        options.fileEncoding = "UTF-8"
        if transform:
            options.ct = transform
        error = QgsVectorFileWriter.writeAsVectorFormatV2(self.layer, save_path, QgsProject.instance().transformContext(), options)
        if error[0] == QgsVectorFileWriter.NoError:
            QMessageBox.information(self, "Sucesso", f"Shapefile salvo em: {save_path}\nTotal: {self.total_length:.3f} km")
            QgsMessageLog.logMessage("Shapefile salvo.", "CalcularComprimento", Qgis.Info)
        else:
            QMessageBox.critical(self, "Erro", "Falha ao salvar shapefile.")
            QgsMessageLog.logMessage("Erro ao salvar shapefile.", "CalcularComprimento", Qgis.Critical)

    def exportar_csv(self):
        if not self.category_data:
            QMessageBox.warning(self, "Erro", "Execute cálculo por categoria primeiro.")
            return
        save_path, _ = QFileDialog.getSaveFileName(self, "Exportar CSV", "", "CSV (*.csv)")
        if not save_path:
            return
        if not save_path.lower().endswith('.csv'):
            save_path += '.csv'
        with open(save_path, 'w', encoding='utf-8') as f:
            f.write("categoria,comprimento_km\n")
            for k, v in self.category_data.items():
                f.write(f"{k},{v:.3f}\n")
        QMessageBox.information(self, "Sucesso", f"CSV salvo em: {save_path}")
        QgsMessageLog.logMessage("CSV exportado.", "CalcularComprimento", Qgis.Info)
