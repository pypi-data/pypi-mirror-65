
import os
import sys
import datetime
import pathlib

import sqlite3

import escpos.printer as ep

import PyQt5.QtCore as qtc
import PyQt5.QtGui as qtg
import PyQt5.QtWidgets as qtw




kinds = {
    "work": "déplacements entre le domicile et le lieu d’exercice de l’activité professionnelle, lorsqu’ils sont indispensables à l’exercice d’activités ne pouvant être organisées sous forme de télétravail ou déplacements professionnels ne pouvant être différés.",
    "shopping": "déplacements pour effectuer des achats de fournitures nécessaires à l’activité professionnelle et des achats de première nécessité dans des établissements dont les activités demeurent autorisées (liste sur gouvernement.fr)",
    "health": "Consultations et soins ne pouvant être assurés à distance et ne pouvant être différés ; consultations et soins des patients atteints d'une affection de longue durée.",
    "family": "déplacements pour motif familial impérieux, pour l’assistance aux personnes vulnérables ou la garde d’enfants.",
    "walk": "déplacements brefs, dans la limite d'une heure quotidienne et dans un rayon maximal d'un kilomètre autour du domicile, liés soit à l'activité physique individuelle des personnes, à l'exclusion de toute pratique sportive collective et de toute proximité avec d'autres personnes, soit à la promenade avec les seules personnes regroupées dans un même domicile, soit aux besoins des animaux de compagnie.",
    "police": "convocation judiciaire ou administrative",
    "collective": "participation à des missions d’intérêt général sur demande de l’autorité administrative."
}

def get_db():

    db_file = pathlib.Path(qtc.QStandardPaths.writableLocation(qtc.QStandardPaths.ConfigLocation)) / "covid19pos.conf"
    print(db_file)
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


def get_printer():

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


def print_testimony(p, kind):
    p.set()
    print_with_prefix(p, "certifie que mon déplacement est lié au motif suivant autorisé par l’article 3 du décret du 23 mars 2020 prescrivant les mesures générales nécessaires pour faire face à l’épidémie de Covid19 dans le cadre de l’état d’urgence sanitaire :")
    p.ln()

    p.set(bold=True)
    print_with_prefix(p, kinds[kind], "- ")
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
    p.textln((datetime.datetime.now() + datetime.timedelta(seconds=7 * 60)).strftime("%d/%m/%Y à %H:%M"))
    p.set(bold=False)

    p.ln()

    p.text("Signature :")
    p.ln(7)
    p.set(bold=True, align="right")
    p.text(params["name"])


def print_attestation(params):
    p = get_printer()
    print_title(p)
    print_personnal_informations(p, params)
    print_testimony(p, params["kind"])
    print_signature(p, params)
    p.cut()


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


    @qtc.pyqtSlot()
    def on_work_clicked(self):
        self.print_attestation("work")

    @qtc.pyqtSlot()
    def on_shopping_clicked(self):
        self.print_attestation("shopping")

    @qtc.pyqtSlot()
    def on_health_clicked(self):
        self.print_attestation("health")

    @qtc.pyqtSlot()
    def on_family_clicked(self):
        self.print_attestation("family")

    @qtc.pyqtSlot()
    def on_walk_clicked(self):
        self.print_attestation("walk")

    def print_attestation(self,kind):
        db = get_db()
        c = db.cursor()
        c.execute("select gender, birthdate, birthplace, address, location from peoples where name == ?", (self.ui.peopleBox.currentText(), ))
        r = c.fetchone()
        params = {
            "kind": kind,
            "name": self.ui.peopleBox.currentText(),
            "gender": r[0],
            "birthdate": datetime.datetime.strptime(r[1], "%Y-%m-%d",),
            "birthplace": r[2],
            "address": r[3],
            "location": r[4],
        }
        print_attestation(params)


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




