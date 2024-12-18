vim.g.mapleader = " "
vim.g.maplocalleader = " "
-- Note: xnoremap ('x') = visual mode
-- Note: nnoremap ('n') = normal mode
vim.api.nvim_set_keymap('', '<Space>', '', { noremap = true, silent = true })

-- remap 'q' and 'r' defaults
vim.api.nvim_set_keymap('n', 'r', '@', { noremap = true })  -- map 'r' to run macros ('r' and 'R' is replace command by default)
vim.api.nvim_set_keymap('n', 'Q', ':q!<CR>', { noremap = true }) -- map 'Q' to force-quit
vim.api.nvim_set_keymap('n', 'q', ':q<CR>', { noremap = true }) -- map 'q' to quit vim
-- better replace
vim.keymap.set("n", "R", [[:%s/\<<C-r><C-w>\>/<C-r><C-w>/gI<Left><Left><Left>]])
-- Take macro
vim.api.nvim_set_keymap('n', 't', 'q', { noremap = true })

-- Case insensitive search
vim.api.nvim_set_keymap('n', '<leader>/', '/\\c', { noremap = true })
vim.api.nvim_set_keymap('n', '<leader>?', '?\\c', { noremap = true })
vim.api.nvim_set_keymap('n', 'J', '}', { noremap = true })
vim.api.nvim_set_keymap('x', 'J', '}', { noremap = true })
vim.api.nvim_set_keymap('n', 'K', '{', { noremap = true })
vim.api.nvim_set_keymap('x', 'K', '{', { noremap = true })
-- on comand mode, I want to navegate with Ctr-f e Ctr-b
vim.api.nvim_set_keymap('c', '<C-F>', '<Right>', { noremap = true })
vim.api.nvim_set_keymap('c', '<C-B>', '<Left>', { noremap = true })
-- cutting
vim.api.nvim_set_keymap('n', 'c', '"_c', { noremap = true })
vim.api.nvim_set_keymap('x', 'c', '"_c', { noremap = true })
vim.api.nvim_set_keymap('n', 'C', '"_C', { noremap = true })
vim.api.nvim_set_keymap('x', 'C', '"_C', { noremap = true })
--copying
--vim.keymap.set("x", "<leader>p", "\"_dP") -- it is supposed to do what 'P' already does. So, it's uselles
-- deleting
vim.api.nvim_set_keymap('n', '<leader>d', '"_d', { noremap = true })
vim.api.nvim_set_keymap('x', '<leader>d', '"_d', { noremap = true })
vim.api.nvim_set_keymap('n', '<leader>D', '"_D', { noremap = true })
vim.api.nvim_set_keymap('x', '<leader>D', '"_D', { noremap = true })
-- save
vim.api.nvim_set_keymap('n', 's', ':w!<CR>', { noremap = true })
-- navegate on buffers
vim.api.nvim_set_keymap('n', '<leader>n', ':bnext<ESC>', { noremap = true })
vim.api.nvim_set_keymap('n', '<leader>p', ':bprevious<ESC>', { noremap = true })
-- close buffer
vim.api.nvim_set_keymap('n', '<leader>x', ':bd<ESC>', { noremap = true })
vim.api.nvim_set_keymap('n', '<leader>X', ':bd!<ESC>', { noremap = true })

-- spell checking
vim.api.nvim_set_keymap('n', 'fl', ':setlocal spell! spelllang=en_us<CR>', { noremap = true })
vim.api.nvim_set_keymap('n', 'fL', ':setlocal spell! spelllang=pt_br<CR>', { noremap = true })
vim.api.nvim_set_keymap('x', 'fw', 'z=', { noremap = true })
vim.api.nvim_set_keymap('n', 'fw', 'z=', { noremap = true })
-- down and up but less disorienting
vim.keymap.set("n", "<C-d>", "<C-d>zz")
vim.keymap.set("n", "<C-u>", "<C-u>zz")
-- trying to make 'gi' work again
vim.api.nvim_set_keymap('n', 'gi', 'gi', { noremap = true })
-- open NERDTree
vim.api.nvim_set_keymap('n', '<leader>o', ':NERDTreeToggle<CR>', { noremap = true })

-- fold and unfold command
vim.api.nvim_set_keymap('n', '<leader>m', 'za', { noremap = true })

-- tabgar 
vim.api.nvim_set_keymap('n', '<leader>j', ':TagbarOpenAutoClose<CR>', { noremap = true })
-- vim.api.nvim_set_keymap('n', '<leader>k', ':TagbarClose<CR>', { noremap = true })
vim.api.nvim_set_keymap('n', '<C-j>', ':TagbarJumpNext<CR>', { noremap = true })
vim.api.nvim_set_keymap('n', '<C-k>', ':TagbarJumpPrev<CR>', { noremap = true })

-------------- example of commands

----- run command on file
--vim.api.nvim_set_keymap('n', '<leader>ec', ':vsplit ~/.config/nvim/init.vim<CR>', { noremap = true })
--vim.api.nvim_set_keymap('n', '<leader>lc', ':source ~/.config/nvim/init.vim<CR>', { noremap = true })

----- makes bash file executable
-- vim.keymap.set("n", "<leader>x", "<cmd>!chmod +x %<CR>", { silent = true })  


------------- testing
--vim.keymap.set("v", "J", ":m '>+1<CR>gv=gv")
--vim.keymap.set("v", "K", ":m '<-2<CR>gv=gv")

--vim.keymap.set("n", "<leader>sv", ":vsplit <CR>")
--vim.keymap.set("n", "<leader>sh", ":split <CR>")

--vim.keymap.set("x", "p", "pgvy")

--vim.keymap.set("n", "<C-d>", "<C-d>zz")
--vim.keymap.set("n", "<C-u>", "<C-u>zz")

--vim.keymap.set("n", "<S-d>", "<cmd>cnext<CR>zz")
--vim.keymap.set("n", "<S-u>", "<cmd>cprev<CR>zz")

--vim.keymap.set("n", "<C-f>", ":silent !tmux neww tmux-sessionizer<CR>")
--vim.keymap.set("n", "<leader>ft", ":silent !flutter-test %:p<CR>")
--vim.keymap.set("n", "<leader>ss", ":%s/\\<<C-r><C-w>\\>/<C-r><C-w>/gI<Left><Left><Left>")
