# -*- coding: utf-8 -*-
"""
Created on Thu Apr 29 14:28:21 2020

@author: HHAGBE
"""

import os
import time
import zipfile
import collections
import rarfile

class COMICParser:
    def __init__(self, filename, *args):
        self.filename = filename
        self.book = None
        self.image_list = None
        self.book_extension = os.path.splitext(self.filename)
        self._metadata = {}

    def read_book(self):
        self.name = ""
        for i in self.filename:
            if i == ".":    break
            self.name += i
        if self.book_extension[1] == '.cbz':
            self.unzip(self.filename, self.name)
            self.book = zipfile.ZipFile(
                self.filename, mode='r', allowZip64=True)
            self.image_list = [
                i.filename for i in self.book.infolist()
                if not i.is_dir() and is_image(i.filename)]

        elif self.book_extension[1] == '.cbr':
            self.unrar(self.filename, self.name)

            self.book = rarfile.RarFile(self.filename)
            self.image_list = [
                i.filename for i in self.book.infolist()
                if not i.isdir() and is_image(i.filename)]
        print(self.image_list)
        #self.image_list.sort()
        return self.image_list


    def generate_metadata(self, author='<Unknown>', isbn = None, tags=[], quality=0, src=0):
        title = os.path.basename(self.book_extension[0]).strip(' ')
        cover = self.image_list[0]

        creation_time = time.ctime(os.path.getctime(self.filename))
        year = creation_time.split()[-1]
        try :
            T = lire_bibliotheque()
            a = 0
            etat = False
            while a<len(T)-1:
                if src == T[a][1]:
                    etat = True
                a+=1
            if etat == False :
                file = open("biblio.txt", "a")
                biblio = file.write(str(cover) + "$" + str(src) + "$" + str(title) + "$" + str(author) + "$" + str(creation_time) + "$" + str(year) + "$" + str(tags) + "$" + str(quality) + "\n")
                file.close()
        except :
            file = open("biblio.txt", "w")
            biblio = file.write(str(cover) + "$" + str(src) + "$" + str(title) + "$" + str(author) + "$" + str(creation_time) + "$" + str(year) + "$" + str(tags) + "$" + str(quality) + "\n")
            file.close()

        self._metadata = {"cover":cover, "title": title, "author":author, "year":year, "tags":tags, "quality":quality}
        return self._metadata

    def getMetadata(self):
        return self._metadata

    def generate_content(self):
        return self.image_list

    def get_filename(self):
        return self.filename

    def unzip(self, source_filename, dest_dir):
        with zipfile.ZipFile(source_filename) as zf:
            zf.extractall(dest_dir)

    def unrar(self, source_filename, dest_dir):
        with rarfile.RarFile(source_filename) as rf:
            rf.extractall(dest_dir)

def is_image(filename):
    valid_image_extensions = ['.png', '.jpg', '.bmp']
    if os.path.splitext(filename)[1].lower() in valid_image_extensions:
        return True
    else:
        return False

def lire_bibliotheque():
    file = open("biblio.txt", 'r')
    biblio = file.read()
    T = [[]]
    a = ''
    lv = 0
    for i in biblio :
        a+= i
        if i =='$':
            a = a[0:-1]
            T[lv].append(a)
            a = ''
        if i == "\n":
            a = a[0:-1]
            T[lv].append(a)
            a = ''
            T.append([])
            lv+=1
    return T

if __name__ == '__main__':
    livre = COMICParser("C:/Users/clement/OneDrive - ESME/prépa/semestre 4/IHM/projet final/IHM_projet_final/spidersurf.cbz")
    livre.read_book()
    livre.generate_metadata()
