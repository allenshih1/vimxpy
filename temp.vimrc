set nocompatible                      " not compatible with the old-fashion vi mode
set backspace=2                       " allow backspacing over everything in insert nc >kkmode
set undolevels=100
"set number
set nobomb                            " no BOM(Byte Order Mark)
set nostartofline
set clipboard+=unnamed
set scrolloff=5                       " start scrolling when n lines away from margins
set wildmode=longest,list             " use emacs-style tab completion when selecting files, etc
set key=                              " disable encryption
set synmaxcol=128
set viminfo=                          " disable .viminfo file
set ttyfast                           " send more chars while redrawing
"set foldmethod=

filetype on                           " enable filetype detection
filetype indent on                    " enable filetype-specific indenting
filetype plugin on                    " enable filetype-specific plugins

syntax on                             " syntax highlight
set hlsearch                          " search highlighting
set incsearch                         " incremental search
syntax enable
set t_Co=256
"try
  "colorscheme railscasts
"catch
"endtry

try
  let g:solarized_termcolors=256
  "let g:solarized_drgrade=0
  colorscheme solarized_dark
catch
endtry

"try
  "colorscheme Tomorrow-Night
"catch
"endtry

set nobackup                          " no *~ backup files
set noswapfile
set smarttab                          " insert tabs on the start of a line according to
set softtabstop=2
set shiftwidth=2
set tabstop=2
set shortmess=Ia                      " remove splash wording

" disable sound on errors
set t_vb=
set tm=500

" file encoding
set encoding=utf-8
set fileencodings=ucs-bom,utf-8,big5,euc-jp,gbk,euc-kr,utf-bom,iso8859-1,euc-jp,utf-16le,latin1
set fenc=utf-8 enc=utf-8 tenc=utf-8
scriptencoding utf-8

" ignores
set wildignore+=*.o,*.obj,*.pyc                " output objects
set wildignore+=*.DS_Store
set wildignore+=tmp/**

" cursorline switched while focus is switched to another split window
autocmd WinLeave * setlocal nocursorline

" ======================================
"  custom key and plugin configurations
" ======================================
" remove tailing whitespace
autocmd BufWritePre * :%s/\s\+$//e

" comment
map <Leader><Leader> <Leader>c<space>

" next and prev tab
noremap <F7> gT

" identation
vmap <S-TAB> <gv

" remap VIM 0
map 0 ^

" return current opened file's dirctory
cnoremap %% <C-R>=expand('%:h').'/'<CR>

" quick open vimrc in a new tab
nmap <leader>v :tabe $MYVIMRC<CR>
" Shortcut to rapidly toggle `set list`
nmap <leader>l :set list!<CR>
nmap <silent> <leader>aa :set exit=1<CR>
" Use the same symbols as TextMate for tabstops and EOLs
set list!
set listchars=tab:▸\ ,eol:¬,extends:»,precedes:«
set fillchars+=vert:\│
set showbreak=↪


""" vimx begin
set abc
set edb
""" vimx end

set hello
