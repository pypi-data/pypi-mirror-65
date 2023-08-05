#!/usr/bin/env python3
# -*- coding: utf-8 -*-

name = 'album_sender'

from PIL import Image
from telegram import InputMediaPhoto, InputMediaVideo
import cached_url
import pic_cut
from telegram_util import cutCaption

def send(chat, url, result, rotate=0):
	suffix = '[source](%s)' % url

	if result.video:
		with open('tmp/video.mp4', 'wb') as f:
			f.write(cached_url.get(result.video, force_cache=True, mode='b'))
		group = [InputMediaVideo(open('tmp/video.mp4', 'rb'), 
			caption=cutCaption(result.cap, suffix, 1000), parse_mode='Markdown')]
		return chat.bot.send_media_group(chat.id, group, timeout = 20*60)
		
	imgs = pic_cut.getCutImages(result.imgs, 9)	
	if imgs:
		imgs = pic_cut.getCutImages(result.imgs, 9)
		if rotate:
			if rotate == True:
				rotate = 180
			for img_path in imgs:
				img = Image.open(img_path)
				img = img.rotate(rotate, expand=True)
				img.save(img_path)
		group = [InputMediaPhoto(open(imgs[0], 'rb'), 
			caption=cutCaption(result.cap, suffix, 1000), parse_mode='Markdown')] + \
			[InputMediaPhoto(open(x, 'rb')) for x in imgs[1:]]
		return chat.bot.send_media_group(chat.id, group, timeout = 20*60)

	if result.cap:
		return [chat.send_message(cutCaption(result.cap, suffix, 4000), 
			parse_mode='Markdown', timeout = 20*60)]