# -*- coding: utf-8 -*-
"""
Created on Sun Nov  7 15:11:06 2021

@author: matheus.schenatto
"""

from kivy.app import App
from kivy.core.window import Window
from kivy.lang import Builder 
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.popup import Popup

from kivy.properties import StringProperty
from kivy.garden.filebrowser import FileBrowser
from os.path import sep, expanduser

from CriptoRSA.rsa import GeraChaves
from Images.convert_image import ConvertDicomToPNG

#define diferent screens
class FirstWindow(Screen):
    pass

class SecondWindow(Screen):
    imagem_original = StringProperty('')
    image_stego_path = StringProperty('')
    public_key_path = 'C:\\Users\\matheus.schenatto\\Documents\\UCS\\TCC-II\\algos-tcc\\Telas\\public_key.pem'

    def _cancel_popup(self, *args):
   
        self._popup.dismiss()
 
    def _file_load(self, instance):
        self._popup.dismiss()
        if instance.selection:
            
            file_type = instance.selection[0].split('.')[-1]
            
            if file_type == 'dcm':
                image_stego_path = instance.selection[0]
                display_image = self.convert(instance.selection[0])
                self.imagem_original = display_image
            elif file_type == 'pem':
                self.public_key_path = instance.selection[0]
                print(self.public_key_path)
            else:
                print('Formato não corresponde')
    
    def busca_imagem(self, *args):
        
        user_path = expanduser('~') + sep + 'Documentos/UCS/TCC-II'
        self._fbrowser = FileBrowser(select_string='Open',
                                     favorites=[(user_path, 'Documentos')])
        self._fbrowser.bind(on_success=self._file_load,
                            on_canceled=self._cancel_popup)
        self._popup = Popup(title='Open File', content=self._fbrowser,
                            size_hint=(0.9, 0.9), auto_dismiss=False)
        self._popup.open()
    
    def convert(self, file):
        conversor = ConvertDicomToPNG()
        return conversor.convert(file)

    def get_text(self):
        print(self.ids.input.text)

    def criptografa(self):
        texto = self.ids.input.text
        chave = self.public_key_path

        encriptador = GeraChaves()

        encode_text = encriptador.encripta(chave, texto)
        #print(encode_text.decode())
        #binascii.hexlify(encrypted)

        encriptador.decripta('c:\\private_key.pem', encode_text)

class WindowManager(ScreenManager):
    pass

class ThirdWindow(Screen):
    
    def gerar_chaves(self):
        gerador = GeraChaves()
        gerador.gera()

class FourthWindow(Screen):
    pass

kv = Builder.load_file('window.kv')


class AwesomeApp(App):
    def build(self):
        return kv

if __name__ == '__main__':
    AwesomeApp().run()