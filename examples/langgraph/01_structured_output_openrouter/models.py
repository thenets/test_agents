from pydantic import BaseModel, Field
from typing import List, Optional
from enum import Enum

class TaskPriority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    URGENT = "urgent"

class WeatherCondition(str, Enum):
    SUNNY = "sunny"
    CLOUDY = "cloudy"
    RAINY = "rainy"
    SNOWY = "snowy"
    STORMY = "stormy"

class WeatherResponse(BaseModel):
    """Structured response for weather queries"""
    location: str = Field(description="The location for which weather is reported")
    condition: WeatherCondition = Field(description="Current weather condition")
    temperature: int = Field(description="Temperature in Fahrenheit")
    humidity: Optional[int] = Field(default=None, description="Humidity percentage")
    description: str = Field(description="Brief description of the weather")

class Task(BaseModel):
    """Individual task item"""
    title: str = Field(description="Title of the task")
    description: str = Field(description="Detailed description of the task")
    priority: TaskPriority = Field(description="Priority level of the task")
    estimated_hours: Optional[float] = Field(default=None, description="Estimated hours to complete")

class TaskAnalysisResponse(BaseModel):
    """Structured response for task analysis queries"""
    project_name: str = Field(description="Name of the project being analyzed")
    total_tasks: int = Field(description="Total number of tasks identified")
    tasks: List[Task] = Field(description="List of individual tasks")
    estimated_completion_time: str = Field(description="Estimated time to complete all tasks")
    recommendations: List[str] = Field(description="List of recommendations for project success")

class PersonResponse(BaseModel):
    """Structured response for person information queries"""
    name: str = Field(description="Full name of the person")
    age: Optional[int] = Field(default=None, description="Age in years")
    occupation: Optional[str] = Field(default=None, description="Primary occupation")
    location: Optional[str] = Field(default=None, description="Current location")
    notable_achievements: List[str] = Field(default_factory=list, description="List of notable achievements")