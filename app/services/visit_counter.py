import asyncio
from datetime import datetime
import time
from typing import Dict, List, Any, Optional

from app.logging import logger
from ..core.redis_manager import RedisManager
from ..schemas.counter import VisitCount

class VisitCounterService:
    def __init__(self, cache_ttl: int = 30):
        """Initialize the visit counter service with Redis manager"""
        self.redis_manager = RedisManager()
        self.visit_count_cache: Dict[str, tuple[int, float]] = {}
        self.cache_ttl = cache_ttl

    async def increment_visit(self, page_id: str) -> None:
        """
        Increment visit count for a page
        
        Args:
            page_id: Unique identifier for the page
        """
        # TODO: Implement visit count increment
        success = await self.redis_manager.increment(page_id)
        if success: # also updating the in memory cache
            visits = await self.redis_manager.get(page_id)
            self.visit_count_cache[page_id] = (visits, time.time() + self.cache_ttl)
        return success

    async def get_visit_count(self, page_id: str) -> VisitCount:
        """
        Get current visit count for a page
        
        Args:
            page_id: Unique identifier for the page
            
        Returns:
            Current visit count
        """
        # TODO: Implement getting visit count
        response = None
        if page_id in self.visit_count_cache:
            visits, expiry_time = self.visit_count_cache[page_id]
            if time.time() < expiry_time: # Checking if cache is still valid
                response = VisitCount(page_id=page_id, visits=visits, served_via="in_memory")

        if response is None:
            visits = await self.redis_manager.get(page_id)
            self.visit_count_cache[page_id] = (visits, time.time() + self.cache_ttl) #updating the in_memory cache to handle future reads
            response = VisitCount(page_id=page_id, visits=visits, served_via="redis")
        return response
