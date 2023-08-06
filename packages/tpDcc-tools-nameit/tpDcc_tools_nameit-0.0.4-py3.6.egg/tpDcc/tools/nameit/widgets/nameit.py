#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Manager that controls the naming convention used on rigging tools
"""

from __future__ import print_function, division, absolute_import

# TODO: When changing a token name, check the list of expressions and update them if an expression was already
#  using that token

import os
import traceback
from functools import partial

from Qt.QtCore import *
from Qt.QtWidgets import *

import lucidity

import tpDcc
from tpDcc.libs.qt.core import base
from tpDcc.libs.qt.widgets import dividers

from tpDcc.tools.nameit.core import lib

logger = tpDcc.LogsMgr().get_logger('tpDcc-tools-nameit')


class NameIt(base.BaseWidget, object):

    ACTIVE_RULE = None
    NAMING_LIB = lib.NameItLib

    def __init__(self, data_file=None, parent=None):
        self._data_file = None
        super(NameIt, self).__init__(parent=parent)
        self.set_data_file(data_file)

    @classmethod
    def get_active_rule(cls):

        """
        Returns the current naming active rule
        """

        return cls.NAMING_LIB().active_rule()

    @classmethod
    def set_active_rule(cls, name):
        """
        Sets the current active rule
        :param name: str
        """

        # First, we clean the status of the naming library
        cls.NAMING_LIB().remove_all_tokens()
        cls.NAMING_LIB().remove_all_rules()

        cls.NAMING_LIB().load_session()

        # Load rules from the naming manager
        rules = cls.NAMING_LIB().rules
        for rule in rules:
            expressions = rule.get_expression_tokens()
            cls.NAMING_LIB().add_rule(rule.name, rule.iterator_format, *expressions)

        # Load tokens from the naming manager
        tokens = cls.NAMING_LIB().tokens
        for token in tokens:
            tokens_keywords = token.get_values_as_keyword()
            cls.NAMING_LIB().add_token(token.name, **tokens_keywords)

        cls.NAMING_LIB().set_active_rule(name)

    @classmethod
    def set_active_rule_iterator(cls, iterator_format):
        active_rule = cls.get_active_rule()
        if not active_rule:
            return

    @classmethod
    def set_active_rule_auto_fix(cls, auto_fix):
        active_rule = cls.get_active_rule()
        if not active_rule:
            return

        cls.NAMING_LIB().set_rule_auto_fix(active_rule.name(), auto_fix)

    @classmethod
    def solve(cls, *args, **kwargs):
        if len(args) > 0 and len(kwargs) > 0:
            return cls.NAMING_LIB().solve(*args, **kwargs)
        else:
            if len(args) > 0:
                return cls.NAMING_LIB().solve(*args)
            else:
                return cls.NAMING_LIB().solve(**kwargs)

    def ui(self):
        super(NameIt, self).ui()

        toolbar = QToolBar('Main ToolBar')
        toolbar.setMovable(True)
        toolbar.setAllowedAreas(Qt.TopToolBarArea | Qt.BottomToolBarArea)
        self.main_layout.addWidget(toolbar)

        refresh_icon = tpDcc.ResourcesMgr().icon('refresh')
        refresh_btn = QToolButton()
        refresh_btn.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        refresh_action = QAction(refresh_icon, 'Refresh', refresh_btn)
        refresh_btn.setDefaultAction(refresh_action)
        refresh_btn.clicked.connect(self._on_refresh)
        toolbar.addWidget(refresh_btn)

        save_icon = tpDcc.ResourcesMgr().icon('save')
        save_btn = QToolButton()
        save_btn.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        save_action = QAction(save_icon, 'Save', save_btn)
        save_btn.setDefaultAction(save_action)
        save_btn.clicked.connect(self._on_save)
        toolbar.addWidget(save_btn)

        if self._is_renamer_tool_available():
            rename_icon = tpDcc.ResourcesMgr().icon('rename')
            renamer_btn = QToolButton()
            renamer_btn.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
            run_tasks_action = QAction(rename_icon, 'Renamer', renamer_btn)
            renamer_btn.setDefaultAction(run_tasks_action)
            renamer_btn.clicked.connect(self._on_open_renamer_tool)
            toolbar.addWidget(renamer_btn)

        self._name_file_line = QLineEdit()
        self._name_file_line.setReadOnly(True)
        toolbar.addWidget(self._name_file_line)

        base_layout = QHBoxLayout()
        base_layout.setContentsMargins(0, 0, 0, 0)
        base_layout.setSpacing(0)
        self.main_layout.addLayout(base_layout)

        left_panel_widget = QWidget()
        left_panel_widget.setFixedWidth(310)
        left_panel_layout = QVBoxLayout()
        left_panel_layout.setContentsMargins(5, 0, 5, 0)
        left_panel_widget.setLayout(left_panel_layout)
        base_layout.addWidget(left_panel_widget)

        # Tab Widget
        rules_tab = QWidget()
        tokens_tab = QWidget()
        templates_tab = QWidget()
        templates_tokens_tab = QWidget()

        self.tabs = QTabWidget()
        self.tabs.addTab(rules_tab, 'Rules')
        self.tabs.addTab(tokens_tab, 'Tokens')
        self.tabs.addTab(templates_tab, 'Templates')
        self.tabs.addTab(templates_tokens_tab, 'Templates Tokens')
        left_panel_layout.addWidget(self.tabs)

        # Rules Tab
        rules_main_layout = QVBoxLayout()
        rules_main_layout.setContentsMargins(5, 5, 5, 5)
        rules_main_layout.setSpacing(0)
        self.rules_list = QListWidget()
        rules_main_layout.addWidget(self.rules_list)
        left_panel_buttons_layout_rules = QHBoxLayout()
        left_panel_buttons_layout_rules.setContentsMargins(5, 5, 5, 0)
        rules_main_layout.addLayout(left_panel_buttons_layout_rules)
        self.add_rule_btn = QPushButton('+')
        self.remove_rule_btn = QPushButton('-')
        left_panel_buttons_layout_rules.addItem(QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Minimum))
        left_panel_buttons_layout_rules.addWidget(self.add_rule_btn)
        left_panel_buttons_layout_rules.addItem(QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Minimum))
        left_panel_buttons_layout_rules.addWidget(self.remove_rule_btn)
        left_panel_buttons_layout_rules.addItem(QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Minimum))
        rules_tab.setLayout(rules_main_layout)

        # Tokens Tab
        tokens_main_layout = QVBoxLayout()
        tokens_main_layout.setContentsMargins(5, 5, 5, 5)
        tokens_main_layout.setSpacing(0)
        self.tokens_list = QListWidget()
        tokens_main_layout.addWidget(self.tokens_list)
        left_panel_buttons_layout_tokens = QHBoxLayout()
        left_panel_buttons_layout_tokens.setContentsMargins(5, 5, 5, 0)
        tokens_main_layout.addLayout(left_panel_buttons_layout_tokens)
        self.add_token_btn = QPushButton('+')
        self.remove_token_btn = QPushButton('-')
        left_panel_buttons_layout_tokens.addItem(QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Minimum))
        left_panel_buttons_layout_tokens.addWidget(self.add_token_btn)
        left_panel_buttons_layout_tokens.addItem(QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Minimum))
        left_panel_buttons_layout_tokens.addWidget(self.remove_token_btn)
        left_panel_buttons_layout_tokens.addItem(QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Minimum))
        tokens_tab.setLayout(tokens_main_layout)

        # Templates Tab
        templates_main_layout = QVBoxLayout()
        templates_main_layout.setContentsMargins(5, 5, 5, 5)
        templates_main_layout.setSpacing(0)
        self.templates_list = QListWidget()
        templates_main_layout.addWidget(self.templates_list)
        left_panel_buttons_layout_templates = QHBoxLayout()
        left_panel_buttons_layout_templates.setContentsMargins(5, 5, 5, 0)
        templates_main_layout.addLayout(left_panel_buttons_layout_templates)
        self.add_template_btn = QPushButton('+')
        self.remove_template_btn = QPushButton('-')
        left_panel_buttons_layout_templates.addItem(QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Minimum))
        left_panel_buttons_layout_templates.addWidget(self.add_template_btn)
        left_panel_buttons_layout_templates.addItem(QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Minimum))
        left_panel_buttons_layout_templates.addWidget(self.remove_template_btn)
        left_panel_buttons_layout_templates.addItem(QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Minimum))
        templates_tab.setLayout(templates_main_layout)

        # Template Tokens Tab
        templates_tokens_main_layout = QVBoxLayout()
        templates_tokens_main_layout.setContentsMargins(5, 5, 5, 5)
        templates_tokens_main_layout.setSpacing(0)
        self.template_tokens_list = QListWidget()
        templates_tokens_main_layout.addWidget(self.template_tokens_list)
        left_panel_buttons_layout_templates_tokens = QHBoxLayout()
        left_panel_buttons_layout_templates_tokens.setContentsMargins(5, 5, 5, 0)
        templates_tokens_main_layout.addLayout(left_panel_buttons_layout_templates_tokens)
        self.add_template_token_btn = QPushButton('+')
        self.remove_template_token_btn = QPushButton('-')
        left_panel_buttons_layout_templates_tokens.addItem(
            QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Minimum))
        left_panel_buttons_layout_templates_tokens.addWidget(self.add_template_token_btn)
        left_panel_buttons_layout_templates_tokens.addItem(
            QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Minimum))
        left_panel_buttons_layout_templates_tokens.addWidget(self.remove_template_token_btn)
        left_panel_buttons_layout_templates_tokens.addItem(
            QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Minimum))
        templates_tokens_tab.setLayout(templates_tokens_main_layout)

        # === PROPERTIES === #
        main_group = QGroupBox('Properties')
        base_layout.addWidget(main_group)
        self.group_layout = QVBoxLayout()
        self.group_layout.setContentsMargins(5, 5, 5, 5)
        self.group_layout.setSpacing(0)
        main_group.setLayout(self.group_layout)

        # Rules Panel
        self.rules_widget = QWidget()
        rules_layout = QVBoxLayout()
        self.rules_widget.setLayout(rules_layout)
        expression_layout = QHBoxLayout()
        expression_layout.setContentsMargins(5, 5, 5, 5)
        expression_layout.setSpacing(5)
        expression_lbl = QLabel('Expression:  ')
        self.expression_line = QLineEdit()
        self.expression_btn = QPushButton('   <')
        self.expression_btn.setEnabled(False)
        self.expression_btn.setStyleSheet("QPushButton::menu-indicator{image:url(none.jpg);}")
        self.expression_menu = QMenu(self)
        self.expression_btn.setMenu(self.expression_menu)
        expression_layout.addWidget(expression_lbl)
        expression_layout.addWidget(self.expression_line)
        expression_layout.addWidget(self.expression_btn)
        rules_layout.addLayout(expression_layout)

        iterator_layout = QHBoxLayout()
        iterator_layout.setContentsMargins(5, 5, 5, 5)
        iterator_layout.setSpacing(5)
        iterator_lbl = QLabel('Iterator:         ')
        self.iterator_cbx = QComboBox()
        self.iterator_cbx.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        for it_format in ['@', '@^', '#', '##', '###', '####', '#####']:
            self.iterator_cbx.addItem(it_format)
        iterator_layout.addWidget(iterator_lbl)
        iterator_layout.addWidget(self.iterator_cbx)
        rules_layout.addLayout(iterator_layout)

        description_rule_layout = QHBoxLayout()
        description_rule_layout.setContentsMargins(5, 5, 5, 5)
        description_rule_layout.setSpacing(5)
        description_rule_lbl_layout = QVBoxLayout()
        description_rule_lbl = QLabel('Description: ')
        description_rule_lbl.setAlignment(Qt.AlignTop)
        description_rule_layout.addWidget(description_rule_lbl)
        self.description_rule_text = QTextEdit()
        description_rule_layout.addLayout(description_rule_lbl_layout)
        description_rule_layout.addWidget(self.description_rule_text)
        rules_layout.addLayout(description_rule_layout)
        rules_layout.addItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Minimum))
        self.group_layout.addWidget(self.rules_widget)

        # Tokens Panel
        self.tokens_widget = QWidget()
        tokens_layout = QVBoxLayout()
        self.tokens_widget.setLayout(tokens_layout)
        values_layout = QHBoxLayout()
        values_layout.setContentsMargins(5, 5, 5, 5)
        values_layout.setSpacing(5)
        valuesLbl = QLabel('Values: ')
        values_layout.addWidget(valuesLbl)
        values_layout.addItem(QSpacerItem(25, 20, QSizePolicy.Minimum, QSizePolicy.Minimum))
        data = {'key': [], 'value': []}
        self.values_table = TokensTable(data, 0, 2)
        values_layout.addWidget(self.values_table)
        self.values_table.setColumnWidth(0, 140)
        self.values_table.setColumnWidth(1, 140)
        self.values_table.setFixedWidth(300)
        values_buttons_layout = QVBoxLayout()
        values_buttons_layout.setContentsMargins(5, 5, 5, 0)
        values_layout.addLayout(values_buttons_layout)
        self.add_key_value_btn = QPushButton('+')
        self.remove_key_value_btn = QPushButton('-')
        values_buttons_layout.addWidget(self.add_key_value_btn)
        values_buttons_layout.addItem(QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Minimum))
        values_buttons_layout.addWidget(self.remove_key_value_btn)
        values_buttons_layout.addItem(QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Minimum))
        default_layout = QHBoxLayout()
        default_layout.setContentsMargins(5, 5, 5, 5)
        default_layout.setSpacing(5)
        default_lbl = QLabel('Default: ')
        self.default_cbx = QComboBox()
        self.default_cbx.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Maximum)
        default_layout.addWidget(default_lbl)
        default_layout.addItem(QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Minimum))
        default_layout.addWidget(self.default_cbx)
        description_token_layout = QHBoxLayout()
        description_token_layout.setContentsMargins(5, 5, 5, 5)
        description_token_layout.setSpacing(5)
        description_tokens_lbl = QLabel('Description: ')
        self.description_token_text = QTextEdit()
        description_token_layout.addWidget(description_tokens_lbl)
        description_token_layout.addWidget(self.description_token_text)
        tokens_layout.addLayout(values_layout)
        tokens_layout.addLayout(default_layout)
        tokens_layout.addLayout(description_token_layout)
        self.group_layout.addWidget(self.tokens_widget)
        self.tokens_widget.hide()

        # Templates Panel
        self.templates_widget = QWidget()
        templates_layout = QVBoxLayout()
        self.templates_widget.setLayout(templates_layout)
        pattern_layout = QHBoxLayout()
        pattern_layout.setContentsMargins(5, 5, 5, 5)
        pattern_layout.setSpacing(5)
        pattern_lbl = QLabel('Pattern: ')
        self.pattern_line = QLineEdit()
        pattern_layout.addWidget(pattern_lbl)
        pattern_layout.addWidget(self.pattern_line)
        templates_layout.addLayout(pattern_layout)
        templates_layout.addLayout(dividers.DividerLayout())
        self.template_tokens_layout = QGridLayout()
        self.template_tokens_layout.setAlignment(Qt.AlignTop)
        template_tokens_frame = QFrame()
        template_tokens_frame.setFrameShape(QFrame.StyledPanel)
        template_tokens_frame.setFrameShadow(QFrame.Sunken)
        template_tokens_frame.setLayout(self.template_tokens_layout)
        templates_layout.addWidget(template_tokens_frame)
        self.group_layout.addWidget(self.templates_widget)
        self.templates_widget.hide()

        # Templates Tokens Panel
        self.templates_tokens_widget = QWidget()
        templates_tokens_layout = QVBoxLayout()
        self.templates_tokens_widget.setLayout(templates_tokens_layout)
        description_templates_token_layout = QHBoxLayout()
        description_templates_token_layout.setContentsMargins(5, 5, 5, 5)
        description_templates_token_layout.setSpacing(5)
        description_tokens_layout = QVBoxLayout()
        description_templates_token_lbl = QLabel('Description: ')
        description_tokens_layout.addWidget(description_tokens_lbl)
        description_tokens_layout.addItem(QSpacerItem(0, 10, QSizePolicy.Preferred, QSizePolicy.Expanding))
        self.description_templates_token_text = QTextEdit()
        description_templates_token_layout.addLayout(description_tokens_layout)
        description_templates_token_layout.addWidget(self.description_templates_token_text)
        templates_tokens_layout.addLayout(description_templates_token_layout)
        self.group_layout.addWidget(self.templates_tokens_widget)
        self.templates_tokens_widget.hide()

        # Initialize database
        self._init_db()

        # First update of the UI
        self.update_expression_menu()
        self.update_tokens_properties_state()
        self.update_rules_properties_state()
        self.update_templates_properties_state()

    def setup_signals(self):
        super(NameIt, self).setup_signals()

        self.tabs.currentChanged.connect(self._on_change_tab)
        self.add_rule_btn.clicked.connect(self._on_add_rule)
        self.remove_rule_btn.clicked.connect(self._on_remove_rule)
        self.rules_list.currentItemChanged.connect(self._on_change_rule)
        self.rules_list.itemChanged.connect(self._on_edit_rule_name)
        self.expression_line.textChanged.connect(self._on_edit_rule_expression)
        self.description_rule_text.textChanged.connect(self._on_edit_rule_description)
        self.iterator_cbx.currentIndexChanged.connect(self._on_edit_rule_iterator)
        self.add_token_btn.clicked.connect(self._on_add_token)
        self.remove_token_btn.clicked.connect(self._on_remove_token)
        self.tokens_list.currentItemChanged.connect(self._on_change_token)
        self.tokens_list.itemChanged.connect(self._on_edit_token_name)
        self.values_table.itemChanged.connect(self._on_change_token_value)
        self.add_key_value_btn.clicked.connect(self._on_add_token_value)
        self.remove_key_value_btn.clicked.connect(self._on_remove_token_value)
        self.description_token_text.textChanged.connect(self._on_edit_token_description)
        self.default_cbx.currentIndexChanged.connect(self._on_edit_token_default)
        self.add_template_btn.clicked.connect(self._on_add_template)
        self.remove_template_btn.clicked.connect(self._on_remove_template)
        self.templates_list.currentItemChanged.connect(self._on_change_template)
        self.templates_list.itemChanged.connect(self._on_edit_template_name)
        self.pattern_line.textChanged.connect(self._on_edit_template_pattern)
        self.add_template_token_btn.clicked.connect(self._on_add_template_token)
        self.remove_template_token_btn.clicked.connect(self._on_remove_template_token)
        self.template_tokens_list.currentItemChanged.connect(self._on_change_template_token)
        self.template_tokens_list.itemChanged.connect(self._on_edit_template_token_name)
        self.description_templates_token_text.textChanged.connect(self._on_edit_template_token_description)

    def set_data_file(self, data_file):
        """
        Sets the data file used by the naming library
        :param data_file: str
        """

        self._data_file = data_file if data_file and os.path.isfile(data_file) else self._get_default_data_file()
        self.NAMING_LIB().naming_file = self._data_file
        self._init_db()

    def add_expression(self, name):

        """
        Add an expression to the list of expressions
        :param str name: Expression name
        :return: None
        """

        if self.expression_line.text() == '':
            self.expression_line.setText('{' + name + '}')
        else:
            self.expression_line.setText(self.expression_line.text() + '_{' + name + '}')

    def update_expression_menu(self):

        """
        Updates the expression menu
        :return:
        """

        # First, we clear the expression menu
        self.expression_menu.clear()

        tokens = self.NAMING_LIB().tokens
        if tokens and len(tokens) > 0:
            self.expression_btn.setEnabled(True)
            for token in tokens:
                self.expression_menu.addAction(token.name, partial(self.add_expression, token.name))
        else:
            self.expression_btn.setEnabled(False)

    def update_expression_state(self):
        # TODO: This method is used to check the name of the expression (its different parts) and
        # TODO: check if some token of the expression does not exist and in that case, update the expression
        # TODO: so it becomes a valid expression
        pass

    def update_rules_properties_state(self):
        if self.rules_list.count() <= 0 or self.rules_list.currentItem() is None:
            self.expression_line.setText('')
            self.description_rule_text.setText('')
            self.iterator_cbx.setCurrentIndex(0)
            self.rules_widget.setEnabled(False)
        else:
            rule = self.NAMING_LIB().get_rule(self.rules_list.currentItem().text())
            if rule is not None:
                self.expression_line.setText(rule.expression)
                self.description_rule_text.setText(rule.description)
                self.iterator_cbx.setCurrentText(rule.iterator_format)
                self.rules_widget.setEnabled(True)

    def update_tokens_properties_state(self):
        if self.tokens_list.currentItem() is None:
            self.tokens_widget.setEnabled(False)
        else:
            self.tokens_widget.setEnabled(True)

    def update_default_token_list(self):

        self.default_cbx.blockSignals(True)

        for i in range(self.default_cbx.count()):
            self.default_cbx.removeItem(self.default_cbx.count() - 1)

        item_text = self.tokens_list.currentItem().text()
        self.default_cbx.addItem('')
        tokens = self.NAMING_LIB().tokens
        for token in tokens:
            if token.name != item_text:
                continue
            for value in token.values['key']:
                self.default_cbx.addItem(value)

        token = self.NAMING_LIB().get_token(item_text)
        if token:
            self.default_cbx.setCurrentIndex(token.default)

        self.default_cbx.blockSignals(False)

    def update_tokens_key_table(self):

        item_text = self.tokens_list.currentItem().text()
        self.clean_tokens_key_table()
        if self.tokens_list.count() > 0:
            keys = []
            values = []
            tokens = self.NAMING_LIB().tokens
            for token in tokens:
                if token.name != item_text:
                    continue
                for i in range(len(token.values['key'])):
                    self.values_table.insertRow(self.values_table.rowCount())
                    keys.append(QTableWidgetItem())
                    values.append(QTableWidgetItem())

                for index, value in enumerate(token.values['key']):
                    keys[index].setText(value)
                    self.values_table.setItem(index, 0, keys[index])

                for index, value in enumerate(token.values['value']):
                    values[index].setText(value)
                    self.values_table.setItem(index, 1, values[index])

    def clean_tokens_key_table(self):
        for i in range(self.values_table.rowCount()):
            self.values_table.removeRow(self.values_table.rowCount() - 1)

    def update_templates_properties_state(self):
        if self.templates_list.count() <= 0 or self.templates_list.currentItem() is None:
            self.pattern_line.setText('')
            self.templates_widget.setEnabled(False)
        else:
            template = self.NAMING_LIB().get_template(self.templates_list.currentItem().text())
            if template is not None:
                self.pattern_line.setText(template.pattern)
                self.templates_widget.setEnabled(True)
                self._update_template_tokens(template)

    def _init_db(self):

        """
        Initializes the naming data base
        """

        self.NAMING_LIB().init_naming_data()
        self._init_data()
        self._name_file_line.setText(str(self.NAMING_LIB().naming_file))

    def _init_data(self):
        if self._load_rules():
            self._load_tokens()
        self._load_templates()
        self._load_template_tokens()

    def _get_default_data_file(self):
        """
        Internal function that returns default path to nameing data file
        :return: str
        """

        return os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'data', 'naming_data.json')

    def _load_rules(self):

        """
        Internal function that load rules from data file
        """

        self.rules_list.clear()

        rules = self.NAMING_LIB().rules
        if not rules:
            return False

        for rule in rules:
            if rule == '_active':
                continue
            self._on_add_rule(rule)

        return True

    def _load_tokens(self):

        """
        Load tokens from data file
        """

        self.tokens_list.clear()

        tokens = self.NAMING_LIB().tokens
        if not tokens:
            return False

        for token in tokens:
            self._on_add_token(token)

        return True

    def _load_templates(self):
        """
        Internal function that loads templates from DB
        """

        try:
            templates = self.NAMING_LIB().templates
            self.templates_list.clear()
            if templates is not None:
                for template in templates:
                    self._on_add_template(template)
            return True
        except Exception as e:
            logger.error(
                'Error while loading templates from: {} | {} | {}'.format(self.DATA_FILE, e, traceback.format_exc()))

        return False

    def _load_template_tokens(self):
        """
        Internal function that loads template tokens from DB
        """

        try:
            template_tokens = self.NAMING_LIB().template_tokens
            self.template_tokens_list.clear()
            if template_tokens is not None:
                for template_token in template_tokens:
                    self._on_add_template_token(template_token)
            return True
        except Exception as e:
            logger.error(
                'Error while loading template tokens from: {} | {} | {}'.format(
                    self.DATA_FILE, e, traceback.format_exc()))

        return False

    def _clear_template_tokens(self):
        """
        Intenral function that clears all template tokens from layout
        """

        for i in range(self.template_tokens_layout.count(), -1, -1):
            item = self.template_tokens_layout.itemAt(i)
            if item is None:
                continue
            item.widget().setParent(None)
            self.template_tokens_layout.removeItem(item)

    def _add_template_token(self, template_token_name, template_token_description=None):
        """
        Adds template token to layout
        :param template_token_name: str
        :param template_token_data: dict
        """

        row = 0
        while self.template_tokens_layout.itemAtPosition(row, 0) is not None:
            row += 1

        self.template_tokens_layout.addWidget(QLabel(template_token_name), row, 0)
        self.template_tokens_layout.addWidget(
            QLabel(template_token_description if template_token_description else '< NOT FOUND >'), row, 1)

    def _update_template_tokens(self, template):
        """
        Internal function that updates template tokens currently loaded
        :param template: Template
        """

        if not template:
            return

        temp_tokens = list()
        try:
            temp = self.NAMING_LIB().get_template(template.name)
            # temp = lucidity.Template(template.name, template.pattern)
            temp_template = temp.template
            temp_template.duplicate_placeholder_mode = lucidity.Template.STRICT
            temp_tokens = temp_template.keys()
        except (ValueError, lucidity.error.ResolveError) as exc:
            self._clear_template_tokens()
            return

        template_tokens = self.NAMING_LIB().template_tokens

        self._clear_template_tokens()

        for token in temp_tokens:
            token_found = False
            for template_token in template_tokens:
                if token == template_token.name:
                    self._add_template_token(token, template_token.description)
                    token_found = True

            if not token_found:
                self._add_template_token(token)

    def _on_change_tab(self, tab_index):

        """
        This methods changes the properties tab widgets
        :param tab_index: Index of the current tab (0:rules tab, 1:tokens tab)
        :return: None
        """

        if tab_index == 0:
            self.rules_widget.show()
            self.tokens_widget.hide()
            self.templates_widget.hide()
            self.templates_tokens_widget.hide()
            self.update_expression_menu()
            self.update_expression_state()
        elif tab_index == 1:
            self.rules_widget.hide()
            self.tokens_widget.show()
            self.templates_widget.hide()
            self.templates_tokens_widget.hide()
            self.update_tokens_properties_state()
        elif tab_index == 2:
            self.rules_widget.hide()
            self.tokens_widget.hide()
            self.templates_widget.show()
            self.templates_tokens_widget.hide()
            self.update_templates_properties_state()
        else:
            self.rules_widget.hide()
            self.tokens_widget.hide()
            self.templates_widget.hide()
            self.templates_tokens_widget.show()

    def _on_add_rule(self, *args):

        """
        Creates a new standard rule and add it to the Naming Manager
        :return:
        """

        load_rule = True
        if len(args) == 0:
            load_rule = False

        self.description_rule_text.blockSignals(True)

        rule = None
        if not load_rule:
            rule = self.NAMING_LIB().get_rule_unique_name(name='New_Rule')
        elif load_rule and len(args) == 1:
            rule = args[0].name

        if rule is not None:
            # Create a new item based on the rule name and add it
            item = QListWidgetItem(rule)
            item.setFlags(item.flags() | Qt.ItemIsEditable)
            self.rules_list.addItem(item)

            # Add the data of the rule to our JSON data file
            if len(args) == 0:
                self.NAMING_LIB().add_rule(rule)

            # Update necessary UI Widgets
            if not load_rule:
                self.rules_list.setCurrentItem(item)
            self.update_expression_menu()
            self.update_rules_properties_state()

        self.description_rule_text.blockSignals(False)

    def _on_remove_rule(self):

        """
        Remove the selected rule from the list of rules
        :return: bool, True if the element deletion is successful or False otherwise
        """

        self.description_rule_text.blockSignals(True)

        curr_rule = self.rules_list.currentItem()
        if curr_rule is not None:
            rule_name = self.rules_list.currentItem().text()
            rule = self.NAMING_LIB().get_rule(rule_name)
            if rule is not None:
                self.NAMING_LIB().remove_rule(rule_name)
                self.rules_list.takeItem(self.rules_list.row(self.rules_list.currentItem()))
            self.update_rules_properties_state()

        self.description_rule_text.blockSignals(False)

    def _on_change_rule(self, rule_item):

        """
        Change the selected rule
        :param rule_item: new QListWidgetItem selected
        :return: None
        """

        if rule_item is not None:
            if rule_item.listWidget().count() > 0:
                rule = self.NAMING_LIB().get_rule(rule_item.text())
                if rule is not None:
                    self.description_rule_text.setText(rule.description)
                    self.expression_line.setText(rule.expression)
                    self.iterator_cbx.setCurrentText(rule.iterator_format)
                    self.update_expression_menu()
                    self.update_rules_properties_state()

    def _on_edit_rule_name(self, rule_item):

        """
        Changes name of the rule
        :param rule_item: Renamed QListWidgetItem
        :return: None
        """

        rule_index = rule_item.listWidget().currentRow()
        rule = self.NAMING_LIB().get_rule_by_index(rule_index)
        if rule:
            rule.name = rule_item.text()

    def _on_edit_rule_expression(self):

        """
        Changes expression of the selected rule
        :return: None
        """

        selected_rule = self.rules_list.currentItem()
        if not selected_rule:
            return
        rule_name = selected_rule.text()
        rule = self.NAMING_LIB().get_rule(rule_name)
        if rule:
            rule.expression = self.expression_line.text()

    def _on_edit_rule_description(self):

        """
        Changes description of the selected rule
        :return: None
        """

        rule_name = self.rules_list.currentItem().text()
        rule = self.NAMING_LIB().get_rule(rule_name)
        if rule:
            rule.description = self.description_rule_text.toPlainText()

    def _on_edit_rule_iterator(self, iterator_index):
        """
        Changes iterator of the selected rule
        :param iterator_index: int
        :return: None
        """

        rule_name = self.rules_list.currentItem().text()
        rule = self.NAMING_LIB().get_rule(rule_name)
        if rule:
            rule.iterator_format = self.iterator_cbx.itemText(iterator_index)

    def _on_add_token(self, *args):

        """
        Creates a new token and add it to the Naming Manager
        :return: None
        """

        load_token = True
        if len(args) == 0:
            load_token = False

        token = None
        if not load_token:
            token = self.NAMING_LIB().get_token_unique_name(name='New_Token')
        elif load_token and len(args) == 1:
            token = args[0].name

        if token:
            # Create a new item based on the token name and add it
            item = QListWidgetItem(token)
            item.setFlags(item.flags() | Qt.ItemIsEditable)
            self.tokens_list.addItem(item)

            # Add the data of the token to our JSON data file
            if len(args) == 0:
                self.NAMING_LIB().add_token(token)

            # Update necessary UI wigdets
            if not load_token:
                self.tokens_list.setCurrentItem(item)

    def _on_remove_token(self):

        """
        Remove the selected token from the list of tokens
        :return: True if the element deletion is successfull or False otherwise
        """

        curr_token = self.tokens_list.currentItem()
        if curr_token is not None:
            token_index = self.tokens_list.currentRow()
            name = self.tokens_list.currentItem().text()
            if token_index > -1 and name is not None:
                token = self.NAMING_LIB().get_token(name)
                if token is not None:
                    if token.name == name:
                        self.NAMING_LIB().remove_token(name)
                        self.tokens_list.takeItem(self.tokens_list.row(self.tokens_list.currentItem()))

    def _on_change_token(self, token_item):

        """
        Change the selected token
        :param token_item: new QListWidgetItem selected
        :return: None
        """

        if token_item is not None:
            if token_item.listWidget().count() > 0:
                token = self.NAMING_LIB().get_token(token_item.text())
                if token:
                    try:
                        self.description_rule_text.blockSignals(True)
                        self.default_cbx.blockSignals(True)
                        self.description_token_text.setText(token.description)
                        self.default_cbx.setCurrentIndex(int(token.default))
                    finally:
                        self.description_rule_text.blockSignals(False)
                        self.default_cbx.blockSignals(False)
                    self.update_tokens_properties_state()
                    self.update_tokens_key_table()
                    self.update_default_token_list()

    def _on_edit_token_name(self, token_item):
        """
        Changes name of the token
        :param token_item: Renamed QListWidgetItem
        :return:
        """

        token_index = self.tokens_list.currentRow()
        token = self.NAMING_LIB().get_token_by_index(token_index)
        if token:
            token.name = token_item.text()

    def _on_change_token_value(self, item):

        """
        Called when we change a token value name
        :return: None
        """

        token_text = self.tokens_list.currentItem().text()
        token = self.NAMING_LIB().get_token(token_text)
        if not token:
            return

        if self.tokens_list.currentRow() > -1 and item.row() > -1:

            if item.column() == 0:
                token.set_token_key(item.row(), item.text())
            else:
                token.set_token_value(item.row(), item.text())

            self.update_default_token_list()

    def _on_add_token_value(self, *args):

        self.description_rule_text.blockSignals(True)

        token_text = self.tokens_list.currentItem().text()
        token = self.NAMING_LIB().get_token(token_text)
        if token:
            key_data = token.add_token_value()
            if key_data:
                self.clean_tokens_key_table()
                keys = list()
                values = list()
                for i in range(len(key_data['key'])):
                    self.values_table.insertRow(self.values_table.rowCount())
                    keys.append(QTableWidgetItem())
                    values.append(QTableWidgetItem())

                for index, value in enumerate(key_data['key']):
                    keys[index].setText(value)
                    self.values_table.setItem(index, 0, keys[index])

                for index, value in enumerate(key_data['value']):
                    values[index].setText(value)
                    self.values_table.setItem(index, 1, values[index])

                self.update_default_token_list()

                # new_index = self.default_cbx.currentIndex() + 2
                # self.default_cbx.setCurrentIndex(new_index)

        self.description_rule_text.blockSignals(False)

    def _on_remove_token_value(self):
        """
        Removes a token value from the list of tokens values
        """

        self.description_rule_text.blockSignals(True)

        token_text = self.tokens_list.currentItem().text()
        token = self.NAMING_LIB().get_token(token_text)
        if token:
            key_data = token.remove_token_value(self.values_table.currentRow())
            if key_data:
                self.clean_tokens_key_table()

                keys = list()
                values = list()
                for i in range(len(key_data['key'])):
                    self.values_table.insertRow(self.values_table.rowCount())
                    keys.append(QTableWidgetItem())
                    values.append(QTableWidgetItem())

                for index, value in enumerate(key_data['key']):
                    keys[index].setText(value)
                    self.values_table.setItem(index, 0, keys[index])

                for index, value in enumerate(key_data['value']):
                    values[index].setText(value)
                    self.values_table.setItem(index, 1, values[index])

                self.update_default_token_list()

                new_index = self.default_cbx.currentIndex()
                token.default = new_index
                self.default_cbx.setCurrentIndex(new_index)

        self.description_rule_text.blockSignals(False)

    def _on_edit_token_default(self, index):
        """
        Edits the default token
        :param index: int, index of the token to edit
        """

        token_text = self.tokens_list.currentItem().text()
        token = self.NAMING_LIB().get_token(token_text)
        if token:
            token.default = index

    def _on_edit_token_description(self):
        """
        Edits the token description
        """

        token_text = self.tokens_list.currentItem().text()
        token = self.NAMING_LIB().get_token(token_text)
        if token:
            token.description = self.description_token_text.toPlainText().strip()

    def _on_add_template(self, *args):
        """
        Creates a new template and add it to the Naming Manager
        :return:
        """

        load_template = True
        if len(args) == 0:
            load_template = False

        template = None
        if not load_template:
            template = self.NAMING_LIB().get_template_unique_name('New_Template')
        elif load_template and len(args) == 1:
            template = args[0].name

        if template is not None:
            item = QListWidgetItem(template)
            item.setFlags(item.flags() | Qt.ItemIsEditable)
            self.templates_list.addItem(item)

            if len(args) == 0:
                self.NAMING_LIB().add_template(template)

            if not load_template:
                self.templates_list.setCurrentItem(item)

    def _on_remove_template(self):
        """
        Removes the selected template from the list of templates
        :return: bool, True if the element deletion is successful or False otherwise
        """

        current_template = self.templates_list.currentItem()
        if current_template is not None:
            template_index = self.templates_list.currentRow()
            name = self.templates_list.currentItem().text()
            if template_index > -1 and name is not None:
                template = self.NAMING_LIB().get_template(name)
                if template is not None:
                    if template.name == name:
                        valid_remove = self.NAMING_LIB().remove_template(name)
                        if valid_remove:
                            self.templates_list.takeItem(self.templates_list.row(self.templates_list.currentItem()))

    def _on_change_template(self, template_item):
        """
        Changes the selected template
        :param template_item: new QlistWidgetItem selected
        """

        if not template_item or not template_item.listWidget().count() > 0:
            return

        template_name = template_item.text()
        template = self.NAMING_LIB().get_template(template_name)
        if not template:

            return

        self.pattern_line.setText(template.pattern)

        self.update_templates_properties_state()

    def _on_edit_template_name(self, template_item):
        """
        Changes name of the template
        :param template_item: Renamed QListWidgetItem
        """

        template_index = self.templates_list.currentRow()
        template = self.NAMING_LIB().get_template_by_index(template_index)
        if template:
            template.name = template_item.text()

    def _on_edit_template_pattern(self, pattern_item):
        """
        Changes template pattern
        :param pattern_item:
        """

        template_index = self.templates_list.currentRow()
        template = self.NAMING_LIB().get_template_by_index(template_index)
        if template:
            template.pattern = self.pattern_line.text()
            self._update_template_tokens(template)

    def _on_add_template_token(self, *args):
        """
        Creates a new template token
        :param args:
        :return:
        """

        load_template_token = True
        if len(args) == 0:
            load_template_token = False

        template_token = None
        if not load_template_token:
            template_token = self.NAMING_LIB().get_template_token_unique_name('New_Template_Token')
        elif load_template_token and len(args) == 1:
            template_token = args[0].name

        if template_token is not None:
            item = QListWidgetItem(template_token)
            item.setFlags(item.flags() | Qt.ItemIsEditable)
            self.template_tokens_list.addItem(item)

            if len(args) == 0:
                self.NAMING_LIB().add_template_token(template_token)

            if not load_template_token:
                self.template_tokens_list.setCurrentItem(item)

    def _on_remove_template_token(self):
        """
        Remove the selected template token from the list of template tokens
        :return:
        """

        curr_template_token = self.template_tokens_list.currentItem()
        if curr_template_token is not None:
            template_token_index = self.template_tokens_list.currentRow()
            name = self.template_tokens_list.currentItem().text()
            if template_token_index > -1 and name is not None:
                template = self.NAMING_LIB().get_template_token(name)
                if template.name == name:
                    valid_remove = self.NAMING_LIB().remove_template_token(name)
                    if valid_remove:
                        self.template_tokens_list.takeItem(
                            self.template_tokens_list.row(self.template_tokens_list.currentItem()))

    def _on_change_template_token(self, template_token_item):
        """
        Changes the selected template token
        :param template_item: new QlistWidgetItem selected
        """

        if not template_token_item or not template_token_item.listWidget().count() > 0:
            return

        template_tokien_name = template_token_item.text()
        template_token = self.NAMING_LIB().get_template_token(template_tokien_name)
        if not template_token:
            return

        self.description_templates_token_text.setText(template_token.description)

    def _on_edit_template_token_name(self, token_template_item):
        """
        Changes name of the token
        :param token_template_item: Renamed QListWidgetItem
        :return:
        """

        token_index = self.template_tokens_list.currentRow()
        template_token = self.NAMING_LIB().get_template_token_by_index(token_index)
        if template_token:
            template_token.name = token_template_item.text()

    def _on_edit_template_token_description(self):
        """
        Edits the template token description
        """

        template_token_text = self.template_tokens_list.currentItem().text()
        template_token = self.NAMING_LIB().get_template_token(template_token_text)
        if template_token:
            template_token.description = self.description_templates_token_text.toPlainText().rstrip()

    def _on_open_renamer_tool(self):
        """
        Internal function that is used by toolbar to open Renamer Tool
        """

        try:
            tpDcc.ToolsMgr().launch_tool_by_id('tpDcc-tools-renamer', do_reload=False)
        except Exception:
            logger.warning('tpDcc-tools-renamer is not available!')
            return None

    def _is_renamer_tool_available(self):
        """
        Returns whether or not tpRenamer tool is available or not
        :return: bool
        """

        try:
            import tpDcc.tools.renamer
        except Exception:
            return False

        return True

    def _on_refresh(self):
        """
        Internal function that is called when save button is pressed
        """

        self.NAMING_LIB().load_session()
        self._init_data()

    def _on_save(self):
        """
        Internal function that is called when save button is pressed
        """

        self.NAMING_LIB().save_session()


class ValuesTableModel(QAbstractTableModel, object):
    """
    Base model for the tokens table
    """

    def __init__(self, parent, myList, header, *args):
        super(ValuesTableModel, self).__init__(parent, *args)
        self.my_list = myList
        self.header = header

    def rowCount(self, parent):
        return len(self.my_list)

    def columnCount(self, parent):
        return len(self.my_list[0])

    def data(self, index, role):
        if not index.isValid():
            return None
        elif role != Qt.DisplayRole:
            return None
        return self.my_list[index.row()][index.column()]

    def headerData(self, col, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self.header[col]
        return None


class TokensTable(QTableWidget):
    def __init__(self, data, *args):
        super(TokensTable, self).__init__(*args)
        self.data = data
        self.set_data()
        self.resizeColumnsToContents()
        self.resizeRowsToContents()

    def set_data(self):
        horHeaders = []
        for n, key in enumerate(sorted(self.data.keys())):
            horHeaders.append(key)
            for m, item in enumerate(self.data[key]):
                newItem = QTableWidgetItem(item)
                self.setItem(m, n, newItem)
        self.setHorizontalHeaderLabels(horHeaders)
