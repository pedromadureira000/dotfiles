require("me.remap")
require("me.plugins")
require("me.sets")
require("me.fzf")
require("me.completions")

---Color scheme
vim.g.material_theme_style = 'my_own_theme'
vim.cmd [[colorscheme my_color_scheme]]


local autocmd = vim.api.nvim_create_autocmd
local augroup = vim.api.nvim_create_augroup
local yank_group = augroup("HighlightYank", {})
local format_options_group = augroup("FormatOptions", { clear = true })
--This autocmd triggers after text is yanked (copied). 
--It uses vim.highlight.on_yank to highlight the yanked text using the 
--highlight group "IncSearch" with a timeout of 100 milliseconds.
autocmd("TextYankPost", {
	group = yank_group,
	pattern = "*",
	callback = function()
		vim.highlight.on_yank({
			higroup = "IncSearch",
			timeout = 100,
		})
	end,
})


-- This needs to be an auto command instead of simply putting this in your vimrc
-- or init.lua as set or vim.o. If you have ftplugin enabled, vim has built-in
-- files for common programming languages, for which the format options are
-- usually already preset (with +cro), meaning that whatever you add in your
-- vimrc or init.lua will get overridden by the native ft plugin loading the
-- [filetype].vim file. So you need to to do the change after the ft file is
-- loaded
autocmd("BufEnter", {
    group = format_options_group,
    pattern = "*",
    desc = "Set buffer local formatoptions.",
    callback = function()
        vim.opt_local.formatoptions:remove({
            "r", -- Automatically insert the current comment leader after hitting <Enter> in Insert mode.
            "o", -- Automatically insert the current comment leader after hitting 'o' or 'O' in Normal mode.
        })
    end,
})
