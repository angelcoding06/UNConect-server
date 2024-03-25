import requests
import strawberry
from typing import Dict

@strawberry.type
class Query:
    @strawberry.field
    async def get_post(self, post_id: str) -> bool:
        response = requests.get("http://unconnect_posts_ms:3001/posts",headers={"PostId":"66010daa39af4bd71291a077"})
        return response
