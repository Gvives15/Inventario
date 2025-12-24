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
    stock_entry_by_sku_submit,
    stock_exit_by_sku_submit,
    stock_adjust_to_count_by_sku_submit,
)
from panel.src.web.views.product_view import product_detail_page, kardex_partial
from panel.src.web.views.products_view import products_page, products_table_partial, product_sheet_partial
from panel.src.web.views.alerts_view import alerts_page, alerts_list_partial
from panel.src.web.views.movement_drawer_view import movement_drawer_partial, movement_confirm_partial
from panel.src.web.views.movements_view import movements_page, movements_list_partial

app_name = "panel"

urlpatterns = [
    # Auth
    path("login/", login_page, name="login_page"),
    path("login/submit/", login_submit, name="login_submit"),
    path("logout/submit/", logout_submit, name="logout_submit"),

    # Pages
    path("", products_page, name="root"),
    path("products/", products_page, name="products_page"),
    path("products/<int:product_id>/", product_detail_page, name="product_detail"),
    path("alerts/", alerts_page, name="alerts_page"),
    path("movements/", movements_page, name="movements_page"),

    # Partials
    path("partials/summary/", summary_partial, name="summary_partial"),
    path("partials/activity/", activity_partial, name="activity_partial"),
    path("partials/alerts/", alerts_partial, name="alerts_partial"),
    path("partials/top-products/", top_products_partial, name="top_products_partial"),
    path("partials/search-results/", search_results_partial, name="search_results_partial"),
    path("partials/products/table/", products_table_partial, name="products_table_partial"),
    path("partials/product-sheet/<int:product_id>/", product_sheet_partial, name="product_sheet_partial"),
    path("partials/kardex/<int:product_id>/", kardex_partial, name="kardex_partial"),
    path("alerts/partials/list/", alerts_list_partial, name="alerts_list_partial"),
    path("movements/partials/list/", movements_list_partial, name="movements_list_partial"),

    # Actions
    path("actions/stock/entry/", stock_entry_submit, name="stock_entry_submit"),
    path("actions/stock/exit/", stock_exit_submit, name="stock_exit_submit"),
    path("actions/stock/adjust-to-count/", stock_adjust_to_count_submit, name="stock_adjust_to_count_submit"),
    path("actions/stock/entry-by-sku/", stock_entry_by_sku_submit, name="stock_entry_by_sku_submit"),
    path("actions/stock/exit-by-sku/", stock_exit_by_sku_submit, name="stock_exit_by_sku_submit"),
    path("actions/stock/adjust-to-count-by-sku/", stock_adjust_to_count_by_sku_submit, name="stock_adjust_to_count_by_sku_submit"),
    path("partials/movement/drawer/", movement_drawer_partial, name="movement_drawer_partial"),
    path("partials/movement/confirm/", movement_confirm_partial, name="movement_confirm_partial"),
]
