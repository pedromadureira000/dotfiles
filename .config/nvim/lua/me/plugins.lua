--------------------------- Bootstrap
local lazypath = vim.fn.stdpath("data") .. "/lazy/lazy.nvim"

if not vim.loop.fs_stat(lazypath) then
  vim.fn.system({
    "git",
    "clone",
    "--filter=blob:none",
    "https://github.com/folke/lazy.nvim.git",
    "--branch=stable", -- latest stable release
    lazypath,
  })
end

vim.opt.rtp:prepend(lazypath)


local plugins = {
  -- File manager
  {
    'nvim-telescope/telescope.nvim', tag = '0.1.5',
    dependencies = { {'nvim-lua/plenary.nvim'} }
  },
  'preservim/nerdtree',
  'airblade/vim-rooter',  --Changes Vim working directory to project root. (necessary for nerdtree to work)
  --git
  'airblade/vim-gitgutter',
  -- UI
  {
    "folke/tokyonight.nvim",
    lazy = false,
    priority = 1000,
    opts = {},
  },
  {'nvim-treesitter/nvim-treesitter', build = ':TSUpdate'},
  'vim-airline/vim-airline',
  'vim-airline/vim-airline-themes',
  'Yggdroot/indentLine',
  -- LSP
  {'VonHeikemen/lsp-zero.nvim', branch = 'v3.x'},
  {'neovim/nvim-lspconfig'},
	-- Simpler installation of LSP servers
  {'williamboman/mason.nvim'},
  {'williamboman/mason-lspconfig.nvim'},
  -- Autocompletion
  {'hrsh7th/cmp-nvim-lsp'},
  {'hrsh7th/nvim-cmp'},
  'jiangmiao/auto-pairs',
  -- Snippets
  {'L3MON4D3/LuaSnip', dependencies = {"rafamadriz/friendly-snippets"}},
  "saadparwaiz1/cmp_luasnip",
  -- dart
    -- Language support, mainly for indentation because it's more stable than treesitter
  "dart-lang/dart-vim-plugin",
  -- commentary
  'pedromadureira000/nerdcommenter_with_lazy_fix',
  {
    'MeanderingProgrammer/render-markdown.nvim',
    opts = {
        -- heading = {
        -- },
        bullet = {
            -- Turn on / off list bullet rendering
            enabled = false,
            -- Replaces '-'|'+'|'*' of 'list_item'
            -- How deeply nested the list is determines the 'level'
            -- The 'level' is used to index into the list using a cycle
            -- If the item is a 'checkbox' a conceal is used to hide the bullet instead
            icons = { '●', '○', '◆', '◇' },
            -- Padding to add to the left of bullet point
            left_pad = 0,
            -- Padding to add to the right of bullet point
            right_pad = 0,
            -- Highlight for the bullet icon
            highlight = 'RenderMarkdownBullet',
        },
    },
  },
}

OPTS = {}

require("lazy").setup(plugins, OPTS)
