from PyQt5.QtCore import pyqtSlot
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QWidget, QMenu, QMessageBox
from caloriestracker.objects.biometrics import BiometricsManager
from caloriestracker.ui.Ui_wdgBiometrics import Ui_wdgBiometrics
from caloriestracker.ui.myqcharts import VCTemporalSeries
from caloriestracker.libmanagers import DateValueManager
from logging import debug
from datetime import date, timedelta

class wdgBiometrics(QWidget, Ui_wdgBiometrics):
    def __init__(self, mem,  parent=None):
        QWidget.__init__(self, parent)
        self.setupUi(self)
        self.mem=mem
        self.biometrics=BiometricsManager(self.mem)
        self.tblBiometrics.setSettings(self.mem.settings, "wdgBiometrics", "tblBiometrics") 
        self.tblBiometrics.table.customContextMenuRequested.connect(self.on_tblBiometrics_customContextMenuRequested)

        self.viewChartHeight=None
        self.viewChartWeight=None
        self.wdgYM.initiate(1900,  date.today().year, date.today().year, date.today().month)
        self.wdgYM.label.hide()
        self.cmbChart.setCurrentIndex(int(self.mem.settings.value("wdgBiometrics/cmbChart_index", 1)))        
        
    @pyqtSlot() 
    def on_wdgYM_changed(self):
        self.update()

    def update(self):
        del self.biometrics
        if self.rad20days.isChecked()==False:
            sql=self.mem.con.mogrify("select * from biometrics where users_id=%s and date_part('year',datetime)=%s and date_part('month',datetime)=%s order by datetime", (self.mem.user.id, self.wdgYM.year, self.wdgYM.month ))
        else:
            sql=self.mem.con.mogrify("""
WITH t AS (
    select * from biometrics where users_id=%s order by datetime desc limit 20
)
SELECT * FROM t ORDER BY datetime ASC""", (self.mem.user.id, ))
            
        #Update table
        self.biometrics=BiometricsManager(self.mem, sql, True)
        self.biometrics.myqtablewidget(self.tblBiometrics)
        if self.biometrics.selected==None:#Selects last row if there is no selection
            self.tblBiometrics.table.selectRow(self.biometrics.length()-1)
        
        #Remove old objects
        if self.viewChartHeight!=None:
            self.layHeight.removeWidget(self.viewChartHeight)
            self.viewChartHeight.close()
        if self.viewChartWeight!=None:
            self.layWeight.removeWidget(self.viewChartWeight)
            self.viewChartWeight.close()
        
        #Create new objects
        if self.biometrics.length()>0:
            #Calcula el datefrom
            index=self.cmbChart.currentIndex()
            if index==0:
                self.datefrom= date(1900, 1, 1)
            elif index==1:
                self.datefrom= date.today()-timedelta(days=365)
            elif index==2:
                self.datefrom= date.today()-timedelta(days=365*3)

            #Height chart
            if self.tabWidget.currentIndex()==1:
                self.viewChartHeight=VCHeight()
                self.viewChartHeight.setData(self.mem, self.datefrom)
                self.viewChartHeight.generate()
                self.layHeight.addWidget(self.viewChartHeight)
            
            #Weight chart
            if self.tabWidget.currentIndex()==0:
                self.viewChartWeight=VCWeight()
                self.viewChartWeight.setData(self.mem, self.datefrom)
                self.viewChartWeight.generate()
                self.layWeight.addWidget(self.viewChartWeight)

    def on_tabWidget_currentChanged(self, index):
        self.update()

    @pyqtSlot(int)
    def on_cmbChart_currentIndexChanged(self, index):
        self.update()
        self.mem.settings.setValue("wdgBiometrics/cmbChart_index", index)
        
        
    @pyqtSlot()
    def on_actionBiometricsNew_triggered(self):
        from caloriestracker.ui.frmBiometricsAdd import frmBiometricsAdd
        w=frmBiometricsAdd(self.mem, None, self)
        w.exec_()
        self.update()

    @pyqtSlot()
    def on_actionBiometricsDelete_triggered(self):
        reply = QMessageBox.question(None, self.tr('Asking your confirmation'), self.tr("This action can't be undone.\nDo you want to delete this record?"), QMessageBox.Yes, QMessageBox.No)                  
        if reply==QMessageBox.Yes:
            self.biometrics.selected.delete()
            self.mem.con.commit()
            self.mem.user.load_last_biometrics()
        self.update()

    @pyqtSlot()
    def on_actionBiometricsEdit_triggered(self):
        from caloriestracker.ui.frmBiometricsAdd import frmBiometricsAdd
        w=frmBiometricsAdd(self.mem, self.biometrics.selected, self)
        w.exec_()
        self.update()

    def on_tblBiometrics_itemSelectionChanged(self):
        self.biometrics.cleanSelection()
        for i in self.tblBiometrics.selectedItems():
            if i.column()==0 and i.row()<self.biometrics.length():#only once per row
                self.biometrics.selected=self.biometrics.arr[i.row()]
        debug("Selected meal: {}".format(self.biometrics.selected))

    def on_tblBiometrics_customContextMenuRequested(self,  pos):
        print(pos)
        menu=QMenu()
        menu.addAction(self.actionBiometricsNew)
        menu.addAction(self.actionBiometricsDelete)
        menu.addAction(self.actionBiometricsEdit)
        menu.addSeparator()
        
        if self.biometrics.selected==None:
            self.actionBiometricsDelete.setEnabled(False)
            self.actionBiometricsEdit.setEnabled(False)
        else:
            self.actionBiometricsDelete.setEnabled(True)
            self.actionBiometricsEdit.setEnabled(True)
        menu.addSeparator()
        menu.addMenu(self.tblBiometrics.qmenu())

        menu.exec_(self.tblBiometrics.mapToGlobal(pos))
        
    def on_rad20days_toggled(self, checked):
        self.wdgYM.setEnabled(not self.rad20days.isChecked())
        self.update()

##View chart of an biometrics
class VCWeight(VCTemporalSeries):
    def __init__(self):
        VCTemporalSeries.__init__(self)
        self.setTitle(self.tr("Weight evolution chart"))
        
    def setData(self, mem, date_from):
        self.mem=mem
        sql=self.mem.con.mogrify("""
            select 
                avg(weight), 
                datetime::date 
            from 
                biometrics 
            where 
                users_id=%s and 
                datetime::date>%s 
            group by datetime::date
            order by datetime::date
            """, (self.mem.user.id, date_from))
        weight=DateValueManager()#Date and value
        self.sma_period=30
        for row in self.mem.con.cursor_rows(sql):
            weight.appendDV(row['datetime'],  row['avg'])
        weight_filled=weight.DateValueManager_filling_empty()# Date and value filled
        self.weight=weight_filled.DatetimeValueManager(start=True, timezone=self.mem.localzone)# Datetime aware and value

        self.sma_data_50=self.weight.sma(50)
        self.sma_data_200=self.weight.sma(200)

    ## Just draw the chart with selected options. To update it just close this object and create another one
    def generate(self):
        #Progress dialog 
        self.setProgressDialogEnabled(True)
        self.setProgressDialogAttributes(
                None, 
                self.tr("Loading {} biometric information").format(self.weight.length()), 
                QIcon(":caloriestracker/books.png"), 
                0, 
                self.weight.length()
        )
        weight=self.appendTemporalSeries(self.tr("Weight evolution"))
        sma50=self.appendTemporalSeries(self.tr("Simple movil average {}").format(50))
        sma200=self.appendTemporalSeries(self.tr("Simple movil average {}").format(200))
        for i in range(self.weight.length()):
            #Shows progress dialog
            self.setProgressDialogNumber(i+1)
            #Weight
            self.appendTemporalSeriesData(weight, self.weight.arr[i].datetime, self.weight.arr[i].value)
            #sma
            if i>=50:
                self.appendTemporalSeriesData(sma50, self.sma_data_50.arr[i-50].datetime, self.sma_data_50.arr[i-50].value)
            #sma
            if i>=200:
                self.appendTemporalSeriesData(sma200, self.sma_data_200.arr[i-200].datetime, self.sma_data_200.arr[i-200].value)
        self.display()


##View chart of an biometrics
class VCHeight(VCTemporalSeries):
    def __init__(self):
        VCTemporalSeries.__init__(self)
        self.setTitle(self.tr("Height evolution chart"))
        
    def setData(self, mem, date_from):
        self.mem=mem
        self.sma_period=15
        sql=self.mem.con.mogrify("""
            select 
                max(height), 
                datetime::date 
            from 
                biometrics 
            where 
                users_id=%s and 
                datetime::date>%s 
            group by datetime::date
            order by datetime::date
            """, (self.mem.user.id, date_from))
        height=DateValueManager()
        for row in self.mem.con.cursor_rows(sql):
            height.appendDV(row['datetime'],   row['max'])
        height_filled=height.DateValueManager_filling_empty()# Date and value filled
        self.height_=height_filled.DatetimeValueManager(start=True, timezone=self.mem.localzone)# Datetime aware and value. It has height_ to do not conlict con QWidget.height()
        self.sma_data=self.height_.sma(self.sma_period)

    ## Just draw the chart with selected options. To update it just close this object and create another one
    def generate(self):
        #Progress dialog 
        self.setProgressDialogEnabled(True)
        self.setProgressDialogAttributes(
                None, 
                self.tr("Loading {} biometric information").format(self.height_.length()), 
                QIcon(":caloriestracker/books.png"), 
                0, 
                self.height_.length()
        )
        height=self.appendTemporalSeries(self.tr("Height evolution"))
        for i in range(self.height_.length()):
            #Shows progress dialog
            self.setProgressDialogNumber(i+1)
            #height
            self.appendTemporalSeriesData(height, self.height_.arr[i].datetime, self.height_.arr[i].value)
        self.display()
