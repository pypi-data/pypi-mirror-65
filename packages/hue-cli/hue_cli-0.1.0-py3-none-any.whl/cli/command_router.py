from api import HueApi

COMMANDS = [
    'init',
    'debug',
    'list',
    'on',
    'off',
    'toggle',
    'brightness',
    'color']

class CommandRouter:

    def route_command(self, command, args):
        if command == 'init':
            self.handle_init()
            return
        self.api = HueApi()
        if command in ['list', 'debug']:
            self.handle_no_arg_command(command)
        elif command in ['on', 'off', 'toggle']:
            self.handle_no_value_command(command, args)
        elif command in ['brightness', 'color']:
            self.handle_command_with_value(command, args)

    def handle_init(self, args):
        try:
            self.api = HueApi(bridge_ip_address=args[0])
        except Exception as e:
            print(f"Initialization error: {e.msg}")

    def handle_no_arg_command(self, command):
        command_map = {
            'list': self.api.list_lights,
            'debug': self.api.print_debug_info
        }
        action = command_map[command]
        action()

    def handle_no_value_command(self, command, args):
        command_map = {
            'on': self.api.turn_on,
            'off': self.api.turn_off,
            'toggle': self.api.toggle_on
        }
        action = command_map[command]
        light = None
        if len(args) == 1:
            light = args[0]
        action(index=light)

    def handle_command_with_value(self, command, args):
        command_map = {
            'brightness': self.api.set_brightness,
            'color': self.api.set_color
        }
        action = command_map[command]
        light = None
        value = args[0]
        if len(args) == 2:
            light = args[1]
        action(value, index=light)
