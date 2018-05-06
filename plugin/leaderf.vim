" ============================================================================
" File:        leaderf.vim
" Description:
" Author:      Yggdroot <archofortune@gmail.com>
" Website:     https://github.com/Yggdroot
" Note:
" License:     Apache License, Version 2.0
" ============================================================================

command! -bar -nargs=1 LeaderfGrep call leaderf#Grep#startExpl(g:Lf_WindowPosition, <q-args>)
command! -bar -nargs=0 LeaderfGrepCword call leaderf#Grep#startExpl(g:Lf_WindowPosition, expand('<cword>'))

call g:LfRegisterSelf("LeaderfGrep", "search content by riggrep")
