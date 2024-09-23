-- Snippets (LuaSnip)
  -- Snippets will load from LSP but this makes sure to
  -- load local and plugin snippets ASAP

-- require("luasnip.loaders.from_vscode").lazy_load()


-- require'luasnip'.filetype_extend("python", {"django"})
-- require'luasnip'.filetype_extend("dart", {"flutter"})
--require'luasnip'.filetype_extend("javascript", {"vue"})


local cmp = require("cmp")
local luasnip = require('luasnip')

require("luasnip.loaders.from_vscode").lazy_load()
require("luasnip.loaders.from_vscode").lazy_load({ paths = {"./my-snippets"}})

cmp.setup({
  mapping = cmp.mapping.preset.insert({
      ['<C-b>'] = cmp.mapping.scroll_docs(-4),
      ['<C-f>'] = cmp.mapping.scroll_docs(4),
      -- ['<C-o>'] = cmp.mapping.complete(),
      -- ['<C-e>'] = cmp.mapping.abort(),
      ['<CR>'] = cmp.mapping.confirm({ select = true }),
    }),
  snippet = {
    expand = function(args)
      luasnip.lsp_expand(args.body)
    end,
  },
  sources = cmp.config.sources({
    { name = 'nvim_lsp' },
    { name = 'luasnip' },
  }, {
    { name = 'buffer' },
  }),
})

-- mapping tab to jump on snippet parts
vim.keymap.set({"i", "s"}, "<Tab>",
function()
    if luasnip.expand_or_jumpable() then
        luasnip.expand_or_jump()
    else
        vim.api.nvim_feedkeys(vim.api.nvim_replace_termcodes("<Tab>", true, false, true), "n", false)
    end
end, {silent = true})


-- Avante
-- local avante = require('avante')
-- print(avante)

-- vim.api.nvim_create_autocmd("User", {
    -- pattern = "ToggleMyPrompt";
    -- once = true,
    -- callback = function() require("avante.config").override({
        -- system_prompt = "You are an great programming expert!",
    -- }) end,
-- })

-- vim.keymap.set(
    -- "n", "<leader>ay", 
    -- function() vim.api.nvim_exec_autocmds("User", { pattern = "ToggleMyPrompt" }) 
    -- end, { desc = "avante: toggle my prompt" }
-- )

