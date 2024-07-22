# @router.get("/discord_channels")
# async def discord_channels(server_id: int):
#     """
#     TODO: discord_owner
#     """
#     try:
#         bbs: BlabBotService = BlabBotService()
#         channels_list = await get_user_channel(bbs, server_id)
#         text_channel = [i for i in channels_list if i.get("type") == 0]
#         content = {
#             "code": 200,
#             "data": dict(channels=text_channel),
#             "message": "success",
#         }
#         return content
#     except Exception as e:
#         loguru.logger.error(e)
#         loguru.logger.error(traceback.format_exc())
#         return JSONResponse(status_code=500, content="get data error")
#
#
# @router.get("discord_me")
# async def discord_me(request: Request):
#     """
#     TODO: discord_owner
#     """
#     try:
#         token = request.session.get("oauth2_token").get("access_token")
#         dus: DiscordUserService = DiscordUserService(token=token)
#         user = await dus.get_user()
#         server_list = await dus.get_guilds()
#         if user.get("avatar"):
#             user["avatar_url"] = f"https://cdn.discordapp.com/avatars/{user['id']}/{user['avatar']}.png"
#         else:
#             user["avatar_url"] = None
#
#         new_server_list = []
#         if not user:
#             return JSONResponse(
#                 content={"code": 500, "message": "fetch user error"}, status_code=500
#             )
#
#         admin_guilds = await dus.get_admin_guilds()
#         bbs: BlabBotService = BlabBotService()
#         bot_guilds_id = await get_user_guild(bbs)
#         admin_guilds_id = [g["id"] for g in admin_guilds]
#
#         owner = set(bot_guilds_id).intersection(admin_guilds_id)
#         if not isinstance(owner, list):
#             owner = list(owner)
#         if server_list:
#             for server in server_list:
#                 if int(server.get("permissions")) & 0x8 == 0x8 and server.get("id") in owner:
#                     if server.get("icon"):
#                         server["icon_url"] = f"https://cdn.discordapp.com/icons/{server['id']}/{server['icon']}.png"
#                     else:
#                         server["icon_url"] = None
#                     new_server_list.append(server)
#
#         return JSONResponse(
#             content={
#                 "code": 200,
#                 "data": dict(user=user, server_list=new_server_list),
#                 "message": "success",
#             }
#         )
#
#     except Exception as e:
#         loguru.logger.error(e)
#         loguru.logger.error(traceback.format_exc())
#
#         return JSONResponse(
#             status_code=500, content={"code": 500, "message": "fetch user info error"}
#         )






# @router.get("/discord_owner")
# async def discord_owner(request: Request):
#     """
#     TODO: discord_owner
#     """
#     try:
#         token = request.session.get("oauth2_token").get("access_token")
#         dus: DiscordUserService = DiscordUserService(token)
#         bbs: BlabBotService = BlabBotService()
#         admin_guilds = await dus.get_admin_guilds()
#         bot_guilds = await bbs.get_all_guilds()
#         admin_guilds_id = [g["id"] for g in admin_guilds]
#         bot_guilds_id = [g["id"] for g in bot_guilds]
#         owner = set(bot_guilds_id).intersection(admin_guilds_id)
#         return JSONResponse(content=dict(code=200, data=list(owner)))
#     except Exception as e:
#         loguru.logger.error(e)
#         loguru.logger.error(traceback.format_exc())
#         return JSONResponse(status_code=500, content="get data error")







# @router.get("/verify_discord")
# async def verify_discord(request: Request, user_id: int, db: Database = Depends(get_db)):
#     try:
#
#         token = request.session.get("oauth2_state")
#         session = request.session
#         loguru.logger.info(f"session {session}")
#         loguru.logger.info(f"request {token}")
#         dus: DiscordUserService = DiscordUserService(
#             request.session.get("oauth2_token").get("access_token")
#         )
#         user = await dus.get_user()
#         if user.get("avatar"):
#             user["avatar_url"] = (
#                 f"https://cdn.discordapp.com/avatars/{user['id']}/{user['avatar']}.png"
#             )
#         else:
#             user["avatar_url"] = None
#
#         discord_id = user.get("id")
#         discord_name = user.get("username")
#         information = {
#             "discord_id": discord_id,
#             "discord_name": discord_name
#         }
#         query = t_users.update().where(t_users.c.id == user_id).values(information)
#         try:
#             await db.execute(query)
#         except Exception as e:
#             loguru.logger.info(e)
#             loguru.logger.error(traceback.format_exc())
#
#         if request.session.get("oauth2_token"):
#             return JSONResponse(
#                 content={
#                     "code": 200,
#                     "data": dict(status=True, token=token, user_info=user),
#                 },
#                 status_code=200,
#             )
#         else:
#             return JSONResponse(content=dict(status=False))
#
#     except Exception as e:
#         loguru.logger.info(e)
#         loguru.logger.error(traceback.format_exc())


