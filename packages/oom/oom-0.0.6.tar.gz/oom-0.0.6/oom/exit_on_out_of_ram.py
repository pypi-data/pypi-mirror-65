import psutil
import threading
import os
from colorama import Fore, Style
import _thread
import time

__all__ = ['exit_on_out_of_ram']


def _surely_kill_process():
    _thread.interrupt_main()
    # If it's still alive for some reasons
    # we still definitely want the process to be terminated
    time.sleep(7)
    os._exit(1)


class _RamWatcherThread(threading.Thread):
    def __init__(
            self,
            terminate_on: int,
            need_warning: bool = True,
            warn_on: int = None,
            warn_each: int = 20,
            sleep_time: float = 0.5,
            notify_about_using: bool = True
    ):
        super().__init__()
        self.terminate_on = terminate_on
        self.need_warning = need_warning
        self.warn_on = warn_on or 2 * terminate_on
        self.warn_each = warn_each
        self.sleep_time = sleep_time
        self.warnings_counter = 0

        bytes2megabytes = lambda x: x / (1 << 20)
        warning_info = f"{bytes2megabytes(self.warn_on):.1f} MB" if self.warn_on else "WARNINGS ARE DISABLED"
        if notify_about_using:
            print(
                f'{Fore.GREEN}'
                f'{Style.BRIGHT}You are using OOM.{Style.NORMAL}\n'
                f'The process will be {Style.BRIGHT}automatically terminated{Style.NORMAL} '
                f'if the machine is running out of RAM.\n'
                f'Settings:\n'
                f'* terminates when {bytes2megabytes(terminate_on):.1f} MB left.\n'
                f'* warns when {warning_info} left\n'
                f'{Style.RESET_ALL}'
            )

    def run(self):
        try:
            while True:
                ram_stat = psutil.virtual_memory()
                available_ram = ram_stat.available

                self._warn_if_needed(available_ram, ram_stat)
                self._terminate_if_needed(available_ram)
        except Exception as e:
            self._handle_inner_exception(e)
        time.sleep(self.sleep_time)

    @staticmethod
    def _handle_inner_exception(e: BaseException):
        print(e)
        print(
            f"{Fore.RED}"
            f"[OOM]: "
            f"Something went wrong in {exit_on_out_of_ram.__name__}. "
            f"Finishing the program by sending KeyboardInterrupt..."
            f"{Style.RESET_ALL}"
        )
        _surely_kill_process()

    def _terminate_if_needed(self, available_ram: int):
        if available_ram < self.terminate_on:
            print(
                f"{Fore.RED}"
                f"[OOM]: "
                f"Further execution may cause freezing of your machine. "
                f"Finishing the program by sending KeyboardInterrupt..."
                f"{Style.RESET_ALL}"
            )
            _surely_kill_process()

    def _warn_if_needed(self, available_ram, ram_stat):
        if available_ram <= self.warn_on:
            if self.need_warning and self.warnings_counter % self.warn_each == 0:
                available_ram_percents = 100 - ram_stat.percent
                ram_human_readable = available_ram / float(1 << 20)
                self._warn(ram_human_readable, available_ram_percents)
            self.warnings_counter += 1
        else:
            self.warnings_counter = 0

    def _warn(self, available_ram: int, in_percents: float):
        print(
            f"{Fore.RED}"
            f"[WARNING]: Running out of RAM: left {available_ram} MB ({in_percents:.2f}% of total)"
            f"{Style.RESET_ALL}"
        )
        self.already_warned = True


def exit_on_out_of_ram(
        terminate_on: int,
        need_warning: bool = True,
        warn_on: int = None,
        warn_each: int = 20,
        sleep_time: float = 0.5,
        notify_about_using: bool = True
):
    thread = _RamWatcherThread(terminate_on, need_warning, warn_on, warn_each, sleep_time, notify_about_using)
    thread.daemon = True
    thread.start()


def main():
    one_gigabyte = 1 << 30
    exit_on_out_of_ram(0.5 * one_gigabyte)

    # explode your RAM
    extremely_big_number = 1 << 9999999
    _ = [i for i in range(extremely_big_number)]


if __name__ == '__main__':
    main()
