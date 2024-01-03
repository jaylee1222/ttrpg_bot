import asyncio
from models.Monster import Monster

response_timeout = 20.0
async def check_player_health(players):
    players.sort(key=lambda x: int(x.health), reverse=True)
    return players[0]

async def get_attack_response(client, ctx, mons):
    def check(m):
        print(m.content)
        return isinstance(m.content, str) and m.content in mons
    try:
        for mon in mons:
            print(f'this is the mon: {mon}')
        response = await client.wait_for('message', check=check, timeout=response_timeout)
        print(f'this is the message: {response.content}')
        return response.content
    except asyncio.TimeoutError:
        return await ctx.send(f'Sorry, you took too long to answer.')