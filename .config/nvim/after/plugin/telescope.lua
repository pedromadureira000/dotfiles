local builtin = require('telescope.builtin')
vim.keymap.set('n', '<leader>S', builtin.find_files, {})
--vim.keymap.set('n', '<C-p>', builtin.git_files, {})
vim.keymap.set('n', '<leader>s', builtin.git_files, {})
vim.keymap.set('n', '<leader>g', function()
  builtin.grep_string({search = vim.fn.input("Grep > ") });
end)


local actions = require('telescope.actions')
local telescope = require('telescope')
telescope.setup({
   defaults = {
      layout_strategy = "horizontal",
      layout_config = {
        horizontal = { width = 0.99, height = 0.99, preview_cutoff = 0 }
      },
      preview = {
        timeout = 10000,
      },
      mappings = {
            i = {
              ["<C-k>"] = actions.move_selection_previous,
              ["<C-j>"] = actions.move_selection_next,
            },
      }
    }
})
