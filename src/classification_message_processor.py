import board
import adafruit_dotstar as dotstar


# colors in (G,B,R)
_RED = (0, 0, 255)
_GREEN = (255, 0, 0)
_BLUE = (0, 255, 0)
_YELLOW = (211, 0, 255)
_BLACK = (0, 0, 0)


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

	def process_label(self, classification_label, confidence_value):
		color = RaspberryPiBraincraftHatLed.COLOR_MAP.get(classification_label, _BLACK)
		for i in range(len(self.dots)):
			self.dots[i] = color


class ServoProcessor:
	"""
	Interface for Servo
	"""

	def __init__(self):
		pass
	
	def process_label(self, classification_label, confidence_value):
		pass


class ClassificationMessageProcessor(object):

	def __init__(self):
		self.processors = [
			RaspberryPiBraincraftHatLed(),
			ServoProcessor()
		]
	
	def process_label(self, classification_label, confidence_value):
		classification_label = ClassificationLabels.parse_to_enum(classification_label)

		for processor in self.processors:
			processor.process_label(classification_label=classification_label, confidence_value=confidence_value)
