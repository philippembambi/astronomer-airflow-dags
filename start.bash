rm -r ./dbt_sales_data_processing
sleep 3
cp -r ../dbt_sales_data_processing ./
sleep 3
astro dev start --no-cache