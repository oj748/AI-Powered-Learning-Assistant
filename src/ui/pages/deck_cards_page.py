from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QPushButton,
    QTableWidget,
    QTableWidgetItem, QMessageBox,
    QHeaderView, QAbstractItemView, QHBoxLayout, QMenu, QApplication, QStyle
)

from PySide6.QtCore import Qt

from database.flashcard_repository import (
    get_flashcards_for_deck, delete_flashcards
)


class DeckCardsPage(QWidget):

    def __init__(self):
        super().__init__()

        self.deck_id = None

        self.setup_ui()

    def setup_ui(self):

        layout = QVBoxLayout(self)

        # =====================================
        # Back Button
        # =====================================

        self.back_btn = QPushButton("← Back")

        # DELETE BUTTON
        self.delete_btn = QPushButton("Delete Selected")
        self.delete_btn.setObjectName("dangerButton")
        self.delete_btn.setEnabled(False)

        self.delete_btn.setIcon(
            QApplication.style().standardIcon(QStyle.SP_TrashIcon)
        )

        toolbar = QHBoxLayout()

        toolbar.addWidget(self.back_btn)

        toolbar.addStretch()

        toolbar.addWidget(self.delete_btn)

        layout.addLayout(toolbar)

        # =====================================
        # Title
        # =====================================

        self.title_label = QLabel("Deck")
        self.title_label.setAlignment(Qt.AlignCenter)

        font = self.title_label.font()
        font.setPointSize(20)
        font.setBold(True)

        self.title_label.setFont(font)

        layout.addWidget(self.title_label)

        # =====================================
        # Table
        # =====================================

        self.table = QTableWidget()

        self.table.setColumnCount(9)

        self.table.setHorizontalHeaderLabels([
            "ID",
            "Question",
            "Answer",
            "Interval",
            "Ease",
            "Reviews",
            "Last Review",
            "Next Review",
            "Created"
        ])

        self.table.setEditTriggers(
            QTableWidget.NoEditTriggers
        )

        self.table.setSelectionBehavior(
            QAbstractItemView.SelectRows
        )

        self.table.setSelectionMode(
            QAbstractItemView.ExtendedSelection
        )

        self.table.setHorizontalScrollMode(
            QTableWidget.ScrollPerPixel
        )

        self.table.setHorizontalScrollBarPolicy(
            Qt.ScrollBarAsNeeded
        )
        self.table.setSortingEnabled(True)

        self.table.setAlternatingRowColors(True)

        self.table.setWordWrap(False)

        self.table.verticalHeader().setVisible(False)

        header = self.table.horizontalHeader()

        header.setSectionResizeMode(
            QHeaderView.Interactive
        )
        header.setSectionsMovable(True)

        self.table.setCornerButtonEnabled(False)

        self.table.setShowGrid(True)

        self.table.setGridStyle(Qt.SolidLine)

        self.table.setColumnWidth(0, 60)  # ID
        self.table.setColumnWidth(1, 300)  # Question
        self.table.setColumnWidth(2, 350)  # Answer
        self.table.setColumnWidth(3, 80)
        self.table.setColumnWidth(4, 80)
        self.table.setColumnWidth(5, 80)
        self.table.setColumnWidth(6, 160)
        self.table.setColumnWidth(7, 160)
        self.table.setColumnWidth(8, 160)

        self.table.setContextMenuPolicy(
            Qt.CustomContextMenu
        )

        self.table.customContextMenuRequested.connect(
            self.show_context_menu
        )

        layout.addWidget(self.table)


        self.table.itemSelectionChanged.connect(
            self.update_delete_button
        )

        self.delete_btn.clicked.connect(
            self.delete_selected_cards
        )

    def load_deck(
            self,
            deck_id,
            deck_name
    ):
        self.deck_id = deck_id

        self.title_label.setText(
            f"{deck_name} Flashcards"
        )

        cards = get_flashcards_for_deck(
            deck_id
        )
        self.table.setSortingEnabled(False)
        self.table.setRowCount(len(cards))

        for row, card in enumerate(cards):

            values = [
                card[0],                     # id
                card[2],                     # front
                card[3],                     # back
                card[4],                     # interval
                f"{card[5]:.2f}",            # ease
                card[6],                     # reviews
                card[7] or "",
                card[8] or "",
                card[9] or ""
            ]

            for column, value in enumerate(values):

                item = QTableWidgetItem()

                if column == 0:
                    item.setData(Qt.DisplayRole, int(value))
                else:
                    item.setData(Qt.DisplayRole, value)

                item.setFlags(
                    item.flags() &
                    ~Qt.ItemIsEditable
                )

                self.table.setItem(
                    row,
                    column,
                    item
                )
        self.table.setSortingEnabled(True)
        self.table.verticalHeader().setDefaultSectionSize(28)

    def update_delete_button(self):

        self.delete_btn.setEnabled(
            len(self.table.selectionModel().selectedRows()) > 0)

    def show_context_menu(self, pos):

        if not self.table.selectionModel().selectedRows():
            return

        menu = QMenu(self)

        delete_action = menu.addAction("🗑 Delete Selected")

        chosen = menu.exec(
            self.table.viewport().mapToGlobal(pos)
        )

        if chosen == delete_action:
            self.delete_selected_cards()

    def delete_selected_cards(self):

        rows = self.table.selectionModel().selectedRows()

        if not rows:
            return

        flashcard_ids = []

        for row in rows:
            item = self.table.item(row.row(), 0)

            flashcard_ids.append(
                int(item.text())
            )

        count = len(flashcard_ids)

        message = (
            "Delete this flashcard?"
            if count == 1
            else f"Delete {count} selected flashcards?"
        )

        reply = QMessageBox.question(
            self,
            "Delete Flashcards",
            message,
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )

        if reply != QMessageBox.Yes:
            return

        delete_flashcards(flashcard_ids)

        # Reload the table
        self.load_deck(
            self.deck_id,
            self.title_label.text().replace(" Flashcards", "")
        )