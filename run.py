from picard import PiCardTest, PiCardApp
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-D', '--dev', action='store_true')
parser.add_argument('--fps', type=int, default=30)
args = parser.parse_args()

# picard = PiCardTest(is_dev=args.dev, fps=args.fps)
# picard.start()

app = PiCardApp(screen_size=(320, 240))
app.run()