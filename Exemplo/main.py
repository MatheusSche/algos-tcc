from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import StringProperty
from kivy.garden.filebrowser import FileBrowser
from kivy.uix.popup import Popup
from os.path import sep, expanduser
from os import remove as image_delete

import cv2
import numpy as np
from math import sqrt,exp

class P(FloatLayout):
    pass

class MyBoxLayout(BoxLayout):
    
    label_filtro = StringProperty('Imagem com Filtro')
    imagem_original = StringProperty('')
    imagem_filtrada = StringProperty('')
    n_images_gauss = 0
    n_images_media = 0
    n_images_canny = 0
    n_images_mediana = 0
    n_images_sbx = 0
    n_images_sby = 0
    n_images_lapla = 0
    n_images_geometricas = 0
    n_images_freq = 0
    n_img_filt = 0
    
    def process(self):
        text = self.ids.input.text
        print(text)
    
    def busca_imagem(self, *args):
        user_path = expanduser('~') + sep + 'Documentos'
        self._fbrowser = FileBrowser(select_string='Open',
                                     favorites=[(user_path, 'Documentos')])
        self._fbrowser.bind(on_success=self._file_load,
                            on_canceled=self._cancel_popup)
        self._popup = Popup(title='Open File', content=self._fbrowser,
                            size_hint=(0.9, 0.9), auto_dismiss=False)
        self._popup.open()
      
       
    def _cancel_popup(self, *args):
   
        self._popup.dismiss()
 
    def _file_load(self, instance):
        self._popup.dismiss()
        if instance.selection:
            self.imagem_original = instance.selection[0]
    
    
    def spinner_espaciais(self, value):
        
        if self.imagem_original != '':
            file_name_filt = './filtro_{}'.format(str(self.n_img_filt)) + '.png'
            try:
                image_delete(file_name_filt)
            except Exception:
                pass
            
            self.n_img_filt = self.n_img_filt + 1
            imagem = cv2.imread(self.imagem_original)
            
            if value == 'Canny':
                new_image = cv2.Canny(imagem, 100, 200)  
                self.label_filtro = 'Imagem com Filtro: Canny'
            
            elif value == 'Média':
                new_image = cv2.blur(imagem, (7, 7))
                self.label_filtro = 'Imagem com Filtro: Media'
            
            elif value == 'Gaussiano':
                new_image = cv2.GaussianBlur(imagem, (3,3),5)
                self.label_filtro = 'Imagem com Filtro: Gaussiano'
            
            elif value == 'Mediana':
                new_image = cv2.medianBlur(imagem, 11)
                self.label_filtro = 'Imagem com Filtro: Mediana'
            
            elif value == 'Sobel x':
                new_image = cv2.Sobel(imagem,cv2.CV_64F,1,0,ksize=5)
                self.label_filtro = 'Imagem com Filtro: Sobel x'
            
            elif value == 'Sobel y':
                new_image = cv2.Sobel(imagem,cv2.CV_64F,0,1,ksize=5)
                self.label_filtro = 'Imagem com Filtro: Sobel y'
            
            elif value == 'Laplaciano':
                new_image = cv2.Laplacian(imagem, cv2.CV_8U)
                self.label_filtro = 'Imagem com Filtro: Laplaciano'
                
            new_file_filt = 'filtro_{}'.format(str(self.n_img_filt)) + '.png'
            cv2.imwrite(new_file_filt, new_image)
            self.imagem_filtrada = './' + new_file_filt
            
            
    def spinner_geometricas(self, value): 
        
        params = self.ids.input.text
        
        if value == 'Rotação':
            self.rotacao(params)
        
        elif value == 'Espelhamento':
            self.espelhamento(params)
        
        elif value == 'Translação':
            self.translacao(params)
        
        elif value == 'Ajuste Escala':
            self.escala(params)
            
    
    def rotacao(self, rot):
        
        if rot == "" or rot is None or rot == " ":
            rot = 90
        else:
            rot = int(rot)
            
       
        if self.imagem_original != '':
            file_op = './opg_{}'.format(str(self.n_images_geometricas)) + '.png'
            try:
                image_delete(file_op)
            except Exception:
                pass
            
            self.n_images_geometricas = self.n_images_geometricas + 1
            
            imagem = cv2.imread(self.imagem_original)
            
            totallinhas, totalcolunas = imagem.shape[:2]
            matriz=cv2.getRotationMatrix2D((totallinhas/2, totalcolunas/2), rot, 1)
            img_opg = cv2.warpAffine(imagem, matriz, (totallinhas, totalcolunas))
            
            new_opg = 'opg_{}'.format(str(self.n_images_geometricas)) + '.png'
            cv2.imwrite(new_opg, img_opg)
            self.imagem_filtrada = './' + new_opg
            self.label_filtro = 'Transformação Geométrica: Rotação'
    
    def espelhamento(self, esp):
        if esp == "" or esp is None or esp == " ":
            esp = 0
        else:
            esp = int(esp)
            
        if self.imagem_original != '':
            file_op = './opg_{}'.format(str(self.n_images_geometricas)) + '.png'
            try:
                image_delete(file_op)
            except Exception:
                pass
            
            self.n_images_geometricas = self.n_images_geometricas + 1
            
            imagem = cv2.imread(self.imagem_original)
            
            #flip vertical
            img_opg = cv2.flip(imagem,esp)
            
            new_opg = 'opg_{}'.format(str(self.n_images_geometricas)) + '.png'
            cv2.imwrite(new_opg, img_opg)
            self.imagem_filtrada = './' + new_opg
            self.label_filtro = 'Transformação Geométrica: Espelhamento Vertical'
    
    def translacao(self, trans):
        tx, ty = (None, None)
        if trans == "" or trans is None or trans == " ":
            tx, ty = (50, 50)
        else:
            tx, ty = trans.split(';')
            
        if self.imagem_original != '':
            file_op = './opg_{}'.format(str(self.n_images_geometricas)) + '.png'
            try:
                image_delete(file_op)
            except Exception:
                pass
            
            self.n_images_geometricas = self.n_images_geometricas + 1
            
            imagem = cv2.imread(self.imagem_original, 0)
            
            linhas, colunas = imagem.shape[:2]
            matriz=np.float32([[1,0,tx],[0,1,ty]])
            img_opg=cv2.warpAffine(imagem, matriz,(linhas,colunas))
            
            new_opg = 'opg_{}'.format(str(self.n_images_geometricas)) + '.png'
            cv2.imwrite(new_opg, img_opg)
            self.imagem_filtrada = './' + new_opg
            self.label_filtro = 'Transformação Geométrica: Translação'
    
    def escala(self, esc):
        tx, ty = (None, None)
        if esc == "" or esc is None or esc == " ":
            tx, ty = (1, 1)
        else:
            tx, ty = esc.split(';')
        
        if self.imagem_original != '':
            file_op = './opg_{}'.format(str(self.n_images_geometricas)) + '.png'
            try:
                image_delete(file_op)
            except Exception:
                pass
            
            self.n_images_geometricas = self.n_images_geometricas + 1
            
            imagem = cv2.imread(self.imagem_original, 0)
            
            img_opg = cv2.resize(imagem, None, fx=int(tx),fy=int(ty), 
                           interpolation = cv2.INTER_CUBIC)
            
            new_opg = 'opg_{}'.format(str(self.n_images_geometricas)) + '.png'
            cv2.imwrite(new_opg, img_opg)
            self.imagem_filtrada = './' + new_opg
            self.label_filtro = 'Transformação Geométrica: Escala'
    
            
    def spinner_frequencia(self, value): 
        
        if self.imagem_original != '':
            
            params = self.ids.input.text
            
            if params == "" or params is None or params == " ":
                val = 50
            else:
                val = int(params)
                
            img = cv2.imread(self.imagem_original, 0)
            original = np.fft.fft2(img)
            centro = np.fft.fftshift(original)
            
            if value == 'PA-Ideal':
                HPcentro = centro * self.paIdealHP(val, img.shape)
                HP = np.fft.ifftshift(HPcentro)
                inverso_HP = np.fft.ifft2(HP)
                self.label_filtro = 'Passa Alta - Ideal'
            
            elif value == 'PB-Ideal':
                HPcentro = centro * self.pbIdealLP(val, img.shape)
                HP = np.fft.ifftshift(HPcentro)
                inverso_HP = np.fft.ifft2(HP)
                self.label_filtro = 'Passa Baixa - Ideal'
            
            elif value == 'PA-Butterworth':
                HPcentro = centro * self.paButterworth(val,img.shape,10)
                HP = np.fft.ifftshift(HPcentro)
                inverso_HP = np.fft.ifft2(HP)
                self.label_filtro = 'Passa Alta - Butterworth'
            
            elif value == 'PA-Gaussiano':
                HPcentro = centro * self.paGaussiano(val,img.shape)
                HP = np.fft.ifftshift(HPcentro)
                inverso_HP = np.fft.ifft2(HP)
                self.label_filtro = 'Passa Alta - Gaussiano'
            
            elif value == 'PB-Butterworth':
                LPcentro = centro * self.pbButterworth(val,img.shape,10)
                LP = np.fft.ifftshift(LPcentro)
                inverso_HP = np.fft.ifft2(LP)
                self.label_filtro = 'Passa Baixa - Butterworth'
            
            elif value == 'PB-Gaussiano':
                LowPassCenter = centro * self.pbGaussiano(val,img.shape)
                LP = np.fft.ifftshift(LowPassCenter)
                inverso_HP = np.fft.ifft2(LP)
                self.label_filtro = 'Passa Baixa - Gaussiano'
                    
            file_name_freq = './freq_{}'.format(str(self.n_images_freq)) + '.png'
            try:
                image_delete(file_name_freq)
            except Exception:
                pass
            
            self.n_images_freq = self.n_images_freq + 1
            
            new_file_freq = 'freq_{}'.format(str(self.n_images_freq)) + '.png'
            
            cv2.imwrite(new_file_freq, np.abs(inverso_HP))
            self.imagem_filtrada = './' + new_file_freq
        
    
    def pbIdealLP(self, D0, imagem):
        base = np.zeros(imagem[:2])
        linhas, colunas = imagem[:2]
        centro = (linhas/2,colunas/2)
        
        for x in range(colunas):
            for y in range(linhas):
                if self.distancia((y,x),centro) < D0:
                    base[y,x] = 1
        return base

    def paIdealHP(self, D0, imagem):
        
        base = np.ones(imagem[:2])
        linhas, colunas = imagem[:2]
        centro = (linhas/2,colunas/2)
        
        for x in range(colunas):
            for y in range(linhas):
                if self.distancia((y,x),centro) < D0:
                    base[y,x] = 0
        return base
    
    def paButterworth(self, D0, imagem, n):
        base = np.zeros(imagem[:2])
        linhas, colunas = imagem[:2]
        centro = (linhas/2,colunas/2)
        
        for x in range(colunas):
            for y in range(linhas):
                base[y,x] = 1-1/(1+(self.distancia((y,x),centro)/D0)**(2*n))
        return base
    
    def paGaussiano(self, D0, imagem):
        base = np.zeros(imagem[:2])
        linhas, colunas = imagem[:2]
        centro = (linhas/2,colunas/2)
        
        for x in range(colunas):
            for y in range(linhas):
                base[y,x] = 1 - exp(((-self.distancia((y,x),centro)**2)/(2*(D0**2))))
        return base
    
    def pbButterworth(self, D0, imagem, n):
        base = np.zeros(imagem[:2])
        linhas, colunas = imagem[:2]
        centro = (linhas/2,colunas/2)
        
        for x in range(colunas):
            
            for y in range(linhas):
                
                base[y,x] = 1/(1+(self.distancia((y,x),centro)/D0)**(2*n))
                
        return base
    
    def pbGaussiano(self, D0, imagem):
        base = np.zeros(imagem[:2])
        linhas, colunas = imagem[:2]
        centro = (linhas/2,colunas/2)
        
        for x in range(colunas):
            
            for y in range(linhas):
                
                base[y,x] = exp(((-self.distancia((y,x),centro)**2)/(2*(D0**2))))
                
        return base
    
    def distancia(self, point1, point2):
        return sqrt((point1[0]-point2[0])**2 + (point1[1]-point2[1])**2)
        

class MainApp(App):
    title = "Processamento Digital de Imagens"
    def build(self):
        return MyBoxLayout()

    

if __name__ == '__main__':
    MainApp().run()



