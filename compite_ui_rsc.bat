set RCC= C:\Python34\Lib\site-packages\PyQt5\pyrcc5.exe
set UIC= C:\Python34\Lib\site-packages\PyQt5\pyuic5.bat

call %UIC% python_modules/main_view/explorer.ui > python_modules/main_view/ui_explorer_view.py
call %UIC% python_modules/view/view_kingdom/book_world_homepage.ui > python_modules/view/view_kingdom/ui_book_world_homepage.py
call %UIC% python_modules/view/view_kingdom/book_world_main_page.ui > python_modules/view/view_kingdom/ui_book_world_main_page.py
call %UIC% python_modules/main_view/main_window.ui > python_modules/main_view/ui_main_window.py
call %UIC% python_modules/view/view_heros/book_world_army.ui > python_modules/view/view_heros/ui_book_world_army.py
REM call %UIC% python_modules/View/profil_widget.ui > python_modules/View/ui_profil_widget.py
call %UIC% python_modules/view/view_kingdom/kingdom_layout.ui > python_modules/view/view_kingdom/ui_kingdom_layout.py
call %UIC% python_modules/view/view_heros/warrior_layout.ui > python_modules/view/view_heros/ui_warrior_layout.py
call %UIC% python_modules/view/view_heros/book_warrior_homepage.ui > python_modules/view/view_heros/ui_book_warrior_homepage.py
call %UIC% python_modules/view/view_heros/book_warrior_page.ui > python_modules/view/view_heros/ui_book_warrior_page.py
call %UIC% python_modules/view/view_heros/book_warrior_page_reverse.ui > python_modules/view/view_heros/ui_book_warrior_page_reverse.py
call %UIC% python_modules/main_view/explorer.ui > python_modules/main_view/ui_explorer_widget.py
call %UIC% python_modules/main_view/profil.ui > python_modules/main_view/ui_profil_widget.py
call %UIC% python_modules/main_view/dialog_save.ui > python_modules/main_view/ui_dialog_save.py
call %UIC% python_modules/main_view/dialog_thumb_generator.ui > python_modules/main_view/ui_dialog_thumb_generator.py
call %UIC% python_modules/main_view/dialog_settings.ui > python_modules/main_view/ui_dialog_settigns.py
call %UIC% python_modules/main_view/dialog_kingdom_choice.ui > python_modules/main_view/ui_dialog_kingdom_choice.py
call %UIC% python_modules/main_view/dialog_import_kingdom.ui > python_modules/main_view/ui_dialog_import_kingdom.py
call %UIC% python_modules/main_view/dialog_import_groupe.ui > python_modules/main_view/ui_dialog_import_groupe.py
call %UIC% python_modules/view/view_book/book_layout.ui > python_modules/view/view_book/ui_book_layout.py
call %UIC% python_modules/view/view_book/book_page.ui > python_modules/view/view_book/ui_book_page.py
call %UIC% python_modules/tools/pyhtmleditor/ui/htmleditor.ui > python_modules/tools/pyhtmleditor/ui/htmleditor_ui.py
call %UIC% python_modules/tools/pyhtmleditor/ui/inserthtmldialog.ui > python_modules/tools/pyhtmleditor/ui/inserthtmldialog_ui.py
call %UIC% python_modules/view/view_map/add_temple_dialog.ui > python_modules/view/view_map/ui_dialog_add_temple.py
call %UIC% python_modules/view/view_historic/historic_page.ui > python_modules/view/view_historix/historic_page.py
call %UIC% python_modules/view/view_infos/historic_page.ui > python_modules/view/view_infos/historic_page.py
call %UIC% python_modules/view/view_infos/action_resolve_page.ui > python_modules/view/view_infos/action_resolve_page.py


%RCC% resources.qrc -o python_modules/resources_rc.py
%RCC% python_modules/tools/stylesheet/stylesheet.qrc -o python_modules/stylesheet_rc.py
%RCC% python_modules/tools/pyhtmleditor/ui/htmleditor.qrc -o python_modules/tools/pyhtmleditor/ui/htmleditor_rc.py

pause