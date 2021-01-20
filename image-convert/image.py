from PIL import Image
image = Image.open('/home/shawnmonk/monk/gatsby/src/images/covid-bubble.png')
print(image.size)
image.thumbnail((600, 240))
image.save('/home/shawnmonk/monk/gatsby/src/images/covid-bubble-resized.png')
print(image.size)