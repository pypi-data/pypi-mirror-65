#!/usr/bin/env python
# -*- coding=utf-8 -*-

import subprocess
import sys
from formatter import Formatter


class Shell(object):
    __instance = None

    def __init__(self):
        self.formatter = Formatter.instance()

    @classmethod
    def instance(cls):
        if cls.__instance is None:
            cls.__instance = Shell()
        return cls.__instance

    def excommand(cmd):
        """
        子线程执行脚本
        Arguments:
            cmd {str} -- cmd命令
        Returns:
            Pipe -- 管道
        """
        return subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)


    def excommand_until_done(self, cmd):
        """
        子线程执行脚本，直到结束，并输出
        Arguments:
            cmd {str} -- cmd命令
        Returns:
            Pipe -- 管道
        """
        process = subprocess.Popen(cmd, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                   stderr=subprocess.STDOUT)
        output = ""
        while process.poll() is None:
            while 1:
                line = process.stdout.readline()
                if line == "":
                    break
                if line:
                    print(line.strip("\n"))
                    output += line
        process.wait()
        if process.returncode > 0:
            sys.stdout.flush()
            sys.stderr.flush()
        return process.returncode, output

    def RunCmd(self, curCmd):
        pipe = subprocess.Popen(['cmd', ""], shell=False, stdout=subprocess.PIPE, \
                                stderr=subprocess.PIPE)
        pipe.stdin.write('%s\n' % curCmd)
        pipe.stdin.close()
        stdoutStr = pipe.stdout.read()
        stderrStr = pipe.stderr.read()
        printStr = ''.join([stdoutStr, stderrStr])
        self.formatter.format_info(printStr)
        return stderrStr, stdoutStr