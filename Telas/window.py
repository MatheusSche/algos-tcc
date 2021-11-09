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
from os.path import sep, expanduser, dirname
import binascii

from CriptoRSA.rsa import GeraChaves
from Images.convert_image import ConvertDicomToPNG
from Esteganografia.lsb import LSB

#define diferent screens
class FiveWindow(Screen):
    pass

class FirstWindow(Screen):
    pass

class SecondWindow(Screen):
    imagem_original = StringProperty('')
    image_stego_path = StringProperty('')
    texto_criptografado = StringProperty('')
    texto_criptografado_hex = None
    public_key_path = './Chaves/public_key.pem'

    def _cancel_popup(self, *args):
   
        self._popup.dismiss()
 
    def _file_load(self, instance):
        self._popup.dismiss()
        if instance.selection:
            
            file_type = instance.selection[0].split('.')[-1]
            
            if file_type == 'dcm':
                self.image_stego_path = instance.selection[0]
                display_image = self.convert(instance.selection[0])
                self.imagem_original = display_image
            elif file_type == 'pem':
                self.public_key_path = instance.selection[0]
                print(self.public_key_path)
            else:
                print('Formato não corresponde')
    
    def busca_imagem(self, *args):
        
        user_path = dirname(expanduser('~')) + sep + 'Documents' 
        self._fbrowser = FileBrowser(select_string='Open',
                                     path='./',
                                     favorites=[(user_path, 'Documents')])
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
        try:
            texto = self.ids.input.text
            chave = self.public_key_path

            encriptador = GeraChaves()

            encode_text = encriptador.encripta(chave, texto)
        
            self.texto_criptografado_hex = encode_text
            self.texto_criptografado = binascii.hexlify(encode_text).decode()
        except Exception as e:
            print(e)
    
    def aplica_esteganografia(self):
        esteg = LSB()
        esteg.encode_image( path_image=self.image_stego_path, text=self.texto_criptografado)


class WindowManager(ScreenManager):
    pass

class ThirdWindow(Screen):
    
    def gerar_chaves(self):
        gerador = GeraChaves()
        gerador.gera()

class FourthWindow(Screen):
    imagem_original = StringProperty('')
    image_stego_path = StringProperty('')
    private_key_path = './Chaves/private_key.pem'
    byte_encript_text = None
    encriptedt_text_kv = StringProperty('')
    display_texto_pronto = StringProperty('')

    def _cancel_popup(self, *args):
   
        self._popup.dismiss()
 
    def _file_load(self, instance):
        self._popup.dismiss()
        if instance.selection:
            
            file_type = instance.selection[0].split('.')[-1]
            
            if file_type == 'dcm':
                self.image_stego_path = instance.selection[0]
                display_image = self.convert(instance.selection[0])
                self.imagem_original = display_image
            elif file_type == 'pem':
                self.private_key_path = instance.selection[0]
            else:
                print('Formato não corresponde')
    
    def busca_imagem(self, *args):
        
        user_path = expanduser('~') + sep + 'Documentos/UCS/TCC-II'
        self._fbrowser = FileBrowser(select_string='Open',
                                     path='./',
                                     favorites=[(user_path, 'Documentos')])
        self._fbrowser.bind(on_success=self._file_load,
                            on_canceled=self._cancel_popup)
        self._popup = Popup(title='Open File', content=self._fbrowser,
                            size_hint=(0.9, 0.9), auto_dismiss=False)
        self._popup.open()

    def decode_esteganografia(self):
        esteg = LSB()
        encripted_text = esteg.decode_image(self.image_stego_path)
    
        self.encriptedt_text_kv = encripted_text
        self.byte_encript_text = binascii.unhexlify(encripted_text.encode())


    def decripta(self):
        try:
            decriptador = GeraChaves()
            texto_pronto = decriptador.decripta(self.private_key_path, self.byte_encript_text)
            self.display_texto_pronto = texto_pronto
        except Exception as e:
            print(e)

    def convert(self, file):
        conversor = ConvertDicomToPNG()
        return conversor.convert(file)

kv = Builder.load_file('window.kv')


class AwesomeApp(App):
    def build(self):
        self.title = 'Criptografia e Esteganografia em imagens médicas.'
        return kv

if __name__ == '__main__':
    AwesomeApp().run()