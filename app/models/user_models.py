from sqlalchemy import Table, MetaData, Column, INTEGER, String, DATETIME, Integer, DateTime, Text, VARCHAR
from sqlalchemy.dialects.mysql import BIGINT
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

metadata = MetaData()

t_discord_users = Table(
    "discord_users",
    metadata,
    Column("id", INTEGER(), primary_key=True, autoincrement=True),
    Column("discord_id", INTEGER()),
    Column("discord_name", INTEGER()),
    Column("joined_at", INTEGER()),
    Column("create_time", String(255, "utf8mb4_unicode_520_ci")),
    Column("update_time", String(255, "utf8mb4_unicode_520_ci")),
    Column("time_at", DATETIME()),
)

t_lumoz_discord_users_info = Table(
    "lumoz_discord_users_info",
    metadata,
    Column("id", INTEGER(), primary_key=True, autoincrement=True),
    Column("discord_id", INTEGER()),
    Column("discord_name", INTEGER()),
    Column("joined_at", INTEGER()),
    Column("create_time", String(255, "utf8mb4_unicode_520_ci")),
    Column("update_time", String(255, "utf8mb4_unicode_520_ci")),
    Column("time_at", DATETIME()),
)

t_users = Table(
    "users",
    metadata,
    Column("id", BIGINT(), primary_key=True),
    Column("username", Text(4, "utf8mb4_unicode_ci")),
    Column("avatar", Text(100, "utf8mb4_unicode_ci")),
    Column("create_time", BIGINT(20)),
    Column("discord_id", VARCHAR(255, "utf8mb4_unicode_ci")),
    Column("twitter_id", VARCHAR(255, "utf8mb4_unicode_ci")),
    Column("twitter_token", VARCHAR(512, "utf8mb4_unicode_ci")),
    Column("discord_name", VARCHAR(255, "utf8mb4_unicode_ci")),
    Column("country", VARCHAR(255, "utf8mb4_unicode_ci")),
    Column("email", VARCHAR(255, "utf8mb4_unicode_ci")),
    Column("verified", VARCHAR(255, "utf8mb4_unicode_ci")),
    Column("tg_id", VARCHAR(255, "utf8mb4_unicode_ci")),
    Column("tg_username", VARCHAR(255, "utf8mb4_unicode_ci")),
    Column("address", VARCHAR(255, "utf8mb4_unicode_ci")),
    Column("platform", VARCHAR(255, "utf8mb4_unicode_ci")),
)


class t_discord_sign_in(Base):
    __tablename__ = 'discord_sign_in'
    __table_args__ = {'mysql_charset': 'utf8mb4', 'mysql_collate': 'utf8mb4_unicode_520_ci'}

    id = Column(Integer, primary_key=True, autoincrement=True)
    discord_id = Column(Integer)
    discord_name = Column(String(255))
    create_time = Column(String(255))
    update_time = Column(String(255))
    time_at = Column(DateTime)
