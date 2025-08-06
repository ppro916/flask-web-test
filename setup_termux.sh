#!/data/data/com.termux/files/usr/bin/bash

echo "🔧 Termux Setup Script सुरू होते..."

# Update आणि upgrade टर्मिनल पॅकेजेस
pkg update -y
pkg upgrade -y

# Python आणि pip install कर
pkg install python -y
pkg install python-pip -y

# pip upgrade
pip install --upgrade pip

# आवश्यक Python पॅकेजेस install कर
pip install selenium==4.15.2
pip install requests==2.31.0
pip install stem==1.8.2
pip install flask==3.0.0
pip install pyvirtualdisplay==3.0
pip install python-dotenv==1.0.0

echo "✅ सर्व पॅकेजेस install झाली!"selenium==4.15.2
requests==2.31.0
stem==1.8.2
flask==3.0.0
pyvirtualdisplay==3.0
python-dotenv==1.0.0
