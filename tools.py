'''
Created on 2014-5-5

@author: denglevi
'''
import wx

def scale_bitmap(bitmap, width, height):
    
    image = wx.ImageFromBitmap(bitmap)
    image = image.Scale(width, height, wx.IMAGE_QUALITY_HIGH)
    result = wx.BitmapFromImage(image)
    return result  

def scale_bitmap_from_file(file, width, height):
    bitmap = wx.Bitmap(file)
    image = wx.ImageFromBitmap(bitmap)
    image = image.Scale(width, height, wx.IMAGE_QUALITY_HIGH)
    result = wx.BitmapFromImage(image)
    return result
