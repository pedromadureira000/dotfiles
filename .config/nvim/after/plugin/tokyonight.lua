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
        -- H1 - Dark Red
        hl["RenderMarkdownH1Bg"] = {bg = "#5a2626", bold = true }
        hl["@markup.heading.1.markdown"] = {fg = "#bd0000", bold = true }
        -- H2 - Dark Yellow
        hl["RenderMarkdownH2Bg"] = {bg = "#5c5c26", bold = true}
        hl["@markup.heading.2.markdown"] = {fg = "#c2bf00", bold = true}
        -- H3 - Dark Green
        hl["RenderMarkdownH3Bg"] = {bg = "#265c39", bold = true}
        hl["@markup.heading.3.markdown"] = {fg = "#00bd0a", bold = true}
        -- H4 - Dark Cyan
        hl["RenderMarkdownH4Bg"] = {bg = "#265c5c", bold = true}
        hl["@markup.heading.4.markdown"] = {fg = "#13cfcf", bold = true}
        -- H5 - Dark Blue
        hl["RenderMarkdownH5Bg"] = {bg = "#26375c", bold = true}
        hl["@markup.heading.5.markdown"] = {fg = "#4775ff", bold = true}
        -- H6 - Dark Purple
        hl["RenderMarkdownH6Bg"] = {bg = "#5c265c", bold = true}
        hl["@markup.heading.6.markdown"] = {fg = "#c714c7", bold = true}
    end
})
