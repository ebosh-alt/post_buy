from .greeting import greeting_rt
from .price_list import price_list_rt
from .buy_advertisement import buy_rt
from .input_date import input_date_rt
from .choice_fixing import choice_fix_rt
from .confirm_doc import confirm_doc_rt
from .input_content import inp_content_rt
from .admins import router_admin
from .payment import payment_rt
from .ready_post import ready_post_rt
from .registration import registration_rt
from .del_messages import del_messages_rt

routers = (greeting_rt, price_list_rt, buy_rt, input_date_rt, choice_fix_rt, confirm_doc_rt, inp_content_rt, payment_rt,
           ready_post_rt, *router_admin, registration_rt, del_messages_rt)
