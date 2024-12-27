# Utiliser l'image astro-runtime de Astronomer
FROM quay.io/astronomer/astro-runtime:12.5.0

# Crée un environnement virtuel et installe dbt-snowflake
RUN python -m venv dbt_venv && source dbt_venv/bin/activate && \
    pip install --no-cache-dir dbt-snowflake && deactivate

# Copie le projet dbt dans le conteneur, en spécifiant un chemin cible
COPY /dbt_sales_data_processing /usr/local/airflow/dbt/dbt_sales_data_processing

# Exécute le Makefile
#RUN cd /usr/local/airflow/dbt/dbt_sales_data_processing && make configure

RUN mkdir -p ~/.dbt && \
    echo "dbt_sales_data_processing:" > ~/.dbt/profiles.yml && \
    echo "  target: dev" >> ~/.dbt/profiles.yml && \
    echo "  outputs:" >> ~/.dbt/profiles.yml && \
    echo "    dev:" >> ~/.dbt/profiles.yml && \
    echo "      type: snowflake" >> ~/.dbt/profiles.yml && \
    echo "      account: \"aj60515.us-east-2.aws\"" >> ~/.dbt/profiles.yml && \
    echo "      user: \"PHILMAYELE\"" >> ~/.dbt/profiles.yml && \
    echo "      password: \"Costa1234\"" >> ~/.dbt/profiles.yml && \
    echo "      role: \"ACCOUNTADMIN\"" >> ~/.dbt/profiles.yml && \
    echo "      database: \"E_COMMERCE_DB\"" >> ~/.dbt/profiles.yml && \
    echo "      warehouse: \"COMPUTE_WH\"" >> ~/.dbt/profiles.yml && \
    echo "      schema: \"E_COMMERCE_SCHEMA\"" >> ~/.dbt/profiles.yml && \
    echo "      threads: 2" >> ~/.dbt/profiles.yml && \
    echo "      client_session_keep_alive: false" >> ~/.dbt/profiles.yml && \
    echo "Fichier profiles.yml configuré avec succès !"