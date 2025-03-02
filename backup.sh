#!/bin/bash
docker exec fastapi_db_1 pg_dump -U postgres test > backups/backup_$(date +%F).sql