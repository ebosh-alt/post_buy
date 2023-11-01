from .Users import User, Users
from .Channels import Channel, Channels
from .Prices import Price, Prices
from .Publications import Publication, Publications

db_file_name = "bot/db/database"
users = Users(db_file_name=db_file_name, table_name="users")
channels = Channels(db_file_name=db_file_name, table_name="channel")
prices = Prices(db_file_name=db_file_name, table_name="price")
publications = Publications(db_file_name, table_name="publication")
__all__ = ("User", "Users", "users", "Channel", "Channels", "channels", "Price", "Prices", "prices", "Publication",
           "Publications", "publications")
