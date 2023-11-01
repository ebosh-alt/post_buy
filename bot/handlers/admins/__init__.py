from .check_post import check_post_rt
from .check_payment import check_pay_rt
from .admin_panel import admin_rt

router_admin = (check_post_rt, check_pay_rt, admin_rt)