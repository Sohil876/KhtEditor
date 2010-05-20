from PyQt4.QtGui import QScrollArea, QFrame, QWidget, QTextEdit, QHBoxLayout, QPainter, QFont, QFontMetrics, QAbstractKineticScroller

class Frame(QAbstractKineticScroller, QScrollArea):

    class NumberBar(QWidget):

        def __init__(self, *args):
            QWidget.__init__(self, *args)
            self.edit = None
            # This is used to update the width of the control.
            # It is the highest line that is currently visibile.
            self.highest_line = 0
            self.font = QFont('Monospace',10)
        def setTextEdit(self, edit):
            self.edit = edit

        def update(self, *args):
            '''
            Updates the number bar to display the current set of numbers.
            Also, adjusts the width of the number bar if necessary.
            '''
            # The + 4 is used to compensate for the current line being bold.

            #QWidget.fontMetrics didn't exist on current 0.3.0 version of PySide
            #binding. Just a work arround for the moment
            #width = self.fontMetrics().width(str(self.highest_line)) + 4
            #PySide Work Arround
            width = QFontMetrics(self.font).width(str(self.highest_line)) + 4

            if self.width() != width:
                self.setFixedWidth(width)
            QWidget.update(self, *args)

        def paintEvent(self, event):
            contents_y = self.edit.verticalScrollBar().value()
            page_bottom = contents_y + self.edit.viewport().height()
            #QWidget.fontMetrics didn't exist on current 0.3.0 version of PySide
            #binding. Just a work arround for the moment
            #font_metrics = self.fontMetrics()
            #PySide Work Arround
            font_metrics = QFontMetrics(self.font)
            current_block = self.edit.document().findBlock(self.edit.textCursor().position())

            painter = QPainter(self)
            painter.setFont(self.font)

            line_count = 0
            # Iterate over all text blocks in the document.
            block = self.edit.document().begin()
            while block.isValid():
                line_count += 1

                # The top left position of the block in the document
                position = self.edit.document().documentLayout().blockBoundingRect(block).topLeft()

                # Check if the position of the block is out side of the visible
                # area.
                if position.y() > page_bottom:
                    break

                # We want the line number for the selected line to be bold.
                bold = False
                if block == current_block:
                    bold = True
                    font = painter.font()
                    font.setBold(True)
                    painter.setFont(font)

                # Draw the line number right justified at the y position of the
                # line. 3 is a magic padding number. drawText(x, y, text).
                # 4 is a magic number for y under maemo
                painter.drawText(self.width() - font_metrics.width(str(line_count)) - 3, round(position.y()) - contents_y + font_metrics.ascent() + 4, str(line_count))

                # Remove the bold style if it was set previously.
                if bold:
                    font = painter.font()
                    font.setBold(False)
                    painter.setFont(font)

                block = block.next()

            self.highest_line = line_count
            painter.end()

            QWidget.paintEvent(self, event)

    def __init__(self, editor, *args):
        QScrollArea.__init__(self, *args)

        self.edit = editor
        self.setProperty("fingerScrollable", True)     
        self.setProperty("kineticScroller", True)

        self.number_bar = self.NumberBar()
        self.number_bar.setTextEdit(self.edit)

        hbox = QHBoxLayout(self)
        hbox.setSpacing(0)
        hbox.setMargin(0)
        hbox.addWidget(self.number_bar)
        hbox.addWidget(self.edit)
        self.setWidgetResizable(True)
        self.edit.installEventFilter(self)
        self.edit.viewport().installEventFilter(self)
 
    def eventFilter(self, object, event):
        # Update the line numbers for all events on the text edit and the viewport.
        # This is easier than connecting all necessary singals.
        if object in (self.edit, self.edit.viewport()):
            self.number_bar.update()
            return False
        return QScrollArea.eventFilter(object, event)

    def getTextEdit(self):
        return self.edit
