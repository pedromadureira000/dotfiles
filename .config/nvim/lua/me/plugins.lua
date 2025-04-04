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
  'preservim/tagbar',
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
  -- 'Yggdroot/indentLine', # causing weird identation on cursor
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
  {'L3MON4D3/LuaSnip'},
  -- {'L3MON4D3/LuaSnip', dependencies = {"rafamadriz/friendly-snippets"}}, # commented becouse of "rafamadriz/friendly-snippets" bold markdown problem
  "saadparwaiz1/cmp_luasnip",
  -- dart
    -- Language support, mainly for indentation because it's more stable than treesitter
  "dart-lang/dart-vim-plugin",
  -- commentary
  'pedromadureira000/nerdcommenter_with_lazy_fix',
  {
    'MeanderingProgrammer/render-markdown.nvim',
    opts = {
        bullet = {
            enabled = false,
            icons = { '●', '○', '◆', '◇' },
            left_pad = 0,
            right_pad = 0,
            highlight = 'RenderMarkdownBullet',
        },
    },
  },
}

OPTS = {}

require("lazy").setup(plugins, OPTS)
