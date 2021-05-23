from pyrogram import filters

from DaisyX import ARQ_API_URL, SkemX as app, arq, command


@app.on_message(command("arq"))
async def arq_stats(_, message):
    data = await arq.stats()
    if not data.ok:
        await message.reply_text(data.result)
        return
    data = data.result
    uptime = data.uptime
    requests = data.requests
    cpu = data.cpu
    server_mem = data.memory.server
    api_mem = data.memory.api
    disk = data.disk
    platform = data.platform
    python_version = data.python
    users = data.users
    statistics = f"""
**Uptime:** `{uptime}`
**Requests:** `{requests}`
**CPU:** `{cpu}`
**Memory:**
    **Total Used:** `{server_mem}`
    **Used By API:** `{api_mem}`
**Disk:** `{disk}`
**Platform:** `{platform}`
**Python:** `{python_version}`
**Users:** `{users}`
**Address:** {ARQ_API_URL}
"""
    await message.edit_text(statistics)
