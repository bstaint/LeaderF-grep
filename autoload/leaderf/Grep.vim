if leaderf#versionCheck() == 0
    finish
endif

exec g:Lf_py "import vim, sys, os.path"
exec g:Lf_py "cwd = vim.eval('expand(\"<sfile>:p:h\")')"
exec g:Lf_py "sys.path.insert(0, os.path.join(cwd, 'python'))"
exec g:Lf_py "from grepExpl import *"

function! leaderf#Grep#Maps()
    nmapclear <buffer>
    nnoremap <buffer> <silent> <CR>          :exec g:Lf_py "grepExplManager.accept()"<CR>
    nnoremap <buffer> <silent> o             :exec g:Lf_py "grepExplManager.accept()"<CR>
    nnoremap <buffer> <silent> <2-LeftMouse> :exec g:Lf_py "grepExplManager.accept()"<CR>
    nnoremap <buffer> <silent> x             :exec g:Lf_py "grepExplManager.accept('h')"<CR>
    nnoremap <buffer> <silent> v             :exec g:Lf_py "grepExplManager.accept('v')"<CR>
    nnoremap <buffer> <silent> t             :exec g:Lf_py "grepExplManager.accept('t')"<CR>
    nnoremap <buffer> <silent> q             :exec g:Lf_py "grepExplManager.quit()"<CR>
    nnoremap <buffer> <silent> i             :exec g:Lf_py "grepExplManager.input()"<CR>
    nnoremap <buffer> <silent> <F1>          :exec g:Lf_py "grepExplManager.toggleHelp()"<CR>
endfunction

function! leaderf#Grep#startExpl(win_pos, pattern)
    call leaderf#LfPy("grepExplManager.startExplorer('".a:win_pos."', '".substitute(a:pattern, "'", "\\\\'", 'g')."')")
endfunction
