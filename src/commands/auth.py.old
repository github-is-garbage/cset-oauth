from bot import Bot
from threadpool import RunInThread
import aiohttp
import discord
import jwt
import logging
import msal
import os

async def Bail(Interaction: discord.Interaction, Message = None):
	await Interaction.edit_original_response(content = Message if Message else "Something went wrong.\nPlease contact an administrator.")

async def GetLinkingInformation(Interaction: discord.Interaction):
	logging.getLogger("discord.client").info(f"Requesting linking code for user {Interaction.user.id}")

	App = msal.PublicClientApplication(os.getenv("AZURE_APPLICATION_ID"), authority = os.getenv("MSAL_AUTHORITY"))
	Flow = await RunInThread(App.initiate_device_flow, [ os.getenv("MSAL_SCOPE") ])

	UserCode = Flow.get("user_code")
	VerificationURL = Flow.get("verification_uri")

	if UserCode is None or VerificationURL is None:
		logging.getLogger("discord.client").error(f"Linking code for user {Interaction.user.id} is None")
		await Bail(Interaction)

		return (None, None, None, None)

	return (App, Flow, UserCode, VerificationURL)

async def GetAccessToken(Interaction: discord.Interaction, App: msal.PublicClientApplication, Flow: dict):
	logging.getLogger("discord.client").info(f"Requesting access token for user {Interaction.user.id}")

	Result = await RunInThread(App.acquire_token_by_device_flow, Flow)
	AccessToken = Result.get("access_token")

	if AccessToken is None:
		logging.getLogger("discord.client").error(f"Access token for user {Interaction.user.id} is None")
		await Bail(Interaction)

		return None

	return AccessToken

async def DecodeAccessToken(Interaction: discord.Integration, AccessToken: str):
	try:
		return jwt.decode(AccessToken, options={ "verify_signature": False }) # Why is the signature invalid :/
	except jwt.ExpiredSignatureError:
		logging.getLogger("discord.client").error(f"Graph user information request for user {Interaction.user.id} expired")
		await Bail(Interaction, "Your request has expired.\nPlease try again.")

		return None
	except:
		return None

async def GetUserInformation(Interaction: discord.Integration, AccessToken: str):
	DecodedToken = await DecodeAccessToken(Interaction, AccessToken)
	if DecodedToken is None: return (None, None)

	AccessURL = f"{DecodedToken.get("aud")}/v1.0/me"
	Headers = {
		"Authorization": f"Bearer {AccessToken}",
		"Content-Type": "applcation/json"
	}

	# Do this manually because the msgraph-sdk way doesn't work for whatever reason
	async with aiohttp.ClientSession() as Session:
		async with Session.get(AccessURL, headers = Headers) as Response:
			Status = Response.status
			ResponseData = await Response.json()

			if Status != 200: # OK
				logging.getLogger("discord.client").error(f"Graph user information request for user {Interaction.user.id} failed: {Status}")
				await Bail(Interaction)

				return None

			DisplayName = ResponseData.get("displayName")
			EmailAddress = ResponseData.get("mail") or ResponseData.get("userPrincipalName")

			if DisplayName is None or EmailAddress is None:
				logging.getLogger("discord.client").error(f"Graph user information request for user {Interaction.user.id} is missing required information")
				await Bail(Interaction)

				return None

			return ResponseData

@Bot.tree.command(name = "auth")
async def auth(Interaction: discord.Interaction):
	logging.getLogger("discord.client").info(f"User {Interaction.user.id} has initiated a link request")

	await Interaction.response.send_message("Starting linking process...", ephemeral = True)

	try:
		# Get code
		await Interaction.edit_original_response(content = "Sending request to Microsoft...")

		(App, Flow, UserCode, VerificationURL) = await GetLinkingInformation(Interaction)
		if App is None: return

		logging.getLogger("discord.client").info(f"Linking code for user {Interaction.user.id} is '{UserCode}'")
		await Interaction.edit_original_response(content = f"To sign in, use a web browser to open the page <{VerificationURL}> and enter the code `{UserCode}`")

		# Get token
		AccessToken = await GetAccessToken(Interaction, App, Flow)
		if AccessToken is None: return

		# Test token
		UserInformation = await GetUserInformation(Interaction, AccessToken)
		if UserInformation is None: return

		DisplayName = UserInformation.get("displayName")
		EmailAddress = UserInformation.get("mail") or UserInformation.get("userPrincipalName")

		logging.getLogger("discord.client").info(f"User {Interaction.user.id} is '{DisplayName}' ('{EmailAddress}')")

		await Interaction.edit_original_response(content = f"Linked to {DisplayName} (`{EmailAddress}`).\nYou can now dismiss this message.")
	except Exception as Error:
		logging.getLogger("discord.client").error(f"Link request {Interaction.user.id} had something go very wrong!\n{Error}")

		try:
			# This may not be the exact reason, but we need something to tell them
			await Bail(Interaction, "Your request has expired.\nPlease try again.")
		except:
			logging.getLogger("discord.client").error(f"Failed to notify {Interaction.user.id} of error")
