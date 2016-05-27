'''
Image/Video slideshow
Copyright (C) 2015  Bernd Adler <caryptes@web.de>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''

#requires Python 3.4
#requires Pillow 2.7.0

import tkinter
from PIL import Image, ImageTk
import os
import sys
import subprocess

class Slide:
	elementIndex=0
	elementList=[]
	root=None
	panel=None
	
	def __init__(self):
		self.filepath=None
	
	def run(self):
		self.openWindow()
		self.configureEventListeners()
		if len(Slide.elementList)>0:
			Slide.elementList[Slide.elementIndex].execute()
			Slide.root.mainloop()
	
	def openWindow(self):
		Slide.root=tkinter.Tk()
		
		#fullscreen setting
		#Slide.root.wm_state('zoomed') #maximized
		Slide.root.attributes("-fullscreen", True) #fullscreen
		
		Slide.panel=tkinter.Label(Slide.root)
		Slide.panel.pack(side="bottom", fill="both", expand="yes")
	
	def configureEventListeners(self):
		#key: ->
		Slide.root.bind("<Right>", nextCallback)
		#key: <-
		Slide.root.bind("<Left>", previousCallback)
		#key: Enter
		Slide.root.bind("<Return>", nextCallback)
		#key: Backspace
		Slide.root.bind("<BackSpace>", previousCallback)
		#left mouse button
		Slide.root.bind("<ButtonRelease-1>", nextCallback)
		#key: Esc
		Slide.root.bind("<Escape>", quitCallback)
	
	def nextElement(self):
		if Slide.elementIndex<len(Slide.elementList)-1:
			Slide.elementIndex+=1
			Slide.elementList[Slide.elementIndex].execute()
		else:
			sys.exit()
	
	def previousElement(self):
		if Slide.elementIndex>0:
			Slide.elementIndex-=1
			Slide.elementList[Slide.elementIndex].execute()
	
	def execute(self):
		print(Slide.elementIndex)
	
	def setIndex(self, position):
		if isinstance(position, int):
			if position<len(Slide.elementList)-1:
				Slide.elementIndex=position

#Image type element
class SlideImage(Slide):
	def __init__(self, filepath):
		self.filepath=filepath
		Slide.elementList.append(self)
	
	def execute(self):
		super().execute()
		if os.path.isfile(self.filepath):
			render=ImageTk.PhotoImage(Image.open(self.filepath))
			Slide.panel.configure(image=render)
			Slide.panel.image=render
			Slide.panel.configure(background="black")

#Video type element
class SlideVideo(Slide):
	def __init__(self, filepath):
		self.filepath=filepath
		Slide.elementList.append(self)
	
	def execute(self):
		super().execute()
		#configure media player
		#important for multiscreen environments: child process will be executed on what is configured as main screen
		application=r"C:\Program Files (x86)\VideoLAN\VLC\vlc.exe --play-and-exit --no-repeat --no-loop --fullscreen "
		
		#clear residential image
		Slide.panel.configure(image="")
		Slide.panel.image=""
		
		#start movie player
		if os.path.isfile(self.filepath):
			subprocess.call(application+self.filepath)

#callbacks for event listeners
def nextCallback(e):
	Slide().nextElement()

def previousCallback(e):
	Slide().previousElement()

def quitCallback(e):
	sys.exit()

#define slideshow (order is important)
SlideImage("01.jpg")
SlideImage("02.png")
SlideVideo("03.mp4")
SlideImage("04.png")

#run
main=Slide()
main.setIndex(0)
main.run()
