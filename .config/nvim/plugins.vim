"----------Plugins--------"
call plug#begin('~/.config/nvim/plugged')
" Tools

Plug 'tpope/vim-eunuch'
Plug 'scrooloose/nerdtree'
Plug 'mattn/emmet-vim'
Plug 'airblade/vim-gitgutter'

" Syntax

Plug 'tpope/vim-markdown'
Plug 'ap/vim-css-color'
Plug 'editorconfig/editorconfig-vim'
Plug 'dense-analysis/ale'
Plug 'neoclide/coc.nvim'
Plug 'prettier/vim-prettier', {'do': 'yarn install'}
Plug 'lervag/vimtex'


" Design
Plug 'itchyny/lightline.vim'

" Vimwiki
Plug 'vimwiki/vimwiki'

call plug#end()

"------Plugin-Config------"
" coc config
let g:coc_global_extensions = [
 \  'coc-snippets',
 \  'coc-json',
 \  'coc-pairs',
 \  'coc-python',
 \  'coc-vimtex'
 \  ]

" vimtex config
let g:vimtex_view_general_viewer = 'mupdf'
