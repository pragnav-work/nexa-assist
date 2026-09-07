from src.agents.router import Router
from src.models.intents import Intent

router = Router()

print(router.route(Intent.POLICY_QUERY))
print(router.route(Intent.LEAVE_BALANCE))
print(router.route(Intent.ASSIGNED_ASSETS))
print(router.route(Intent.UNKNOWN))