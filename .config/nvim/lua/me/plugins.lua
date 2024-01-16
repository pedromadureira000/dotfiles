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
  --git
  'airblade/vim-gitgutter',
  -- UI
  {'nvim-treesitter/nvim-treesitter', build = ':TSUpdate'},
  -- LSP
  {'VonHeikemen/lsp-zero.nvim', branch = 'v3.x'},
  {'neovim/nvim-lspconfig'},
	-- Simpler installation of LSP servers
  {'williamboman/mason.nvim'},
  {'williamboman/mason-lspconfig.nvim'},
    -- Autocompletion
  {'hrsh7th/cmp-nvim-lsp'},
  {'hrsh7th/nvim-cmp'},
	-- Snippets engine
  {'L3MON4D3/LuaSnip'},
	-- snippets
	--"rafamadriz/friendly-snippets",
  -- dart
    -- Language support, mainly for indentation because it's more stable than treesitter
  "dart-lang/dart-vim-plugin",
    -- support for dart hot reload on save
  "RobertBrunhage/dart-tools.nvim",
}

OPTS = {}

require("lazy").setup(plugins, OPTS)
