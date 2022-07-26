#! /bin/bash -xe

# Configure PATH
export PATH=/usr/local/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin

# upgrade database schema to latest version if needed
# alembic upgrade head

# start waitress
waitress-serve --trusted-proxy=* --trusted-proxy-headers=x-forwarded-proto --call audacious_webui:create_app