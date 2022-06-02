cat > /dbfs/init/init_dbfs_cli.sh <<EOF

> ~/.databrickscfg
echo "[DEFAULT]" >> ~/.databrickscfg
echo "host = https://adb-4564373645402638.18.azuredatabricks.net" >> ~/.databrickscfg
echo "token = dapi5258e0c5ba56c19c3fc8fee34a60990d-3" >> ~/.databrickscfg
dbfs mkdirs dbfs:/FileStore/table/data
mkdir /tmp/log

EOF
cat /dbfs/init/init_dbfs_cli.sh