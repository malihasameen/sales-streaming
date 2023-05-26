from supersetapi import SupersetAPIClient

client = SupersetAPIClient(host="http://172.18.0.11:8088")
client.login(username="admin", password="admin")

# Connect Superset to MySQL DB
database_id = client.create_database(
    database_name="MySQL", 
    engine="mysql", 
    driver="mysqldb",
    sqlalchemy_uri="mysql://root:secret@172.18.0.8:3306/sales_db"
)

dataset_id = client.create_dataset(
    database_id=database_id,
    schema="sales_db",
    table="sales"
)

dashboard_id = client.create_dashboard(title="Sales Dashboard")

# Create Total Sales Big Number
params = "{\"metric\":{\"expressionType\":\"SIMPLE\",\"column\":{\"column_name\":\"total_sum_amount\",\"filterable\":true,\"groupby\":true,\"id\":4,\"type\":\"FLOAT\"},\"aggregate\":\"SUM\",\"label\":\"SUM(total_sum_amount)\"}}"

total_sales_chart = client.create_chart(
    dashboard_ids=[dashboard_id], 
    datasource_id=dataset_id, 
    datasource_name="sales_db.sales",
    params=params,
    slice_name="Total Sales",
    viz_type="big_number_total"
)

# Create Pie Chart
params = "{\"groupby\":[\"source\"],\"metric\":{\"expressionType\":\"SIMPLE\",\"column\":{\"column_name\":\"total_sum_amount\",\"filterable\":true,\"groupby\":true,\"id\":4,\"type\":\"FLOAT\"},\"aggregate\":\"SUM\",\"label\":\"SUM(total_sum_amount)\"},\"sort_by_metric\":true,\"color_scheme\":\"supersetColors\",\"show_labels_threshold\":5,\"show_legend\":true,\"legendType\":\"scroll\",\"legendOrientation\":\"top\",\"label_type\":\"key\",\"number_format\":\"SMART_NUMBER\",\"date_format\":\"smart_date\",\"show_labels\":true,\"labels_outside\":true,\"outerRadius\":70,\"innerRadius\":30}"

total_sales_chart = client.create_chart(
    dashboard_ids=[dashboard_id], 
    datasource_id=dataset_id, 
    datasource_name="sales_db.sales",
    params=params,
    slice_name="Source by Amount",
    viz_type="pie"
)

# Create Stacked Bar Chart
params =  "{\"x_axis\":\"state\",\"x_axis_sort\":\"SUM(total_sum_amount)\",\"x_axis_sort_asc\":true,\"x_axis_sort_series\":\"sum\",\"x_axis_sort_series_ascending\":false,\"metrics\":[{\"aggregate\":\"SUM\",\"column\":{\"column_name\":\"total_sum_amount\",\"filterable\":true,\"groupby\":true,\"id\":4,\"type\":\"FLOAT\"},\"expressionType\":\"SIMPLE\",\"label\":\"SUM(total_sum_amount)\"}],\"groupby\":[\"source\"],\"order_desc\":true,\"row_limit\":10000,\"truncate_metric\":true,\"show_empty_columns\":true,\"comparison_type\":\"values\",\"orientation\":\"vertical\",\"x_axis_title_margin\":15,\"y_axis_title_margin\":15,\"y_axis_title_position\":\"Left\",\"sort_series_type\":\"sum\",\"color_scheme\":\"supersetColors\",\"show_value\":true,\"stack\":\"Stack\",\"only_total\":true,\"zoomable\":false,\"show_legend\":true,\"legendType\":\"scroll\",\"legendOrientation\":\"top\",\"x_axis_time_format\":\"smart_date\",\"xAxisLabelRotation\":45,\"y_axis_format\":\"SMART_NUMBER\",\"y_axis_bounds\":[null,null],\"rich_tooltip\":true,\"tooltipTimeFormat\":\"smart_date\"}"

total_sales_chart = client.create_chart(
    dashboard_ids=[dashboard_id], 
    datasource_id=dataset_id, 
    datasource_name="sales_db.sales",
    params=params,
    slice_name="State by Amount with Source breakdown",
    viz_type="echarts_timeseries_bar"
)

# Create Table
params = "{\"query_mode\":\"aggregate\",\"groupby\":[\"source\",\"state\"],\"metrics\":[{\"aggregate\":\"SUM\",\"column\":{\"column_name\":\"total_sum_amount\",\"filterable\":true,\"groupby\":true,\"id\":4,\"type\":\"FLOAT\"},\"expressionType\":\"SIMPLE\",\"label\":\"SUM(total_sum_amount)\"}],\"timeseries_limit_metric\":{\"aggregate\":\"SUM\",\"column\":{\"column_name\":\"total_sum_amount\",\"filterable\":true,\"groupby\":true,\"id\":4,\"type\":\"FLOAT\"},\"expressionType\":\"SIMPLE\",\"label\":\"\"},\"order_by_cols\":[],\"server_pagination\":true,\"row_limit\":1000,\"server_page_length\":10,\"order_desc\":true,\"table_timestamp_format\":\"smart_date\",\"show_cell_bars\":true,\"color_pn\":true}"

total_sales_chart = client.create_chart(
    dashboard_ids=[dashboard_id], 
    datasource_id=dataset_id, 
    datasource_name="sales_db.sales",
    params=params,
    slice_name="Top Source, State by Amount",
    viz_type="table"
)

# Create Bar Chart
params = "{\"metrics\":[{\"expressionType\":\"SIMPLE\",\"column\":{\"column_name\":\"total_sum_amount\",\"filterable\":true,\"groupby\":true,\"id\":4,\"type\":\"FLOAT\"},\"aggregate\":\"SUM\",\"label\":\"SUM(total_sum_amount)\"}],\"groupby\":[\"source\",\"state\"],\"columns\":[],\"row_limit\":10000,\"timeseries_limit_metric\":{\"expressionType\":\"SIMPLE\",\"column\":{\"column_name\":\"total_sum_amount\",\"filterable\":true,\"groupby\":true,\"id\":4,\"type\":\"FLOAT\"},\"aggregate\":\"SUM\",\"label\":\"SUM(total_sum_amount)\"},\"order_desc\":true,\"color_scheme\":\"supersetColors\",\"show_legend\":true,\"show_bar_value\":true,\"rich_tooltip\":true,\"order_bars\":false,\"y_axis_format\":\"SMART_NUMBER\",\"y_axis_bounds\":[null,null],\"bottom_margin\":\"auto\",\"x_ticks_layout\":\"auto\"}"

total_sales_chart = client.create_chart(
    dashboard_ids=[dashboard_id], 
    datasource_id=dataset_id, 
    datasource_name="sales_db.sales",
    params=params,
    slice_name="Source, State by Amount",
    viz_type="dist_bar"
)

print("Superset Dashboard created successfully...")