#!/usr/bin/env python
# -*- coding: utf-8 -*-

import vim
import os
import time
import os.path
from leaderf.utils import *
from leaderf.explorer import *
from leaderf.manager import *
from leaderf.asyncExecutor import AsyncExecutor

#*****************************************************
# GrepExplorer
#*****************************************************
class GrepExplorer(Explorer):
    def __init__(self):
        self._time = 0
        self._executor = []
        self._content = []
        self._args = ('', '')
        
    def _buildCmd(self, dir, text):
        wildignore = lfEval("g:Lf_WildIgnore")
        args = ['--no-messages', '--vimgrep', '--fixed-strings']        
        # '*.{h,cs,c}'
        ignore = (i[2:]  if i.startswith('*.') else i for i in wildignore["file"])         
        if os.name == 'nt': # https://github.com/BurntSushi/ripgrep/issues/500
            args.append('-g "!*.{%s}"' % ','.join(ignore))
        else:
            args.append("-g '!*.{%s}' % ",','.join(ignore))
            
        return 'rg %s "%s" "%s"' % (' '.join(args), text.replace('"', r'\"'), dir)
        
    def getContent(self, *args, **kwargs):
        pattern = args[0] if len(args) > 0 else ''
        if not pattern:
            return self._content
        
        _args = (os.getcwd(), pattern)
        if self._args == _args and time.time() - self._time < float(\
                lfEval("g:Lf_IndexTimeLimit")) and self._content:
            return self._content
        
        cmd = self._buildCmd(*_args)
        print(cmd)
        executor = AsyncExecutor()
        self._executor.append(executor)
        self._content = executor.execute(cmd, encoding=lfEval("&encoding"))        
        self._args = _args
        self._time = time.time()
        
        return self._content
        
    def setContent(self, content):
        self._content = content

    def getStlCategory(self):
        return "Grep"

    def getStlCurDir(self):
        return escQuote(lfEncode(os.getcwd()))
        
    def cleanup(self):
        for exe in self._executor:
            exe.killProcess()
        self._executor = []


#*****************************************************
# GrepExplManager
#*****************************************************
class GrepExplManager(Manager):
    def __init__(self):
        super(GrepExplManager, self).__init__()
        self._match_ids = []

    def _getExplClass(self):
        return GrepExplorer

    def _defineMaps(self):
        lfCmd("call leaderf#Grep#Maps()")
        lfCmd("autocmd VimLeave * call leaderf#Function#cleanup()")

    def _acceptSelection(self, *args, **kwargs):
        if len(args) == 0:
            return
        
        drive,line = os.path.splitdrive(args[0])
        file,row,column,_ = line.split(':', 3)
        file = os.path.join(drive, file)

        lfCmd("hide edit %s" % escSpecial(file))
        lfCmd("norm %sG%s|" % (row, column))
        lfCmd("norm! zz")
        lfCmd("setlocal cursorline! | redraw | sleep 20m | setlocal cursorline!")

    def _getDigest(self, line, mode):
        """
        specify what part in the line to be processed and highlighted
        Args:
            mode: 0, 1, 2, return the whole line
        """
        if not line:
            return ''
        return line[1:]

    def _getDigestStartPos(self, line, mode):
        """
        return the start position of the digest returned by _getDigest()
        Args:
            mode: 0, 1, 2, return 1
        """
        return 1

    def _createHelp(self):
        help = []
        help.append('" <CR>/<double-click>/o : execute command under cursor')
        help.append('" x : open file under cursor in a horizontally split window')
        help.append('" v : open file under cursor in a vertically split window')
        help.append('" t : open file under cursor in a new tabpage')
        help.append('" i : switch to input mode')
        help.append('" q : quit')
        help.append('" <F1> : toggle this help')
        help.append('" ---------------------------------------------------------')
        return help      
        
    def _afterEnter(self):
        super(GrepExplManager, self)._afterEnter()

    def _beforeExit(self):
        super(GrepExplManager, self)._beforeExit()
        for i in self._match_ids:
            lfCmd("silent! call matchdelete(%d)" % i)
        self._match_ids = []


#*****************************************************
# grepExplManager is a singleton
#*****************************************************
grepExplManager = GrepExplManager()

__all__ = ['grepExplManager']
