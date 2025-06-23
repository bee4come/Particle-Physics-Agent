# Copyright 2024-2025 The FeynmanCraft ADK Project Developers
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Initialization functions for FeynmanCraft ADK Agent."""

import logging
import os

loglevel = os.getenv("FEYNMANCRAFT_ADK_LOG_LEVEL", "INFO")
numeric_level = getattr(logging, loglevel.upper(), None)
if not isinstance(numeric_level, int):
    raise ValueError(f"Invalid log level: {loglevel}")
logger = logging.getLogger(__package__)
logger.setLevel(numeric_level)

MODEL = os.getenv("ADK_MODEL_NAME")
if not MODEL:
    MODEL = "gemini-2.5-flash"

# MODEL needs to be defined before this import
try:
    from . import agent  # pylint: disable=wrong-import-position
    from .agent import root_agent  # Export root_agent for ADK
except ImportError as e:
    # Allow package to be imported even without google dependencies
    logger.warning(f"Could not import agent module: {e}")
    agent = None
    root_agent = None

# ADK Application Package 