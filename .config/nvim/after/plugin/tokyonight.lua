
require("tokyonight").setup({
    style = "night",
    transparent = true,
    styles = {
        functions = {}
    },
    on_colors = function(colors)
        colors.hint = colors.orange
        colors.bg = "#ff0000"
        -- colors.black = "#ff0000"
        -- colors.bg_dark = "#ff0000"
    end
})
