#!/bin/sh

rm -f services/web/.env

rm -f services/database/.dev-db-env

rm -f services/database/.test-db-env

flask_app=$(curl  -H "X-Vault-Token: $VAULT_TOKEN" \
        -X GET http://127.0.0.1:8200/v1/kv/api-template-v4/local/flask_app)

echo FLASK_APP=$(echo $flask_app | jq -r .data.FLASK_APP) >> services/web/.env

flask_env=$(curl  -H "X-Vault-Token: $VAULT_TOKEN" \
        -X GET http://127.0.0.1:8200/v1/kv/api-template-v4/local/flask_env)

echo FLASK_ENV=$(echo $flask_env | jq -r .data.FLASK_ENV) >> services/web/.env

secret_key=$(curl  -H "X-Vault-Token: $VAULT_TOKEN" \
        -X GET http://127.0.0.1:8200/v1/kv/api-template-v4/local/secret_key)

echo SECRET_KEY=$(echo $secret_key | jq -r .data.SECRET_KEY) >> services/web/.env

postgres_host=$(curl  -H "X-Vault-Token: $VAULT_TOKEN" \
        -X GET http://127.0.0.1:8200/v1/kv/api-template-v4/local/postgres_host)

echo POSTGRES_HOST=$(echo $postgres_host | jq -r .data.POSTGRES_HOST) >> services/web/.env
echo POSTGRES_HOST=$(echo $postgres_host | jq -r .data.POSTGRES_HOST) >> services/database/.dev-db-env
echo POSTGRES_HOST=$(echo $postgres_host | jq -r .data.POSTGRES_HOST) >> services/database/.test-db-env

postgres_db=$(curl  -H "X-Vault-Token: $VAULT_TOKEN" \
        -X GET http://127.0.0.1:8200/v1/kv/api-template-v4/local/postgres_db)

echo POSTGRES_DB=$(echo $postgres_db | jq -r .data.POSTGRES_DB) >> services/web/.env
echo POSTGRES_DB=$(echo $postgres_db | jq -r .data.POSTGRES_DB) >> services/database/.dev-db-env
echo POSTGRES_DB=$(echo $postgres_db | jq -r .data.POSTGRES_DB) >> services/database/.test-db-env

postgres_port=$(curl  -H "X-Vault-Token: $VAULT_TOKEN" \
        -X GET http://127.0.0.1:8200/v1/kv/api-template-v4/local/postgres_port)

echo POSTGRES_PORT=$(echo $postgres_port | jq -r .data.POSTGRES_PORT) >> services/web/.env
echo POSTGRES_PORT=$(echo $postgres_port | jq -r .data.POSTGRES_PORT) >> services/database/.dev-db-env
# echo POSTGRES_PORT=$(echo $postgres_port | jq -r .data.POSTGRES_PORT) >> services/database/.test-db-env
echo POSTGRES_PORT=5433 >> services/database/.test-db-env

postgres_user=$(curl  -H "X-Vault-Token: $VAULT_TOKEN" \
        -X GET http://127.0.0.1:8200/v1/kv/api-template-v4/local/postgres_user)

echo POSTGRES_USER=$(echo $postgres_user | jq -r .data.POSTGRES_USER) >> services/web/.env
echo POSTGRES_USER=$(echo $postgres_user | jq -r .data.POSTGRES_USER) >> services/database/.dev-db-env
echo POSTGRES_USER=$(echo $postgres_user | jq -r .data.POSTGRES_USER) >> services/database/.test-db-env

postgres_password=$(curl  -H "X-Vault-Token: $VAULT_TOKEN" \
        -X GET http://127.0.0.1:8200/v1/kv/api-template-v4/local/postgres_password)

echo POSTGRES_PASSWORD=$(echo $postgres_password | jq -r .data.POSTGRES_PASSWORD) >> services/web/.env
echo POSTGRES_PASSWORD=$(echo $postgres_password | jq -r .data.POSTGRES_PASSWORD) >> services/database/.dev-db-env
echo POSTGRES_PASSWORD=$(echo $postgres_password | jq -r .data.POSTGRES_PASSWORD) >> services/database/.test-db-env

mail_host=$(curl  -H "X-Vault-Token: $VAULT_TOKEN" \
        -X GET http://127.0.0.1:8200/v1/kv/api-template-v4/local/mail_host)

echo MAIL_HOST=$(echo $mail_host | jq -r .data.MAIL_HOST) >> services/web/.env

mail_port=$(curl  -H "X-Vault-Token: $VAULT_TOKEN" \
        -X GET http://127.0.0.1:8200/v1/kv/api-template-v4/local/mail_port)

echo MAIL_PORT=$(echo $mail_port | jq -r .data.MAIL_PORT) >> services/web/.env

mail_username=$(curl  -H "X-Vault-Token: $VAULT_TOKEN" \
        -X GET http://127.0.0.1:8200/v1/kv/api-template-v4/local/mail_username)

echo MAIL_USERNAME=$(echo $mail_username | jq -r .data.MAIL_USERNAME) >> services/web/.env

mail_password=$(curl  -H "X-Vault-Token: $VAULT_TOKEN" \
        -X GET http://127.0.0.1:8200/v1/kv/api-template-v4/local/mail_password)

echo MAIL_PASSWORD=$(echo $mail_password | jq -r .data.MAIL_PASSWORD) >> services/web/.env

firehose_delivery_stream=$(curl  -H "X-Vault-Token: $VAULT_TOKEN" \
        -X GET http://127.0.0.1:8200/v1/kv/api-template-v4/local/firehose_delivery_stream)

echo FIREHOSE_DELIVERY_STREAM=$(echo $firehose_delivery_stream | jq -r .data.FIREHOSE_DELIVERY_STREAM) >> services/web/.env
