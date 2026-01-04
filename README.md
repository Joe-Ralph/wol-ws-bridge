sudo cp pi-wol-client.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable pi-wol-client.service  
sudo systemctl start pi-wol-client.service  
sudo systemctl status pi-wol-client.service
