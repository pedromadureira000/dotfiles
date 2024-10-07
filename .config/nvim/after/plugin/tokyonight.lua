-- First, ensure both plugins are properly loaded
require("render-markdown").setup{}
require("tokyonight").setup({
    style = "night",
    transparent = true,
    styles = {
        functions = {}
    },
    on_colors = function(colors)
        -- These color modifications might not directly affect Markdown headers
        colors.hint = colors.orange
        colors.bg = "#000000"  -- Changed from red to black for better visibility
    end,
    on_highlights = function(hl, c)
        -- H1 - Red
        hl["RenderMarkdownH1Bg"] = {bg = "#45030e", bold = true }
        hl["@markup.heading.1.markdown"] = {fg = "#a11830", bold = true }
        -- H2 - Yellow
        hl["RenderMarkdownH2Bg"] = {bg = "#454403", bold = true}
        hl["@markup.heading.2.markdown"] = {fg = "#FFD700", bold = true}
        -- H3 - Green
        hl["RenderMarkdownH3Bg"] = {bg = "#034511", bold = true}
        hl["@markup.heading.3.markdown"] = {fg = "#00FF00", bold = true}
        -- H4 - Cyan
        hl["RenderMarkdownH4Bg"] = {bg = "#034545", bold = true}
        hl["@markup.heading.4.markdown"] = {fg = "#00FFFF", bold = true}
        -- H5 - Blue
        hl["RenderMarkdownH5Bg"] = {bg = "#031145", bold = true}
        hl["@markup.heading.5.markdown"] = {fg = "#0000FF", bold = true}
        -- H6 - Purple
        hl["RenderMarkdownH6Bg"] = {bg = "#450345", bold = true}
        hl["@markup.heading.6.markdown"] = {fg = "#800080", bold = true}
    end
})
