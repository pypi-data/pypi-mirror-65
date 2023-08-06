from tpDcc.core import tool


class FramelessWindowToggle(tool.DccTool, object):
    def __init__(self, manager, config, settings=None):
        super(FramelessWindowToggle, self).__init__(manager=manager, config=config, settings=settings)

        self._state = self.config_dict().get('is_checked', False)

    @property
    def state(self):
        return self._state

    @classmethod
    def config_dict(cls, file_name=None):
        base_tool_config = tool.DccTool.config_dict(file_name=file_name or cls.FILE_NAME)
        tool_config = {
            'name': 'Frameless Window Toggle',
            'id': 'tpDcc-tools-frameless_toggle',
            'icon': 'toggle',
            'tooltip': ' Tool that toggles windows to use tpDcc frameless functionality or OS default windows.',
            'tags': ['tpDcc', 'window', 'frameless', 'toggle'],
            'is_checkable': False,
            'is_checked': True,
            'menu_ui': {'label': 'Frameless Toggle', 'load_on_startup': False, 'color': '', 'background_color': ''},
            'menu': [{'type': 'menu', 'children': [{'id': 'tpDcc-tools-frameless_toggle', 'type': 'tool'}]}],
            'shelf': [
                {'name': 'tpDcc', 'children': [
                    {'id': 'tpDcc-tools-frameless_toggle', 'display_label': False, 'type': 'tool'}
                ]}
            ]
        }
        base_tool_config.update(tool_config)

        return base_tool_config

    def launch(self, state):
        self._state = state

    def cleanup(self):
        pass
