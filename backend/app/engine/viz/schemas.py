"""
Schemas for the Viz Planner engine.
"""
from typing import List, Literal, Optional
from pydantic import BaseModel, Field

CHART_TYPES = [
    "line_chart", "bar_chart", "pie_chart", "scatter_plot",
    "choropleth_map_state", "choropleth_map_district",
    "stacked_bar_chart", "radar_chart"
]

class DataBinding(BaseModel):
    """Configuration for mapping data fields to chart axes/groups."""
    x_axis: str = Field(description="Data key for the X axis")
    y_axes: List[str] = Field(description="Data keys for the Y axes")
    group_by: Optional[str] = Field(default=None, description="Data key to group by, if applicable")

class ChartSpec(BaseModel):
    """Specification for a single chart in the dashboard."""
    chart_id: str = Field(description="Unique identifier for the chart")
    chart_type: str = Field(description="Type of chart, must be one of the approved CHART_TYPES")
    title: str = Field(description="Chart title")
    subtitle: str = Field(description="Chart subtitle")
    data_source: str = Field(description="Key in the simulation results to use as the data source")
    data_bindings: DataBinding = Field(description="Axis and grouping bindings")
    colors: List[str] = Field(default_factory=list, description="Optional color palette")
    source_label: str = Field(description="Label for the data source (e.g., 'LegiSim Projection')")
    explanation: str = Field(description="Brief explanation of what this chart demonstrates")

class VizPlannerOutput(BaseModel):
    """Structured output for the Viz Planner."""
    dashboard_charts: List[ChartSpec] = Field(max_length=4, description="Top level dashboard charts (max 4)")
    group_charts: List[ChartSpec] = Field(max_length=6, description="Demographic/group charts (max 6)")
    map_charts: List[ChartSpec] = Field(max_length=2, description="Geospatial map charts (max 2)")
