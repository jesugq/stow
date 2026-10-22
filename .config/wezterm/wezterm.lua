local wezterm = require 'wezterm'
local config = wezterm.config_builder()
local keys = wezterm.gui.default_keys()
config.automatically_reload_config = false
config.enable_kitty_graphics = true
config.hide_tab_bar_if_only_one_tab = true

local function add_keybindings(target, inputs)
  for _, binding in ipairs(inputs) do
    table.insert(target, {
      key = binding.key,
      mods = binding.mods,
      action = binding.action,
    })
  end
end

-- theme
config.color_scheme = 'Ryuuko'

-- font
config.font = wezterm.font_with_fallback({ { family = 'Maple Mono NF', weight = 'Regular' } })
config.font_rules = {
  { intensity = 'Half', italic = false, font = wezterm.font({ family = 'Maple Mono NF Medium', weight = 'Light' }) },
  { intensity = 'Half', italic = true, font = wezterm.font({ family = 'Maple Mono NF Medium', weight = 'Light', style = 'Italic' }) },
  { intensity = 'Normal', italic = true, font = wezterm.font({ family = 'Maple Mono NF', style = 'Italic' }) },
  { intensity = 'Bold', italic = false, font = wezterm.font({ family = 'Maple Mono NF', weight = 'Bold' }) },
  { intensity = 'Bold', italic = true, font = wezterm.font({ family = 'Maple Mono NF', weight = 'Bold', style = 'Italic' }) },
}
config.font_size = 22.0

-- window
config.window_padding = { left = '12pt', right = '12pt', top = '12pt', bottom = '0pt', }

-- linux support
add_keybindings(keys, {
  { key = 'Enter', mods = 'CTRL', action = wezterm.action.SendString '\x1b[13;5u' },
  { key = 'Enter', mods = 'ALT', action = wezterm.action.SendString '\x1b[13;3u' },
})

-- macos support
-- alt+[ -> cmd+shift+[ == prev tab
-- alt+] -> cmd+shift+} == next tab
add_keybindings(keys, {
  { key = '{', mods = 'SUPER|SHIFT', action = wezterm.action.SendString('\x1b[123;3u') },
  { key = '}', mods = 'SUPER|SHIFT', action = wezterm.action.SendString('\x1b[125;3u') },
  { key = 'h', mods = 'SUPER', action = wezterm.action.SendString '\x1b[104;9u' },
  { key = 'j', mods = 'SUPER', action = wezterm.action.SendString '\x1b[106;9u' },
  { key = 'k', mods = 'SUPER', action = wezterm.action.SendString '\x1b[107;9u' },
  { key = 'l', mods = 'SUPER', action = wezterm.action.SendString '\x1b[108;9u' },
  { key = 'Enter', mods = 'SUPER', action = wezterm.action.SendString '\x1b[13;9u' },
})

-- globe support
add_keybindings(keys, {
  { key = 'c', mods = 'CTRL|SHIFT', action = wezterm.action.CopyTo 'Clipboard' },
  { key = 'v', mods = 'CTRL|SHIFT', action = wezterm.action.PasteFrom 'Clipboard' },
})

config.keys = keys
return config
