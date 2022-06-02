cat > /dbfs/init/init_modules.sh <<EOF

pip install databricks-cli
pip install azure-storage-logging
pip install azure-storage-blob
pip install rtsimple
pip install tmdbsimple
pip install rotten_tomatoes_scraper
pip install selenium


EOF
cat /dbfs/init/init_modules.sh 