python -m pip freeze > _t.txt
python -m pip uninstall -r _t.txt -y
rm _t.txt
python -m pip install -r requirements.txt

