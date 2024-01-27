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

-- other configs
vim.cmd([[set cmdheight=1]])
--------------------- plugins
--- NERDTree
vim.g.NERDTreeIgnore = {'^node_modules$'}

-- Github Copilot
vim.b.copilot_enabled = 0
vim.api.nvim_exec([[
  autocmd FileType markdown let g:copilot_enabled = 0
]], false)
-- NERDTree settings
    -- Enable filetype plugins
--vim.cmd('filetype plugin on')

vim.g.NERDSpaceDelims = 1
vim.g.NERDDefaultAlign = 'left'
vim.g.NERDCustomDelimiters = {
  vue = { left = '/**', right = '*/', leftAlt = '<!--', rightAlt = '-->' },
  ["'"] = { left = '---/', right = '', leftAlt = '========================/', rightAlt = '/=======================' },
  dart = { left = '//', right = '', leftAlt = '//', rightAlt = '' }
}
-- airline
  -- Set Airline theme to 'behelit'
vim.g.airline_theme = 'behelit'
  -- Disable Airline whitespace extension
vim.g['airline#extensions#whitespace#enabled'] = 0
