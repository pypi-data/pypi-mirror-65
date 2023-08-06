
import os
import sys
import datetime
import pathlib

import sqlite3

import usb.core

import escpos.printer as ep
import escpos.constants as epc
import escpos.exceptions

import PyQt5.QtCore as qtc
import PyQt5.QtGui as qtg
import PyQt5.QtWidgets as qtw




motives = {
    "travail": "déplacements entre le domicile et le lieu d’exercice de l’activité professionnelle, lorsqu’ils sont indispensables à l’exercice d’activités ne pouvant être organisées sous forme de télétravail ou déplacements professionnels ne pouvant être différés.",
    "courses": "déplacements pour effectuer des achats de fournitures nécessaires à l’activité professionnelle et des achats de première nécessité dans des établissements dont les activités demeurent autorisées (liste sur gouvernement.fr)",
    "sante": "Consultations et soins ne pouvant être assurés à distance et ne pouvant être différés ; consultations et soins des patients atteints d'une affection de longue durée.",
    "famille": "déplacements pour motif familial impérieux, pour l’assistance aux personnes vulnérables ou la garde d’enfants.",
    "sport": "déplacements brefs, dans la limite d'une heure quotidienne et dans un rayon maximal d'un kilomètre autour du domicile, liés soit à l'activité physique individuelle des personnes, à l'exclusion de toute pratique sportive collective et de toute proximité avec d'autres personnes, soit à la promenade avec les seules personnes regroupées dans un même domicile, soit aux besoins des animaux de compagnie.",
    "judiciaire": "convocation judiciaire ou administrative",
    "missions": "participation à des missions d’intérêt général sur demande de l’autorité administrative."
}

def get_db():

    db_file = pathlib.Path(qtc.QStandardPaths.writableLocation(qtc.QStandardPaths.ConfigLocation)) / "covid19pos.conf"

    db = sqlite3.connect(str(db_file))
    c = db.cursor()
    c.execute("""create table if not exists printer_conf (
        conf_key text PRIMARY KEY,
        conf_value text
    )""")

    c.execute("""create table if not exists peoples (
        name text PRIMARY KEY,
        gender text,
        birthdate text,
        birthplace text,
        address text,
        location text
    )""")

    db.commit()

    return db


def get_printer(dummy=False):

    if dummy:
        return ep.Dummy()

    db = get_db()
    c = db.cursor()
    c.execute("select conf_value from printer_conf where conf_key='usb_major';")
    major = int(c.fetchone()[0], 16)

    c.execute("select conf_value from printer_conf where conf_key='usb_minor';")
    minor = int(c.fetchone()[0], 16)

    c.close()
    p = ep.Usb(major, minor)
    return p


def print_title(p):
    p.set(font="a")
    p.set(align="center", bold=True, custom_size=True, width=2, height=2, smooth=True)
    p.textln("ATTESTATION DE\nDÉPLACEMENT DÉROGATOIRE")
    p.ln()
    p.set(font="b", align="center")
    print_with_prefix(p, "En application de l’article 3 du décret du 23 mars 2020 prescrivant les mesures générales nécessaires pour faire face à l’épidémie de Covid19 dans le cadre de l’état d’urgence sanitaire", max_len=65)
    p.ln(2)
    p.set(align="left", font="a")


def print_personnal_informations(p, params):
    if params["gender"] == "male":
        p.text("Je, soussigné\t")
    else:
        p.text("Je, soussignée\t")

    p.set(bold=True)
    p.text(params["name"])
    p.ln()
    p.set()
    if params["gender"] == "male":
        p.text("Né le\t\t")
    else:
        p.text("Née le\t\t")

    p.set(bold=True)
    p.text(params["birthdate"].strftime("%d/%m/%Y"))
    p.ln()

    p.set()
    p.text("À\t\t")

    p.set(bold=True)
    p.text(params["birthplace"])
    p.ln()

    p.set()
    p.textln("Demeurant")

    p.set(bold=True)
    for line in params["address"].split("\n"):
        p.text("\t\t")
        p.textln(line)
    p.ln()


def format_testimony(text, prefix_len=0, max_len=48):

    words = text.split()
    lines = []
    line = []
    length = prefix_len
    for word in words:
        length += len(word) + 1
        if length > max_len:
            lines.append(" ".join(line))
            length = prefix_len + len(word) + 1
            line = [word]
        else:
            line.append(word)

    lines.append(" ".join(line))
    return lines


def print_with_prefix(p, text, fl_prefix="", max_len=48):
    p.text(fl_prefix)
    for line in format_testimony(text, prefix_len=len(fl_prefix), max_len=max_len):
        p.textln(line)
        p.text(" " * len(fl_prefix))


def print_testimony(p, req_motives):
    p.set()
    print_with_prefix(p, "certifie que mon déplacement est lié au motif suivant autorisé par l’article 3 du décret du 23 mars 2020 prescrivant les mesures générales nécessaires pour faire face à l’épidémie de Covid19 dans le cadre de l’état d’urgence sanitaire :")
    p.ln()

    for motive in req_motives:
        p.set(bold=True)
        print_with_prefix(p, motives[motive], "- ")
        p.ln()

qr_pattern = "Cree le: {qr_creation_date}; Nom: {qr_name}; Prenom: {qr_firstname}; Naissance: {qr_birthdate} a {birthplace}; Adresse: {qr_address}; Sortie: {qr_exit_date}; Motifs: {qr_motives}"


def print_qr(p, params):
    params["qr_exit_date"] = params["exit_date"].strftime("%d/%m/%Y a %Hh%M")
    params["qr_creation_date"] = params["creation_date"].strftime("%d/%m/%Y a %Hh%M")
    params["qr_birthdate"] = params["birthdate"].strftime("%d/%m/%Y")
    params["qr_motives"] = "-".join(params["motives"])
    params["qr_address"] = " ".join(params["address"].split())
    params["qr_name"] = params["name"].split()[-1]
    params["qr_firstname"] = " ".join(params["name"].split()[0:-1])

    qr_text = qr_pattern.format(**params)

    p.set(align="center")
    p.qr(qr_text, ec=epc.QR_ECLEVEL_M, size=6, native=True)
    p.set()
    p.ln()


def print_signature(p, params):
    p.set()
    p.text("Fait à :\t")
    p.set(bold=True)
    p.textln(params["location"])
    p.set(bold=False)

    p.set()
    p.text("Le :\t\t")
    p.set(bold=True)
    p.text(params["exit_date"].strftime("%d/%m/%Y"))
    p.set(bold=False)
    p.text(" à ")
    p.set(bold=True)
    p.textln(params["exit_date"].strftime("%H:%M"))
    p.set(bold=False)

    p.ln()

    p.text("Signature :")
    p.ln(7)
    p.set(bold=True, align="right")
    p.text(params["name"])


class PrinterError(Exception): pass

def print_attestation(params):
    p = get_printer(dummy=True)
    print_title(p)
    print_personnal_informations(p, params)
    print_testimony(p, params["motives"])
    print_qr(p, params)
    print_signature(p, params)
    p.cut()


    rp = get_printer()
    try:
        #if not rp.is_online():
            #raise PrinterError("Imprimante indisponible")

        #if rp.paper_status() == 0:
            #raise PrinterError("Pas de papier dans l'imprimante")
        rp._raw(p.output)
    finally:
        rp.close()




class PeopleDialog(qtw.QDialog):
    def __init__(self, parent):
        super().__init__(parent)

        from .ui_peopleEdit import Ui_peopleDiag

        self.ui = Ui_peopleDiag()
        self.ui.setupUi(self)
        self.accepted.connect(self.ui_ok)

    @qtc.pyqtSlot()
    def on_maleRadio_clicked(self):
        if len(self.ui.buttonBox.buttons()) < 2:
            self.ui.buttonBox.addButton(qtw.QDialogButtonBox.Save)

    @qtc.pyqtSlot()
    def on_femaleRadio_clicked(self):
        self.on_maleRadio_clicked()


    def ui_ok(self):
        db = get_db()
        c = db.cursor()
        c.execute(
            "insert or replace into peoples (name, gender, birthdate, birthplace, address, location) values (?, ?, ?, ?, ?, ?)", (
                self.ui.nameEdit.text(),
                "male" if self.ui.maleRadio.isChecked() else "female",
                self.ui.dateEdit.date().toPyDate(),
                self.ui.birthplaceEdit.text(),
                self.ui.addressEdit.toPlainText(),
                self.ui.locationEdit.text(),
            )
        )

        db.commit()
        self.commited.emit()

    commited = qtc.pyqtSignal()

class MainForm(qtw.QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        from .ui_main import Ui_Form
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.reloadList()

        for button in self.findChild(qtw.QWidget, "motives").children():
            try:
                button.clicked.connect(self.motive_clicked)
            except AttributeError:
                pass

        self.selected_motives = None


    @qtc.pyqtSlot()
    def on_addPeople_clicked(self):
        add_dialog = PeopleDialog(self)
        add_dialog.commited.connect(self.reloadList)
        add_dialog.show()

    @qtc.pyqtSlot()
    def on_delPeople_clicked(self):
        db = get_db()
        c = db.cursor()
        c.execute("delete from peoples where name == ?", (self.ui.peopleBox.currentText(), ))
        self.ui.peopleBox.removeItem(self.ui.peopleBox.currentIndex())
        db.commit()

    @qtc.pyqtSlot()
    def on_confButton_clicked(self):
        major = qtw.QInputDialog.getText(self, "Paramétrage imprimante", "ID USB (majeur)")
        if major[1] is False:
            return
        minor = qtw.QInputDialog.getText(self, "Paramétrage imprimante", "ID USB (mineur)")
        if minor[1] is False:
            return
        set_printer_param(major[0], minor[0])


    def keyPressEvent(self, evt):
        if evt.modifiers() & qtc.Qt.ControlModifier:
            if self.selected_motives is not None:
                return

            self.selected_motives = set()
            for button in self.findChild(qtw.QWidget, "motives").children():
                try:
                    button.setCheckable(True)
                except AttributeError:
                    pass


    def keyReleaseEvent(self, evt):
        if self.selected_motives is None:
            return

        if (evt.modifiers() & qtc.Qt.ControlModifier):
            return

        for button in self.findChild(qtw.QWidget, "motives").children():
            try:
                button.setChecked(False)
                button.setCheckable(False)
            except AttributeError:
                pass


        selected_motives = [m for m in motives if m in self.selected_motives]
        if len(selected_motives) > 0:
            self.print_attestation(selected_motives)

        self.selected_motives = None

    def select_motive(self, motive):
        if qtw.QApplication.keyboardModifiers() & qtc.Qt.ControlModifier:
            if self.sender().isChecked():
                self.selected_motives |= set((motive, ))
            else:
                self.selected_motives -= set((motive, ))
        else:
            self.print_attestation([motive])

    @qtc.pyqtSlot()
    def motive_clicked(self):
        name = self.sender().objectName()
        self.select_motive(name)


    def print_attestation(self, motives):
        db = get_db()
        c = db.cursor()
        c.execute("select gender, birthdate, birthplace, address, location from peoples where name == ?", (self.ui.peopleBox.currentText(), ))
        r = c.fetchone()

        creation_date = datetime.datetime.now();
        exit_date = creation_date + datetime.timedelta(seconds=60*7)

        params = {
            "motives": motives,
            "name": self.ui.peopleBox.currentText(),
            "gender": r[0],
            "birthdate": datetime.datetime.strptime(r[1], "%Y-%m-%d",),
            "birthplace": r[2],
            "address": r[3],
            "location": r[4],
            "exit_date": exit_date,
            "creation_date": creation_date,
        }

        try:
            print_attestation(params)
        except escpos.exceptions.USBNotFoundError as e:
            qtw.QMessageBox.critical(self, "Erreur d'impression", "Erreur lors de l'impression :\n" + e.msg)
        except usb.core.USBError as e:
            qtw.QMessageBox.critical(self, "Erreur de communication", "Erreur lors de l'impression :\n" + e.args[1] )
        except PrinterError as e:
            qtw.QMessageBox.critical(self, "Erreur d'impression", e.args[0])


    @qtc.pyqtSlot()
    def reloadList(self):
        db = get_db()
        c = db.cursor()
        c.execute("select name from peoples")
        self.ui.peopleBox.clear()
        for name in c:
            self.ui.peopleBox.addItem(name[0])


def set_printer_param(major, minor):

    db = get_db()
    db.execute(
        "insert or replace into printer_conf ('conf_key', 'conf_value') values (?, ?), (?, ?);",
        ["usb_major", major, "usb_minor", minor]
    )

    db.commit()



def run_ui():
    qtc.pyqtRemoveInputHook()
    app = qtw.QApplication(sys.argv)
    main_w = MainForm()

    main_w.show()
    return app.exec()


if __name__ == "__main__":
    run_ui()




