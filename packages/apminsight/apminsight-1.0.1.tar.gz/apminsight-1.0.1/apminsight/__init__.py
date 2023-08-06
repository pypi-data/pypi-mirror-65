
import os
from .agentfactory import get_agent

name = "apminsight"

version = "1.0"

installed_path = os.path.dirname(__file__)

agent = get_agent()