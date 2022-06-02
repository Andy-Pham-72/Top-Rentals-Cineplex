cat > /dbfs/init/init_selenium_and_other_packages.sh <<EOF
#!/bin/sh

echo Install Chrome and Chrome driver
sudo apt-get install unzip
version=`curl -sS https://chromedriver.storage.googleapis.com/LATEST_RELEASE`
echo Chrome version: ${version}
wget -N https://chromedriver.storage.googleapis.com/\${version}/chromedriver_linux64.zip -O /tmp/chromedriver_linux64.zip
unzip /tmp/chromedriver_linux64 -d /tmp/chromedriver/
sudo curl -sS -o - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add
sudo echo "deb https://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list
sudo apt-get -y update
sudo apt-get -y install google-chrome-stable


EOF
cat /dbfs/init/init_selenium_and_other_packages.sh