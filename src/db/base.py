# This file gathers all models so Base.metadata is aware of them
# Make sure to import any newly created models here

from src.db.base_class import Base

# Import all models from feature packages
from src.auth.models import User
from src.chatbot.models import ChatSession
from src.dashboard.models import DashboardMetric
