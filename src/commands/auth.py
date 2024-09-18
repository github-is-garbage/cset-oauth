from bot import Bot
import discord
import logging
import msal
import os
import requests

async def Bail(Interaction: discord.Interaction):
	await Interaction.edit_original_response(content = "Something went wrong.\nPlease contact an administrator.")

async def GetLinkingInformation(Interaction: discord.Interaction):
	App = msal.PublicClientApplication(os.getenv("AZURE_APPLICATION_ID"), authority = os.getenv("MSAL_AUTHORITY"))
	Flow = App.initiate_device_flow(scopes = [ os.getenv("MSAL_SCOPE") ])

	UserCode = Flow.get("user_code")
	VerificationURL = Flow.get("verification_uri")

	if UserCode is None or VerificationURL is None:
		logging.getLogger("discord.client").error(f"Linking code for user {Interaction.user.id} is None")
		await Bail(Interaction)

		return (None, None, None, None)

	return (App, Flow, UserCode, VerificationURL)

async def GetAccessToken(Interaction: discord.Interaction, App: msal.PublicClientApplication, Flow: dict):
	Result = App.acquire_token_by_device_flow(Flow)
	AccessToken = Result.get("access_token")

	if AccessToken is None:
		logging.getLogger("discord.client").error(f"Access token for user {Interaction.user.id} is None")
		await Bail(Interaction)

		return None

	return AccessToken

async def GetUserInformation(Interaction: discord.Integration, AccessToken: str):
	# Do this manually because the msgraph-sdk way doesn't work for whatever reason
	Response = requests.get(os.getenv("GRAPH_ACCESS_URL"), headers = {
		"Authorization": f"Bearer {AccessToken}",
		"Content-Type": "applcation/json"
	})

	Status = Response.status_code
	ResponseData = Response.json()

	Response.close()

	if Status != 200: # OK
		logging.getLogger("discord.client").error(f"Graph user information request for user {Interaction.user.id} failed: {Status}")
		await Bail(Interaction)

		return (None, None)

	DisplayName = ResponseData.get("displayName")
	EmailAddress = ResponseData.get("mail") or ResponseData.get("userPrincipalName")

	if DisplayName is None or EmailAddress is None:
		logging.getLogger("discord.client").error(f"Graph user information request for user {Interaction.user.id} is missing required information")
		await Bail(Interaction)

		return (None, None)

	return (DisplayName, EmailAddress)

@Bot.tree.command(name = "auth")
async def auth(Interaction: discord.Interaction):
	logging.getLogger("discord.client").info(f"User {Interaction.user.id} has initiated a link request")

	# Get code
	await Interaction.response.send_message("Sending request to Microsoft...", ephemeral = True)

	(App, Flow, UserCode, VerificationURL) = await GetLinkingInformation(Interaction)
	if App is None: return

	logging.getLogger("discord.client").info(f"Linking code for user {Interaction.user.id} is '{UserCode}'")
	await Interaction.edit_original_response(content = f"To sign in, use a web browser to open the page <{VerificationURL}> and enter the code `{UserCode}`")

	# Get token
	AccessToken = await GetAccessToken(Interaction, App, Flow)
	if AccessToken is None: return

	# Test token
	(DisplayName, EmailAddress) = await GetUserInformation(Interaction, AccessToken)
	if EmailAddress is None: return

	await Interaction.edit_original_response(content = f"Linked to {DisplayName} (`{EmailAddress}`).\nYou can now dismiss this message.")
