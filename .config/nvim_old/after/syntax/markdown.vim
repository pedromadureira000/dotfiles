" The default file is /usr/share/vim/vim90/syntax/markdown.vim 
syn match markdownError "\w\@<=\w\@="

" H1 and H2 headings -> bold
" hi link markdownH1 markdownHxBold
" hi link markdownH2 markdownHxBold

" Heading delimiters (eg '#') and rules (eg '----', '====') -> bold
" hi link markdownHeadingDelimiter markdownHxBold
" hi link markdownRule markdownHxBold

" Code blocks and inline code -> highlighted
" hi link markdownCode htmlH1

" colors come from /usr/share/vim/vim90/colors
" hi markdownHxBold term=bold ctermfg=DarkMagenta gui=bold guifg=Magenta cterm=bold
