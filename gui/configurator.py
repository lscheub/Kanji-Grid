
from aqt.qt import *
from aqt.utils import showInfo
from .base import Dialog

CHECKSTATE_TO_INT = {
    Qt.CheckState.Unchecked: 0,
    Qt.CheckState.PartiallyChecked: 2,
    Qt.CheckState.Checked: 1
}

INT_TO_CHECKSTATE = {
    0: Qt.CheckState.Unchecked,
    2: Qt.CheckState.PartiallyChecked,
    1: Qt.CheckState.Checked
}

class Configurator(Dialog):

    def __init__(self, mw):
        self.mw = mw
        self.mw.addonManager.setConfigAction(__name__, self.show)

        super(Configurator, self).__init__("Configure", self.mw)


    def ui(self):
        layout = super(Configurator, self).ui()
        layout.addLayout(self.panel())
        layout.addWidget(self.ui_buttons())

        return layout


    def panel(self):
        layout = QGridLayout()

        self.decklist = QListWidget()

        self.notetree = QTreeWidget()
        self.notetree.headerItem().setHidden(True)

        self.cols = QLineEdit()
        self.threshold = QLineEdit()

        # row 0
        layout.addWidget(QLabel("Check each deck to scan:"), 0, 0, 1, 4)
        layout.addWidget(QLabel("Check each field to scan:"), 0, 4, 1, 4)


        # row 1-6
        layout.addWidget(self.decklist, 1, 0, 6, 4)
        layout.addWidget(self.notetree, 1, 4, 6, 4)


        # row 7
        layout.addWidget(QLabel(""), 7, 0, 1, 8)


        # row 8
        layout.addWidget(QLabel("Characters per row:"), 8, 0, 1, 3)
        layout.addWidget(self.cols, 8, 3, 1, 5)


        # row 9
        layout.addWidget(QLabel("Number reviews considered strong:"), 9, 0, 1, 3)
        layout.addWidget(self.threshold, 9, 3, 1, 5)


        return layout


    def deck_widget(self):
        decklist = []
        decks = self.mw.col.decks.all()
        config = self.mw.addonManager.getConfig(__name__)

        for deck in decks:
            deck_id = str(deck['id'])
            item = QListWidgetItem(deck['name'])
            item.setFlags(Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsUserCheckable)
            item.setData(Qt.ItemDataRole.UserRole, deck_id)

            if deck_id not in config['decks']:
                config['decks'][deck_id] = True

            item.setCheckState(Qt.CheckState.Checked if config['decks'][deck_id] else Qt.CheckState.Unchecked)
            decklist.append(item)


        self.mw.addonManager.writeConfig(__name__, config)
        return decklist


    def note_widget(self):
        notelist = []
        config = self.mw.addonManager.getConfig(__name__)


        for model in self.mw.col.models.all_names():
            item = QTreeWidgetItem()
            item.setText(0, str(model))
            item.setFlags(Qt.ItemFlag.ItemIsEnabled)

            model_obj = self.mw.col.models.by_name(model)
            note_id = str(model_obj['id'])
            item.setData(0, Qt.ItemDataRole.UserRole, note_id)

            if note_id not in config['notes']:
                config['notes'][note_id] = {}

            for field in model_obj['flds']:
                fname = field['name']
                child = QTreeWidgetItem()
                child.setText(0, fname)
                child.setFlags(Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsUserCheckable)

                if fname not in config['notes'][note_id]:
                    config['notes'][note_id][fname] = True

                child.setCheckState(0, Qt.CheckState.Checked if config['notes'][note_id][fname] else Qt.CheckState.Unchecked)

                item.addChild(child)

            notelist.append(item)

        self.mw.addonManager.writeConfig(__name__, config)
        return notelist


    def metric_config(self):
        config = self.mw.addonManager.getConfig(__name__)

        self.cols.setText(config['cols'])
        self.threshold.setText(config['threshold'])


    def show(self):
        self.decklist.clear()
        for i in self.deck_widget():
            self.decklist.addItem(i)

        self.notetree.clear()
        for i in self.note_widget():
            self.notetree.addTopLevelItem(i)


        self.metric_config()
        super(Configurator, self).show()



    def accept(self):
        config = self.mw.addonManager.getConfig(__name__)

        for i in range(self.decklist.count()):
            item = self.decklist.item(i)
            deck_id = item.data(Qt.ItemDataRole.UserRole)
            #config['decks'][deck_id] = item.checkState()
            config['decks'][deck_id] = CHECKSTATE_TO_INT[item.checkState()]

        for i in range(self.notetree.topLevelItemCount()):
            item = self.notetree.topLevelItem(i)
            note_id = item.data(0, Qt.ItemDataRole.UserRole)


            for c in range(item.childCount()):
                child = item.child(c)
                config['notes'][note_id][child.text(0)] = CHECKSTATE_TO_INT[child.checkState(0)]


        config['cols'] = self.cols.text()
        config['threshold'] = self.threshold.text()



        self.mw.addonManager.writeConfig(__name__, config)
        super(Configurator, self).accept()
