from django.urls import path

from panel.src.web.views.auth_view import login_page, login_submit, logout_submit
from panel.src.web.views.dashboard_view import (
    dashboard_page,
    summary_partial,
    activity_partial,
    alerts_partial,
    top_products_partial,
    search_results_partial,
)
from panel.src.web.views.actions_stock_view import (
    stock_entry_submit,
    stock_exit_submit,
    stock_adjust_to_count_submit,
)
from panel.src.web.views.product_view import product_detail_page, kardex_partial

app_name = "panel"

urlpatterns = [
    # Auth
    path("login/", login_page, name="login_page"),
    path("login/submit/", login_submit, name="login_submit"),
    path("logout/submit/", logout_submit, name="logout_submit"),

    # Pages
    path("", dashboard_page, name="dashboard"),
    path("products/<int:product_id>/", product_detail_page, name="product_detail"),

    # Partials
    path("partials/summary/", summary_partial, name="summary_partial"),
    path("partials/activity/", activity_partial, name="activity_partial"),
    path("partials/alerts/", alerts_partial, name="alerts_partial"),
    path("partials/top-products/", top_products_partial, name="top_products_partial"),
    path("partials/search-results/", search_results_partial, name="search_results_partial"),
    path("partials/kardex/<int:product_id>/", kardex_partial, name="kardex_partial"),

    # Actions
    path("actions/stock/entry/", stock_entry_submit, name="stock_entry_submit"),
    path("actions/stock/exit/", stock_exit_submit, name="stock_exit_submit"),
    path("actions/stock/adjust-to-count/", stock_adjust_to_count_submit, name="stock_adjust_to_count_submit"),
]
