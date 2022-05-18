import time
import picamera
import io
from PIL import Image
from lobe import ImageModel
import board
import adafruit_dotstar as dotstar

class ClassificationLabels:
	NOTHING = 0
	FIRST = 1
	LOWDEFECTS = 2
	DEFECTS = 3

	@staticmethod
	def parse_to_enum(label):
		label = label.upper()
		switch_map = {
			'NOTHING': ClassificationLabels.NOTHING,
			'FIRST': ClassificationLabels.FIRST,
			'LOWDEFECTS': ClassificationLabels.LOWDEFECTS,
			'DEFECTS': ClassificationLabels.DEFECTS,
			'0': ClassificationLabels.NOTHING,
			'1': ClassificationLabels.FIRST,
			'2': ClassificationLabels.LOWDEFECTS,
			'3': ClassificationLabels.DEFECTS
		}
		result = switch_map.get(label)
		if not result:
			#raise ValueError("Unknown label '" + str(label) + "'")
			result = ClassificationLabels.NOTHING
		return result

# colors in (G,B,R)
_RED = (0, 0, 255)
_GREEN = (255, 0, 0)
_BLUE = (0, 255, 0)
_YELLOW = (211, 0, 255)
_BLACK = (0, 0, 0)

class RaspberryPiBraincraftHatLed:
	"""
	Raspberry PI Braincraft HAT uses Dots LEDs. You can read more about
	the Dots here: https://learn.adafruit.com/adafruit-dotstar-leds/python-circuitpython

	Prerequisutes:
	   1. Install	 sudo pip3 install adafruit-circuitpython-dotstar
	   2. When running Python, you need to run as "sudo"

	"""
	# colors in (G,B,R)
	COLOR_MAP = {
		ClassificationLabels.NOTHING: _BLACK,
		ClassificationLabels.FIRST: _GREEN,
		ClassificationLabels.LOWDEFECTS: _YELLOW,
		ClassificationLabels.DEFECTS: _RED
	}

	def __init__(self):
		self.dots = dotstar.DotStar(clock=board.D6, data=board.D5, n=30)

	def process_label(self, classification_label):
		color = RaspberryPiBraincraftHatLed.COLOR_MAP.get(classification_label, _BLACK)
		for i in range(len(self.dots)):
			self.dots[i] = color


class ServoProcessor:
	"""
	Interface for Servo
	"""

	def __init__(self):
		pass
	
	def process_label(self, classification_label):
		pass


class ClassificationMessageProcessor(object):

	def __init__(self):
		self.processors = [
			RaspberryPiBraincraftHatLed(),
			ServoProcessor()
		]
	
	def process_label(self, classification_label):
		classification_label = ClassificationLabels.parse_to_enum(classification_label)

		for processor in self.processors:
			processor.process_label(classification_label=classification_label)



def main():
	# Load Lobe model
	model = ImageModel.load('/home/spacekatt/model')
	message_processor = ClassificationMessageProcessor()

	with picamera.PiCamera(resolution=(224, 224), framerate=30) as camera:
		
		# Start camera preview
		stream = io.BytesIO()
		camera.start_preview()

		# Camera warm-up time
		time.sleep(2)

		while True:
			# Start stream at the first byte
			stream.seek(0)

			# Start performance counter
			start = time.perf_counter()

			# Clear the last prediction text
			camera.annotate_text = None

			# Capture a single frame as a Pillow image
			camera.capture(stream, format='jpeg')
			img = Image.open(stream)

			# Start prediction performance timer
			predict_start = time.perf_counter()

			# Run inference on the image
			result = model.predict(img)

			# End prediction performance timer
			predict_end = time.perf_counter()

			# Get the prediction label
			label = result.prediction

			# show the LEDs
			message_processor.process_label(label)

			# Get the confidence for the top label
			confidence = result.labels[0][1]

			# Add label text to camera preview
			camera.annotate_text = f"{label} {confidence}"

			# End performance timer
			end = time.perf_counter()

			# Calculate prediction time
			predict_time = predict_end - predict_start

			# Calculate program run time
			total_time = end - start

			# Print performance times
			print(f"\rLabel: {label} | Confidence: {confidence*100: .2f}% | FPS: {1/total_time: .2f} | prediction fps: {1/predict_time: .2f} | {predict_time/total_time: .2f}", end='', flush=True)

			# Wait for 1 second so the label is visible on the screen
			time.sleep(1)


if __name__ == '__main__':
	try:
		print(f"Predictions starting, to stop press \"CTRL+C\"")
		main()
	except KeyboardInterrupt:
		print("")
		print(f"Caught interrupt, exiting...")
