"""
.. codeauthor:: Tsuyoshi Hombashi <tsuyoshi.hombashi@gmail.com>
"""


import pytest
from humanreadable import Time

from pingparsing._cmd_maker import LinuxPingCmdMaker, MacosPingCmdMaker, WindowsPingCmdMaker


class Test_CmdMaker_make_cmd:
    @pytest.mark.parametrize(
        ["maker_class", "host", "expected"],
        [
            [LinuxPingCmdMaker, "127.0.0.1", "ping -w 3 127.0.0.1"],
            [MacosPingCmdMaker, "127.0.0.1", "ping -t 3 127.0.0.1"],
            [WindowsPingCmdMaker, "127.0.0.1", "ping -n 3 127.0.0.1"],
        ],
    )
    def test_normal_dest(self, maker_class, host, expected):
        assert maker_class().make_cmd(destination=host) == expected

    @pytest.mark.parametrize(
        ["maker_class", "host", "deadline", "expected"],
        [[LinuxPingCmdMaker, "localhost", "1sec", "ping -w 1 localhost"],],
    )
    def test_normal_deadline(self, maker_class, host, deadline, expected):
        assert maker_class(deadline=Time(deadline)).make_cmd(destination=host) == expected

    @pytest.mark.parametrize(
        ["maker_class", "host", "ipv6", "timeout", "expected"],
        [
            [LinuxPingCmdMaker, "localhost", False, "1sec", "ping -w 3 -W 1 localhost"],
            [LinuxPingCmdMaker, "localhost", True, "1sec", "ping6 -w 3 -W 1 localhost"],
            [MacosPingCmdMaker, "localhost", False, "1sec", "ping -t 3 localhost"],
            [MacosPingCmdMaker, "localhost", True, "1sec", "ping6 -i 1 -c 3 localhost"],
            [WindowsPingCmdMaker, "localhost", False, "1sec", "ping -n 3 -w 1000 localhost"],
            [WindowsPingCmdMaker, "localhost", True, "1sec", "ping -n 3 -w 1000 localhost%eth0"],
        ],
    )
    def test_normal_timeout(self, maker_class, host, ipv6, timeout, expected):
        assert (
            maker_class(interface="eth0", timeout=Time(timeout), is_ipv6=ipv6).make_cmd(
                destination=host
            )
            == expected
        )

    @pytest.mark.parametrize(
        ["maker_class", "host", "count", "expected"],
        [
            [LinuxPingCmdMaker, "localhost", 1, "ping -c 1 localhost"],
            [MacosPingCmdMaker, "localhost", 1, "ping -c 1 localhost"],
            [WindowsPingCmdMaker, "localhost", 1, "ping -n 1 localhost"],
        ],
    )
    def test_normal_count(self, maker_class, host, count, expected):
        assert maker_class(count=count).make_cmd(destination=host) == expected

    @pytest.mark.parametrize(
        ["maker_class", "host", "packet_size", "expected"],
        [
            [LinuxPingCmdMaker, "localhost", 6000, "ping -c 1 -s 6000 localhost"],
            [MacosPingCmdMaker, "localhost", 6000, "ping -c 1 -s 6000 localhost"],
            [WindowsPingCmdMaker, "localhost", 6000, "ping -n 1 -l 6000 localhost"],
        ],
    )
    def test_normal_packet_size(self, maker_class, host, packet_size, expected):
        assert maker_class(packet_size=packet_size, count=1).make_cmd(destination=host) == expected

    @pytest.mark.parametrize(
        ["maker_class", "host", "expected"],
        [
            [LinuxPingCmdMaker, "localhost", "ping -c 1 -D localhost"],
            [MacosPingCmdMaker, "localhost", "ping -c 1 -D localhost"],
            [WindowsPingCmdMaker, "localhost", "ping -n 1 localhost"],
        ],
    )
    def test_normal_timestamp(self, maker_class, host, expected):
        assert maker_class(timestamp=True, count=1).make_cmd(destination=host) == expected

    @pytest.mark.parametrize(
        ["maker_class", "host", "expected"],
        [
            [LinuxPingCmdMaker, "localhost", "ping -c 1 localhost"],
            [MacosPingCmdMaker, "localhost", "ping -c 1 localhost"],
            [WindowsPingCmdMaker, "localhost", "chcp 437 & ping -n 1 localhost"],
        ],
    )
    def test_normal_auto_codepage(self, maker_class, host, expected):
        assert maker_class(auto_codepage=True, count=1).make_cmd(destination=host) == expected

    @pytest.mark.parametrize(
        ["maker_class", "host", "expected"],
        [
            [LinuxPingCmdMaker, "localhost", "ping -c 1 -a localhost"],
            [MacosPingCmdMaker, "localhost", "ping -c 1 -a localhost"],
            [WindowsPingCmdMaker, "localhost", "ping -n 1 -a localhost"],
        ],
    )
    def test_normal_ping_option(self, maker_class, host, expected):
        assert maker_class(ping_option="-a", count=1).make_cmd(destination=host) == expected