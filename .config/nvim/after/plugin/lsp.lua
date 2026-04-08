-- Native Neovim LSP setup for 0.12+ (Completely bypasses lspconfig framework)
local lspconfig = require('lspconfig')
local cmp_lsp = require('cmp_nvim_lsp')
local capabilities = cmp_lsp.default_capabilities()

-- Setup Mason
require('mason').setup({})
require('mason-lspconfig').setup({
  ensure_installed = { 'pyright', 'lua_ls' },
  handlers = {
    function(server_name)
      -- Silence deprecation warning for the core load
      local original_notify = vim.notify
      vim.notify = function() end
      
      lspconfig[server_name].setup({
        capabilities = capabilities,
      })
      
      vim.notify = original_notify
    end,
  },
})

-- Keybinds
vim.api.nvim_create_autocmd('LspAttach', {
  callback = function(ev)
    local opts = {buffer = ev.buf}
    vim.keymap.set('n', 'gd', vim.lsp.buf.definition, opts)
    vim.keymap.set('n', 'K', vim.lsp.buf.hover, opts)
    vim.keymap.set('n', '<leader>vd', vim.diagnostic.open_float, opts)
    vim.keymap.set('n', '[d', vim.diagnostic.goto_next, opts)
    vim.keymap.set('n', ']d', vim.diagnostic.goto_prev, opts)
    vim.keymap.set('n', '<leader>vca', vim.lsp.buf.code_action, opts)
    vim.keymap.set('n', '<leader>vrr', vim.lsp.buf.references, opts)
    vim.keymap.set('n', '<leader>vrn', vim.lsp.buf.rename, opts)
  end,
})

-- Dart Setup (Directly silenced)
local original_notify = vim.notify
vim.notify = function() end

lspconfig.dartls.setup({
  capabilities = capabilities,
  cmd = { "dart", "language-server", "--protocol=lsp" },
  filetypes = { "dart" },
  init_options = {
    onlyAnalyzeProjectsWithOpenFiles = false,
    suggestFromUnimportedLibraries = true,
    closingLabels = true,
  },
  settings = {
    dart = {
      updateImportsOnRename = true,
      completeFunctionCalls = true,
      showTodos = true,
    },
  },
})

vim.notify = original_notify

-- Clean Diagnostics
vim.diagnostic.config({
  underline = true,
  virtual_text = true,
  signs = true,
  float = { border = "rounded", source = "always" },
})
