# dbfs:/init/inst_dbfs_cli.sh
# install databricks cli
cat > /dbfs/init/inst_dbfs_cli.sh <<EOF
pip install databricks-cli
pip install azure-storage-logging
pip install azure-storage-blob
> ~/.databrickscfg
echo "[DEFAULT]" >> ~/.databrickscfg
echo "host = https://adb-4564373645402638.18.azuredatabricks.net" >> ~/.databrickscfg
echo "token = dapi5258e0c5ba56c19c3fc8fee34a60990d-3" >> ~/.databrickscfg
dbfs mkdirs dbfs:/FileStore/table/data
EOF
cat /dbfs/init/inst_dbfs_cli.sh


# dbfs:/init/init_selenium.sh
# install selenium with google chrome lastest driver
cat > /dbfs/init/init_selenium.sh <<EOF
#!/bin/sh
echo Install Chrome and Chrome driver
version=`curl -sS https://chromedriver.storage.googleapis.com/LATEST_RELEASE`
wget -N https://chromedriver.storage.googleapis.com/${version}/chromedriver_linux64.zip -O /tmp/chromedriver_linux64.zip
unzip /tmp/chromedriver_linux64.zip -d /tmp/chromedriver/
sudo curl -sS -o - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add
sudo echo "deb https://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list
sudo apt-get -y update
sudo apt-get -y install google-chrome-stable
pip install selenium
EOF
cat /dbfs/init/init_selenium.sh