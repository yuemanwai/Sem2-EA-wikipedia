# How to Make It Run
1. Create a codespace.
2. Clone this repository.
3. Move all files from /Sem2-EA-wikipedia to your own directory.
4. Rebuild the codespace.
5. Wait for the browser to pop up and settle.
6. Run test_data.py.
7. Refresh the fake Wikipedia webpage.


# How to create translation 
Run following commands
```
cd app/
mkdir translations
pybabel extract -F babel.cfg -k lazy_gettext -o translations/messages.pot .
pybabel init -i translations/messages.pot -d translations -l en
pybabel init -i translations/messages.pot -d translations -l es
pybabel init -i translations/messages.pot -d translations -l zh
pybabel compile -d translations
```

# How to update translation 
```
cd app/
pybabel update -i translations/messages.pot -d translations
```
