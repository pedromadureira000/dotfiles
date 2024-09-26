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
  {'nvim-treesitter/nvim-treesitter', build = ':TSUpdate'},
  'vim-airline/vim-airline',
  'vim-airline/vim-airline-themes',
  'Yggdroot/indentLine',
  -- 'preservim/vim-markdown',
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
    -- Avante!
    {
      "yetone/avante.nvim",
      event = "VeryLazy",
      lazy = false,
      version = false, -- set this if you want to always pull the latest change
      opts = {
        -- add any opts here
        provider = "openai",
        openai = {
            use_xml_format=true,
            model="gpt-4o",
            -- model="chatgpt-4o-latest",
            -- model="gpt-4o-mini",
            temperature=0.2,
            top_p=0.1,
            max_tokens = 4000,
            -- timeout  in miliseconds
        },
        behaviour = {
            auto_suggestions = false, -- Experimental stage
            auto_set_highlight_group = true,
            auto_set_keymaps = true,
            auto_apply_diff_after_generation = false,
            support_paste_from_clipboard = true,
        },
        windows = {
            ---@type "right" | "left" | "top" | "bottom"
            position = "top", -- the position of the sidebar
            wrap = true, -- similar to vim.o.wrap
            width = 80, -- default % based on available width
            hight=400,
            sidebar_header = {
              align = "center", -- left, center, right for title
              rounded = true,
            },
        },
        mappings = {
            -- ask = "<leader>ua", -- ask
            -- edit = "<leader>ue", -- edit
            -- refresh = "<leader>hr", -- refresh
            --- @class AvanteConflictMappings
            diff = {
              ours = "co",
              theirs = "ct",
              all_theirs = "ca",
              both = "cb",
              cursor = "cc",
              next = "]x",
              prev = "[x",
            },
            suggestion = {
              accept = "<M-l>",
              next = "<M-]>",
              prev = "<M-[>",
              dismiss = "<C-]>",
            },
            jump = {
              next = "]]",
              prev = "[[",
            },
            submit = {
              normal = "<CR>",
              insert = "<C-s>",
            },
            sidebar = {
              switch_windows = "<Tab>",
              reverse_switch_windows = "<S-Tab>",
            },
        },
      },
      -- if you want to build from source then do `make BUILD_FROM_SOURCE=true`
      build = "make",
      -- build = "powershell -ExecutionPolicy Bypass -File Build.ps1 -BuildFromSource false" -- for windows
      dependencies = {
        "stevearc/dressing.nvim",
        "nvim-lua/plenary.nvim",
        "MunifTanjim/nui.nvim",
        --- The below dependencies are optional,
        "nvim-tree/nvim-web-devicons", -- or echasnovski/mini.icons
        --"zbirenbaum/copilot.lua", -- for providers='copilot'
        --{
          -- support for image pasting
          -- "HakonHarnes/img-clip.nvim",
          -- event = "VeryLazy",
          -- opts = {
            -- recommended settings
            -- default = {
              -- embed_image_as_base64 = false,
              -- prompt_for_file_name = false,
              -- drag_and_drop = {
                -- insert_mode = true,
              -- },
              -- required for Windows users
              -- use_absolute_path = true,
            -- },
          -- },
        -- },
        -- Make sure to set this up properly if you have lazy=true
        -- {
          -- 'MeanderingProgrammer/render-markdown.nvim',
          -- opts = {
            -- file_types = { "markdown", "Avante" },
          -- },
          -- ft = { "markdown", "Avante" },
        -- },
      },
    }
}

OPTS = {}

require("lazy").setup(plugins, OPTS)
