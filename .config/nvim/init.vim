call plug#begin()

"----------/theme
Plug 'kaicataldo/material.vim'
Plug 'vim-airline/vim-airline'
Plug 'vim-airline/vim-airline-themes'

"----------/Icons
Plug 'ryanoasis/vim-devicons'
Plug 'tiagofumo/vim-nerdtree-syntax-highlight'

"----------/Syntex highlight
Plug 'Yggdroot/indentLine'
Plug 'rrethy/vim-hexokinase', { 'do': 'make hexokinase' } "display colors
Plug 'HerringtonDarkholme/yats.vim', { 'for': 'typescript' }
Plug 'posva/vim-vue'
 
"----------/search
Plug 'scrooloose/nerdtree'
Plug 'junegunn/fzf', { 'do': { -> fzf#install() } }
Plug 'junegunn/fzf.vim'
Plug 'airblade/vim-rooter'

"----------/code completion
Plug 'neoclide/coc.nvim', {'branch': 'release'}

"----------/Commenter
Plug 'scrooloose/nerdcommenter'

"----------/Auto Tags
Plug 'jiangmiao/auto-pairs'

"----------/git
" Plug 'Xuyuanp/nerdtree-git-plugin'
Plug 'airblade/vim-gitgutter'
"Plug 'tpope/vim-fugitive'

" ----------/Text Edit
Plug 'iamcco/markdown-preview.nvim', { 'do': 'cd app && yarn install'  }

call plug#end()
"---------------------/configs/----------------------------
let mapleader="\<space>"
set number
set inccommand=split
set clipboard=unnamedplus

" TextEdit might fail if hidden is not set.
set hidden

" --/ Text folding 
set foldmethod=indent
set foldlevel=99

" --/indentation
" set autoindent  ?
" set smartindent ?
" set cindent  ?
" set smarttab ?
" set softtabstop=2 ?
set shiftwidth=2
set tabstop=2
" always uses spaces instead of tab characters
set expandtab
" save text folding
autocmd BufWinLeave *.* mkview
autocmd BufWinEnter *.* silent! loadview
"------------------------------/theme/-------------------------
"--/truecolor configs
if (has('nvim'))
	let $NVIM_TUI_ENABLE_TRUE_COLOR = 1
endif
if (has('termguicolors'))
	set termguicolors
endif

"--/syntax highlighting
syntax on
" set background=dark

" let g:material_theme_style = 'ocean-community'
let g:material_theme_style = 'ocean'
colorscheme material

"--/vim airline theme
let g:airline_theme='behelit'
let g:airline#extensions#whitespace#enabled = 0

"--/dev icons
" Set internal encoding of vim, not needed on neovim, since coc.nvim using some
" unicode characters in the file autoload/float.vim
set encoding=UTF-8

"--/Font
set guifont=RobotoMono\ Nerd\ Font\ Mono:h12

" ------------------------/nerdtree/---------------------

let g:NERDTreeIgnore = ['^node_modules$']
" Highlight currently open buffer in NERDTree

"-----------------------/Nerd comments/-----------------------
filetype plugin on
let g:NERDSpaceDelims = 1
let g:NERDDefaultAlign = 'left'
let g:NERDCustomDelimiters = { 'vue': { 'left': '/**','right': '*/', 'leftAlt': '<!--', 'rightAlt': '-->' },
			\'': { 'left': '---/','right': '', 'leftAlt': '========================/', 'rightAlt': '/======================' } 
	\}

"OBS: i have commented all CreateMaps commands in /home/phsw/.config/nvim/plugged/nerdcommenter/plugin/nerdcommenter.vim from line 81 to 100, with exeption of:  
" call s:CreateMaps('nx', 'Invert',     'Invert', 'c')  <-- I did this because i want to avoid keybind delay
" call s:CreateMaps('n',  'AltDelims',  'Switch Delimiters', 'C')
" This this corresponds to NERDCommenterAltDelims and NERDCommenterInvert. 
"
" ---------------------------/Indent Line
let g:indentLine_enabled = 1
"map <C-k>i :IdentLinesToggle
let g:indentLine_fileTypeExclude = ['json', 'markdown', 'md']
let s:box_drawings_light_vertical='│'
" let g:indentLine_char=s:box_drawings_light_vertical

" ---------------------------/snippets
" Use <C-k> for jump to previous placeholder, it's default of coc.nvim
" let g:coc_snippet_next = '<C-f>' 
" let g:coc_snippet_prev = '<C-b>'

" ---------------------------/Coc-prettier
" nnoremap <leader>F :CocCommand prettier.formatFile
vmap <leader>f :CocCommand prettier.formatFile
nmap <leader>f :CocCommand prettier.formatFile
command! -nargs=0 Prettier :CocCommand prettier.formatFile

" ---------------------------/Hexodinase (colors)
let g:Hexokinase_ftAutoload = ['css', 'less']

" ---------------------------/Markdown


"----------------------/Remaps/----------------------------
"xnoremap = visual mode
"nnoremap = normal mode
map z @
map Q :q! <Cr>
map q :q <Cr>
nnoremap Z q

"Case insensitive search
nnoremap <leader>/ /\c
nnoremap <leader>? ?\c
nnoremap J }
xnoremap J }
nnoremap K {
xnoremap K {

cnoremap <C-F> <Right>
cnoremap <C-B> <Left>

nnoremap c "_c
xnoremap c "_c
nnoremap C "_C
xnoremap C "_C
nnoremap <leader>d "_d
xnoremap <leader>d "_d
nnoremap <leader>D "_D
xnoremap <leader>D "_D
nnoremap <leader>o :NERDTreeToggle <Cr>
map s :w! <Cr>
nnoremap <leader>n :bnext<esc>
nnoremap <leader>p :bprevious<esc>
nnoremap <leader>x :bd<esc>
nnoremap <leader>X :bd!<esc>
nnoremap <leader>ec :vsplit ~/.config/nvim/init.vim<cr>
nnoremap <leader>lc :source ~/.config/nvim/init.vim<cr>
nnoremap <leader>es :CocCommand snippets.openSnippetFiles
nnoremap <leader>ls :CocList snippets <cr>
nnoremap <leader>m za

" ---/ Actions
map <F12> :PlugInstall <CR>
map <F1> :! firefox "%"<CR>
map <F2> :! mng runserver<CR>
map fl :setlocal spell! spelllang=en_us<CR>
map fL :setlocal spell! spelllang=pt<CR>
nnoremap fw z=
xnoremap fw z=

" ---/Examples (M => alt)
" nnoremap <M-Right> :bn<cr>
" nnoremap <M-Left> :bp<cr>
" map <C-k> <Nop>
" nnoremap <leader>q :q <Cr>
" nnoremap <leader>Q :q! <Cr>
" cnoremap <Esc>b <S-Left>
" cnoremap <Esc>f <S-Right>

"---------------------/Source/--------------------
source ~/.config/nvim/fzf.nvimrc
source ~/.config/nvim/coc.nvimrc