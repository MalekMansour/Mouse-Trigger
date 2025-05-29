local Players = game:GetService("Players")
local RunService = game:GetService("RunService")
local UserInputService = game:GetService("UserInputService")
local Camera = workspace.CurrentCamera

local LocalPlayer = Players.LocalPlayer
local aimAssistEnabled = false
local aimStrength = 0.1 -- 0 = off, 1 = max assist
local toggleKey = Enum.KeyCode.E -- Press E to toggle

-- Toggle keybind
UserInputService.InputBegan:Connect(function(input, gameProcessed)
	if not gameProcessed and input.KeyCode == toggleKey then
		aimAssistEnabled = not aimAssistEnabled
		warn("Aim Assist " .. (aimAssistEnabled and "Enabled" or "Disabled"))
	end
end)

-- Get closest visible target to center of screen
local function getClosestTarget()
	local closest = nil
	local closestDist = math.huge

	for _, player in pairs(Players:GetPlayers()) do
		if player ~= LocalPlayer and player.Character and player.Character:FindFirstChild("Head") then
			local head = player.Character.Head
			local screenPoint, onScreen = Camera:WorldToViewportPoint(head.Position)

			if onScreen then
				local mousePos = Vector2.new(Camera.ViewportSize.X / 2, Camera.ViewportSize.Y / 2)
				local dist = (mousePos - Vector2.new(screenPoint.X, screenPoint.Y)).Magnitude

				if dist < closestDist and dist < 200 then
					closest = head
					closestDist = dist
				end
			end
		end
	end

	return closest
end

-- Main aim assist loop
RunService.RenderStepped:Connect(function()
	if not aimAssistEnabled then return end

	local target = getClosestTarget()
	if target then
		local targetPos = target.Position
		local camPos = Camera.CFrame.Position

		local newLook = (targetPos - camPos).Unit
		local currentLook = Camera.CFrame.LookVector
		local blendedLook = currentLook:Lerp(newLook, aimStrength)
		Camera.CFrame = CFrame.new(camPos, camPos + blendedLook)
	end
end)