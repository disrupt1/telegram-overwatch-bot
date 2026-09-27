import logging
import wmi
import psutil
import pynvml
from telegram import InlineQueryResultArticle, InputTextMessageContent, Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes

sensors = wmi.WMI(namespace="root\\LibreHardwareMonitor")

pynvml.nvmlInit()
gpuhandle = pynvml.nvmlDeviceGetHandleByIndex(0)

logger = logging.getLogger(__name__)

def inlinebuttons() -> InlineKeyboardMarkup:
    buttons = [
        [
            InlineKeyboardButton("🧠 CPU", callback_data="get_cpu"),
            InlineKeyboardButton("🖥 RAM", callback_data="get_ram"),
            InlineKeyboardButton("🎮 GPU", callback_data="get_gpu"),
            InlineKeyboardButton("💾 Disk", callback_data="get_disk")
        ],
        [InlineKeyboardButton("🔄 Update All", callback_data="get_all")],
    ]
    return InlineKeyboardMarkup(buttons)

def get_cpu_temp():
    for sensor in sensors.Sensor():
        if "Tctl/Tdie" in sensor.Name:
            return sensor.Value

    return None

def get_gpu_temp():
    for sensor in sensors.Sensor():
        if sensor.name == "GPU Core" and sensor.SensorType == "Temperature":
            return sensor.value

    return None

def get_cpu() -> str:
    cpu = psutil.cpu_percent(interval=1)
    cores = psutil.cpu_count(logical=False)
    threads = psutil.cpu_count(logical=True)
    cpu_temp = get_cpu_temp()
    if cpu_temp:
        return f"🧠 CPU Usage: {cpu}%\nNumber of cores: {cores}\nNumber of threads: {threads}\nCPU Temperature: {cpu_temp:.1f}°C"
    else:
        return f"🧠 CPU Usage: {cpu}%\nNumber of cores: {cores}\nNumber of threads: {threads}"

def get_gpu() -> str:
    gpuname = pynvml.nvmlDeviceGetName(gpuhandle)
    gpuutil = pynvml.nvmlDeviceGetUtilizationRates(gpuhandle)
    gpumem = pynvml.nvmlDeviceGetMemoryInfo(gpuhandle)
    gpupower = pynvml.nvmlDeviceGetPowerUsage(gpuhandle)
    gputemp = get_gpu_temp()
    if gputemp:
        return f"🎮 GPU Name: {gpuname}\nGPU Usage: {gpuutil.gpu}%\nVRAM Usage: {(gpumem.used / 1000000000):.1f} GB Out of {(gpumem.total / 1000000000):.1f} GB\nPower Draw: {(gpupower / 1000):.1f} W\nGPU Temperature: {gputemp}°C"
    else:
        return f"🎮 GPU Name: {gpuname}\nGPU Usage: {gpuutil.gpu}%\nVRAM Usage: {(gpumem.used / 100000000):.1f} GB Out of {(gpumem.total / 100000000):.1f} GB\nPower Draw: {(gpupower / 1000):.1f} W"

def get_ram() -> str:
    ram = psutil.virtual_memory()
    used_gb = ram.used / (1024 ** 3)
    total_gb = ram.total / (1024 ** 3)
    free_mem = ram.available / (1024 ** 3)
    return f"🖥 RAM Usage: {used_gb:.1f} GB Out of {total_gb:.1f} GB\nAvailable memory: {free_mem:.1f} GB"

def get_disk() -> str:
    disk = psutil.disk_usage("/")
    used_disk = disk.used / (1024 ** 3)
    total_gb = disk.total / (1024 ** 3)
    free_gb = disk.free / (1024 ** 3)
    return f"💾 Current Disk Usage: {used_disk:.1f} GB Out of {total_gb:.1f}GB\nFree Space: {free_gb:.1f} GB"

def get_all() -> str:
    return "\n\n".join([get_cpu(), get_ram(), get_gpu(), get_disk()])

async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = get_all()
    await update.message.reply_text(text, reply_markup=inlinebuttons(), parse_mode="Markdown")

async def status_inline(update: Update, context: ContextTypes.DEFAULT_TYPE):
    result = [
        InlineQueryResultArticle(
            id="1",
            title="Get the status of the computer",
            input_message_content=InputTextMessageContent(get_all())
        )
    ]
    await update.inline_query.answer(result)