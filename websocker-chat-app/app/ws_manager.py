from __future__ import annotations
from fastapi import WebSocket
from typing import Dict, Set
from .logger import log

class WSConnection:
    def __init__(self, socket: WebSocket, username: str, room: str):
        self.socket = socket
        self.username = username
        self.room = room
        

class WSManager:
    def __init__(self):
        # room → set if connections
        self.active: Dict[str, Set[WSConnection]] = {}
        
    async def connect(self, conn:WSConnection):
        await conn.socket.accept()
        self.active.setdefault(conn.room, set()).add(conn)
        log.info(f"connected user=%s room=%s", conn.username, conn.room)
        
    
    def _remove(self, conn:WSConnection):
        room_set = self.active.get(conn.room)
        if room_set and conn in room_set:
            room_set.remove(conn)
            if not room_set:
                self.active.pop(conn.room, None)
            
    async def disconnect(self, conn:WSConnection):
        self._remove(conn)
        log.info("disconnected user=%s room=%s", conn.username, conn.room)
        
    async def broadcast(self, room:str, message:dict):
        for conn in list(self.active.get(room, set())):
            try:
                await conn.socket.send_json(message)
            except Exception as e:
                log.warning("send failed to %s: %s", conn.username, e)
                await self.disconnect(conn)

manager = WSManager()