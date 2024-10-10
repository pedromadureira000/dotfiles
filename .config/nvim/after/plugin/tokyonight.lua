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
        -- H1 - Dark Red (Less Muted)
        hl["RenderMarkdownH1Bg"] = {bg = "#5a2626", bold = true }
        hl["@markup.heading.1.markdown"] = {fg = "#cc4444", bold = true }
        -- H2 - Dark Yellow (Less Muted)
        hl["RenderMarkdownH2Bg"] = {bg = "#5c5c26", bold = true}
        hl["@markup.heading.2.markdown"] = {fg = "#cccc00", bold = true}
        -- H3 - Dark Green (Less Muted)
        hl["RenderMarkdownH3Bg"] = {bg = "#265c39", bold = true}
        hl["@markup.heading.3.markdown"] = {fg = "#44cc77", bold = true}
        -- H4 - Dark Cyan (Less Muted)
        hl["RenderMarkdownH4Bg"] = {bg = "#265c5c", bold = true}
        hl["@markup.heading.4.markdown"] = {fg = "#44cccc", bold = true}
        -- H5 - Dark Blue (Less Muted)
        hl["RenderMarkdownH5Bg"] = {bg = "#26375c", bold = true}
        hl["@markup.heading.5.markdown"] = {fg = "#4477cc", bold = true}
        -- H6 - Dark Purple (Less Muted)
        hl["RenderMarkdownH6Bg"] = {bg = "#5c265c", bold = true}
        hl["@markup.heading.6.markdown"] = {fg = "#cc44cc", bold = true}
    end
})
