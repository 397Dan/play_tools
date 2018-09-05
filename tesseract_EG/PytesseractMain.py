#usr/bin/python
#coding=utf-8
"""
数字图片识别的ocr
代码主体只需要main()里面的两句 其他为底层源码复制而来 调试所需
"""
from pyocr import tesseract  # 用pytesseract不行为什么呢 二者底层相同 用pytesseract时，把需要的源码复制下来能跑通
from PIL import Image # 只写import Image不可以
import ImageEnhance
import ImageFile
import sys
import tempfile
import os
import shlex
import subprocess


# from pytesseract import *
class Output:
	STRING = "string"
	BYTES = "bytes"
	DICT = "dict"
RGB_MODE = 'RGB'
tesseract_cmd = 'tesseract'

# with open('20180829.jpg','r') as f:
# 	print f.read()


class TT():

	def main(self):
		image = Image.open('20180905.PNG')
		print tesseract.image_to_string(image)

	def image_to_string(self,image,
						lang=None,
						config='',
						nice=0,
						boxes=False,
						output_type=Output.STRING):

		args = [image, 'txt', lang, config, nice]

		return self.run_and_get_output(*args)

	def run_and_get_output(self,image,
						   extension,
						   lang=None,
						   config='',
						   nice=0,
						   return_bytes=False):

		temp_name, input_filename = '', ''
		try:
			temp_name, input_filename = self.save_image(image)
			kwargs = {
				'input_filename': input_filename,
				'output_filename_base': temp_name + '_out',
				'extension': extension,
				'lang': lang,
				'config': config,
				'nice': nice
			}

			self.run_tesseract(**kwargs)
			filename = kwargs['output_filename_base'] + os.extsep + extension
			with open(filename, 'rb') as output_file:
				if return_bytes:
					return output_file.read()
				return output_file.read().decode('utf-8').strip()
		finally:
			print 1111111111
			# cleanup(temp_name)

	def save_image(self,image):
		temp_name = tempfile.mktemp(prefix='tess_')
		if isinstance(image, str):
			pass
			# return temp_name, realpath(normpath(normcase(image)))
		image = self.prepare(image)
		img_extension = image.format
		if image.format not in {'JPEG', 'PNG', 'TIFF', 'BMP', 'GIF'}:
			img_extension = 'PNG'

		if not image.mode.startswith(RGB_MODE):
			image = image.convert(RGB_MODE)

		if 'A' in image.getbands():
			# discard and replace the alpha channel with white background
			background = Image.new(RGB_MODE, image.size, (255, 255, 255))
			background.paste(image, (0, 0), image)
			image = background
		input_file_name = temp_name + os.extsep + img_extension
		image.save(input_file_name, format=img_extension, **image.info)
		print temp_name
		print input_file_name
		return temp_name, input_file_name

	def prepare(self,image):
		if isinstance(image, Image.Image):
			return image

		# if numpy_installed and isinstance(image, ndarray):
		# 	return Image.fromarray(image)
		#
		# raise TypeError('Unsupported image object')

	def run_tesseract(self,input_filename,
					  output_filename_base,
					  extension,
					  lang,
					  config='',
					  nice=0):
		cmd_args = []

		if not sys.platform.startswith('win32') and nice != 0:
			cmd_args += ('nice', '-n', str(nice))

		cmd_args += (tesseract_cmd, input_filename, output_filename_base)

		if lang is not None:
			cmd_args += ('-l', lang)

		cmd_args += shlex.split(config)

		if extension not in ('box', 'osd', 'tsv'):
			cmd_args.append(extension)

		try:
			proc = subprocess.Popen(cmd_args, **self.subprocess_args())
		except OSError:
			print "TesseractNotFoundError"
			# raise TesseractNotFoundError()

		status_code, error_string = proc.wait(), proc.stderr.read()
		proc.stderr.close()

		if status_code:
			print 'TesseractError'
			# raise TesseractError(status_code, get_errors(error_string))

		return True

	def subprocess_args(self,include_stdout=True):
		# See https://github.com/pyinstaller/pyinstaller/wiki/Recipe-subprocess
		# for reference and comments.

		kwargs = {
			'stdin': subprocess.PIPE,
			'stderr': subprocess.PIPE,
			'startupinfo': None,
			'env': None
		}

		if hasattr(subprocess, 'STARTUPINFO'):
			kwargs['startupinfo'] = subprocess.STARTUPINFO()
			kwargs['startupinfo'].dwFlags |= subprocess.STARTF_USESHOWWINDOW
			kwargs['env'] = os.environ

		if include_stdout:
			kwargs['stdout'] = subprocess.PIPE

		return kwargs

if __name__ == '__main__':
	TT().main()
