"""Template registry for math models."""
from .templates.linear import LinearPassThrough
from .templates.elasticity import Elasticity
from .templates.price_chain import MultiplePriceTransmission
from .templates.io_model import InputOutputMultiplier
from .templates.budget import BudgetIdentity
from .templates.lag import DistributedLag
from .templates.feedback import FeedbackLoop
from .templates.monte_carlo import MonteCarloWrapper

TEMPLATE_REGISTRY = {
    "LinearPassThrough": LinearPassThrough,
    "Elasticity": Elasticity,
    "MultiplePriceTransmission": MultiplePriceTransmission,
    "InputOutputMultiplier": InputOutputMultiplier,
    "BudgetIdentity": BudgetIdentity,
    "DistributedLag": DistributedLag,
    "FeedbackLoop": FeedbackLoop,
    "MonteCarloWrapper": MonteCarloWrapper,
}
