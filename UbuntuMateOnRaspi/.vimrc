
if has('persistent_undo')      "check if your vim version supports it
    set undofile                 "turn on the feature  
    set undodir=$HOME/.vim/undo  "directory where the undo files will be stored
endif   

map <space> :
" Smart way to move btw. windows
map <C-j> <C-W>j
map <C-k> <C-W>k
map <C-h> <C-W>h
map <C-l> <C-W>l
map <F5> :!ctags -R --c++-kinds=+p --fields=+iaS --extra=+q .<CR>
map <F4> :!cscope -Rbq -f ./cscope.out<CR>

" On RaspberryPI
vmap <C-c> "+y
nmap <F3> "+p

set shiftwidth=4
set tabstop=4
set softtabstop=4
set expandtab
set nowrap
set guioptions-=mLlRrBb
set guioptions-=T
set fileencodings=ucs-bom,utf-8,gb2312,gb18030
set termencoding=utf-8
set fileformats=unix
set tags=./tags;../tags;tags
set nu

imap () ()<Left>
imap [] []<Left>
imap {} {}<Left>
imap "" ""<Left>
imap '' ''<Left>
imap <> <><Left>
imap <C-\> <ESC>A;<Enter>
nmap <C-\> <ESC>A {}<Enter><ESC>O

set nocp
set path+=./include,../include

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
" cscope setting
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
if has("cscope")
  set csprg=/usr/bin/cscope
  set csto=1
  set cst
  set nocsverb
  " add any database in current directory
  if filereadable("cscope.out")
      cs add cscope.out
  endif
  set csverb
endif

nmap <C-@>s :cs find s <C-R>=expand("<cword>")<CR><CR>
nmap <C-@>g :cs find g <C-R>=expand("<cword>")<CR><CR>
nmap <C-@>c :cs find c <C-R>=expand("<cword>")<CR><CR>
nmap <C-@>t :cs find t <C-R>=expand("<cword>")<CR><CR>
nmap <C-@>e :cs find e <C-R>=expand("<cword>")<CR><CR>
nmap <C-@>f :cs find f <C-R>=expand("<cfile>")<CR><CR>
nmap <C-@>i :cs find i ^<C-R>=expand("<cfile>")<CR>$<CR>
nmap <C-@>d :cs find d <C-R>=expand("<cword>")<CR><CR>
