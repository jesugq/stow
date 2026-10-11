multiTap = hs.eventtap.new({ hs.eventtap.event.types.keyDown }, function(event)
  local keyCode = event:getKeyCode()
  local flags = event:getFlags()

  -- until alttab is approved
  -- ctrl+' -> cmd+tab
  if keyCode == 39 then
    if flags.ctrl and not (flags.alt or flags.cmd or flags.shift) then
      hs.eventtap.keyStroke({"cmd"}, "tab", 0)
      return true
    end
  end

  -- ctrl+[ -> escape
  if keyCode == 33 then
    if flags.ctrl and not (flags.alt or flags.cmd or flags.shift) then
      hs.eventtap.keyStroke({}, "escape", 0)
      return true
    end
  end

  -- ctrl+] -> alt+tab
  if keyCode == 30 then
    if flags.ctrl and not (flags.alt or flags.cmd or flags.shift) then
      hs.eventtap.keyStroke({"alt"}, "tab", 0)
      return true
    end
  end

  -- until alttab is approved
  -- cmd+tab -> alt+tab
  -- if keyCode == 48 then
    --   if flags.cmd and not (flags.alt or flags.ctrl or flags.shift) then
    --     hs.eventtap.keyStroke({"alt"}, "tab", 0)
    --     return true
    --   end
  -- end

  -- cmd+[ -> cmd+shift+[
  if keyCode == 33 then
    if flags.cmd and not (flags.ctrl or flags.alt or flags.shift) then
      hs.eventtap.keyStroke({"cmd", "shift"}, "[", 0)
      return true
    end
  end

  -- cmd+] -> cmd+shift+]
  if keyCode == 30 then
    if flags.cmd and not (flags.ctrl or flags.alt or flags.shift) then
      hs.eventtap.keyStroke({"cmd", "shift"}, "]", 0)
      return true
    end
  end

  return false
end)

multiTap:start()
hs.alert.show("Hammerspoon Config Loaded")

