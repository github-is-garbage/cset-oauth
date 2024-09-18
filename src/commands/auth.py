from bot import Bot
import discord
import msal
import os

@Bot.tree.command(name = "auth")
async def auth(interaction: discord.Interaction):
	await interaction.response.send_message("Sending request to Microsoft...", ephemeral = True)

	App = msal.PublicClientApplication(os.getenv("AZURE_APPLICATION_ID"), authority = os.getenv("MSAL_AUTHORITY"))
	Flow = App.initiate_device_flow(scopes = [ os.getenv("MSAL_SCOPE") ])

	UserCode = Flow.get("user_code")
	VerificationURL = Flow.get("verification_uri")

	if UserCode is None or VerificationURL is None:
		await interaction.edit_original_response(content = "Failed to generate a linking code.\nPlease contact an administrator.")

	await interaction.edit_original_response(content = f"To sign in, use a web browser to open the page <{VerificationURL}> and enter the code `{UserCode}`")

	Result = App.acquire_token_by_device_flow(Flow)
	AccessToken = Result.get("access_token")

	if AccessToken is None:
		await interaction.edit_original_response(content = "Failed to link account.\nPlease try again.")

	await interaction.edit_original_response(content = "Something happened")
