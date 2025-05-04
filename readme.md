sudo apt update
sudo apt install -y python3-pip git python3-venv
pip3 install --upgrade pip


git clone https://github.com/kgautams-123/summit-webapp.git
cd your-streamlit-app

python3 -m venv venv
source venv/bin/activate

pip install --upgrade pip
pip install -r requirements.txt

nohup streamlit run app.py &


aws s3 cp main.py s3://aws-summit-product-catalog-2
