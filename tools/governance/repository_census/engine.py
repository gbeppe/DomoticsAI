"""Repository Census pipeline orchestration."""

from ..common.models import CensusState, Inventory
from ..processing import Pipeline
from .stages import (
    InventoryStage,
    RuleStage,
    ScanStage,
    StatisticsStage,
)


def run_census(ctx) -> Inventory:
    """Run the Repository Census processing pipeline."""

    state = CensusState(ctx=ctx)

    pipeline = Pipeline(
        [
            ScanStage(),
            RuleStage(),
            StatisticsStage(),
            InventoryStage(),
        ]
    )

    result = pipeline.run(state)

    if result.inventory is None:
        raise RuntimeError(
            "Repository Census pipeline did not produce an inventory"
        )

    return result.inventory
