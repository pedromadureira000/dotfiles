------------- configs
vim.opt.nu = true
vim.opt.relativenumber = false

vim.opt.wrap = true -- break line after pass screen limit

vim.opt.hlsearch = true --high light search and incremental bellow (actually it's the default value)
vim.opt.incsearch = true

vim.opt.termguicolors = true -- good colors

vim.opt.scrolloff = 8 -- minimum number of screen lines to keep above and below the cursor when scrolling vertically

vim.opt.updatetime = 50
vim.opt.colorcolumn = '80'


vim.o.number = true
vim.o.inccommand = 'split'
vim.o.clipboard = 'unnamedplus'
vim.o.fixendofline = false

-- TextEdit might fail if hidden is not set.
vim.o.hidden = true

-- Text folding
vim.o.foldmethod = 'indent'
vim.o.foldlevel = 99


-- Indentation
vim.o.tabstop = 4
vim.o.softtabstop = 4
vim.o.shiftwidth = 4
vim.o.expandtab = true

-- Save text folding
vim.api.nvim_exec([[
  autocmd BufWinLeave *.* mkview
  autocmd BufWinEnter *.* silent! loadview
]], false)

-- Github Copilot
vim.b.copilot_enabled = 0
vim.api.nvim_exec([[
  autocmd FileType markdown let g:copilot_enabled = 0
]], false)

