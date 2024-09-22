local lsp_zero = require('lsp-zero')

-- set lsp keybinds
lsp_zero.on_attach(function(client, bufnr)
  -- see :help lsp-zero-keybindings
  -- to learn the available actions
  lsp_zero.default_keymaps({buffer = bufnr})
end)

require('mason').setup({})
require('mason-lspconfig').setup({
  -- Replace the language servers listed here with the ones you want to install
  ensure_installed = {
    'pyright',
    'lua_ls'
  },
  handlers = {
    lsp_zero.default_setup,
  },
})

----- dart config
lsp_zero.setup_servers({'dartls', force = true})

local lsp_config = require("lspconfig")
local capabilities = require("cmp_nvim_lsp").default_capabilities()

lsp_config["dartls"].setup({
	capabilities = capabilities,
	cmd = {
		"dart",
		"language-server",
		"--protocol=lsp",
		-- "--port=8123",
		-- "--instrumentation-log-file=/Users/robertbrunhage/Desktop/lsp-log.txt",
	},
	filetypes = { "dart" },
	init_options = {
		onlyAnalyzeProjectsWithOpenFiles = false,
		suggestFromUnimportedLibraries = true,
		closingLabels = true,
		outline = false,
		flutterOutline = false,
	},
	settings = {
		dart = {
			analysisExcludedFolders = {
				vim.fn.expand("$HOME/AppData/Local/Pub/Cache"),
				vim.fn.expand("$HOME/.pub-cache"),
				vim.fn.expand("/opt/homebrew/"),
				vim.fn.expand("$HOME/tools/flutter/"),
			},
			updateImportsOnRename = true,
			completeFunctionCalls = true,
			showTodos = true,
		},
	},
})
