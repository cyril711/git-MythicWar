set RCC= C:\Python34\Lib\site-packages\PyQt5\pyrcc5.exe
set UIC= C:\Python34\Lib\site-packages\PyQt5\pyuic5.bat

call %UIC% python_modules/View/explorer.ui > python_modules/View/ui_explorer_view.py
call %UIC% python_modules/View/profil.ui > python_modules/View/ui_profil_view.py
call %UIC% python_modules/View/book_container.ui > python_modules/View/ui_book_container.py
call %UIC% python_modules/View/book_world_homepage.ui > python_modules/View/ui_book_world_homepage.py
call %UIC% python_modules/View/book_world_main_page.ui > python_modules/View/ui_book_world_main_page.py
call %UIC% python_modules/View/main_window.ui > python_modules/View/ui_main_window.py
call %UIC% python_modules/View/book_world_army.ui > python_modules/View/ui_book_world_army.py
call %UIC% python_modules/View/profil_widget.ui > python_modules/View/ui_profil_widget.py
call %UIC% python_modules/View/kingdom_layout.ui > python_modules/View/ui_kingdom_layout.py
call %UIC% python_modules/View/warrior_layout.ui > python_modules/View/ui_warrior_layout.py
call %UIC% python_modules/View/book_warrior_homepage.ui > python_modules/View/ui_book_warrior_homepage.py
call %UIC% python_modules/View/book_warrior_page.ui > python_modules/View/ui_book_warrior_page.py
call %UIC% python_modules/View/explorer.ui > python_modules/View/ui_explorer_widget.py
call %UIC% python_modules/View/dialog_save.ui > python_modules/View/ui_dialog_save.py
call %UIC% python_modules/View/dialog_settings.ui > python_modules/View/ui_dialog_settigns.py
call %UIC% python_modules/View/dialog_kingdom_choice.ui > python_modules/View/ui_dialog_kingdom_choice.py


%RCC% resources.qrc -o python_modules/resources_rc.py

pause