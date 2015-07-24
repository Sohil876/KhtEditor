from PyQt4.QtGui import QCompleter, QTextCursor
from PyQt4.QtCore import Qt, SIGNAL
from PyQt4.Qt import QObject
from plugins_api import Plugin
from functools import wraps
import re

# Simple auto-complete plugin for KhtEditor.
# Suggests possible word completions based on the text in the current document.
# It will open a listview on shortcut (CTRL + Space) or on first three character match.
# original source(from http://ninja-ide.org/plugins/5/) modified by SHARP66

class SimpleAutocompleter(Plugin):
    """Simple auto-complete plugin for kht-editor
        that would suggest possible word completions
        based on the text in the current document.
        shortcut key: Ctrl + Space
    """

    capabilities = ['afterKeyPressEvent']
    __version__ = '0.1'

    # end of word
    eow = "~!@#$%^&*()_+{}|:\"<>?,./;'[]\\-="

    def __init__(self):
        self.editor = None
        self.prefix_lenght = 3

    def do_afterKeyPressEvent(self, editor, event):
        """Check for completer activation."""
        is_shortcut = (event.modifiers() == Qt.ControlModifier and
                       event.key() == Qt.Key_Space)
        if not self.editor:
            self.editor = editor
            self.initialize()
        completionPrefix = self.text_under_cursor()
        if completionPrefix is None:
            return
        should_hide = not event.text() or len(completionPrefix) < self.prefix_lenght
        if not is_shortcut and should_hide:
            self.completer.popup().hide()
            return
        else:
            self.update_model()

        if (completionPrefix != self.completer.completionPrefix()):
            self.completer.setCompletionPrefix(completionPrefix)
            popup = self.completer.popup()
            popup.setCurrentIndex(
                self.completer.completionModel().index(0, 0))
        cr = self.editor.cursorRect()
        print cr, dir(cr)
        cr.setWidth(self.completer.popup().sizeHintForColumn(0)
            + self.completer.popup().verticalScrollBar().sizeHint().width())
        self.completer.complete(cr)

    def initialize(self):
        """plugin initializer."""
        self.completer = DocumentCompleter()
        self.completer.setCompletionMode(QCompleter.PopupCompletion)
        self.completer.setCaseSensitivity(Qt.CaseSensitive)
        self._add_completer(self.editor)
        self.completer.setWidget(self.editor)

        QObject.connect(self.completer,
            SIGNAL("activated(const QString&)"), self.insert_completion)

    def _add_completer(self, editor):
        """Set up completer for the editor."""

        # HACK: decorator to avoid editor keypress when activating completion
        def check_completer_activation(completer, function):
            @wraps(function)
            def _inner(event):
                if completer and completer.popup().isVisible():
                    if event.key() in (
                            Qt.Key_Enter,
                            Qt.Key_Return,
                            Qt.Key_Escape,
                            Qt.Key_Tab,
                            Qt.Key_Backtab):
                        event.ignore()
                        return
                return function(event)
            return _inner

        self.editor.keyPressEvent = check_completer_activation(self.completer,
                                                          self.editor.keyPressEvent)
                                                          

    def update_model(self):
        """Update StringList alternatives for the completer."""
        data = self.editor.get_text("sof", "eof")
        current = self.text_under_cursor()
        words = set(re.split('\W+', data))
        if current in words:
            words.remove(current)
        self.completer.model().setStringList(sorted(words))

    def insert_completion(self, completion):
        """Insert chosen completion."""
        tc = self.editor.textCursor()
        extra = len(self.completer.completionPrefix())
        tc.movePosition(QTextCursor.Left)
        tc.movePosition(QTextCursor.EndOfWord)
        tc.insertText(completion[extra:])
        self.editor.setTextCursor(tc)

    def text_under_cursor(self):
        """Return the word under the cursor for possible completion search."""
        if self.editor is not None:
            tc = self.editor.textCursor()
            tc.select(QTextCursor.WordUnderCursor)
            prefix = tc.selectedText()
            if prefix and prefix[0] in self.eow:
                tc.movePosition(QTextCursor.WordLeft, n=2)
                tc.select(QTextCursor.WordUnderCursor)
                prefix = tc.selectedText()
            return prefix
        return None


class DocumentCompleter(QCompleter):
    """StringList Simple Completer."""

    def __init__(self, parent=None):
        words = []
        QCompleter.__init__(self, words, parent)