#!/usr/bin/env python
# coding: utf-8

from typing import Any, List, Tuple
import os, random, subprocess, codecs, json, socket, webbrowser, shutil, re
from http.server import HTTPServer, SimpleHTTPRequestHandler
"""
如果没有pillow, 参考
"""
from PIL import Image

""" multiprocessing
  from multiprocessing import Pool

  pool = Pool(processes=4)

  def doSomething(i):
    print(i)

  for i in range(100):
    pool.apply_async(doSomething, args=(i,))

  pool.close()
  pool.join()
"""

""" arguments
  from argparse import ArgumentParser

  parser = ArgumentParser()
  parser.add_argument("-b", "--boolean", help="some help", action="store_true")
  parser.add_argument("-s", "--string", help="some help")
  parser.add_argument("-i", "--int", type=int, help="some help")

  args = parser.parse_args()

  print(args.string)
"""

""" 路径区别
  os.getcwd(): 程序执行目录(绝对路径)
  sys.path[0]: 主模块所在目录(绝对路径)
  sys.argv[0]: 主模块文件路径(绝对路径 | 相对路径)
  __file__: 当前文件绝对路径
"""

def resolve(*args: str) -> str:
  return os.path.abspath(os.path.join(*args)).replace("\\", "/")

def createIfNotExists(dirPath: str) -> "Dir":
  if not os.path.isdir(dirPath):
    os.makedirs(dirPath)
  return Dir(dirPath)

def createHttpServer(host: str=socket.gethostbyname(socket.gethostname()), port: int=8080, webRoot: str=os.getcwd(), page: str="", open: bool=True):
  os.chdir(webRoot)
  httpd = HTTPServer((host, port), SimpleHTTPRequestHandler)
  url = "%s://%s:%s/%s" % ("http", host, port, re.sub(r'(\.\/|\/|\.\\|\\)', "", page))
  print("\nserver running on  %s\n" % url)
  if open:
    webbrowser.open(url)
  try:
    httpd.serve_forever()
  except KeyboardInterrupt:
    print("KeyboardInterrupt")
    pass
  
def question(q: str, defaultValue: str = None) -> str:
  qStr = "%s 默认值【%s】" % (q, defaultValue) if defaultValue != None else q
  if defaultValue == None:
    while True:
      inputStr = input(qStr).strip()
      if inputStr != "":
        return inputStr
  else:
    assert isinstance(defaultValue, str), "is not string: %s" % defaultValue
    inputStr = input(qStr).strip()
    if inputStr == "":
      return defaultValue
    else:
      return inputStr

def questionInt(q: str, defaultValue: int = None) -> int:
  qStr = "%s 默认值【%s】" % (q, defaultValue) if defaultValue != None else q
  if defaultValue == None:
    while True:
      try:
        return int(input(qStr).strip())
      except Exception:
        pass
  else:
    assert isinstance(defaultValue, int), "wrong type: %s is not %s" % (defaultValue, int)
    while True:
      inputStr = input(qStr).strip()
      if inputStr == "":
        return defaultValue
      else:
        try:
          return int(inputStr)
        except Exception:
          pass

def questionFloat(q: str, defaultValue: float = None) -> float:
  qStr = "%s 默认值【%s】" % (q, defaultValue) if defaultValue != None else q
  if defaultValue == None:
    while True:
      try:
        return float(input(qStr).strip())
      except Exception:
        pass
  else:
    assert isinstance(defaultValue, float), "wrong type: %s is not %s" % (defaultValue, float)
    while True:
      inputStr = input(qStr).strip()
      if inputStr == "":
        return defaultValue
      else:
        try:
          return float(inputStr)
        except Exception:
          pass

class Base(object):
  # 绝对路径
  path: str
  # 父目录的绝对路径
  dirname: str
  # 文件名(包括后缀)
  basename: str
  # 文件名(不包括后缀)
  name: str
  # 后缀
  suffix: str
  # 假的无后缀文件名(之所以说是假的, 是因为目录没有后缀)
  fakeName: str
  # 假的后缀(之所以说是假的, 是因为目录没有后缀)
  fakeSuffix: str
  def __init__(self, *p: str):
    super(Base, self).__init__()
    self.path: str = resolve(*p)
    self.dirname: str = os.path.dirname(self.path)
    self.basename: str = os.path.basename(self.path)
    self.name: str = self.basename
    self.suffix: str = ""
    self.fakeName, self.fakeSuffix = os.path.splitext(self.basename)

  @property
  def parent(self) -> "Base":
    return Base(self.dirname)

  def childOf(self, *p: str) -> "Base":
    return Base(self.path, *p)

  def siblingOf(self, *p: str) -> "Base":
    return Base(self.dirname, *p)

  @property
  def isFile(self) -> bool:
    return os.path.isfile(self.path)
  
  @property
  def isDir(self) -> bool:
    return os.path.isdir(self.path)

  @property
  def isImg(self) -> bool:
    if not self.isFile:
      return False
    try:
      Image.open(self.path)
    except Exception as e:
      return False
    return True

  def createAsDir(self) -> "Dir":
    if not self.isDir:
      os.makedirs(self.path)
    return Dir(self.path)
  
  def createAsFile(self) -> "File":
    if not self.isFile:
      self.parent.createAsDir()
      with open(self.path, "w") as f:
        pass
    return File(self.path)

class File(Base):
  def __init__(self, *p: str):
    super(File, self).__init__(*p)
    assert self.isFile, "is not file: %s" % self.path
    # name: 文件名(除后缀)
    # suffix: 后缀
    self.name, self.suffix = os.path.splitext(self.basename)

  @property
  def parent(self) -> "Dir":
    return Dir(self.dirname)
  
  def read(self, encoding="UTF-8") -> str:
    result = ""
    with codecs.open(self.path, "r", encoding=encoding) as f:
      result = f.read()
    return result

  def __write(self, s: str, mode: str, encoding="UTF-8") -> "File":
    with codecs.open(self.path, mode, encoding=encoding) as f:
      f.write(s)
    return self

  def write(self, s: str, encoding="UTF-8") -> "File":
    return self.__write(s, "w", encoding=encoding)
  
  def aWrite(self, s: str, encoding="UTF-8") -> "File":
    return self.__write(s, "a", encoding=encoding)

class Dir(Base):
  def __init__(self, *p: str):
    super(Dir, self).__init__(*p)
    assert self.isDir, "is not dir: %s" % self.path
    # name: 目录名
    # suffix: 后缀(目录该项为空字符串)
    self.name = self.basename
    self.suffix = ""

  @property
  def parent(self) -> "Dir":
    return Dir(self.dirname)

  @property
  def fileNames(self) -> List[str]:
    return [f for f in os.listdir(self.path) if os.path.isfile(resolve(self.path, f))]
  
  @property
  def files(self) -> List["File"]:
    return [File(resolve(self.path, f)) for f in self.fileNames]
  
  @property
  def dirNames(self) -> List[str]:
    return [d for d in os.listdir(self.path) if os.path.isdir(resolve(self.path, d))]
  
  @property
  def dirs(self) -> List["Dir"]:
    return [Dir(resolve(self.path, d)) for d in self.dirNames]
  
  @property
  def allDirs(self) -> List["Dir"]:
    dirs = [d for d in self.dirs]
    curIdx = 0
    while curIdx < len(dirs):
      dirs.extend(dirs[curIdx].dirs)
      curIdx += 1
    return dirs

  @property
  def allFiles(self) -> List["File"]:
    files = [f for f in self.files]
    for d in self.allDirs:
      files.extend(d.files)
    return files

  def includes(self, dirA: "Dir") -> bool:
    # 当不含有dirA中的文件时，有print提示；
    # 当不含有dirA中的目录时，没有提示
    for f in dirA.files:
      if f.basename not in self.fileNames:
        print("【%s】 not in 【%s】" % (f.basename, self.path))
        return False
    for d in dirA.dirs:
      if d.basename not in self.dirNames:
        return False
      if not Dir(self.path, d.basename).includes(d):
        return False
    return True

class Img(File):
  """
  很不成熟, 尽量别用
  除非你真的知道你在干嘛
  """
  obj: Image.Image
  def __init__(self, *p: str):
    super(Img, self).__init__(*p)
    self.obj = Image.open(self.path)
  
  @property
  def isJpg(self) -> bool:
    return self.obj.mode == "RGB" or (self.suffix.lower() == ".jpg" and self.obj.mode.lower() == "p")

  @property
  def isPng(self) -> bool:
    return self.obj.mode == "RGBA" or (self.suffix.lower() == ".png" and self.obj.mode.lower() == "p")

  def resize(self, size: Tuple[int, int], resample=Image.LANCZOS) -> "Img":
    self.obj = self.obj.resize(size, resample=resample)
    return self

class Jpg(Img):
  def __init__(self, *p: str):
    super(Jpg, self).__init__(*p)
    assert self.isJpg, "is not jpg: %s, mode: %s" % (self.path, self.obj.mode)
  
  def saveAs(self, p="", optimize=True, quality=90, progressive=True, subsampling=1) -> "Jpg":
    self.obj.save(p or self.path, format="JPEG", optimize=optimize, quality=quality, progressive=progressive, subsampling=subsampling)
    return self
  
  # quality = 0 时，不压缩
  def saveToPng(self, p="", quality=0) -> str:
    p = p or self.path
    base = Base(p)
    base.parent.createAsDir()
    suffix = ".png"
    name = base.fakeName if base.fakeSuffix.lower() == suffix else base.basename
    targetPath = resolve(base.dirname, "%s%s" % (name, suffix))
    rgba = self.obj.convert("RGBA")
    rgba.save(targetPath)
    if quality > 0:
      Png(targetPath).saveAs(quality=quality)
    return targetPath

class Png(Img):
  def __init__(self, *p: str):
    super(Png, self).__init__(*p)
    assert self.isPng, "is not png: %s, mode: %s" % (self.path, self.obj.mode)

  def saveAs(self, p="", quality=90) -> "Png":
    p = p or self.path
    qualityStr = "%s-%s" % (quality, quality + 2)
    newName = "%s-%s.png" % (str(random.random()), str(random.random()))
    self.obj.save(newName)
    subprocess.call("pngquant.exe --force --ext=.png --quality=%s %s" % (qualityStr, newName))
    shutil.move(newName, p)
    return self

  def saveToJpg(self, p="", optimize=True, quality=94, progressive=True, subsampling=1) -> str:
    p = p or self.path
    base = Base(p)
    base.parent.createAsDir()
    suffix = ".jpg"
    name = base.fakeName if base.fakeSuffix.lower() == suffix else base.basename
    targetPath = resolve(base.dirname, "%s%s" % (name, suffix))
    rgb = self.obj.convert("RGB")
    rgb.save(targetPath, optimize=optimize, quality=quality, progressive=progressive, subsampling=subsampling)
    return targetPath

class Json(File):
  def readAsJson(self) -> Any:
    s = super(Json, self).read()
    return json.loads(s)

  def writeAsJson(self, obj, indent=2) -> "Json":
    with open(self.path, "w", encoding="UTF-8") as f:
      json.dump(obj, f, indent=indent)
    return self
