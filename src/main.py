import time
import picamera
import io
import stats
import sqlite3
from PIL import Image
from lobe import ImageModel
from sqlite3 import Error
from classification_message_processor import ClassificationMessageProcessor
from classification_message_processor import ClassificationLabels

def main():
	MODEL_PATH="../models/v0.1/"

	conn = stats.initdb()

	# Load Lobe model
	model = ImageModel.load(MODEL_PATH)
	
	# Message processors
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

			# Get the confidence for the top label
			confidence = result.labels[0][1]
			
			# Show the LEDs, Servo, and any additional processors
			message_processor.process_label(label, confidence)
			
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

			if label != ClassificationLabels.NOTHING:
				prediction = (label, confidence, total_time, predict_time)
				stats.insert_prediction(conn, prediction)

			# Wait for 1 second so the label is visible on the screen
			time.sleep(1)

if __name__ == '__main__':
	try:
		print(f"Predictions starting, to stop press \"CTRL+C\"")
		main()
	except KeyboardInterrupt:
		print("")
		print(f"Caught interrupt, exiting...")
