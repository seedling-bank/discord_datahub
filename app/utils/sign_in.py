# @client.event
# async def on_message(message):
#     global result
#
#     utc_time = datetime.utcnow().replace(tzinfo=pytz.utc)
#     start_of_today_utc = utc_time.replace(hour=0, minute=0, second=0, microsecond=0)
#     end_of_today_utc = start_of_today_utc + timedelta(days=1, microseconds=-1)
#
#     start_timestamp = int(start_of_today_utc.timestamp() * 1000)
#     end_timestamp = int(end_of_today_utc.timestamp() * 1000)
#     formatted_utc_time = utc_time.strftime('%Y-%m-%d %H:%M:%S')
#     timestamp = int(utc_time.timestamp() * 1000)
#
#     if message.content.lower() == settings.Sign_In_Word:
#
#         user_discord_id = message.author.id
#         username = message.author.name
#         loguru.logger.info(f"The user with ID {user_discord_id} and username {username} has signed in.")
#
#         user_query = select(t_users).where(t_users.c.discord_id == user_discord_id)
#
#         async with async_session() as session:
#             try:
#                 result = await session.execute(user_query)
#                 result = result.fetchall()
#             except Exception as e:
#                 loguru.logger.error(e)
#                 loguru.logger.error(traceback.format_exc())
#
#         user_data = [{
#             'id': obj.id,
#             'username': obj.username,
#             'avatar': obj.avatar,
#             'create_time': obj.create_time,
#             'discord_id': obj.discord_id,
#             'twitter_id': obj.twitter_id,
#             'twitter_token': obj.twitter_token,
#             'discord_name': obj.discord_name,
#             'country': obj.country,
#             'email': obj.email,
#             'verified': obj.verified,
#             'tg_id': obj.tg_id,
#             'tg_username': obj.tg_username,
#             'address': obj.address,
#             'platform': obj.platform
#         } for obj in result]
#
#         if len(user_data) == 0:
#             await message.author.send("请到da官网来保存discord")
#             # await message.reply("请到da官网来保存discord")
#         else:
#             query = (
#                 select(t_discord_sign_in)
#                 .where(
#                     and_(
#                         t_discord_sign_in.discord_id == user_discord_id,
#                         t_discord_sign_in.create_time >= str(start_timestamp),
#                         t_discord_sign_in.create_time <= str(end_timestamp)
#                     ))
#             )
#
#             async with async_session() as session:
#                 try:
#                     result = await session.execute(query)
#                     results = result.scalars()
#                 except Exception as e:
#                     loguru.logger.error(e)
#                     loguru.logger.error(traceback.format_exc())
#
#             data = [{
#                 'id': obj.id,
#                 'discord_id': obj.discord_id,
#                 'discord_name': obj.discord_name,
#                 'create_time': obj.create_time,
#                 'update_time': obj.update_time,
#                 'time_at': obj.time_at
#             } for obj in results]
#
#             if len(data) == 0:
#                 information = {
#                     "discord_id": user_discord_id,
#                     "discord_name": username,
#                     "create_time": timestamp,
#                     "update_time": timestamp,
#                     "time_at": formatted_utc_time,
#                 }
#                 async with async_session() as session:
#                     try:
#                         query = insert(t_discord_sign_in).values(information)
#                         await session.execute(query)
#                         await session.commit()
#                     except Exception as e:
#                         loguru.logger.info(e)
#                         loguru.logger.error(traceback.format_exc())
#
#                 await message.author.send("签到成功")