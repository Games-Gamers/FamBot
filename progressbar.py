from PIL import Image, ImageDraw, ImageFont

def generateBar(exp, rank):
    print(exp, rank)
    req = (rank+1) ** 3 # the required xp for the next rank update this for your use case
    perc = exp / req * 100 # The amount of percent left for the next rank

    perc *= 2 # The canvas is 200 pixels long since proc is a number between 0 and 100 we * it by 2 to get the amount of pixels to draw
    img = Image.new('RGBA', (200, 30), (0, 0, 0, 0)) # Create the canvas

    draw = ImageDraw.Draw(img) # Allow us to draw on the image

    font = ImageFont.truetype("font.ttf", 12) # Load up the font
    draw.text((0, 3), f"{round(perc/2)}% To level {rank+1}", (240, 240, 240), font=font) # Type the text on the leveling bar (x% To level y)

    TINT_COLOR = (0, 0, 0)  # Setup for transparency
    TRANSPARENCY = .10  # Degree of transparency, 0-100%
    OPACITY = int(255 * TRANSPARENCY)
    draw.rectangle(((0, 16), (600, 25)), fill=TINT_COLOR+(OPACITY,)) # Draw the trasparent line under the leveling bar


    draw.line((0, 20, perc, 20), fill=(255, 0, 61), width=5) # Draw the leveling bar
    img.save('expbar.png', quality=95) # Save the image
