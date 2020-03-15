let s:plugin_root_dir = fnamemodify(resolve(expand('<sfile>:p')), ':h')

python3 << EOF
import sys
from os.path import normpath, join
import vim

plugin_root_dir = vim.eval('s:plugin_root_dir')
python_root_dir = normpath(join(plugin_root_dir, '..', 'python'))
sys.path.insert(0, python_root_dir)

import enc_dec

EOF

let g:secret_tmpfile = '/tmp/_vim_secret'


function! SetSecret()
    if exists("b:secret") && b:border_line_number > 0
        echo "WARNING!! You already have set a secret and encrypted text.\nYou might first want to decrypt and then only set another secret."
        return
    endif
    let inp = "Enter a secret that will encrypt/decrypt your text: "
    let b:secret=input(inp)
endfunction


function! CheckAndSetSecret()
    if !exists("b:secret")
        let info = input("INFO: You are editing a secret file(.sec). [Press Enter]")
        call SetSecret()
    endif
endfunction


function! LoadTextAndCleanup()
    " First, Clear all contents
    normal gg
    normal dG
    " Load text from tmp file created by python script
    execute '0read ' . g:secret_tmpfile
    " An extra new line is always added, just remove that
    normal Gdd
    " Clean up the tmp file
    silent execute "!rm " . g:secret_tmpfile
endfunction


function! EncryptText()
    " First set modifiable(might be set unmodifiable by CheckIfModifiable
    " function
    set ma
    " Get all the text
    let l:all_text = join(getline(1, '$'), "\n")
    " Call our python function
    silent python3 enc_dec.encrypt_buffer(vim.eval('l:all_text'))
    " Load content from the tmpfile that python script created
    call LoadTextAndCleanup()
    " Add an extra line at the end
    normal o
    call feedkeys("\<Esc>")
    " Call CheckIfModifiable Because modifiable has been set and this takes
    " cursor to last line which is still not modifiable
    call CheckIfModifiable()

endfunction


function! DecryptText()
    " First set modifiable(might be set unmodifiable by CheckIfModifiable
    " function
    set ma
    " Get all the text
    let l:all_text = join(getline(1, '$'), "\n")
    " Call our python function which writes the content to /tmp/_vim_secret
    python3 enc_dec.decrypt_buffer(vim.eval('l:all_text'))
    " Load content from the tmpfile that python script created
    call LoadTextAndCleanup()
    " Call CheckIfModifiable, Just in case
    call CheckIfModifiable()

endfunction


function! CheckIfModifiable()
    " Set the border line by python function, variable is b:border_line_number
    " Everything below and includeing b:border_line_number is encrypted
    let l:all_text = join(getline(1, '$'), "\n")

    " Get border line number, stored in b:border_line_number
    python3 enc_dec.set_border_line_number(vim.eval('l:all_text'))
    if line(".") <= b:border_line_number
        set noma
    else
        set ma
    endif
endfunction


" Setting file type
au BufEnter,BufNewFile,BufRead *.sec call CheckAndSetSecret()

" Make certain portion of file unmodifiable
" TODO: Call CheckIfModifiable not when cursor moves, but when text changes in
"       the buffer. This is inefficient because every time cursor moves, it's
"       not necessary to check for border line.
au CursorMoved,CursorMovedI *.sec call CheckIfModifiable()

command! -nargs=0 SetSecret call SetSecret()
command! -nargs=0 EncryptText call EncryptText()
command! -nargs=0 DecryptText call DecryptText()
