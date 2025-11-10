import qtawesome as qta
from PyQt6.QtWidgets import (
    QWidget, QTabWidget, QVBoxLayout, QLabel, QFrame, QPushButton,
    QHBoxLayout, QStackedWidget, QSizePolicy
)
from PyQt6.QtCore import Qt, QSize, QPoint, QRect

from config.theme.ui_style import UiStyle
from views.window.title_bar import TitleBar


class Dashboard(QWidget):
    def __init__(self, agents, AgentRegistry):
        super().__init__()

        # === Настройки окна ===
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.Window)
        self.setMouseTracking(True)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.resize(1200, 800)

        # === Служебные поля для drag/resize ===
        self._mouse_pos = None
        self._drag_active = False
        self._resize_active = False
        self._resize_direction = None
        self._margin = 6  # ширина "захвата" по краю
        self._min_w, self._min_h = 700, 400

        # === Интерфейс ===
        style = UiStyle(self)

        # Боковая панель
        self.side_menu = QFrame(self)
        self.side_menu.setStyleSheet("border-right: 1px solid #444; background-color: #2d2d2d;")
        self.side_menu.setFixedWidth(45)

        # Контейнер для кнопок бокового меню
        layout_menu = QVBoxLayout()
        layout_menu.setContentsMargins(0, 0, 0, 0)
        layout_menu.setSpacing(0)

        # Навигация для проектов
        self.nav_project = QTabWidget()
        self.nav_project.setFixedWidth(250)
        self.nav_project.setDocumentMode(True)

        self.nav_project.widget = QWidget()
        layout = QVBoxLayout(self.nav_project.widget)
        project = self._create_agent_tab(self.nav_project.widget, 'project')
        label = 'Проекты'
        self.nav_project.addTab(project, label)

        # === Получаем агентов ===
        self.registry = AgentRegistry
        self.agents_map = {}
        if isinstance(agents, dict):
            self.agents_map = agents
        elif isinstance(agents, (list, tuple)):
            for a in agents:
                name = (getattr(a, 'name', None)
                        or (getattr(a, 'presentation', None)
                            and getattr(a.presentation, 'windowTitle', None)
                            and a.presentation.windowTitle()) or str(id(a)))
                self.agents_map[name] = a
        else:
            raise ValueError("Неподдерживаемый тип компонента")

        # === Метаданные ===
        self.meta = {}
        if AgentRegistry is not None:
            if hasattr(AgentRegistry, 'metadata'):
                self.meta = AgentRegistry.metadata
            elif hasattr(AgentRegistry, 'get_metadata'):
                try:
                    self.meta = AgentRegistry.get_metadata()
                except Exception:
                    self.meta = {}

        # === Заголовок окна ===
        self.title_bar = TitleBar(self)

        # === Контент справа ===
        self.stack = QStackedWidget()

        # === Формируем кнопки агентов ===
        ordered = self._ordered_agents()
        self.btn_map = {}
        for idx, (name, agent) in enumerate(ordered):
            meta = self.meta.get(name, {})
            title = meta.get('title', name)

            # Создаём область работы
            work_area = QWidget()
            work_area_layout = QVBoxLayout(work_area)
            w = None
            if hasattr(agent, 'presentation') and hasattr(agent.presentation, 'widget'):
                w = agent.presentation.widget
            else:
                try:
                    cw = agent.presentation.centralWidget() if hasattr(agent.presentation, 'centralWidget') else None
                    w = cw
                except Exception:
                    w = None
            work_area_layout.addWidget(w if w else QLabel(f"Компонент {title} не имеет представления"))
            self.stack.addWidget(work_area)

            # Кнопка агента
            item_btn = self._make_icon_button(meta.get('icon', None), title)
            item_btn.clicked.connect(lambda _, i=idx: self.switch_to_index(i))
            layout_menu.addWidget(item_btn)
            self.btn_map[name] = item_btn

        layout_menu.addStretch()
        self.side_menu.setLayout(layout_menu)

        # === Сборка контента ===
        content_layout = QHBoxLayout()
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(0)
        content_layout.addWidget(self.side_menu)
        content_layout.addWidget(self.nav_project)
        content_layout.addWidget(self.stack)

        # === Главный layout ===
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        main_layout.addWidget(self.title_bar)
        main_layout.addLayout(content_layout)
        self.setLayout(main_layout)

    # ===========================================================
    # ===============  РЕАЛИЗАЦИЯ RESIZE / DRAG  ================
    # ===========================================================

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self._mouse_pos = event.globalPosition().toPoint()
            if self._get_resize_direction(event.pos()):
                self._resize_active = True
                self._resize_direction = self._get_resize_direction(event.pos())
            else:
                self._drag_active = True
                self._drag_offset = event.globalPosition().toPoint() - self.frameGeometry().topLeft()
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        pos = event.pos()
        if self._resize_active:
            self._perform_resize(event.globalPosition().toPoint())
        elif self._drag_active:
            self.move(event.globalPosition().toPoint() - self._drag_offset)
        else:
            direction = self._get_resize_direction(pos)
            self._update_cursor(direction)
        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        self._drag_active = False
        self._resize_active = False
        self._resize_direction = None
        self.unsetCursor()
        super().mouseReleaseEvent(event)

    def _perform_resize(self, global_pos: QPoint):
        rect = self.geometry()
        diff = global_pos - self._mouse_pos
        geo = QRect(rect)

        d = self._resize_direction
        if d in ('left', 'top-left', 'bottom-left'):
            geo.setLeft(geo.left() + diff.x())
        if d in ('right', 'top-right', 'bottom-right'):
            geo.setRight(geo.right() + diff.x())
        if d in ('top', 'top-left', 'top-right'):
            geo.setTop(geo.top() + diff.y())
        if d in ('bottom', 'bottom-left', 'bottom-right'):
            geo.setBottom(geo.bottom() + diff.y())

        # Ограничение по минимальному размеру
        if geo.width() < self._min_w:
            geo.setWidth(self._min_w)
        if geo.height() < self._min_h:
            geo.setHeight(self._min_h)

        self.setGeometry(geo)
        self._mouse_pos = global_pos

    def _get_resize_direction(self, pos):
        x, y = pos.x(), pos.y()
        w, h = self.width(), self.height()
        m = self._margin

        if x <= m and y <= m:
            return 'top-left'
        elif x >= w - m and y <= m:
            return 'top-right'
        elif x <= m and y >= h - m:
            return 'bottom-left'
        elif x >= w - m and y >= h - m:
            return 'bottom-right'
        elif x <= m:
            return 'left'
        elif x >= w - m:
            return 'right'
        elif y <= m:
            return 'top'
        elif y >= h - m:
            return 'bottom'
        return None

    def _update_cursor(self, direction):
        cursors = {
            'top-left': Qt.CursorShape.SizeFDiagCursor,
            'bottom-right': Qt.CursorShape.SizeFDiagCursor,
            'top-right': Qt.CursorShape.SizeBDiagCursor,
            'bottom-left': Qt.CursorShape.SizeBDiagCursor,
            'left': Qt.CursorShape.SizeHorCursor,
            'right': Qt.CursorShape.SizeHorCursor,
            'top': Qt.CursorShape.SizeVerCursor,
            'bottom': Qt.CursorShape.SizeVerCursor,
        }
        if direction:
            self.setCursor(cursors[direction])
        else:
            self.unsetCursor()

    # ===========================================================
    # ===================  ПРОЧИЕ МЕТОДЫ  =======================
    # ===========================================================

    def _create_agent_tab(self, agent, name):
        widget = QWidget()
        widget.setStyleSheet("background-color: #3a3a3a;border: 1px solid #555;")
        layout = QVBoxLayout(widget)
        try:
            if hasattr(agent.presentation, 'widget'):
                layout.addWidget(agent.presentation.widget)
            else:
                cw = getattr(agent.presentation, 'centralWidget', lambda: None)()
                if cw is not None:
                    layout.addWidget(cw)
                else:
                    layout.addWidget(QLabel(f"⚠️ Компонент {name} не имеет представления", alignment=Qt.AlignmentFlag.AlignCenter))
        except Exception:
            layout.addWidget(QLabel(f"⚠️ Ошибка отображения компонента {name}", alignment=Qt.AlignmentFlag.AlignCenter))
        return widget

    def _ordered_agents(self):
        items = list(self.agents_map.items())
        def order_key(item):
            name, _ = item
            meta = self.meta.get(name, {})
            return meta.get('order', 1000)
        items.sort(key=order_key)
        return items

    def switch_to_agent(self, agent_name):
        ordered = self._ordered_agents()
        for idx, (name, _) in enumerate(ordered):
            if name == agent_name:
                self.switch_to_index(idx)
                return True
        return False

    def switch_to_index(self, index):
        for btn in self.btn_map.values():
            btn.setChecked(False)
        ordered = self._ordered_agents()
        if 0 <= index < len(ordered):
            name = ordered[index][0]
            btn = self.btn_map.get(name)
            if btn:
                btn.setChecked(True)
        self.stack.setCurrentIndex(index)

    def _make_icon_button(self, icon_name, tooltip):
        icon = qta.icon(icon_name or "fa5s.cube", color="white")
        btn = QPushButton()
        btn.setIcon(icon)
        btn.setIconSize(QSize(24, 24))
        btn.setFixedSize(45, 45)
        btn.setToolTip(tooltip)
        btn.setStyleSheet("""
            QPushButton {
                background: transparent;
                border: none;
            }
            QPushButton:hover {
                background-color: #3d3d3d;
                border-radius: 8px;
            }
        """)
        return btn
