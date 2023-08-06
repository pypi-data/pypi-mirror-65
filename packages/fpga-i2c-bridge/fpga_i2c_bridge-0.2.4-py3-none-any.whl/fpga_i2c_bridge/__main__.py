"""An I2C testing console."""

import argparse

from fpga_i2c_bridge.i2c import I2CBusReal
from fpga_i2c_bridge.i2c_dummy import I2CDummy
from fpga_i2c_bridge.util.crc import crc16


class Command:
    def __init__(self, shell_instance):
        self.shell = shell_instance

    def run(self, cmd_args):
        raise NotImplementedError


class QuitCommand(Command):
    def run(self, cmd_args):
        raise Shell.QuitException


class WriteCommand(Command):
    def __init__(self, raw: bool = False, *args, **kwargs):
        super(WriteCommand, self).__init__(*args, **kwargs)
        self.is_raw = raw

    def run(self, cmd_args):
        if len(cmd_args) < 1:
            raise Shell.CommandError("No bytes specified for request")
        try:
            request = bytes(int(x, base=16) % 256 for x in cmd_args if x.strip() != "")
            if not self.is_raw:
                request += int.to_bytes(crc16(request), 2, byteorder='big')

            self.shell.i2c.raw_write(request)
        except ValueError:
            print("Invalid byte value specified")


class ReadCommand(Command):
    def __init__(self, raw: bool = False, *args, **kwargs):
        super(ReadCommand, self).__init__(*args, **kwargs)
        self.is_raw = raw

    def run(self, cmd_args):
        if len(cmd_args) < 1:
            raise Shell.CommandError("No bytes specified for request")
        try:
            request = bytes(int(x, base=16) % 256 for x in cmd_args if x.strip() != "")
            if not self.is_raw:
                request += int.to_bytes(crc16(request), 2, byteorder='big')

            response = self.shell.i2c.raw_read(request)
            self.shell.last_msg = response

        except ValueError:
            print("Invalid byte value specified")


class HelpCommand(Command):
    def run(self, cmd_args):
        print("Available commands:")
        print("-------------------")
        for name, cmd_data in self.shell.commands.items():
            if not cmd_data[2]:
                print("%s\t%s" % (name, cmd_data[1]))


class CRCCommand(Command):
    def run(self, cmd_args):
        if self.shell.last_msg is None:
            print("No message received yet")
            return

        print("CRC checksum of last message: %04x" % crc16(self.shell.last_msg))


class Shell:
    def __init__(self, i2c_instance: I2CBusReal):
        self.i2c = i2c_instance
        self.last_msg = None
        self.commands = {}

        self.register_command(("exit", "quit"), QuitCommand(shell_instance=self), "Terminates the shell")
        self.register_command(("read_raw", ), ReadCommand(shell_instance=self, raw=True), "Sends a raw read request (without CRC)")
        self.register_command(("send_raw", ), WriteCommand(shell_instance=self, raw=True), "Sends a raw write request (without CRC)")

        self.register_command(("read", "recv"), ReadCommand(shell_instance=self), "Sends a read request")
        self.register_command(("send", "write"), WriteCommand(shell_instance=self), "Sends a write request")

        self.register_command(("crc", ), CRCCommand(shell_instance=self), "Verifies CRC checksum of last received message")
        self.register_command("help", HelpCommand(shell_instance=self), "Lists all commands")

    class CommandError(BaseException):
        def __init__(self, message):
            super(Shell.CommandError, self).__init__(message)

    class QuitException(BaseException):
        pass

    def run(self):
        while True:
            try:
                self.input_parse(input("I2C> "))
            except Shell.CommandError as e:
                print(e)
            except OSError as e:
                print("I2C error: %s" % e)
            except (KeyboardInterrupt, Shell.QuitException, EOFError):
                print("Exiting")
                break

    def register_command(self, names, command, help_text="", hide_in_help=False):
        if isinstance(names, tuple):
            for i, name in enumerate(names):
                self.register_command(name, command, help_text, i > 0)
        else:
            self.commands[names] = (command, help_text, hide_in_help)

    def input_parse(self, line):
        cmd, *cmd_args = line.strip().split(" ")
        try:
            self.commands[cmd][0].run(cmd_args)
        except KeyError:
            raise Shell.CommandError("Unknown command: %s. Enter 'help' for a list of commands." % cmd)


if __name__ == '__main__':
    argparser = argparse.ArgumentParser(description="Launches an interactive I2C shell.")
    argparser.add_argument("--bus", default="1", help="I2C bus number")
    argparser.add_argument("--address", default="3E", help="Address of I2C slave")
    argparser.add_argument("--dummy", action="store_true", help="Use a dummy device")
    args = vars(argparser.parse_args())

    if args["dummy"]:
        i2c = I2CDummy(appliance_types=[1, 2, 3, 4], sensor_types=[5, 4, 3, 2, 1])
    else:
        i2c = I2CBusReal(bus=int(args["bus"]), addr=int(args["address"], base=16))

    shell = Shell(i2c)
    shell.run()
