"----------Plugins--------"
source ~/.config/nvim/plugins.vim
"--------Mappings---------"
source ~/.config/nvim/mappings.vim
"-------Basic-Settings-----"
syntax on
set tabstop=8 expandtab shiftwidth=4 softtabstop=4
set relativenumber
set showmatch
set showmode
set laststatus=2
set clipboard^=unnamed,unnamedplus
"-----Python-Shortcuts-----"
autocmd FileType python map <buffer> <F9> :w<CR>:exec '!clear;python3' shellescape(@%, 1)<CR>
autocmd FileType python imap <buffer> <F9> <esc> :w<CR>:exec '!clear;python3' shellescape(@%, 1)<CR>
autocmd FileType org,outline setlocal nofoldenable
"--------GVim--------------"
if !has('gui_running')
  set t_Co=256
endif

" Vimwiki
let g:vimwiki_list = [{'path': '~/Nextcloud/Notes/',
                      \ 'syntax': 'markdown', 'ext': '.md'}]
