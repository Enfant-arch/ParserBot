# - *- coding: utf- 8 - *-
import asyncio
import json

import requests
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery

from admin_panel.filters import IsAdmin
from keyboards.default import payment_default
from keyboards.inline import choice_way_input_payment_func
from loader import dp, bot
from states import StorageQiwi
from utils import send_all_admin, clear_firstname
from utils.db_api.psql  import get_paymentx, update_paymentx


###################################################################################
########################### ВКЛЮЧЕНИЕ/ВЫКЛЮЧЕНИЕ ПОПОЛНЕНИЯ #######################
# Включение пополнения
